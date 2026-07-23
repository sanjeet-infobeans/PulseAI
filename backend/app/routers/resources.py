import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.project_resource import LeaveStatus, ProjectResource
from app.models.user import User
from app.routers.auth import CurrentUser, require_super_admin
from app.routers.projects import _load_project
from app.services.resource_service import (
    add_leave,
    compute_resource_risk,
    create_resource,
    delete_leave,
    delete_resource,
    get_resources,
    update_leave,
    update_resource,
)

router = APIRouter(tags=["resources"])


@router.get("/projects/{project_id}/resources")
async def get_resource_risk(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await compute_resource_risk(db, project_id)


@router.get("/projects/{project_id}/resources/roster")
async def project_resources_roster(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    await _load_project(db, project_id, user)
    return await get_resources(db, project_id)


class LeaveIn(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    total_days: int
    status: str = LeaveStatus.pending.value


class LeaveUpdateIn(BaseModel):
    leave_type: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    total_days: int | None = None
    status: str | None = None


class ResourceIn(BaseModel):
    name: str
    employee_code: str | None = None
    designation: str | None = None
    email: str | None = None
    allocation_percentage: float = 100.0
    billable: bool = True
    skills: list[str] = []


class ResourceUpdateIn(BaseModel):
    name: str | None = None
    employee_code: str | None = None
    designation: str | None = None
    email: str | None = None
    allocation_percentage: float | None = None
    billable: bool | None = None
    skills: list[str] | None = None


class LeaveOut(BaseModel):
    leave_id: str
    leave_type: str
    start_date: str
    end_date: str
    total_days: int
    status: str


class ResourceOut(BaseModel):
    resource_id: str
    employee_code: str
    name: str
    designation: str
    email: str
    allocation_percentage: float
    billable: bool
    skills: list[str]
    planned_leaves: list[LeaveOut]

    @classmethod
    def of(cls, r: ProjectResource) -> "ResourceOut":
        return cls(
            resource_id=str(r.id),
            employee_code=r.employee_code or "",
            name=r.name,
            designation=r.designation or "",
            email=r.email or "",
            allocation_percentage=r.allocation_percentage,
            billable=r.billable,
            skills=r.skills or [],
            planned_leaves=[
                LeaveOut(
                    leave_id=str(lv.id), leave_type=lv.leave_type,
                    start_date=lv.start_date.isoformat(), end_date=lv.end_date.isoformat(),
                    total_days=lv.total_days, status=lv.status.value,
                )
                for lv in r.leaves
            ],
        )


@router.post("/projects/{project_id}/resources/roster", response_model=ResourceOut, status_code=201)
async def create_project_resource(
    project_id: uuid.UUID, body: ResourceIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ResourceOut:
    await _load_project(db, project_id, user)
    resource = await create_resource(db, project_id, **body.model_dump())
    return ResourceOut.of(resource)


@router.patch("/projects/{project_id}/resources/roster/{resource_id}", response_model=ResourceOut)
async def update_project_resource(
    project_id: uuid.UUID, resource_id: uuid.UUID, body: ResourceUpdateIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ResourceOut:
    await _load_project(db, project_id, user)
    resource = await update_resource(db, project_id, resource_id, **body.model_dump(exclude_unset=True))
    return ResourceOut.of(resource)


@router.delete("/projects/{project_id}/resources/roster/{resource_id}", status_code=204)
async def delete_project_resource(
    project_id: uuid.UUID, resource_id: uuid.UUID,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await _load_project(db, project_id, user)
    await delete_resource(db, project_id, resource_id)


@router.post(
    "/projects/{project_id}/resources/roster/{resource_id}/leaves",
    response_model=ResourceOut, status_code=201,
)
async def add_resource_leave(
    project_id: uuid.UUID, resource_id: uuid.UUID, body: LeaveIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ResourceOut:
    await _load_project(db, project_id, user)
    resource = await add_leave(
        db, project_id, resource_id,
        leave_type=body.leave_type, start_date=body.start_date, end_date=body.end_date,
        total_days=body.total_days, status=LeaveStatus(body.status),
    )
    return ResourceOut.of(resource)


@router.patch(
    "/projects/{project_id}/resources/roster/{resource_id}/leaves/{leave_id}",
    response_model=ResourceOut,
)
async def update_resource_leave(
    project_id: uuid.UUID, resource_id: uuid.UUID, leave_id: uuid.UUID, body: LeaveUpdateIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ResourceOut:
    await _load_project(db, project_id, user)
    data = body.model_dump(exclude_unset=True)
    if "status" in data and data["status"] is not None:
        data["status"] = LeaveStatus(data["status"])
    resource = await update_leave(db, project_id, resource_id, leave_id, **data)
    return ResourceOut.of(resource)


@router.delete(
    "/projects/{project_id}/resources/roster/{resource_id}/leaves/{leave_id}",
    status_code=204,
)
async def delete_resource_leave(
    project_id: uuid.UUID, resource_id: uuid.UUID, leave_id: uuid.UUID,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await _load_project(db, project_id, user)
    await delete_leave(db, project_id, resource_id, leave_id)
