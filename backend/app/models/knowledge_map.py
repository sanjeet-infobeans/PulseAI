import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class KnowledgeMapEntry(Base):
    """One (module, developer) pairing derived from Story.labels x Story.assignee,
    recomputed wholesale on each run. is_sole_holder flags a module with exactly
    one distinct assignee across all its stories — the knowledge-concentration
    signal for Resource Risk (#7) and Knowledge Gap Detection (#12)."""

    __tablename__ = "knowledge_map"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    module_key: Mapped[str] = mapped_column(String(128), nullable=False)
    developer: Mapped[str] = mapped_column(String(255), nullable=False)
    story_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_touched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_sole_holder: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", "module_key", "developer", name="uq_knowledge_map_project_module_dev"),
    )
