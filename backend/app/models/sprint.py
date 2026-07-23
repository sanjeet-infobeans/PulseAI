import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SprintState(str, enum.Enum):
    future = "future"
    active = "active"
    closed = "closed"


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    connector_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("connectors.id", ondelete="SET NULL"), nullable=True
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[SprintState] = mapped_column(
        SQLEnum(SprintState, name="sprint_state_enum", native_enum=False),
        nullable=False,
        default=SprintState.future,
    )
    goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    complete_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    committed_points: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    completed_points: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_sprints_project_external"),
    )

    project: Mapped["Project"] = relationship("Project", back_populates="sprints")
    stories: Mapped[list["Story"]] = relationship(
        "Story", back_populates="sprint", foreign_keys="Story.sprint_id"
    )
