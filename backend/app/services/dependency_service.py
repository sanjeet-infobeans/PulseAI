"""Hidden Dependency Detection (#4): one LLM pass over stories/documents/
blockers plus the simulated Teams/Slack signals, inferring chains like
"Story(Payment Gateway) depends_on Tax API, which blocks QA/release" that
aren't explicitly tracked as a Jira link. Nightly-cron only (LLM cost
control) — see app/worker.py's nightly_all_projects fan-out.
"""
import json
import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.dependency_edge import DependencyEdge, DependencyRelation
from app.models.llm_call_log import LLMFeature
from app.services.retrieval import build_context, simulated_signals

_VALID_RELATIONS = {r.value for r in DependencyRelation}


async def detect_dependencies(db: AsyncSession, project_id: uuid.UUID) -> list[DependencyEdge]:
    context = await build_context(db, project_id)
    simulated = await simulated_signals(db, project_id)

    if context["totals"]["stories"] == 0:
        return []

    edges: list[dict] = []
    try:
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=prompts.dependency_messages(context, simulated),
            model=settings.llm_model_analysis,
            project_id=project_id,
            temperature=0.2,
            json_mode=True,
        )
        edges = json.loads(raw).get("edges", [])
    except Exception:  # noqa: BLE001 — best-effort; keep previous edges on failure
        return (
            await db.execute(select(DependencyEdge).where(DependencyEdge.project_id == project_id))
        ).scalars().all()

    await db.execute(delete(DependencyEdge).where(DependencyEdge.project_id == project_id))
    rows = []
    for e in edges:
        relation = e.get("relation")
        if relation not in _VALID_RELATIONS:
            continue
        row = DependencyEdge(
            project_id=project_id,
            from_type=str(e.get("from_type", ""))[:32],
            from_ref=str(e.get("from_ref", ""))[:255],
            to_type=str(e.get("to_type", ""))[:32],
            to_ref=str(e.get("to_ref", ""))[:255],
            relation=DependencyRelation(relation),
            confidence=max(0.0, min(1.0, float(e.get("confidence", 0.5)))),
            rationale=e.get("rationale"),
            source="llm",
        )
        db.add(row)
        rows.append(row)
    await db.commit()
    return rows


async def latest_dependencies(db: AsyncSession, project_id: uuid.UUID) -> list[DependencyEdge]:
    return (
        await db.execute(
            select(DependencyEdge)
            .where(DependencyEdge.project_id == project_id)
            .order_by(DependencyEdge.confidence.desc())
        )
    ).scalars().all()
