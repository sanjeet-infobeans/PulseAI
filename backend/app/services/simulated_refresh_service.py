"""SimulatedDataset (seed_simulated.py) is seeded once and never updated —
without this nightly nudge, Resource Risk (#7) and Sentiment (#13) have
nothing to trend (see docs/ai-features-gap-analysis-and-plan.md: this is a
hard prerequisite, not optional polish). Applies a small bounded random walk
to each simulated connector's headline scalar and appends a metric_snapshots
row so a real trend accumulates over successive nightly runs.
"""
import random
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.connector import ConnectorType
from app.models.metric_snapshot import MetricSnapshot
from app.models.project import Project
from app.models.simulated import SimulatedDataset


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


async def _refresh_project(db: AsyncSession, project_id: uuid.UUID) -> None:
    rows = (
        await db.execute(select(SimulatedDataset).where(SimulatedDataset.project_id == project_id))
    ).scalars().all()

    for row in rows:
        payload = dict(row.payload or {})
        metric_key: str | None = None
        value: float | None = None

        if row.source == ConnectorType.sentiment:
            score = _clamp(float(payload.get("score", 75)) + random.uniform(-4, 3), 0, 100)
            payload["score"] = round(score)
            series = list(payload.get("series", []))
            series.append(payload["score"])
            payload["series"] = series[-12:]
            metric_key, value = "sentiment_score", score
        elif row.source == ConnectorType.resource:
            util = _clamp(float(payload.get("utilization_pct", 85)) + random.uniform(-3, 4), 40, 130)
            payload["utilization_pct"] = round(util)
            metric_key, value = "resource_utilization_pct", util
        elif row.source == ConnectorType.budget:
            variance = _clamp(float(payload.get("forecast_variance_pct", 0)) + random.uniform(-2, 2), -50, 50)
            payload["forecast_variance_pct"] = round(variance, 1)
            metric_key, value = "budget_forecast_variance_pct", variance
        elif row.source == ConnectorType.timeline:
            slip = max(0.0, float(payload.get("slip_days", 0)) + random.uniform(-1, 2))
            payload["slip_days"] = round(slip, 1)
            metric_key, value = "timeline_slip_days", slip

        if metric_key is None:
            continue
        row.payload = payload
        db.add(MetricSnapshot(
            project_id=project_id, metric_key=metric_key, value=value,
            meta=payload, source="simulated_refresh",
        ))

    await db.commit()


async def refresh_all_projects(db: AsyncSession) -> None:
    project_ids = (await db.execute(select(Project.id))).scalars().all()
    for pid in project_ids:
        await _refresh_project(db, pid)
