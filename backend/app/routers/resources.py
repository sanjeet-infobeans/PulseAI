import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services.resource_service import compute_resource_risk

router = APIRouter(tags=["resources"])


@router.get("/projects/{project_id}/resources")
async def get_resource_risk(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await compute_resource_risk(db, project_id)
