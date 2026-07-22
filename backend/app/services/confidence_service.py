"""Confidence engine: rule-based signals blended with an LLM judge. No ML model.

score = round(0.6 * rule_score + 0.4 * judge_score); band red<50 / amber 50-74 / green>=75.
"""
import json
import statistics
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.confidence import ConfidenceBand, ConfidenceScore
from app.models.llm_call_log import LLMFeature
from app.models.sprint import Sprint, SprintState
from app.models.status_ref import StatusCategory
from app.models.story import IssueType, Story
from app.services.retrieval import build_context

# (name, weight, higher_is_better) — weights sum to 1.0
_WEIGHTS = {
    "sprint_completion_ratio": (0.25, True),
    "blocked_ratio": (0.20, False),
    "overdue_ratio": (0.15, False),
    "velocity_stability": (0.15, True),
    "unassigned_ratio": (0.10, False),
    "bug_ratio": (0.10, False),
    "scope_health": (0.05, True),
}

# Explainable breakdown (#8): every signal (rule-based + alignment) maps to one
# of 6 categories. Some categories are single-signal proxies until later
# phases add dedicated signals (Resource from #7/#12, Customer from #6/#13,
# Dependencies from #4) — see docs/ai-features-gap-analysis-and-plan.md.
_CATEGORY_MAP = {
    "sprint_completion_ratio": "engineering",
    "velocity_stability": "engineering",
    "blocked_ratio": "dependencies",
    "bug_ratio": "testing",
    "unassigned_ratio": "resource",
    "overdue_ratio": "customer",
    "scope_health": "requirement",
    "requirement_coverage": "requirement",
    "story_alignment": "requirement",
    "requirement_volatility": "requirement",
}
_CATEGORIES = ["requirement", "engineering", "testing", "dependencies", "resource", "customer"]


def _sub_scores(signals: list[dict]) -> dict:
    buckets: dict[str, list[float]] = {c: [] for c in _CATEGORIES}
    for s in signals:
        category = _CATEGORY_MAP.get(s["name"])
        if not category:
            continue
        # Normalize back to a 0-100 "how good is this" score: weighted rule
        # signals store contribution = weight * normalized * 100; alignment
        # signals (weight=None) already store a 0-100 pct as contribution.
        pct = s["contribution"] / s["weight"] if s.get("weight") else s["contribution"]
        buckets[category].append(max(0.0, min(100.0, pct)))
    return {
        category: round(sum(vals) / len(vals), 1) if vals else None
        for category, vals in buckets.items()
    }


def _band(score: float) -> ConfidenceBand:
    if score < 50:
        return ConfidenceBand.red
    if score < 75:
        return ConfidenceBand.amber
    return ConfidenceBand.green


async def _signals(db: AsyncSession, project_id: uuid.UUID) -> list[dict]:
    sprints = (
        await db.execute(select(Sprint).where(Sprint.project_id == project_id).order_by(Sprint.sequence))
    ).scalars().all()
    stories = (
        await db.execute(select(Story).where(Story.project_id == project_id))
    ).scalars().all()

    closed_sprint_ids = {s.id for s in sprints if s.state == SprintState.closed}
    total = len(stories) or 1
    blocked = sum(1 for s in stories if s.is_blocked)
    unassigned = sum(1 for s in stories if not s.assignee and s.status_category != StatusCategory.done)
    bugs = sum(1 for s in stories if s.issue_type == IssueType.bug)
    # Overdue = still open but its sprint has already closed
    overdue = sum(
        1 for s in stories
        if s.status_category != StatusCategory.done and s.sprint_id in closed_sprint_ids
    )

    active = [s for s in sprints if s.state == SprintState.active]
    ref = active[0] if active else (sprints[-1] if sprints else None)
    completion = (ref.completed_points / ref.committed_points) if ref and ref.committed_points else 0.0

    closed = [s for s in sprints if s.state == SprintState.closed and s.completed_points]
    if len(closed) >= 2:
        vals = [s.completed_points for s in closed]
        mean = statistics.mean(vals)
        stdev = statistics.pstdev(vals)
        stability = max(0.0, 1.0 - (stdev / mean)) if mean else 0.5
    else:
        stability = 0.6  # insufficient history — neutral-ish

    raw = {
        "sprint_completion_ratio": min(completion, 1.0),
        "blocked_ratio": blocked / total,
        "overdue_ratio": overdue / total,
        "velocity_stability": stability,
        "unassigned_ratio": unassigned / total,
        "bug_ratio": bugs / total,
        "scope_health": 1.0,  # placeholder for scope-churn once history is tracked
    }

    signals = []
    for name, (weight, higher) in _WEIGHTS.items():
        value = raw[name]
        normalized = value if higher else (1.0 - value)
        signals.append({
            "name": name,
            "value": round(value, 3),
            "weight": weight,
            "contribution": round(weight * normalized * 100, 2),
        })
    return signals


async def compute_confidence(
    db: AsyncSession, project_id: uuid.UUID, sprint_id: uuid.UUID | None = None
) -> ConfidenceScore:
    from app.services.alignment_service import compute_alignment

    signals = await _signals(db, project_id)
    rule_score = round(sum(s["contribution"] for s in signals), 1)

    context = await build_context(db, project_id, sprint_id)

    # ── LLM judge ────────────────────────────────────────────────────────────
    judge_score = rule_score
    rationale = None
    try:
        raw = await client.complete(
            feature=LLMFeature.confidence,
            messages=prompts.confidence_judge_messages(context, signals, rule_score),
            model=settings.llm_model_judge,
            project_id=project_id,
            temperature=0.1,
            json_mode=True,
        )
        parsed = json.loads(raw)
        judge_score = float(parsed.get("judge_score", rule_score))
        rationale = parsed.get("rationale")
    except Exception:  # noqa: BLE001 — judge is best-effort; rules still stand
        pass

    # ── Requirements alignment (documents = source of truth) ──────────────────
    alignment_score = None
    try:
        alignment = await compute_alignment(db, project_id, context)
        if alignment.get("has_knowledge_base"):
            cov = alignment["requirement_coverage_pct"] or 0.0
            sal = alignment["story_alignment_pct"] or 0.0
            alignment_score = round(0.6 * cov + 0.4 * sal, 1)
            signals.append({"name": "requirement_coverage", "value": round(cov / 100, 3),
                            "weight": None, "contribution": cov})
            signals.append({"name": "story_alignment", "value": round(sal / 100, 3),
                            "weight": None, "contribution": sal})
            oos = len(alignment["out_of_scope_stories"])
            summary = alignment["summary"] or ""
            rationale = (
                f"Requirements alignment: {cov:.0f}% of documented requirements covered, "
                f"{sal:.0f}% of stories traceable, {oos} out-of-scope. {summary} "
                + (rationale or "")
            ).strip()
    except Exception:  # noqa: BLE001 — alignment is best-effort
        pass

    # Requirement Volatility (#5) — display-only signal for the sub_scores
    # breakdown; not factored into rule_score/judge_score/alignment_score so
    # the overall blend formula stays unchanged.
    try:
        from app.services.volatility_service import latest_volatility

        volatility = await latest_volatility(db, project_id)
        if volatility is not None:
            signals.append({"name": "requirement_volatility", "value": round(volatility / 100, 3),
                            "weight": None, "contribution": volatility})
    except Exception:  # noqa: BLE001 — best-effort
        pass

    # Blend: with a knowledge base, requirement alignment weighs on confidence.
    if alignment_score is not None:
        score = round(0.5 * rule_score + 0.2 * judge_score + 0.3 * alignment_score)
    else:
        score = round(0.6 * rule_score + 0.4 * judge_score)

    row = ConfidenceScore(
        project_id=project_id, sprint_id=sprint_id, score=score, band=_band(score),
        rule_score=rule_score, judge_score=round(judge_score, 1), signals=signals,
        rationale=rationale, model=settings.llm_model_judge,
        sub_scores=_sub_scores(signals),
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def latest_confidence(db: AsyncSession, project_id: uuid.UUID) -> ConfidenceScore | None:
    return (
        await db.execute(
            select(ConfidenceScore)
            .where(ConfidenceScore.project_id == project_id)
            .order_by(ConfidenceScore.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
