import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.confidence import ConfidenceScore
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services import confidence_service
from app.services.alignment_service import compute_alignment

router = APIRouter(tags=["confidence"])


class ConfidenceOut(BaseModel):
    score: float
    band: str
    rule_score: float
    judge_score: float
    signals: list
    rationale: str | None
    created_at: str

    @classmethod
    def of(cls, c: ConfidenceScore) -> "ConfidenceOut":
        return cls(
            score=c.score, band=c.band.value, rule_score=c.rule_score,
            judge_score=c.judge_score, signals=c.signals or [], rationale=c.rationale,
            created_at=c.created_at.isoformat(),
        )


@router.post("/projects/{project_id}/confidence/compute", response_model=ConfidenceOut)
async def compute(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)],
    sprint_id: uuid.UUID | None = None,
) -> ConfidenceOut:
    await _load_project(db, project_id, user)
    row = await confidence_service.compute_confidence(db, project_id, sprint_id)
    return ConfidenceOut.of(row)


@router.get("/projects/{project_id}/confidence", response_model=ConfidenceOut | None)
async def latest(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> ConfidenceOut | None:
    await _load_project(db, project_id, user)
    row = await confidence_service.latest_confidence(db, project_id)
    return ConfidenceOut.of(row) if row else None


@router.post("/projects/{project_id}/alignment")
async def alignment(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    """Validate all stories against the documented requirements knowledge base."""
    await _load_project(db, project_id, user)
    return await compute_alignment(db, project_id)
