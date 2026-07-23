"""Delivery Completion Prediction (#1): rule+LLM-judge blend, same pattern as
confidence_service.py — rule side projects a completion date from velocity
trend (metric_snapshots), LLM side reasons about probability/causes/
recommendations on top of that projection. Append-only table
(delivery_predictions), like ConfidenceScore.
"""
import json
import statistics
import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.delivery_prediction import DeliveryPrediction
from app.models.llm_call_log import LLMFeature
from app.models.metric_snapshot import MetricSnapshot
from app.models.project import Project
from app.models.sprint import Sprint, SprintState
from app.models.status_ref import StatusCategory
from app.models.story import Story
from app.services.retrieval import build_context

_DEFAULT_CADENCE_DAYS = 14


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


async def _rule_projection(db: AsyncSession, project_id: uuid.UUID) -> dict:
    velocity_rows = (
        await db.execute(
            select(MetricSnapshot)
            .where(MetricSnapshot.project_id == project_id, MetricSnapshot.metric_key == "velocity_completed_points")
            .order_by(MetricSnapshot.recorded_at.asc())
        )
    ).scalars().all()
    velocities = [r.value for r in velocity_rows if r.value]
    avg_velocity = statistics.mean(velocities[-5:]) if velocities else 0.0

    stories = (
        await db.execute(select(Story).where(Story.project_id == project_id))
    ).scalars().all()
    remaining_points = sum(s.story_points or 0.0 for s in stories if s.status_category != StatusCategory.done)

    sprints = (
        await db.execute(select(Sprint).where(Sprint.project_id == project_id).order_by(Sprint.sequence))
    ).scalars().all()
    closed = [s for s in sprints if s.state == SprintState.closed and s.start_date and s.end_date]
    if closed:
        cadence_days = statistics.mean([(s.end_date - s.start_date).days for s in closed]) or _DEFAULT_CADENCE_DAYS
    else:
        cadence_days = _DEFAULT_CADENCE_DAYS

    project = await db.get(Project, project_id)
    baseline_target_date = project.target_end_date if project else None

    predicted_completion_date = None
    if avg_velocity > 0:
        sprints_needed = remaining_points / avg_velocity
        predicted_completion_date = date.today() + timedelta(days=sprints_needed * cadence_days)

    if baseline_target_date and predicted_completion_date:
        slack_days = (baseline_target_date - predicted_completion_date).days
        rule_probability = _clamp(50 + slack_days * 2)
    else:
        rule_probability = 50.0  # insufficient history/target — neutral

    return {
        "remaining_points": round(remaining_points, 1),
        "avg_velocity": round(avg_velocity, 1),
        "cadence_days": round(cadence_days, 1),
        "predicted_completion_date": predicted_completion_date.isoformat() if predicted_completion_date else None,
        "baseline_target_date": baseline_target_date.isoformat() if baseline_target_date else None,
        "rule_probability": round(rule_probability, 1),
        "closed_sprints_count": len(closed),
    }


async def predict_completion(
    db: AsyncSession, project_id: uuid.UUID, sprint_id: uuid.UUID | None = None
) -> DeliveryPrediction:
    rule = await _rule_projection(db, project_id)
    context = await build_context(db, project_id, sprint_id)

    llm_probability = rule["rule_probability"]
    reasons: list = []
    recommendations: list = []
    try:
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=prompts.completion_prediction_messages(context, rule, context.get("blockers", [])),
            model=settings.llm_model_judge,
            project_id=project_id,
            temperature=0.2,
            json_mode=True,
        )
        parsed = json.loads(raw)
        llm_probability = _clamp(float(parsed.get("probability_on_time", llm_probability)))
        reasons = parsed.get("reasons", [])
        recommendations = parsed.get("recommendations", [])
    except Exception:  # noqa: BLE001 — LLM reasoning is best-effort; rule projection still stands
        pass

    probability_on_time = round(0.5 * rule["rule_probability"] + 0.5 * llm_probability, 1)
    # More closed-sprint history behind the velocity trend = more confidence in the estimate itself.
    confidence_pct = round(_clamp(40 + 12 * rule["closed_sprints_count"]), 1)

    predicted_date = date.fromisoformat(rule["predicted_completion_date"]) if rule["predicted_completion_date"] else None
    baseline_date = date.fromisoformat(rule["baseline_target_date"]) if rule["baseline_target_date"] else None

    row = DeliveryPrediction(
        project_id=project_id, sprint_id=sprint_id,
        predicted_completion_date=predicted_date, baseline_target_date=baseline_date,
        probability_on_time=probability_on_time, confidence_pct=confidence_pct,
        reasons=reasons, recommendations=recommendations, model=settings.llm_model_judge,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def latest_prediction(db: AsyncSession, project_id: uuid.UUID) -> DeliveryPrediction | None:
    return (
        await db.execute(
            select(DeliveryPrediction)
            .where(DeliveryPrediction.project_id == project_id)
            .order_by(DeliveryPrediction.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
