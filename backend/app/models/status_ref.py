import enum
import uuid

from sqlalchemy import Enum as SQLEnum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class StatusCategory(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    blocked = "blocked"
    in_review = "in_review"
    done = "done"


class StatusRef(Base):
    """Normalized status catalog, populated from a board's status mapping during sync."""

    __tablename__ = "status_refs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    raw_name: Mapped[str] = mapped_column(String(128), nullable=False)
    normalized_category: Mapped[StatusCategory] = mapped_column(
        SQLEnum(StatusCategory, name="status_category_enum", native_enum=False),
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("project_id", "raw_name", name="uq_status_refs_project_raw"),
    )
