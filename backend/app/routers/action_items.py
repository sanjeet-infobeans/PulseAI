import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.action_item import ActionItem, ActionItemStatus
from app.models.user import User
from app.routers.auth import CurrentUser, require_super_admin
from app.routers.projects import _load_project
from app.services.action_item_service import get_action_items_summary, set_action_item_status

router = APIRouter(tags=["action-items"])


@router.get("/projects/{project_id}/action-items")
async def get_action_items(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await get_action_items_summary(db, project_id)


class ActionItemStatusIn(BaseModel):
    status: str


class ActionItemOut(BaseModel):
    id: str
    item: str
    status: str
    created_at: str

    @classmethod
    def of(cls, a: ActionItem) -> "ActionItemOut":
        return cls(id=str(a.id), item=a.item, status=a.status.value, created_at=a.created_at.isoformat())


@router.patch("/projects/{project_id}/action-items/{item_id}", response_model=ActionItemOut)
async def update_action_item_status(
    project_id: uuid.UUID, item_id: uuid.UUID, body: ActionItemStatusIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ActionItemOut:
    await _load_project(db, project_id, user)
    item = await set_action_item_status(db, project_id, item_id, ActionItemStatus(body.status))
    return ActionItemOut.of(item)
