import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ConnectorType(str, enum.Enum):
    jira = "jira"
    teams = "teams"
    slack = "slack"
    clickup = "clickup"
    asana = "asana"
    trello = "trello"
    resource = "resource"
    budget = "budget"
    timeline = "timeline"
    sentiment = "sentiment"


class ConnectorMode(str, enum.Enum):
    real = "real"
    simulated = "simulated"


class ConnectorStatus(str, enum.Enum):
    unconfigured = "unconfigured"
    connected = "connected"
    syncing = "syncing"
    error = "error"


class Connector(Base):
    __tablename__ = "connectors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[ConnectorType] = mapped_column(
        SQLEnum(ConnectorType, name="connector_type_enum", native_enum=False),
        nullable=False,
    )
    mode: Mapped[ConnectorMode] = mapped_column(
        SQLEnum(ConnectorMode, name="connector_mode_enum", native_enum=False),
        nullable=False,
        default=ConnectorMode.real,
    )
    status: Mapped[ConnectorStatus] = mapped_column(
        SQLEnum(ConnectorStatus, name="connector_status_enum", native_enum=False),
        nullable=False,
        default=ConnectorStatus.unconfigured,
    )
    # Non-secret config: {base_url, project_key, board_id, story_point_field}
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # Name of the env var / secret holding the token — never the token itself
    secret_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", "type", name="uq_connectors_project_type"),
    )

    project: Mapped["Project"] = relationship("Project", back_populates="connectors")
