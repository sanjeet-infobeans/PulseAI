import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.risk_item import RiskItem, RiskStatus
from app.models.user import User
from app.routers.auth import CurrentUser, require_super_admin
from app.routers.projects import _load_project
from app.services.risk_service import get_active_risks, resolve_risk, scan_project_risks

router = APIRouter(tags=["risks"])


class RiskItemOut(BaseModel):
    id: str
    title: str
    description: str | None
    severity: str
    status: str
    last_seen_at: str

    @classmethod
    def of(cls, r: RiskItem) -> "RiskItemOut":
        return cls(
            id=str(r.id), title=r.title, description=r.description,
            severity=r.severity.value, status=r.status.value,
            last_seen_at=r.last_seen_at.isoformat(),
        )


@router.get("/projects/{project_id}/risks", response_model=list[RiskItemOut])
async def list_active_risks(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[RiskItemOut]:
    await _load_project(db, project_id, user)
    risks = await get_active_risks(db, project_id)
    return [RiskItemOut.of(r) for r in risks]


@router.post("/projects/{project_id}/risks/scan", response_model=list[RiskItemOut])
async def scan_risks(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[RiskItemOut]:
    await _load_project(db, project_id, user)
    risks = await scan_project_risks(db, project_id)
    return [RiskItemOut.of(r) for r in risks if r.status == RiskStatus.active]


class RiskStatusIn(BaseModel):
    status: str


@router.patch("/projects/{project_id}/risks/{risk_id}", response_model=RiskItemOut)
async def update_risk_status(
    project_id: uuid.UUID, risk_id: uuid.UUID, body: RiskStatusIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RiskItemOut:
    await _load_project(db, project_id, user)
    risk = await resolve_risk(db, project_id, risk_id, RiskStatus(body.status))
    return RiskItemOut.of(risk)
