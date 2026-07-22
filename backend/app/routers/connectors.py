import re
import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.connectors.registry import get_connector
from app.database import get_db
from app.models.connector import Connector, ConnectorMode, ConnectorStatus, ConnectorType
from app.models.sprint import Sprint
from app.models.story import Story
from app.models.user import User
from app.routers.auth import CurrentUser, require_super_admin
from app.routers.projects import _load_project
from app.services.jira_sync import run_sync

router = APIRouter(tags=["connectors"])

# secret_ref is a column *name* in Connector.secret_ref (String(128)), never the
# secret itself — must look like an env var name, not an arbitrary token.
_ENV_VAR_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,127}$")


def _validate_secret_ref(secret_ref: str | None) -> None:
    if secret_ref is None:
        return
    if not _ENV_VAR_NAME_RE.match(secret_ref):
        raise HTTPException(
            status_code=400,
            detail=(
                "Token secret ref must be the NAME of a server-side environment "
                "variable (e.g. JIRA_TOKEN_ATLAS), not the token itself, and at "
                "most 128 characters."
            ),
        )


class ConnectorIn(BaseModel):
    type: ConnectorType
    mode: ConnectorMode = ConnectorMode.real
    config: dict = {}
    secret_ref: str | None = None


class ConnectorOut(BaseModel):
    id: str
    project_id: str
    type: str
    mode: str
    status: str
    config: dict
    secret_ref: str | None
    last_synced_at: str | None
    last_error: str | None

    @classmethod
    def of(cls, c: Connector) -> "ConnectorOut":
        return cls(
            id=str(c.id), project_id=str(c.project_id), type=c.type.value,
            mode=c.mode.value, status=c.status.value, config=c.config or {},
            secret_ref=c.secret_ref,
            last_synced_at=c.last_synced_at.isoformat() if c.last_synced_at else None,
            last_error=c.last_error,
        )


async def _load_connector(db: AsyncSession, project_id: uuid.UUID, cid: uuid.UUID, user: User) -> Connector:
    await _load_project(db, project_id, user)  # enforces project scope
    connector = await db.get(Connector, cid)
    if not connector or connector.project_id != project_id:
        raise HTTPException(status_code=404, detail="Connector not found")
    return connector


@router.get("/projects/{project_id}/connectors", response_model=list[ConnectorOut])
async def list_connectors(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[ConnectorOut]:
    await _load_project(db, project_id, user)
    rows = (
        await db.execute(select(Connector).where(Connector.project_id == project_id))
    ).scalars().all()
    return [ConnectorOut.of(c) for c in rows]


@router.post("/projects/{project_id}/connectors", response_model=ConnectorOut, status_code=201)
async def assign_connector(
    project_id: uuid.UUID,
    body: ConnectorIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ConnectorOut:
    await _load_project(db, project_id, user)
    _validate_secret_ref(body.secret_ref)
    existing = (
        await db.execute(
            select(Connector).where(
                Connector.project_id == project_id, Connector.type == body.type
            )
        )
    ).scalar_one_or_none()
    if existing:
        existing.mode = body.mode
        existing.config = body.config
        existing.secret_ref = body.secret_ref
        existing.status = ConnectorStatus.unconfigured
        connector = existing
    else:
        connector = Connector(
            project_id=project_id, type=body.type, mode=body.mode,
            config=body.config, secret_ref=body.secret_ref,
            status=ConnectorStatus.unconfigured,
        )
        db.add(connector)
    await db.commit()
    await db.refresh(connector)
    return ConnectorOut.of(connector)


@router.post("/projects/{project_id}/connectors/{cid}/test")
async def test_connector(
    project_id: uuid.UUID, cid: uuid.UUID,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    connector = await _load_connector(db, project_id, cid, user)
    await get_connector(connector).test_connection()
    connector.status = ConnectorStatus.connected
    connector.last_error = None
    await db.commit()
    return {"status": "connected"}


@router.post("/projects/{project_id}/connectors/{cid}/sync", status_code=202)
async def sync_connector(
    project_id: uuid.UUID, cid: uuid.UUID,
    background: BackgroundTasks,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    connector = await _load_connector(db, project_id, cid, user)
    connector.status = ConnectorStatus.syncing
    await db.commit()
    background.add_task(run_sync, connector.id)
    return {"status": "syncing", "connector_id": str(connector.id)}


@router.get("/projects/{project_id}/connectors/{cid}/status", response_model=ConnectorOut)
async def connector_status(
    project_id: uuid.UUID, cid: uuid.UUID,
    user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)],
) -> ConnectorOut:
    return ConnectorOut.of(await _load_connector(db, project_id, cid, user))


# ── Delivery reads (populated by sync) ────────────────────────────────────────

class SprintOut(BaseModel):
    id: str
    external_id: str
    name: str
    state: str
    goal: str | None
    start_date: str | None
    end_date: str | None
    committed_points: float
    completed_points: float

    @classmethod
    def of(cls, s: Sprint) -> "SprintOut":
        return cls(
            id=str(s.id), external_id=s.external_id, name=s.name, state=s.state.value,
            goal=s.goal,
            start_date=s.start_date.isoformat() if s.start_date else None,
            end_date=s.end_date.isoformat() if s.end_date else None,
            committed_points=s.committed_points, completed_points=s.completed_points,
        )


class StoryOut(BaseModel):
    id: str
    external_id: str
    title: str
    issue_type: str
    status_category: str
    raw_status: str | None
    story_points: float | None
    assignee: str | None
    priority: str | None
    is_blocked: bool

    @classmethod
    def of(cls, s: Story) -> "StoryOut":
        return cls(
            id=str(s.id), external_id=s.external_id, title=s.title,
            issue_type=s.issue_type.value, status_category=s.status_category.value,
            raw_status=s.raw_status, story_points=s.story_points, assignee=s.assignee,
            priority=s.priority, is_blocked=s.is_blocked,
        )


@router.get("/projects/{project_id}/sprints", response_model=list[SprintOut])
async def list_sprints(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[SprintOut]:
    await _load_project(db, project_id, user)
    rows = (
        await db.execute(
            select(Sprint).where(Sprint.project_id == project_id).order_by(Sprint.sequence)
        )
    ).scalars().all()
    return [SprintOut.of(s) for s in rows]


@router.get("/projects/{project_id}/stories", response_model=list[StoryOut])
async def list_stories(
    project_id: uuid.UUID,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    sprint_id: uuid.UUID | None = None,
) -> list[StoryOut]:
    await _load_project(db, project_id, user)
    stmt = select(Story).where(Story.project_id == project_id)
    if sprint_id:
        stmt = stmt.where(Story.sprint_id == sprint_id)
    rows = (await db.execute(stmt.order_by(Story.external_id))).scalars().all()
    return [StoryOut.of(s) for s in rows]
