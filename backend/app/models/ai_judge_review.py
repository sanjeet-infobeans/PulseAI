import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AIJudgeReview(Base):
    """A second-pass LLM critique of one ai_analyses row: does it cover the
    delivery data, what did it miss. Mirrors the judge pattern already used in
    confidence_service.py's confidence_judge_messages, applied to analyses
    instead of the confidence score."""

    __tablename__ = "ai_judge_reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ai_analyses.id", ondelete="CASCADE"), nullable=False
    )
    coverage_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    missing_risks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    missing_stories_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confidence_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_ai_judge_reviews_analysis", "analysis_id", "created_at"),
    )
