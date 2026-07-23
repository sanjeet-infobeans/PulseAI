import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services.sentiment_service import get_sentiment

router = APIRouter(tags=["sentiment"])


@router.get("/projects/{project_id}/sentiment")
async def project_sentiment(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await get_sentiment(db, project_id)
