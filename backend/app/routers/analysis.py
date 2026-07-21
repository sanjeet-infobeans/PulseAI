import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.ai_analysis import AIAnalysis, AnalysisKind
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services import analysis_service
from app.services.retrieval import build_context

router = APIRouter(tags=["analysis"])


class AnalysisOut(BaseModel):
    id: str
    kind: str
    content: str
    structured: dict
    created_at: str

    @classmethod
    def of(cls, a: AIAnalysis) -> "AnalysisOut":
        return cls(
            id=str(a.id), kind=a.kind.value, content=a.content,
            structured=a.structured or {}, created_at=a.created_at.isoformat(),
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
