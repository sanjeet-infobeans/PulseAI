import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Index, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RequirementSourceType(str, enum.Enum):
    brd = "brd"
    change_request = "change_request"
    transcript = "transcript"
    manual = "manual"


class RequirementStatus(str, enum.Enum):
    proposed = "proposed"
    covered = "covered"
    missing = "missing"
    superseded = "superseded"
    out_of_scope = "out_of_scope"


class RequirementItem(Base):
    """A persisted requirement-like statement extracted from a document, so it
    can be diffed/traced over time instead of recomputed ad-hoc on every call
    (see retrieval.py::_doc_requirements, which this table replaces as the
    source of truth for scope-creep, requirement-drift, and volatility)."""

    __tablename__ = "requirement_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )
    source_type: Mapped[RequirementSourceType] = mapped_column(
        SQLEnum(RequirementSourceType, name="requirement_source_type_enum", native_enum=False, length=32),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[RequirementStatus] = mapped_column(
        SQLEnum(RequirementStatus, name="requirement_status_enum", native_enum=False, length=32),
        nullable=False,
        default=RequirementStatus.proposed,
    )
    matched_story_keys: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    superseded_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requirement_items.id", ondelete="SET NULL"), nullable=True
    )

    __table_args__ = (
        Index("ix_requirement_items_project_status", "project_id", "status"),
    )
