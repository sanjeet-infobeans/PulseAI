"""real, DB-backed project resources + planned leaves

Adds project_resources / resource_leaves tables — a real team roster with
allocation % and planned-leave date ranges, replacing the need for the
simulated `resource` connector payload on new projects (resource_service.py
still falls back to the simulated payload when a project has no real rows).
New tables only, via checkfirst=True create_all matching 001/003's pattern.

Revision ID: 005_project_resources
Revises: 004_project_fields
Create Date: 2026-07-23
"""
from alembic import op

from app.database import Base
import app.models  # noqa: F401  ensures ProjectResource/ResourceLeave are registered

revision = "005_project_resources"
down_revision = "004_project_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    for table in ("resource_leaves", "project_resources"):
        Base.metadata.tables[table].drop(bind=bind, checkfirst=True)
