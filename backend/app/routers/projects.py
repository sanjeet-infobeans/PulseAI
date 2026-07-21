import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.customer import Customer
from app.models.project import Project, ProjectStatus
from app.models.user import User, UserRole
from app.routers.auth import CurrentUser, require_super_admin

router = APIRouter(tags=["projects"])


class ProjectIn(BaseModel):
    name: str
    key: str
    description: str | None = None
    start_date: date | None = None
    target_end_date: date | None = None


class ProjectOut(BaseModel):
    id: str
    customer_id: str
    name: str
    key: str
    description: str | None
    status: str
    start_date: date | None
    target_end_date: date | None

    @classmethod
    def of(cls, p: Project) -> "ProjectOut":
        return cls(
            id=str(p.id),
            customer_id=str(p.customer_id),
            name=p.name,
            key=p.key,
            description=p.description,
            status=p.status.value,
            start_date=p.start_date,
            target_end_date=p.target_end_date,
        )


async def _load_project(db: AsyncSession, project_id: uuid.UUID, user: User) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == UserRole.customer:
        customer = await db.get(Customer, project.customer_id)
        if not customer or customer.id != user.customer_id:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    return project


@router.get("/customers/{customer_id}/projects", response_model=list[ProjectOut])
async def list_projects(
    customer_id: uuid.UUID,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ProjectOut]:
    if user.role == UserRole.customer and user.customer_id != customer_id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    rows = (
        await db.execute(
            select(Project)
            .where(Project.customer_id == customer_id)
            .order_by(Project.created_at.desc())
        )
    ).scalars().all()
    return [ProjectOut.of(p) for p in rows]


@router.get("/projects/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: uuid.UUID,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectOut:
    return ProjectOut.of(await _load_project(db, project_id, user))


@router.post(
    "/customers/{customer_id}/projects", response_model=ProjectOut, status_code=201
)
async def create_project(
    customer_id: uuid.UUID,
    body: ProjectIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectOut:
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    project = Project(
        customer_id=customer_id,
        name=body.name.strip(),
        key=body.key.strip().upper(),
        description=body.description,
        status=ProjectStatus.active,
        start_date=body.start_date,
        target_end_date=body.target_end_date,
        created_by=user.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return ProjectOut.of(project)
