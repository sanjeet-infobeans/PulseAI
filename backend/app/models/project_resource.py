"""Real, DB-backed team roster + planned leaves for a project — coexists with
(does not replace) the simulated `resource` connector payload in
seed_simulated.py: resource_service.get_resources() prefers real rows here
and only falls back to the simulated dataset when a project has none.
"""
import enum
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LeaveStatus(str, enum.Enum):
    # Title-case values are required, not lower_snake — existing read code
    # (resource_service.get_resources(), resources-content.tsx) does exact
    # string comparison against "Approved".
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


class ProjectResource(Base):
    __tablename__ = "project_resources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    employee_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    designation: Mapped[str | None] = mapped_column(String(128), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    allocation_percentage: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    billable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    skills: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc), nullable=False,
    )

    project: Mapped["Project"] = relationship("Project")
    leaves: Mapped[list["ResourceLeave"]] = relationship(
        "ResourceLeave", back_populates="resource", cascade="all, delete-orphan"
    )


class ResourceLeave(Base):
    __tablename__ = "resource_leaves"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("project_resources.id", ondelete="CASCADE"), nullable=False
    )
    leave_type: Mapped[str] = mapped_column(String(64), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_days: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[LeaveStatus] = mapped_column(
        SQLEnum(LeaveStatus, name="leave_status_enum", native_enum=False),
        nullable=False, default=LeaveStatus.pending,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc), nullable=False,
    )

    resource: Mapped["ProjectResource"] = relationship("ProjectResource", back_populates="leaves")
