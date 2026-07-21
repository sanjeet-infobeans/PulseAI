import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ConfidenceBand(str, enum.Enum):
    red = "red"
    amber = "amber"
    green = "green"


class ConfidenceScore(Base):
    __tablename__ = "confidence_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    sprint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    band: Mapped[ConfidenceBand] = mapped_column(
        SQLEnum(ConfidenceBand, name="confidence_band_enum", native_enum=False), nullable=False
    )
    rule_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    judge_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    signals: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (Index("ix_confidence_project", "project_id", "created_at"),)
