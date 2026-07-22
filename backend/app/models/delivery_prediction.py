import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DeliveryPrediction(Base):
    """Append-only, like ConfidenceScore: one row per prediction run so the
    predicted-vs-actual completion date is trendable over time."""

    __tablename__ = "delivery_predictions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    sprint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True
    )
    predicted_completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    baseline_target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    probability_on_time: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reasons: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    recommendations: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_delivery_predictions_project", "project_id", "created_at"),
    )
