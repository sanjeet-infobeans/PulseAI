import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.customer import Customer
from app.models.project import Project, ProjectIndustry, ProjectStatus
from app.models.project_outcome import ProjectOutcome
from app.models.user import User, UserRole
from app.routers.auth import CurrentUser, require_super_admin
from app.services import response_cache
from app.services.outcome_service import get_outcome, mark_project_outcome

router = APIRouter(tags=["projects"])


class ProjectIn(BaseModel):
    name: str
    key: str
    description: str | None = None
    start_date: date | None = None
    target_end_date: date | None = None
    industry: str | None = None
    total_person_hours: float | None = None


class ProjectUpdateIn(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    start_date: date | None = None
    target_end_date: date | None = None
    industry: str | None = None
    total_person_hours: float | None = None


class ProjectOut(BaseModel):
    id: str
    customer_id: str
    name: str
    key: str
    description: str | None
    status: str
    start_date: date | None
    target_end_date: date | None
    industry: str | None
    total_person_hours: float | None

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
            industry=p.industry.value if p.industry else None,
            total_person_hours=p.total_person_hours,
        )


def _coerce_industry(value: str | None) -> ProjectIndustry | None:
    if value is None:
        return None
    try:
        return ProjectIndustry(value)
    except ValueError:
        raise HTTPException(status_code=422, detail=f"Invalid industry: {value!r}")


def _coerce_status(value: str | None) -> ProjectStatus | None:
    if value is None:
        return None
    try:
        return ProjectStatus(value)
    except ValueError:
        raise HTTPException(status_code=422, detail=f"Invalid status: {value!r}")


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
        industry=_coerce_industry(body.industry),
        total_person_hours=body.total_person_hours,
        created_by=user.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return ProjectOut.of(project)


@router.patch("/projects/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdateIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectOut:
    project = await _load_project(db, project_id, user)
    data = body.model_dump(exclude_unset=True)
    if "industry" in data:
        data["industry"] = _coerce_industry(data["industry"])
    if "status" in data:
        data["status"] = _coerce_status(data["status"])
    if "name" in data and data["name"] is not None:
        data["name"] = data["name"].strip()
    for k, v in data.items():
        setattr(project, k, v)
    await db.commit()
    await db.refresh(project)
    await response_cache.invalidate_project_views(project_id)
    return ProjectOut.of(project)


class OutcomeIn(BaseModel):
    delivered_on_time: bool


class OutcomeOut(BaseModel):
    actual_duration_days: int | None
    actual_velocity_avg: float | None
    defect_density: float | None
    delivered_on_time: bool | None
    closed_at: str | None

    @classmethod
    def of(cls, o: ProjectOutcome) -> "OutcomeOut":
        return cls(
            actual_duration_days=o.actual_duration_days, actual_velocity_avg=o.actual_velocity_avg,
            defect_density=o.defect_density, delivered_on_time=o.delivered_on_time,
            closed_at=o.closed_at.isoformat() if o.closed_at else None,
        )


@router.post("/projects/{project_id}/outcome", response_model=OutcomeOut)
async def mark_outcome(
    project_id: uuid.UUID, body: OutcomeIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> OutcomeOut:
    await _load_project(db, project_id, user)
    outcome = await mark_project_outcome(db, project_id, body.delivered_on_time)
    return OutcomeOut.of(outcome)


@router.get("/projects/{project_id}/outcome", response_model=OutcomeOut | None)
async def get_project_outcome(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> OutcomeOut | None:
    await _load_project(db, project_id, user)
    outcome = await get_outcome(db, project_id)
    return OutcomeOut.of(outcome) if outcome else None
