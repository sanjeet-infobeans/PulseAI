"""Composite dashboard payload — one call feeds the whole bento view."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_analysis import AnalysisKind
from app.models.sprint import Sprint, SprintState
from app.models.story import Story
from app.services import analysis_service, confidence_service, prediction_service, scope_service
from app.services.retrieval import build_context, simulated_signals

# Overall health = weighted blend of delivery completion, schedule risk (from
# the latest delivery prediction), and scope-creep risk — see docs plan for
# the rationale behind these weights.
_HEALTH_WEIGHT_COMPLETION = 0.45
_HEALTH_WEIGHT_SCHEDULE = 0.35
_HEALTH_WEIGHT_SCOPE = 0.20


def _scope_creep_penalty(scope_growth_pct: float) -> float:
    if scope_growth_pct <= 10:
        return 0.0
    if scope_growth_pct <= 25:
        return 50.0
    return 100.0


async def get_dashboard(db: AsyncSession, project_id: uuid.UUID) -> dict:
    context = await build_context(db, project_id)
    totals = context["totals"]

    # Schedule-risk input: a cheap DB read of the latest (already-computed)
    # delivery prediction — no new LLM call on this hot path.
    latest_prediction = await prediction_service.latest_prediction(db, project_id)
    schedule_score = latest_prediction.probability_on_time if latest_prediction else 50.0

    # Scope-creep input: pure-rule metrics only (no LLM) — see scope_service's
    # split between scope_growth_metrics (rule) and compute_scope_creep (LLM-enriched).
    scope_metrics = await scope_service.scope_growth_metrics(db, project_id)
    scope_penalty = _scope_creep_penalty(scope_metrics["scope_growth_pct"])

    health = round(
        _HEALTH_WEIGHT_COMPLETION * totals["completion_pct"]
        + _HEALTH_WEIGHT_SCHEDULE * schedule_score
        + _HEALTH_WEIGHT_SCOPE * (100 - scope_penalty)
    )

    confidence = await confidence_service.latest_confidence(db, project_id)
    risk = await analysis_service.latest_analysis(db, project_id, AnalysisKind.risk)
    recs = await analysis_service.latest_analysis(db, project_id, AnalysisKind.recommendations)
    execu = await analysis_service.latest_analysis(db, project_id, AnalysisKind.executive)

    sprints = (
        await db.execute(
            select(Sprint).where(Sprint.project_id == project_id).order_by(Sprint.sequence)
        )
    ).scalars().all()
    active = next((s for s in sprints if s.state == SprintState.active), None)
    ref = active or (sprints[-1] if sprints else None)

    # Sprint timeline panel: only the active sprint (not every past/future
    # sprint), what carried into it from the sprint before, and a commitment-
    # ratio trend across recent closed sprints.
    carried_forward: list[dict] = []
    if active:
        carried_stories = (
            await db.execute(
                select(Story).where(
                    Story.project_id == project_id, Story.sprint_id == active.id,
                    Story.carried_forward_from_sprint_id.is_not(None),
                )
            )
        ).scalars().all()
        from_sprint_names = {s.id: s.name for s in sprints}
        carried_forward = [
            {
                "key": s.external_id, "title": s.title,
                "from_sprint_name": from_sprint_names.get(s.carried_forward_from_sprint_id, "a previous sprint"),
            }
            for s in carried_stories
        ]

    closed_sprints = [s for s in sprints if s.state == SprintState.closed]
    recent_closed = closed_sprints[-5:]
    commitment_ratios = [
        s.completed_points / s.committed_points for s in recent_closed if s.committed_points
    ]
    commitment_trend = round(100 * sum(commitment_ratios) / len(commitment_ratios), 1) if commitment_ratios else None

    sprint_panel = {
        "active": {
            "name": active.name, "state": active.state.value,
            "committed_points": active.committed_points, "completed_points": active.completed_points,
            "completion_pct": round(100 * active.completed_points / active.committed_points, 1)
            if active.committed_points else 0.0,
        } if active else None,
        "carried_forward": carried_forward,
        "commitment_trend": commitment_trend,
        "commitment_trend_sprint_count": len(recent_closed),
    }

    # Blocked / open issues
    blocked = (
        await db.execute(
            select(Story).where(Story.project_id == project_id, Story.is_blocked.is_(True)).limit(25)
        )
    ).scalars().all()

    return {
        "health": health,
        "confidence": {
            "score": confidence.score, "band": confidence.band.value,
            "rule_score": confidence.rule_score, "judge_score": confidence.judge_score,
            "signals": confidence.signals, "rationale": confidence.rationale,
        } if confidence else None,
        "sprint_progress": {
            "name": ref.name, "state": ref.state.value,
            "committed_points": ref.committed_points, "completed_points": ref.completed_points,
            "completion_pct": round(100 * ref.completed_points / ref.committed_points, 1)
            if ref.committed_points else 0.0,
        } if ref else None,
        "status_counts": context["status_counts"],
        "totals": totals,
        "sprint_panel": sprint_panel,
        "risk_cards": (risk.structured or {}).get("risks", []) if risk else [],
        "recommendations": (recs.structured or {}).get("recommendations", []) if recs else [],
        "executive_summary": execu.content if execu else None,
        "open_issues": [
            {"key": b.external_id, "title": b.title, "assignee": b.assignee,
             "status": b.raw_status, "priority": b.priority}
            for b in blocked
        ],
        "signals_available": {
            "simulated": list((await simulated_signals(db, project_id)).keys()),
        },
    }
