"""initial schema — all PulseAI tables

Creates every table from SQLAlchemy metadata with checkfirst=True so the
migration is idempotent and safe to run concurrently across workers
(matches the AIMS Alembic-in-lifespan pattern).

Revision ID: 001_initial
Revises:
Create Date: 2026-07-21
"""
from alembic import op

from app.database import Base
import app.models  # noqa: F401  ensures all tables are registered on metadata

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
