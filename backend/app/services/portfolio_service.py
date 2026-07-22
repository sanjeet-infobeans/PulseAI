"""Portfolio Intelligence (#15): cross-project rollup, org-scoped
(super_admin only). Pure aggregation over data Phase 1/2 already
compute per project (ConfidenceScore, metric_snapshots scope counters,
Story.blocked_reason) — no new modeling.

Phase 3 per docs/ai-features-gap-analysis-and-plan.md: the code ships now
since it's cheap, but with a handful of projects under one org, "most common
blocker" / "highest-risk customer" will be statistically thin until tenant
count grows — that's a data-volume limitation, not a code gap.
"""
import statistics
import uuid
from collections import Counter, defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.project import Project
from app.models.story import Story
from app.services.confidence_service import latest_confidence
from app.services.scope_service import _baseline_and_latest

_ATTENTION_BANDS = {"red", "amber"}


async def get_portfolio(db: AsyncSession, org_id: uuid.UUID) -> dict:
    customers = (
        await db.execute(select(Customer).where(Customer.org_id == org_id))
    ).scalars().all()
    customer_map = {c.id: c for c in customers}

    if not customer_map:
        return {
            "projects": [], "needing_attention_count": 0, "most_common_blocker": None,
            "avg_scope_growth_pct": None, "highest_risk_customer": None,
        }

    projects = (
        await db.execute(select(Project).where(Project.customer_id.in_(customer_map.keys())))
    ).scalars().all()

    project_rows = []
    scope_growth_values: list[float] = []
    customer_confidence: dict[uuid.UUID, list[float]] = defaultdict(list)
    blocker_counter: Counter = Counter()

    for project in projects:
        confidence = await latest_confidence(db, project.id)
        baseline, latest = await _baseline_and_latest(db, project.id, "scope_point_total")
        scope_growth_pct = round(100 * (latest - baseline) / baseline, 1) if baseline and latest is not None else None
        if scope_growth_pct is not None:
            scope_growth_values.append(scope_growth_pct)
        if confidence:
            customer_confidence[project.customer_id].append(confidence.score)

        project_rows.append({
            "project_id": str(project.id),
            "name": project.name,
            "customer_name": customer_map[project.customer_id].name,
            "confidence_score": confidence.score if confidence else None,
            "band": confidence.band.value if confidence else None,
            "scope_growth_pct": scope_growth_pct,
        })

        blocked = (
            await db.execute(
                select(Story).where(
                    Story.project_id == project.id, Story.is_blocked.is_(True),
                    Story.blocked_reason.is_not(None),
                )
            )
        ).scalars().all()
        for s in blocked:
            reason = (s.blocked_reason or "").strip()
            if reason:
                blocker_counter[reason] += 1

    needing_attention_count = sum(1 for p in project_rows if p["band"] in _ATTENTION_BANDS)
    most_common_blocker = blocker_counter.most_common(1)[0][0] if blocker_counter else None
    avg_scope_growth_pct = round(statistics.mean(scope_growth_values), 1) if scope_growth_values else None

    highest_risk_customer = None
    if customer_confidence:
        avgs = {cid: statistics.mean(scores) for cid, scores in customer_confidence.items()}
        worst_cid = min(avgs, key=avgs.get)
        highest_risk_customer = customer_map[worst_cid].name

    return {
        "projects": project_rows,
        "needing_attention_count": needing_attention_count,
        "most_common_blocker": most_common_blocker,
        "avg_scope_growth_pct": avg_scope_growth_pct,
        "highest_risk_customer": highest_risk_customer,
    }
