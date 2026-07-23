"""Action items compiled from meeting/decision transcripts — extracted
per-document into DocumentExtraction.extraction["action_items"] (see
prompts._DOC_TASK["transcript"]) but not otherwise aggregated. Mirrors
decision_log.py's sync-from-documents pattern (#6) so open action items can
be tracked and closed over time instead of read once from raw JSON.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ActionItemStatus(str, enum.Enum):
    open = "open"
    done = "done"


class ActionItem(Base):
    __tablename__ = "action_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    item: Mapped[str] = mapped_column(Text, nullable=False)
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[ActionItemStatus] = mapped_column(
        SQLEnum(ActionItemStatus, name="action_item_status_enum", native_enum=False),
        nullable=False, default=ActionItemStatus.open,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_action_items_project_status", "project_id", "status"),
    )
