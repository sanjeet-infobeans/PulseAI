"""additive chat session scoping — customer/industry-wide admin chat

Widens chat_sessions.project_id to nullable and adds nullable customer_id +
industry columns, so a session can be scoped to a customer or an industry
instead of a single project (see routers/chat_scoped.py). Every existing row
keeps project_id set and the two new columns NULL — 100% backward compatible,
no data migration needed.

Revision ID: 008_chat_scope
Revises: 007_action_items_risk_items
Create Date: 2026-07-23
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "008_chat_scope"
down_revision = "007_action_items_risk_items"
branch_labels = None
depends_on = None


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    existing = {c["name"] for c in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    existing_cols = {c["name"]: c for c in inspector.get_columns("chat_sessions")}
    if not existing_cols["project_id"]["nullable"]:
        op.alter_column("chat_sessions", "project_id", existing_type=UUID(as_uuid=True), nullable=True)

    _add_column_if_missing(
        inspector, "chat_sessions",
        sa.Column("customer_id", UUID(as_uuid=True), sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=True),
    )
    _add_column_if_missing(inspector, "chat_sessions", sa.Column("industry", sa.String(32), nullable=True))


def downgrade() -> None:
    op.drop_column("chat_sessions", "industry")
    op.drop_column("chat_sessions", "customer_id")
    op.alter_column("chat_sessions", "project_id", existing_type=UUID(as_uuid=True), nullable=False)
