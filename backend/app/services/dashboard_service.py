"""Composite dashboard payload — one call feeds the whole bento view."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_analysis import AnalysisKind
from app.models.sprint import Sprint, SprintState
from app.models.story import Story
from app.services import analysis_service, confidence_service
from app.services.retrieval import build_context, simulated_signals


async def get_dashboard(db: AsyncSession, project_id: uuid.UUID) -> dict:
    context = await build_context(db, project_id)
    totals = context["totals"]

    # Health = delivery completion (distinct from confidence)
    health = round(totals["completion_pct"])

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
        "timeline": [
            {"name": s.name, "state": s.state.value,
             "completion_pct": round(100 * s.completed_points / s.committed_points, 1)
             if s.committed_points else 0.0}
            for s in sprints
        ],
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
