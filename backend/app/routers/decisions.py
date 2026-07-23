import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services.decision_service import get_decision_summary

router = APIRouter(tags=["decisions"])


@router.get("/projects/{project_id}/decisions")
async def get_decisions(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await get_decision_summary(db, project_id)
