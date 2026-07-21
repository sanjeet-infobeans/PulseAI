"""align documents.doc_type / status column widths with the model

001_initial builds the schema with ``create_all(checkfirst=True)``, which sizes
a non-native ``SQLEnum`` column to the longest enum value *at the time the table
was first created* and never alters it afterwards. When ``DocType`` gained
"transcript"/"change_request", the pre-existing ``documents.doc_type`` column
stayed VARCHAR(7); inserting the longer values raised StringDataRightTruncation
and the upload endpoint returned HTTP 500.

The model now pins an explicit ``length`` on both enum columns so the width is
decoupled from the enum contents (a fresh ``create_all`` is safe, and future
enum values can't outgrow the column). This migration brings existing databases
to those same widths.

Revision ID: 002_widen_doc_type
Revises: 001_initial
Create Date: 2026-07-21
"""
import sqlalchemy as sa
from alembic import op

revision = "002_widen_doc_type"
down_revision = "001_initial"
branch_labels = None
depends_on = None

# Must match the explicit lengths declared on app.models.document.Document.
DOC_TYPE_LEN = 64
STATUS_LEN = 32


def upgrade() -> None:
    op.alter_column("documents", "doc_type", type_=sa.String(DOC_TYPE_LEN), existing_nullable=False)
    op.alter_column("documents", "status", type_=sa.String(STATUS_LEN), existing_nullable=False)


def downgrade() -> None:
    # Original create_all widths: max("brd","meeting","other") == 7, max DocStatus == 9.
    op.alter_column("documents", "status", type_=sa.String(9), existing_nullable=False)
    op.alter_column("documents", "doc_type", type_=sa.String(7), existing_nullable=False)
