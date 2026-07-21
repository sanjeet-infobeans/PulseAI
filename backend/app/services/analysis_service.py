import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.ai_analysis import AIAnalysis, AnalysisKind
from app.models.llm_call_log import LLMFeature


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
