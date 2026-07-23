import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DependencyRelation(str, enum.Enum):
    blocks = "blocks"
    depends_on = "depends_on"
    mentioned_in = "mentioned_in"
    derived_from = "derived_from"
    impacts = "impacts"


class DependencyEdge(Base):
    """One LLM- or rule-inferred link in a delivery dependency chain, e.g.
    Story(Payment Gateway) --depends_on--> Story(Tax API) --blocks--> QA.
    from_ref/to_ref are free-form references (a story key, doc id, decision
    topic, etc.) since the chain spans heterogeneous entity types."""

    __tablename__ = "dependency_edges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    from_type: Mapped[str] = mapped_column(String(32), nullable=False)
    from_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    to_type: Mapped[str] = mapped_column(String(32), nullable=False)
    to_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    relation: Mapped[DependencyRelation] = mapped_column(
        SQLEnum(DependencyRelation, name="dependency_relation_enum", native_enum=False, length=32),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(16), nullable=False, default="llm")
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_dependency_edges_project", "project_id", "detected_at"),
    )
