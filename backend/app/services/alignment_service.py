"""Requirements alignment: validate that sprints/stories trace back to the
documented knowledge base (BRDs, transcripts, change requests). LLM-computed."""
import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.llm_call_log import LLMFeature
from app.services.retrieval import build_context


def _clamp(v, lo=0.0, hi=100.0) -> float:
    try:
        return round(max(lo, min(hi, float(v))), 1)
    except (TypeError, ValueError):
        return 0.0


async def compute_alignment(db: AsyncSession, project_id: uuid.UUID, context: dict | None = None) -> dict:
    if context is None:
        context = await build_context(db, project_id)

    if not context.get("documents"):
        return {
            "has_knowledge_base": False,
            "requirement_coverage_pct": None,
            "story_alignment_pct": None,
            "unmapped_requirements": [],
            "out_of_scope_stories": [],
            "summary": "No documents uploaded yet — upload a BRD or requirements doc to validate alignment.",
        }

    raw = await client.complete(
        feature=LLMFeature.analysis,
        messages=prompts.alignment_messages(context),
        model=settings.llm_model_judge,
        project_id=project_id,
        temperature=0.1,
        json_mode=True,
    )
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        d = {}

    return {
        "has_knowledge_base": True,
        "requirement_coverage_pct": _clamp(d.get("requirement_coverage_pct", 0)),
        "story_alignment_pct": _clamp(d.get("story_alignment_pct", 0)),
        "unmapped_requirements": [str(x) for x in (d.get("unmapped_requirements") or [])][:20],
        "out_of_scope_stories": [
            {"key": s.get("key", ""), "title": s.get("title", "")}
            for s in (d.get("out_of_scope_stories") or [])
            if isinstance(s, dict)
        ][:20],
        "summary": d.get("summary") or "",
    }
