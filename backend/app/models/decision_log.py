import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DecisionSource(str, enum.Enum):
    teams_sim = "teams_sim"
    transcript_doc = "transcript_doc"
    manual = "manual"


class DecisionStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class DecisionLogEntry(Base):
    """Tracks a customer/stakeholder decision from request to resolution, so
    approval delay and its sprint impact can be measured (Customer Decision
    Delay). requested_at/decided_at are nullable because most current source
    payloads don't carry timestamps yet — see docs/ai-features-gap-analysis-and-plan.md
    Phase 2 note on the #6 hard prerequisite (schema extension to simulated
    Teams payload / transcript extraction) before delay days are real."""

    __tablename__ = "decision_log"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    decided_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[DecisionSource] = mapped_column(
        SQLEnum(DecisionSource, name="decision_source_enum", native_enum=False, length=32),
        nullable=False,
    )
    sprint_impact_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[DecisionStatus] = mapped_column(
        SQLEnum(DecisionStatus, name="decision_status_enum", native_enum=False, length=16),
        nullable=False,
        default=DecisionStatus.pending,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_decision_log_project_status", "project_id", "status"),
    )
