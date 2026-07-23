"""Builds compact, bounded context from the delivery tables for the LLM.

No vector DB — direct SQL aggregation is small, fast, and cheap for the POC.
"""
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import DocStatus, Document, DocumentExtraction
from app.models.project import Project, ProjectIndustry
from app.models.simulated import SimulatedDataset
from app.models.status_ref import StatusCategory
from app.models.sprint import Sprint, SprintState
from app.models.story import Story

_MAX_BLOCKERS = 15
_MAX_SPRINT_STORIES = 40
_MAX_PROJECTS_IN_SCOPE = 15


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
    return await build_documents_multi(db, [project_id])


async def build_documents_multi(db: AsyncSession, project_ids: list[uuid.UUID]) -> list[dict]:
    if not project_ids:
        return []
    rows = (
        await db.execute(
            select(Document, DocumentExtraction)
            .join(DocumentExtraction, DocumentExtraction.document_id == Document.id)
            .where(Document.project_id.in_(project_ids), Document.status == DocStatus.complete)
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


async def resolve_project_ids(
    db: AsyncSession, *,
    project_id: uuid.UUID | None = None,
    customer_id: uuid.UUID | None = None,
    industry: str | None = None,
) -> tuple[list[uuid.UUID], int]:
    """Turns a chat-session scope selection into a list of project ids to
    aggregate context across. customer_id and industry combine as an AND
    filter when both are given (picking more narrows the scope further, down
    to a specific project). Returns (project_ids, total_matched) —
    total_matched can exceed len(project_ids) when a broad scope (a large
    customer/industry) was capped at _MAX_PROJECTS_IN_SCOPE, most-recently-
    active projects first; callers use the gap to disclose truncation."""
    if project_id:
        return [project_id], 1

    if not customer_id and not industry:
        return [], 0

    stmt = select(Project.id)
    if customer_id:
        stmt = stmt.where(Project.customer_id == customer_id)
    if industry:
        try:
            stmt = stmt.where(Project.industry == ProjectIndustry(industry))
        except ValueError:
            return [], 0

    all_ids = list((await db.execute(stmt)).scalars().all())
    if len(all_ids) <= _MAX_PROJECTS_IN_SCOPE:
        return all_ids, len(all_ids)

    capped = list(
        (await db.execute(stmt.order_by(Project.updated_at.desc()).limit(_MAX_PROJECTS_IN_SCOPE)))
        .scalars().all()
    )
    return capped, len(all_ids)


async def build_context(
    db: AsyncSession, project_id: uuid.UUID, sprint_id: uuid.UUID | None = None
) -> dict:
    return await build_context_multi(db, [project_id], sprint_id=sprint_id)


async def build_context_multi(
    db: AsyncSession, project_ids: list[uuid.UUID], *,
    sprint_id: uuid.UUID | None = None, scope_truncated: bool = False,
) -> dict:
    n = len(project_ids)
    empty_project = {"name": "Project", "key": "", "status": "active", "industry": None}

    if n == 0:
        return {
            "project": None, "projects": [], "scope_project_count": 0, "scope_truncated": False,
            "totals": {"stories": 0, "done": 0, "completion_pct": 0.0},
            "status_counts": {}, "sprints": [], "current_sprint": None,
            "current_sprint_stories": [], "all_stories": [], "blockers": [], "documents": [],
        }

    # Scale per-query caps down as scope breadth grows so total context size
    # stays roughly constant, rather than growing linearly with project count.
    max_blockers = _MAX_BLOCKERS if n == 1 else max(3, _MAX_BLOCKERS // n)
    max_sprint_stories = _MAX_SPRINT_STORIES if n == 1 else max(3, _MAX_SPRINT_STORIES // n)

    projects = (
        await db.execute(select(Project).where(Project.id.in_(project_ids)))
    ).scalars().all()
    project_summaries = [
        {"name": p.name, "key": p.key, "status": p.status.value,
         "industry": p.industry.value if p.industry else None}
        for p in projects
    ]

    sprints = (
        await db.execute(
            select(Sprint).where(Sprint.project_id.in_(project_ids)).order_by(Sprint.sequence)
        )
    ).scalars().all()

    stmt = select(Story.status_category, func.count()).where(Story.project_id.in_(project_ids))
    if sprint_id and n == 1:
        stmt = stmt.where(Story.sprint_id == sprint_id)
    counts_rows = (await db.execute(stmt.group_by(Story.status_category))).all()
    status_counts = {cat.value: cnt for cat, cnt in counts_rows}

    blocked = (
        await db.execute(
            select(Story)
            .where(Story.project_id.in_(project_ids), Story.is_blocked.is_(True))
            .limit(max_blockers)
        )
    ).scalars().all()

    total = sum(status_counts.values())
    done = status_counts.get("done", 0)

    # "Current sprint" is only a coherent concept for a single project — a
    # broad customer/industry scope has many unrelated sprints in flight.
    current_sprint_stories: list[dict] = []
    ref_sprint = None
    if n == 1:
        active = next((s for s in sprints if s.state == SprintState.active), None)
        ref_sprint = active or (sprints[-1] if sprints else None)
        if ref_sprint:
            rows = (
                await db.execute(
                    select(Story).where(Story.sprint_id == ref_sprint.id).limit(max_sprint_stories)
                )
            ).scalars().all()
            current_sprint_stories = [
                {"key": s.external_id, "title": s.title, "status": s.status_category.value,
                 "points": s.story_points, "assignee": s.assignee}
                for s in rows
            ]

    documents = await build_documents_multi(db, project_ids)

    all_story_rows = (
        await db.execute(
            select(Story).where(Story.project_id.in_(project_ids)).limit(max_sprint_stories * 3)
        )
    ).scalars().all()
    all_stories = [
        {"key": s.external_id, "title": s.title, "status": s.status_category.value}
        for s in all_story_rows
    ]

    return {
        "project": (project_summaries[0] if project_summaries else empty_project) if n == 1 else None,
        "projects": project_summaries,
        "scope_project_count": n,
        "scope_truncated": scope_truncated,
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
