"""Knowledge Gap Detection (#12) / shared with Resource Risk (#7): groups
Story by (label, assignee) to find modules with a single distinct developer
across all their stories — the knowledge-concentration signal. Pure
rule-based, no LLM — recomputed wholesale on each run (delete+reinsert),
same cadence as confidence recompute (see jira_sync.py::_enqueue_recompute).
"""
import uuid
from collections import defaultdict

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge_map import KnowledgeMapEntry
from app.models.story import Story

_UNLABELED = "unlabeled"


async def compute_knowledge_map(db: AsyncSession, project_id: uuid.UUID) -> list[KnowledgeMapEntry]:
    stories = (
        await db.execute(select(Story).where(Story.project_id == project_id))
    ).scalars().all()

    # (module, developer) -> {story_count, last_touched_at}
    pairs: dict[tuple[str, str], dict] = defaultdict(lambda: {"story_count": 0, "last_touched_at": None})
    module_devs: dict[str, set[str]] = defaultdict(set)

    for s in stories:
        if not s.assignee:
            continue
        modules = s.labels or []
        modules = modules if modules else [_UNLABELED]
        for label in modules:
            module = str(label)
            key = (module, s.assignee)
            pairs[key]["story_count"] += 1
            touched = s.updated_ext or s.updated_at
            if touched and (pairs[key]["last_touched_at"] is None or touched > pairs[key]["last_touched_at"]):
                pairs[key]["last_touched_at"] = touched
            module_devs[module].add(s.assignee)

    await db.execute(delete(KnowledgeMapEntry).where(KnowledgeMapEntry.project_id == project_id))

    rows = []
    for (module, developer), agg in pairs.items():
        row = KnowledgeMapEntry(
            project_id=project_id, module_key=module, developer=developer,
            story_count=agg["story_count"], last_touched_at=agg["last_touched_at"],
            is_sole_holder=len(module_devs[module]) == 1,
        )
        db.add(row)
        rows.append(row)
    await db.commit()
    return rows


async def latest_knowledge_map(db: AsyncSession, project_id: uuid.UUID) -> list[KnowledgeMapEntry]:
    return (
        await db.execute(
            select(KnowledgeMapEntry)
            .where(KnowledgeMapEntry.project_id == project_id)
            .order_by(KnowledgeMapEntry.module_key, KnowledgeMapEntry.developer)
        )
    ).scalars().all()
