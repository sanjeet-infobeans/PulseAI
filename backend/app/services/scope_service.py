"""Scope Creep Detection (#2): diffs current scope against the earliest
metric_snapshots baseline (written by metrics_service.py on every Jira sync)
plus the requirement_items catalog (#3) and decision_log (#6). Computed live
per request, not stored — same "read-through aggregation" pattern as
resource_service.py, no dedicated table needed.
"""
import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.decision_log import DecisionLogEntry
from app.models.llm_call_log import LLMFeature
from app.models.metric_snapshot import MetricSnapshot
from app.models.requirement_item import RequirementItem
from app.services.retrieval import build_context


async def _baseline_and_latest(db: AsyncSession, project_id: uuid.UUID, metric_key: str) -> tuple[float | None, float | None]:
    rows = (
        await db.execute(
            select(MetricSnapshot)
            .where(MetricSnapshot.project_id == project_id, MetricSnapshot.metric_key == metric_key)
            .order_by(MetricSnapshot.recorded_at.asc())
        )
    ).scalars().all()
    if not rows:
        return None, None
    return rows[0].value, rows[-1].value


async def scope_growth_metrics(db: AsyncSession, project_id: uuid.UUID) -> dict:
    """Pure rule computation, no LLM call — safe to call from a hot path like
    dashboard_service.get_dashboard(). compute_scope_creep() below wraps this
    with an LLM-derived risk narrative for the dedicated Scope Creep panel."""
    baseline_stories, latest_stories = await _baseline_and_latest(db, project_id, "scope_story_count_total")
    baseline_points, latest_points = await _baseline_and_latest(db, project_id, "scope_point_total")

    new_stories_added = max(0, int((latest_stories or 0) - (baseline_stories or 0))) if baseline_stories is not None else 0
    scope_growth_pct = (
        round(100 * (latest_points - baseline_points) / baseline_points, 1)
        if baseline_points and latest_points is not None else 0.0
    )

    requirements_total = (
        await db.execute(select(RequirementItem).where(RequirementItem.project_id == project_id))
    ).scalars().all()
    requirements_added = len(requirements_total)

    decisions_total = (
        await db.execute(select(DecisionLogEntry).where(DecisionLogEntry.project_id == project_id))
    ).scalars().all()

    return {
        "scope_growth_pct": scope_growth_pct,
        "new_stories_added": new_stories_added,
        "requirements_tracked": requirements_added,
        "customer_decisions": len(decisions_total),
        "baseline_points": baseline_points,
        "current_points": latest_points,
        "has_baseline": baseline_points is not None,
    }


async def compute_scope_creep(db: AsyncSession, project_id: uuid.UUID) -> dict:
    scope_metrics = await scope_growth_metrics(db, project_id)

    if not scope_metrics["has_baseline"]:
        return {
            **scope_metrics,
            "risk_level": "low",
            "estimated_schedule_impact_weeks": 0,
            "estimated_cost_impact_note": "",
            "summary": "No baseline yet — scope growth will be measurable after the next Jira sync.",
        }

    llm_result = {"risk_level": "low", "estimated_schedule_impact_weeks": 0,
                  "estimated_cost_impact_note": "", "summary": ""}
    try:
        context = await build_context(db, project_id)
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=prompts.scope_creep_messages(context, scope_metrics),
            model=settings.llm_model_analysis,
            project_id=project_id,
            temperature=0.2,
            json_mode=True,
        )
        llm_result = {**llm_result, **json.loads(raw)}
    except Exception:  # noqa: BLE001 — impact estimate is best-effort
        pass

    return {**scope_metrics, **llm_result}
