"""Seeds the simulated (projection) integration datasets for a project.

Payloads are inline (not files) so seeding works identically in Docker and dev.
Idempotent: skips a source that already has a row.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.connector import ConnectorType
from app.models.simulated import SimulatedDataset

_PAYLOADS: dict[ConnectorType, dict] = {
    ConnectorType.teams: {
        "meeting": "Phase 2 kickoff",
        "summary": "Team aligned on checkout API scope. Two risks raised around the payments vendor SLA.",
        "decisions": ["Proceed with circuit-breaker pattern", "Defer legacy export to Q4"],
        "action_items": [
            {"owner": "Priya", "item": "Draft payments fallback design"},
            {"owner": "Marco", "item": "Confirm vendor SLA terms"},
        ],
    },
    ConnectorType.slack: {
        "channel": "#atlas-delivery",
        "digest": "18 messages. Sentiment steady. One escalation about staging flakiness, resolved.",
        "highlights": ["Staging restored", "QA signed off on sprint 41 scope"],
    },
    ConnectorType.resource: {
        "team_size": 11,
        "utilization_pct": 87,
        "developers": [
            {"name": "Priya S.", "skill": "Backend", "experience_yrs": 8, "availability_pct": 60, "utilization_pct": 95},
            {"name": "Marco R.", "skill": "Frontend", "experience_yrs": 5, "availability_pct": 100, "utilization_pct": 80},
            {"name": "Lena K.", "skill": "QA", "experience_yrs": 6, "availability_pct": 80, "utilization_pct": 90},
        ],
    },
    ConnectorType.budget: {
        "total_usd": 1_200_000,
        "spent_usd": 780_000,
        "forecast_variance_pct": -8,
        "note": "Tracking 8% under forecast.",
    },
    ConnectorType.timeline: {
        "predicted_end": "2026-10-14",
        "baseline_end": "2026-10-01",
        "slip_days": 13,
        "confidence_pct": 72,
    },
    ConnectorType.sentiment: {
        "score": 78,
        "trend": "steady",
        "series": [72, 74, 71, 76, 78],
        "note": "Customer sentiment stable; positive on delivery cadence.",
    },
}


async def seed_simulated_for_project(db: AsyncSession, project_id: uuid.UUID) -> None:
    existing = (
        await db.execute(
            select(SimulatedDataset.source).where(SimulatedDataset.project_id == project_id)
        )
    ).scalars().all()
    have = set(existing)
    for source, payload in _PAYLOADS.items():
        if source in have:
            continue
        db.add(SimulatedDataset(project_id=project_id, source=source, payload=payload))
