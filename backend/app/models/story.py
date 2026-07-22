import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.status_ref import StatusCategory


class IssueType(str, enum.Enum):
    story = "story"
    bug = "bug"
    task = "task"
    epic = "epic"
    subtask = "subtask"


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    sprint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True
    )
    connector_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("connectors.id", ondelete="SET NULL"), nullable=True
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    issue_type: Mapped[IssueType] = mapped_column(
        SQLEnum(IssueType, name="issue_type_enum", native_enum=False),
        nullable=False,
        default=IssueType.story,
    )
    status_category: Mapped[StatusCategory] = mapped_column(
        SQLEnum(StatusCategory, name="status_category_enum", native_enum=False),
        nullable=False,
        default=StatusCategory.todo,
    )
    raw_status: Mapped[str | None] = mapped_column(String(128), nullable=True)
    story_points: Mapped[float | None] = mapped_column(Float, nullable=True)
    assignee: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reporter: Mapped[str | None] = mapped_column(String(255), nullable=True)
    priority: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    blocked_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    labels: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # Incremented in jira_sync when a re-sync catches a story flip from `done`
    # back to a non-done category — the requirement-volatility (#5) reopen signal.
    reopened_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_ext: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_ext: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_ext: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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
        UniqueConstraint("project_id", "external_id", name="uq_stories_project_external"),
        Index("ix_stories_project_sprint", "project_id", "sprint_id"),
        Index("ix_stories_project_status", "project_id", "status_category"),
    )

    project: Mapped["Project"] = relationship("Project", back_populates="stories")
    sprint: Mapped["Sprint | None"] = relationship("Sprint", back_populates="stories")
