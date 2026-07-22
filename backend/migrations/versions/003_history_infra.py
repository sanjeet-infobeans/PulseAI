"""history/time-series infra for the 15-feature AI roadmap

Adds the foundational tables and columns described in
docs/ai-features-gap-analysis-and-plan.md: a generic metric_snapshots trend
table, a persisted requirement catalog, dependency/decision/knowledge-map
tables, judge/prediction/what-if log tables, a project_outcomes stub, plus
columns on existing tables (confidence_scores.sub_scores, stories.reopened_count,
document versioning). New tables are created via checkfirst=True create_all,
matching 001_initial's convention; columns added to tables that may already
hold rows use an explicit server_default so the ALTER doesn't fail on existing data.

main.py's lifespan runs `alembic upgrade head` from EVERY uvicorn worker
(the Dockerfile uses --workers 4), so this migration must tolerate two workers
racing to apply it concurrently — each add_column is guarded with an
inspector existence check so a second worker's run is a no-op instead of a
"column already exists" crash (001's create_all(checkfirst=True) and 002's
ALTER COLUMN TYPE are naturally re-appliable the same way).

Revision ID: 003_history_infra
Revises: 002_widen_doc_type
Create Date: 2026-07-22
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database import Base
import app.models  # noqa: F401  ensures all tables (incl. new ones) are registered

revision = "003_history_infra"
down_revision = "002_widen_doc_type"
branch_labels = None
depends_on = None


def _add_column_if_missing(inspector, table: str, column: sa.Column) -> None:
    existing = {c["name"] for c in inspector.get_columns(table)}
    if column.name not in existing:
        op.add_column(table, column)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # ── Columns on existing tables ──────────────────────────────────────────
    _add_column_if_missing(inspector, "confidence_scores", sa.Column("sub_scores", JSONB(), nullable=True))
    _add_column_if_missing(
        inspector, "stories", sa.Column("reopened_count", sa.Integer(), nullable=False, server_default="0")
    )
    _add_column_if_missing(
        inspector, "documents", sa.Column("version_group_id", UUID(as_uuid=True), nullable=True)
    )
    _add_column_if_missing(
        inspector, "documents", sa.Column("version", sa.Integer(), nullable=False, server_default="1")
    )
    _add_column_if_missing(
        inspector, "documents",
        sa.Column("supersedes_document_id", UUID(as_uuid=True),
                  sa.ForeignKey("documents.id", ondelete="SET NULL"), nullable=True),
    )
    _add_column_if_missing(
        inspector, "document_extractions", sa.Column("diff_from_previous", JSONB(), nullable=True)
    )

    # ── New tables ───────────────────────────────────────────────────────────
    Base.metadata.create_all(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    for table in (
        "project_outcomes",
        "what_if_scenarios",
        "delivery_predictions",
        "ai_judge_reviews",
        "knowledge_map",
        "decision_log",
        "dependency_edges",
        "requirement_items",
        "metric_snapshots",
    ):
        Base.metadata.tables[table].drop(bind=bind, checkfirst=True)

    op.drop_column("document_extractions", "diff_from_previous")
    op.drop_column("documents", "supersedes_document_id")
    op.drop_column("documents", "version")
    op.drop_column("documents", "version_group_id")
    op.drop_column("stories", "reopened_count")
    op.drop_column("confidence_scores", "sub_scores")
