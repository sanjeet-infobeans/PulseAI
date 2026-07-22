"""AI Judge (#10): a second-pass LLM critique of an existing ai_analyses row.
Mirrors the judge pattern already proven in confidence_service.py's
confidence_judge_messages, applied to analyses instead of the confidence score.
"""
import json
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.ai_analysis import AIAnalysis
from app.models.ai_judge_review import AIJudgeReview
from app.models.llm_call_log import LLMFeature
from app.services.retrieval import build_context


def _clamp_pct(v, lo=0.0, hi=100.0) -> float:
    try:
        return round(max(lo, min(hi, float(v))), 1)
    except (TypeError, ValueError):
        return 0.0


def _clamp_int(v) -> int:
    try:
        return max(0, int(v))
    except (TypeError, ValueError):
        return 0


async def review_analysis(db: AsyncSession, analysis_id: uuid.UUID) -> AIJudgeReview:
    analysis = await db.get(AIAnalysis, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    context = await build_context(db, analysis.project_id, analysis.sprint_id)
    raw = await client.complete(
        feature=LLMFeature.analysis,
        messages=prompts.judge_review_messages(
            analysis.kind.value, analysis.content, analysis.structured or {}, context
        ),
        model=settings.llm_model_judge,
        project_id=analysis.project_id,
        temperature=0.1,
        json_mode=True,
    )
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        d = {}

    review = AIJudgeReview(
        project_id=analysis.project_id,
        analysis_id=analysis.id,
        coverage_pct=_clamp_pct(d.get("coverage_pct", 0)),
        missing_risks_count=_clamp_int(d.get("missing_risks_count", 0)),
        missing_stories_count=_clamp_int(d.get("missing_stories_count", 0)),
        confidence_pct=_clamp_pct(d.get("confidence_pct", 0)),
        notes=d.get("notes") or "",
        model=settings.llm_model_judge,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def latest_review(db: AsyncSession, analysis_id: uuid.UUID) -> AIJudgeReview | None:
    return (
        await db.execute(
            select(AIJudgeReview)
            .where(AIJudgeReview.analysis_id == analysis_id)
            .order_by(AIJudgeReview.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
