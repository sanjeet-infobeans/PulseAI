import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.ai_analysis import AIAnalysis, AnalysisKind
from app.models.confidence import ConfidenceScore
from app.models.llm_call_log import LLMFeature
from app.models.metric_snapshot import MetricSnapshot


async def generate_analysis(
    db: AsyncSession,
    project_id: uuid.UUID,
    kind: AnalysisKind,
    context: dict,
    sprint_id: uuid.UUID | None = None,
    user_id: uuid.UUID | None = None,
) -> AIAnalysis:
    content = await client.complete(
        feature=LLMFeature.analysis,
        messages=prompts.analysis_messages(kind, context),
        model=settings.llm_model_analysis,
        project_id=project_id,
        temperature=0.3,
    )

    structured: dict = {}
    json_messages = prompts.analysis_json_messages(kind, context)
    if json_messages:
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=json_messages,
            model=settings.llm_model_analysis,
            project_id=project_id,
            temperature=0.1,
            json_mode=True,
        )
        try:
            structured = json.loads(raw)
        except json.JSONDecodeError:
            structured = {}

    analysis = AIAnalysis(
        project_id=project_id,
        sprint_id=sprint_id,
        kind=kind,
        content=content,
        structured=structured,
        model=settings.llm_model_analysis,
        generated_by=user_id,
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def _executive_enrichment(db: AsyncSession, project_id: uuid.UUID) -> dict:
    """Confidence delta + scope-change %, both already accumulating from Phase 1
    infra (ConfidenceScore is append-only; metric_snapshots is written every
    Jira sync) — this is packaging, not new computation (see #9 in
    docs/ai-features-gap-analysis-and-plan.md)."""
    scores = (
        await db.execute(
            select(ConfidenceScore)
            .where(ConfidenceScore.project_id == project_id)
            .order_by(ConfidenceScore.created_at.desc())
            .limit(2)
        )
    ).scalars().all()
    confidence_trend = None
    if scores:
        confidence_trend = {
            "current_score": scores[0].score,
            "current_band": scores[0].band.value,
            "previous_score": scores[1].score if len(scores) > 1 else None,
            "delta": round(scores[0].score - scores[1].score, 1) if len(scores) > 1 else None,
        }

    scope_rows = (
        await db.execute(
            select(MetricSnapshot)
            .where(
                MetricSnapshot.project_id == project_id,
                MetricSnapshot.metric_key == "scope_point_total",
            )
            .order_by(MetricSnapshot.recorded_at.asc())
        )
    ).scalars().all()
    scope_change_pct = None
    if len(scope_rows) >= 2 and scope_rows[0].value:
        scope_change_pct = round(
            100 * (scope_rows[-1].value - scope_rows[0].value) / scope_rows[0].value, 1
        )

    return {"confidence_trend": confidence_trend, "scope_change_pct": scope_change_pct}


async def generate_executive_briefing(db: AsyncSession, project_id: uuid.UUID) -> AIAnalysis | None:
    """Nightly-cron entry point (#9): same generate_analysis path as the
    on-demand executive tab, enriched with confidence/scope trend so the
    briefing can name a direction, not just a snapshot, plus an explicit
    intervention_needed flag in the structured JSON. Skips projects with no
    delivery data yet, same guard as the on-demand endpoint."""
    from app.services.retrieval import build_context

    context = await build_context(db, project_id)
    if context["totals"]["stories"] == 0:
        return None
    context = {**context, **await _executive_enrichment(db, project_id)}
    return await generate_analysis(db, project_id, AnalysisKind.executive, context)


async def latest_analysis(
    db: AsyncSession, project_id: uuid.UUID, kind: AnalysisKind
) -> AIAnalysis | None:
    return (
        await db.execute(
            select(AIAnalysis)
            .where(AIAnalysis.project_id == project_id, AIAnalysis.kind == kind)
            .order_by(AIAnalysis.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
