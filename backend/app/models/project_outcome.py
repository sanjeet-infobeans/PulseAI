import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProjectOutcome(Base):
    """Captured once a project completes — the corpus Delivery DNA (#11) needs
    to eventually group by Customer.industry and answer "can this team build
    another X". Phase 3 per docs/ai-features-gap-analysis-and-plan.md: this
    table is created now purely so outcomes start accumulating; no
    archetype-matching logic is built against it yet — a single org with a
    handful of projects isn't enough of a corpus to derive real probabilities."""

    __tablename__ = "project_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    actual_duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_velocity_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    defect_density: Mapped[float | None] = mapped_column(Float, nullable=True)
    delivered_on_time: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", name="uq_project_outcomes_project"),
    )
