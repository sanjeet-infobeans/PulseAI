"""carry-forward tracking for the sprint timeline panel

Adds stories.carried_forward_from_sprint_id — a single current-value marker
(same lightweight pattern as stories.reopened_count) set by jira_sync when a
re-sync catches a still-not-done story's sprint_id changing, so the executive
view's sprint timeline can show what carried into the active sprint from the
one before it.

Revision ID: 006_carry_forward
Revises: 005_project_resources
Create Date: 2026-07-23
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "006_carry_forward"
down_revision = "005_project_resources"
branch_labels = None
depends_on = None


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    existing = {c["name"] for c in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    _add_column_if_missing(
        inspector, "stories",
        sa.Column(
            "carried_forward_from_sprint_id", UUID(as_uuid=True),
            sa.ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("stories", "carried_forward_from_sprint_id")
