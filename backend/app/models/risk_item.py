"""Persisted risk registry, scanned by the Risk Identifier agent (see
prompts.risk_identification_messages / risk_service.py). Unlike the ephemeral
AnalysisKind.risk narrative (a fresh unlinked list per generation), rows here
have a real active/mitigated/closed lifecycle so "active risks" means
something — upserted by title across scans, not regenerated from scratch.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RiskSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RiskStatus(str, enum.Enum):
    active = "active"
    mitigated = "mitigated"
    closed = "closed"


class RiskSourceType(str, enum.Enum):
    transcript_doc = "transcript_doc"
    brd_doc = "brd_doc"
    change_request_doc = "change_request_doc"
    sprint_signal = "sprint_signal"
    manual = "manual"


class RiskItem(Base):
    __tablename__ = "risk_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[RiskSeverity] = mapped_column(
        SQLEnum(RiskSeverity, name="risk_severity_enum", native_enum=False),
        nullable=False, default=RiskSeverity.medium,
    )
    status: Mapped[RiskStatus] = mapped_column(
        SQLEnum(RiskStatus, name="risk_status_enum", native_enum=False),
        nullable=False, default=RiskStatus.active,
    )
    source_type: Mapped[RiskSourceType] = mapped_column(
        SQLEnum(RiskSourceType, name="risk_source_type_enum", native_enum=False),
        nullable=False, default=RiskSourceType.sprint_signal,
    )
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )
    first_detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)

    __table_args__ = (
        Index("ix_risk_items_project_status", "project_id", "status"),
    )
