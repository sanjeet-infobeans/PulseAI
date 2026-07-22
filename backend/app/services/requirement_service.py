"""Requirement Drift Detection (#3): persists what retrieval.py::_doc_requirements
only computed ad-hoc per call into requirement_items, so a requirement that
never got a story (e.g. "BRD says SSO, a later transcript adds MFA, no story
exists") can be flagged rather than silently recomputed each time. Also the
shared catalog Scope Creep (#2) and Requirement Volatility (#5) build on.
"""
import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.document import Document, DocStatus, DocumentExtraction
from app.models.llm_call_log import LLMFeature
from app.models.requirement_item import RequirementItem, RequirementSourceType, RequirementStatus
from app.services.retrieval import _doc_requirements, build_context

_SOURCE_TYPE_MAP = {
    "brd": RequirementSourceType.brd,
    "change_request": RequirementSourceType.change_request,
    "transcript": RequirementSourceType.transcript,
    "meeting": RequirementSourceType.transcript,
}


async def sync_requirement_catalog(db: AsyncSession, project_id: uuid.UUID) -> None:
    """Runs after each document finishes extraction (see document_service.py).
    Upserts new requirement texts by exact match within their source document,
    then re-matches every open item against current Jira stories in one LLM
    pass so status (covered/missing) reflects the latest sync."""
    rows = (
        await db.execute(
            select(Document, DocumentExtraction)
            .join(DocumentExtraction, DocumentExtraction.document_id == Document.id)
            .where(Document.project_id == project_id, Document.status == DocStatus.complete)
        )
    ).all()

    for doc, ext in rows:
        texts = _doc_requirements(doc.doc_type.value, ext.extraction or {})
        if not texts:
            continue
        existing_texts = set(
            (await db.execute(
                select(RequirementItem.text).where(
                    RequirementItem.project_id == project_id,
                    RequirementItem.source_document_id == doc.id,
                )
            )).scalars().all()
        )
        source_type = _SOURCE_TYPE_MAP.get(doc.doc_type.value, RequirementSourceType.manual)
        for text in texts:
            if text in existing_texts:
                continue
            db.add(RequirementItem(
                project_id=project_id, source_document_id=doc.id, source_type=source_type,
                text=text, status=RequirementStatus.proposed,
            ))
    await db.commit()

    await _rematch_open_items(db, project_id)


async def _rematch_open_items(db: AsyncSession, project_id: uuid.UUID) -> None:
    open_items = (
        await db.execute(
            select(RequirementItem).where(
                RequirementItem.project_id == project_id,
                RequirementItem.status.in_([RequirementStatus.proposed, RequirementStatus.covered,
                                             RequirementStatus.missing]),
            )
        )
    ).scalars().all()
    if not open_items:
        return

    context = await build_context(db, project_id)
    requirement_texts = [{"id": str(item.id), "text": item.text} for item in open_items]

    try:
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=prompts.requirement_match_messages(requirement_texts, context["all_stories"]),
            model=settings.llm_model_judge,
            project_id=project_id,
            temperature=0.1,
            json_mode=True,
        )
        matches = {m["id"]: m.get("matched_story_keys", []) for m in json.loads(raw).get("matches", [])}
    except Exception:  # noqa: BLE001 — matching is best-effort; items keep prior status
        matches = {}

    for item in open_items:
        keys = matches.get(str(item.id))
        if keys is None:
            continue
        item.matched_story_keys = keys
        item.status = RequirementStatus.covered if keys else RequirementStatus.missing
    await db.commit()


async def get_requirement_drift(db: AsyncSession, project_id: uuid.UUID) -> list[dict]:
    """On-demand read for the drift panel: missing items + an LLM effort/risk
    estimate, computed only for this (typically small) subset."""
    missing = (
        await db.execute(
            select(RequirementItem).where(
                RequirementItem.project_id == project_id,
                RequirementItem.status == RequirementStatus.missing,
            ).order_by(RequirementItem.first_seen_at.desc())
        )
    ).scalars().all()
    if not missing:
        return []

    estimates: dict[str, dict] = {}
    try:
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=prompts.requirement_drift_messages([
                {"id": str(m.id), "text": m.text, "source_type": m.source_type.value} for m in missing
            ]),
            model=settings.llm_model_analysis,
            project_id=project_id,
            temperature=0.2,
            json_mode=True,
        )
        estimates = {i["id"]: i for i in json.loads(raw).get("items", [])}
    except Exception:  # noqa: BLE001 — estimate is best-effort
        pass

    return [
        {
            "id": str(m.id),
            "text": m.text,
            "source_type": m.source_type.value,
            "first_seen_at": m.first_seen_at.isoformat(),
            "estimated_effort_sp": estimates.get(str(m.id), {}).get("estimated_effort_sp"),
            "risk": estimates.get(str(m.id), {}).get("risk", "medium"),
            "rationale": estimates.get(str(m.id), {}).get("rationale", ""),
        }
        for m in missing
    ]
