"""Action items aggregation: reads action_items extracted per-document into
DocumentExtraction.extraction (see prompts._DOC_TASK["transcript"]) and
upserts them into a real, trackable table — mirrors decision_service.py's
sync-from-documents pattern (#6), applied to action items instead of
decisions. Unlike decisions (deduped on topic+source, updatable in place),
action items have no natural stable key beyond their text, so dedup is on
(project_id, source_document_id, item text) — re-processing the same
document never duplicates rows.
"""
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.action_item import ActionItem, ActionItemStatus
from app.models.document import Document, DocStatus, DocumentExtraction


async def sync_action_items(db: AsyncSession, project_id: uuid.UUID) -> None:
    rows = (
        await db.execute(
            select(Document, DocumentExtraction)
            .join(DocumentExtraction, DocumentExtraction.document_id == Document.id)
            .where(Document.project_id == project_id, Document.status == DocStatus.complete)
        )
    ).all()

    for doc, ext in rows:
        for ai in (ext.extraction or {}).get("action_items", []):
            if not isinstance(ai, dict) or not ai.get("item"):
                continue
            item_text = str(ai["item"])
            existing = (
                await db.execute(
                    select(ActionItem).where(
                        ActionItem.project_id == project_id,
                        ActionItem.source_document_id == doc.id,
                        ActionItem.item == item_text,
                    )
                )
            ).scalar_one_or_none()
            if not existing:
                db.add(ActionItem(
                    project_id=project_id, owner=ai.get("owner"), item=item_text,
                    source_document_id=doc.id, status=ActionItemStatus.open,
                ))

    await db.commit()


async def get_action_items_summary(db: AsyncSession, project_id: uuid.UUID) -> dict:
    rows = (
        await db.execute(
            select(ActionItem)
            .where(ActionItem.project_id == project_id)
            .order_by(ActionItem.created_at.desc())
        )
    ).scalars().all()

    open_count = sum(1 for r in rows if r.status == ActionItemStatus.open)
    by_owner: dict[str, list] = {}
    for r in rows:
        by_owner.setdefault(r.owner or "Unassigned", []).append({
            "id": str(r.id), "item": r.item, "status": r.status.value,
            "created_at": r.created_at.isoformat(),
        })

    return {"open_count": open_count, "done_count": len(rows) - open_count, "by_owner": by_owner}


async def set_action_item_status(
    db: AsyncSession, project_id: uuid.UUID, item_id: uuid.UUID, status: ActionItemStatus
) -> ActionItem:
    item = (
        await db.execute(
            select(ActionItem).where(ActionItem.id == item_id, ActionItem.project_id == project_id)
        )
    ).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.status = status
    await db.commit()
    await db.refresh(item)
    return item
