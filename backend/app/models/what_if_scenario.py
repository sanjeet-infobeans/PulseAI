import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WhatIfScenario(Base):
    """Log of one what-if simulation run — not a trend, just a history of
    questions asked and the LLM's estimated impact vs baseline."""

    __tablename__ = "what_if_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    requested_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    scenario_text: Mapped[str] = mapped_column(Text, nullable=False)
    scenario_input: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    estimated_weeks: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    resources_needed: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    risk_delta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    confidence_delta: Mapped[float | None] = mapped_column(Float, nullable=True)
    result_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_what_if_scenarios_project", "project_id", "created_at"),
    )
