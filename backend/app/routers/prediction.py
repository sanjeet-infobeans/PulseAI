import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.delivery_prediction import DeliveryPrediction
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services import prediction_service

router = APIRouter(tags=["prediction"])


class PredictionOut(BaseModel):
    predicted_completion_date: str | None
    baseline_target_date: str | None
    probability_on_time: float
    confidence_pct: float
    reasons: list
    recommendations: list
    created_at: str

    @classmethod
    def of(cls, p: DeliveryPrediction) -> "PredictionOut":
        return cls(
            predicted_completion_date=p.predicted_completion_date.isoformat() if p.predicted_completion_date else None,
            baseline_target_date=p.baseline_target_date.isoformat() if p.baseline_target_date else None,
            probability_on_time=p.probability_on_time, confidence_pct=p.confidence_pct,
            reasons=p.reasons or [], recommendations=p.recommendations or [],
            created_at=p.created_at.isoformat(),
        )


@router.post("/projects/{project_id}/prediction/compute", response_model=PredictionOut)
async def compute_prediction(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)],
    sprint_id: uuid.UUID | None = None,
) -> PredictionOut:
    await _load_project(db, project_id, user)
    row = await prediction_service.predict_completion(db, project_id, sprint_id)
    return PredictionOut.of(row)


@router.get("/projects/{project_id}/prediction", response_model=PredictionOut | None)
async def latest_prediction(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> PredictionOut | None:
    await _load_project(db, project_id, user)
    row = await prediction_service.latest_prediction(db, project_id)
    return PredictionOut.of(row) if row else None
