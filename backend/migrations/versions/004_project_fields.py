"""add industry + total_person_hours to projects

Adds two columns collected by the project-creation form: an industry
classification (BFSI/SDO/Media and Publishing/Healthcare/E-com) and a total
person-hours effort estimate. Both nullable — no backfill needed for existing
rows. Follows 003_history_infra's guarded add_column pattern since main.py's
lifespan runs `alembic upgrade head` from every uvicorn worker concurrently.

Revision ID: 004_project_fields
Revises: 003_history_infra
Create Date: 2026-07-23
"""
import sqlalchemy as sa
from alembic import op

revision = "004_project_fields"
down_revision = "003_history_infra"
branch_labels = None
depends_on = None


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    existing = {c["name"] for c in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    _add_column_if_missing(inspector, "projects", sa.Column("industry", sa.String(32), nullable=True))
    _add_column_if_missing(inspector, "projects", sa.Column("total_person_hours", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("projects", "total_person_hours")
    op.drop_column("projects", "industry")
