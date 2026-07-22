import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.ai_analysis import AIAnalysis, AnalysisKind
from app.models.ai_judge_review import AIJudgeReview
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services import analysis_service, judge_service
from app.services.retrieval import build_context

router = APIRouter(tags=["analysis"])


class AnalysisOut(BaseModel):
    id: str
    kind: str
    content: str
    structured: dict
    generated_by: str | None
    created_at: str

    @classmethod
    def of(cls, a: AIAnalysis) -> "AnalysisOut":
        return cls(
            id=str(a.id), kind=a.kind.value, content=a.content,
            structured=a.structured or {}, generated_by=str(a.generated_by) if a.generated_by else None,
            created_at=a.created_at.isoformat(),
        )


@router.post("/projects/{project_id}/analysis/{kind}", response_model=AnalysisOut)
async def run_analysis(
    project_id: uuid.UUID,
    kind: AnalysisKind,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    sprint_id: uuid.UUID | None = None,
) -> AnalysisOut:
    await _load_project(db, project_id, user)
    context = await build_context(db, project_id, sprint_id)
    if context["totals"]["stories"] == 0:
        raise HTTPException(status_code=409, detail="No delivery data yet — sync Jira first")
    if kind == AnalysisKind.executive:
        context = {**context, **await analysis_service._executive_enrichment(db, project_id)}
    analysis = await analysis_service.generate_analysis(
        db, project_id, kind, context, sprint_id=sprint_id, user_id=user.id
    )
    return AnalysisOut.of(analysis)


@router.get("/projects/{project_id}/analysis/{kind}", response_model=AnalysisOut | None)
async def get_latest_analysis(
    project_id: uuid.UUID,
    kind: AnalysisKind,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AnalysisOut | None:
    await _load_project(db, project_id, user)
    latest = await analysis_service.latest_analysis(db, project_id, kind)
    return AnalysisOut.of(latest) if latest else None


class JudgeReviewOut(BaseModel):
    id: str
    analysis_id: str
    coverage_pct: float
    missing_risks_count: int
    missing_stories_count: int
    confidence_pct: float
    notes: str | None
    created_at: str

    @classmethod
    def of(cls, r: AIJudgeReview) -> "JudgeReviewOut":
        return cls(
            id=str(r.id), analysis_id=str(r.analysis_id), coverage_pct=r.coverage_pct,
            missing_risks_count=r.missing_risks_count, missing_stories_count=r.missing_stories_count,
            confidence_pct=r.confidence_pct, notes=r.notes, created_at=r.created_at.isoformat(),
        )


@router.post("/projects/{project_id}/analysis/{analysis_id}/judge", response_model=JudgeReviewOut)
async def judge_analysis(
    project_id: uuid.UUID,
    analysis_id: uuid.UUID,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JudgeReviewOut:
    await _load_project(db, project_id, user)
    analysis = await db.get(AIAnalysis, analysis_id)
    if not analysis or analysis.project_id != project_id:
        raise HTTPException(status_code=404, detail="Analysis not found")
    review = await judge_service.review_analysis(db, analysis_id)
    return JudgeReviewOut.of(review)


@router.get("/projects/{project_id}/analysis/{analysis_id}/judge", response_model=JudgeReviewOut | None)
async def get_latest_judge_review(
    project_id: uuid.UUID,
    analysis_id: uuid.UUID,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JudgeReviewOut | None:
    await _load_project(db, project_id, user)
    review = await judge_service.latest_review(db, analysis_id)
    return JudgeReviewOut.of(review) if review else None
