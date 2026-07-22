import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services.dashboard_service import get_dashboard
from app.services.scope_service import compute_scope_creep

router = APIRouter(tags=["dashboard"])


@router.get("/projects/{project_id}/dashboard")
async def project_dashboard(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await get_dashboard(db, project_id)


@router.get("/projects/{project_id}/scope-creep")
async def scope_creep(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await compute_scope_creep(db, project_id)
