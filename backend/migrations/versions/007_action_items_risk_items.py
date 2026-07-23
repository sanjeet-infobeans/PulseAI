"""action items + persisted risk registry

Adds action_items (aggregated from transcript extraction, mirroring
decision_log's sync-from-documents pattern) and risk_items (the Risk
Identifier agent's persisted, upserted-by-title risk registry with an
active/mitigated/closed lifecycle). New tables only, via checkfirst=True
create_all matching 001/003/005's pattern.

Revision ID: 007_action_items_risk_items
Revises: 006_carry_forward
Create Date: 2026-07-23
"""
from alembic import op

from app.database import Base
import app.models  # noqa: F401  ensures ActionItem/RiskItem are registered

revision = "007_action_items_risk_items"
down_revision = "006_carry_forward"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    for table in ("risk_items", "action_items"):
        Base.metadata.tables[table].drop(bind=bind, checkfirst=True)
