"""Requirement Volatility Score (#5): a 0-100 stability score (100=stable,
0=highly volatile) from story reopens, requirement supersessions, and scope
growth — pure rule-based, no LLM. Written back into metric_snapshots so it's
itself trendable, and feeds the Requirement category of #8's confidence
breakdown (see confidence_service.py::_CATEGORY_MAP).

Note: requirement_items.status only ever reaches `superseded` once a future
cross-document dedup pass (out of scope for this build, see requirement_
service.py) marks one item as replacing another — until then the supersede
signal is legitimately 0, not broken.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metric_snapshot import MetricSnapshot
from app.models.requirement_item import RequirementItem, RequirementStatus
from app.models.story import Story


async def compute_volatility(db: AsyncSession, project_id: uuid.UUID) -> float:
    stories = (
        await db.execute(select(Story).where(Story.project_id == project_id))
    ).scalars().all()
    total_stories = len(stories) or 1
    reopen_rate = sum(s.reopened_count for s in stories) / total_stories

    requirements = (
        await db.execute(select(RequirementItem).where(RequirementItem.project_id == project_id))
    ).scalars().all()
    total_req = len(requirements) or 1
    supersede_rate = sum(1 for r in requirements if r.status == RequirementStatus.superseded) / total_req

    scope_rows = (
        await db.execute(
            select(MetricSnapshot)
            .where(MetricSnapshot.project_id == project_id, MetricSnapshot.metric_key == "scope_story_count_total")
            .order_by(MetricSnapshot.recorded_at.asc())
        )
    ).scalars().all()
    scope_growth_rate = 0.0
    if len(scope_rows) >= 2 and scope_rows[0].value:
        scope_growth_rate = max(0.0, (scope_rows[-1].value - scope_rows[0].value) / scope_rows[0].value)

    volatility = 0.4 * reopen_rate + 0.3 * supersede_rate + 0.3 * min(scope_growth_rate, 1.0)
    stability_score = round(max(0.0, min(100.0, 100 * (1 - volatility))), 1)

    db.add(MetricSnapshot(
        project_id=project_id, metric_key="requirement_volatility_score", value=stability_score,
        meta={"reopen_rate": round(reopen_rate, 3), "supersede_rate": round(supersede_rate, 3),
              "scope_growth_rate": round(scope_growth_rate, 3)},
        source="scheduled_recompute",
    ))
    await db.commit()
    return stability_score


async def latest_volatility(db: AsyncSession, project_id: uuid.UUID) -> float | None:
    row = (
        await db.execute(
            select(MetricSnapshot)
            .where(MetricSnapshot.project_id == project_id, MetricSnapshot.metric_key == "requirement_volatility_score")
            .order_by(MetricSnapshot.recorded_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    return row.value if row else None
