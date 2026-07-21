"""Builds compact, bounded context from the delivery tables for the LLM.

No vector DB — direct SQL aggregation is small, fast, and cheap for the POC.
"""
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import DocStatus, Document, DocumentExtraction
from app.models.project import Project
from app.models.simulated import SimulatedDataset
from app.models.status_ref import StatusCategory
from app.models.sprint import Sprint, SprintState
from app.models.story import Story

_MAX_BLOCKERS = 15
_MAX_SPRINT_STORIES = 40


def _doc_requirements(doc_type: str, extraction: dict) -> list[str]:
    """Flatten a document's extraction into a list of requirement-like statements
    so the LLM can trace them against sprint stories."""
    if not extraction:
        return []
    if doc_type == "brd":
        return [str(x) for x in extraction.get("features", [])]
    if doc_type == "change_request":
        return [str(x) for x in extraction.get("requested_changes", [])]
    if doc_type in ("transcript", "meeting"):
        decisions = [str(x) for x in extraction.get("decisions", [])]
        actions = [a.get("item", "") if isinstance(a, dict) else str(a)
                   for a in extraction.get("action_items", [])]
        return decisions + actions
    return [str(x) for x in extraction.get("key_points", [])]


async def build_documents(db: AsyncSession, project_id: uuid.UUID) -> list[dict]:
    """Analyzed documents with their extracted requirements, for traceability."""
    rows = (
        await db.execute(
            select(Document, DocumentExtraction)
            .join(DocumentExtraction, DocumentExtraction.document_id == Document.id)
            .where(Document.project_id == project_id, Document.status == DocStatus.complete)
        )
    ).all()
    docs = []
    for doc, ext in rows:
        docs.append({
            "filename": doc.filename,
            "type": doc.doc_type.value,
            "summary": ext.summary,
            "requirements": _doc_requirements(doc.doc_type.value, ext.extraction or {}),
        })
    return docs


async def build_context(
    db: AsyncSession, project_id: uuid.UUID, sprint_id: uuid.UUID | None = None
) -> dict:
    project = await db.get(Project, project_id)

    sprints = (
        await db.execute(
            select(Sprint).where(Sprint.project_id == project_id).order_by(Sprint.sequence)
        )
    ).scalars().all()

    # Status-category counts across the project (or one sprint)
    stmt = select(Story.status_category, func.count()).where(Story.project_id == project_id)
    if sprint_id:
        stmt = stmt.where(Story.sprint_id == sprint_id)
    counts_rows = (await db.execute(stmt.group_by(Story.status_category))).all()
    status_counts = {cat.value: n for cat, n in counts_rows}

    # Blocked stories (project-wide) — most relevant for risk/chat
    blocked = (
        await db.execute(
            select(Story)
            .where(Story.project_id == project_id, Story.is_blocked.is_(True))
            .limit(_MAX_BLOCKERS)
        )
    ).scalars().all()

    total = sum(status_counts.values())
    done = status_counts.get("done", 0)

    # Current-sprint story list (titles) so the LLM can trace requirements → stories
    active = next((s for s in sprints if s.state == SprintState.active), None)
    ref_sprint = active or (sprints[-1] if sprints else None)
    current_sprint_stories: list[dict] = []
    if ref_sprint:
        rows = (
            await db.execute(
                select(Story).where(Story.sprint_id == ref_sprint.id).limit(_MAX_SPRINT_STORIES)
            )
        ).scalars().all()
        current_sprint_stories = [
            {"key": s.external_id, "title": s.title, "status": s.status_category.value,
             "points": s.story_points, "assignee": s.assignee}
            for s in rows
        ]

    documents = await build_documents(db, project_id)

    # Project-wide story list so alignment can validate ALL delivery against the
    # documented knowledge base (not just the current sprint).
    all_story_rows = (
        await db.execute(
            select(Story).where(Story.project_id == project_id).limit(_MAX_SPRINT_STORIES * 3)
        )
    ).scalars().all()
    all_stories = [
        {"key": s.external_id, "title": s.title, "status": s.status_category.value}
        for s in all_story_rows
    ]

    return {
        "project": {
            "name": project.name if project else "Project",
            "key": project.key if project else "",
            "status": project.status.value if project else "active",
        },
        "totals": {
            "stories": total,
            "done": done,
            "completion_pct": round(100 * done / total, 1) if total else 0.0,
        },
        "status_counts": status_counts,
        "sprints": [
            {
                "name": s.name,
                "state": s.state.value,
                "committed_points": s.committed_points,
                "completed_points": s.completed_points,
                "goal": s.goal,
            }
            for s in sprints
        ],
        "current_sprint": ref_sprint.name if ref_sprint else None,
        "current_sprint_stories": current_sprint_stories,
        "all_stories": all_stories,
        "blockers": [
            {"key": b.external_id, "title": b.title, "assignee": b.assignee, "status": b.raw_status}
            for b in blocked
        ],
        "documents": documents,
    }


async def simulated_signals(db: AsyncSession, project_id: uuid.UUID) -> dict:
    """Latest seeded signals (sentiment/budget/etc.), keyed by source."""
    rows = (
        await db.execute(select(SimulatedDataset).where(SimulatedDataset.project_id == project_id))
    ).scalars().all()
    return {r.source.value: r.payload for r in rows}
