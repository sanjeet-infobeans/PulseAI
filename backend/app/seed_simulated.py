"""Seeds the simulated (projection) integration datasets for a project.

Payloads are inline (not files) so seeding works identically in Docker and dev.
Idempotent: skips a source that already has a row.
"""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.connector import ConnectorType
from app.models.simulated import SimulatedDataset


def _iso(days_ago: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def _resource_roster(now: datetime) -> dict:
    """Team roster is date-relative (planned leaves) so it stays a meaningful
    demo no matter when this is seeded — see seed_demo_delivery.py for the
    same convention applied to sprint dates."""

    def _leave(leave_id: str, leave_type: str, start_in_days: int, days: int) -> dict:
        start = now + timedelta(days=start_in_days)
        end = start + timedelta(days=days - 1)
        return {
            "leave_id": leave_id,
            "leave_type": leave_type,
            "start_date": start.date().isoformat(),
            "end_date": end.date().isoformat(),
            "total_days": days,
            "status": "Approved",
        }

    return {
        "resources": [
            {
                "resource_id": "RES-001", "employee_code": "EMP001", "name": "John Smith",
                "designation": "Technical Lead", "email": "john.smith@company.com",
                "allocation_percentage": 100, "billable": True,
                "skills": ["React", "FastAPI", "Architecture"],
                "planned_leaves": [_leave("LV-1001", "Vacation", 18, 3)],
            },
            {
                "resource_id": "RES-002", "employee_code": "EMP002", "name": "Sarah Wilson",
                "designation": "Frontend Developer", "email": "sarah.wilson@company.com",
                "allocation_percentage": 100, "billable": True,
                "skills": ["Next.js", "TypeScript", "Tailwind CSS"],
                "planned_leaves": [_leave("LV-1002", "Personal Leave", 25, 2)],
            },
            {
                "resource_id": "RES-003", "employee_code": "EMP003", "name": "Michael Brown",
                "designation": "Backend Developer", "email": "michael.brown@company.com",
                "allocation_percentage": 80, "billable": True,
                "skills": ["Python", "FastAPI", "PostgreSQL"],
                "planned_leaves": [],
            },
            {
                "resource_id": "RES-004", "employee_code": "EMP004", "name": "Emma Davis",
                "designation": "QA Engineer", "email": "emma.davis@company.com",
                "allocation_percentage": 100, "billable": True,
                "skills": ["Manual Testing", "Automation", "Playwright"],
                "planned_leaves": [_leave("LV-1003", "Medical Leave", 22, 2)],
            },
            {
                "resource_id": "RES-005", "employee_code": "EMP005", "name": "David Miller",
                "designation": "UI/UX Designer", "email": "david.miller@company.com",
                "allocation_percentage": 60, "billable": True,
                "skills": ["Figma", "UX", "Design System"],
                "planned_leaves": [],
            },
            {
                "resource_id": "RES-006", "employee_code": "EMP006", "name": "Sophia Taylor",
                "designation": "DevOps Engineer", "email": "sophia.taylor@company.com",
                "allocation_percentage": 40, "billable": True,
                "skills": ["Docker", "Railway", "Vercel", "CI/CD"],
                "planned_leaves": [_leave("LV-1004", "Vacation", 27, 5)],
            },
        ],
    }


def _build_payloads() -> dict[ConnectorType, dict]:
    """A function (not a module-level literal) so requested_at/decided_at on
    seeded pending_decisions are relative to seed time, not import time —
    Customer Decision Delay (#6) needs at least one aged, still-pending
    decision to demonstrate a real delay. Same reasoning applies to the
    resource roster's planned_leaves dates."""
    return {
        ConnectorType.teams: {
            "meeting": "Phase 2 kickoff",
            "summary": "Team aligned on checkout API scope. Two risks raised around the payments vendor SLA.",
            "decisions": ["Proceed with circuit-breaker pattern", "Defer legacy export to Q4"],
            "action_items": [
                {"owner": "Priya", "item": "Draft payments fallback design"},
                {"owner": "Marco", "item": "Confirm vendor SLA terms"},
            ],
            # Customer/stakeholder decisions awaiting approval — resolved over
            # time by simulated_refresh_service so a real delay accumulates.
            "pending_decisions": [
                {
                    "topic": "Approve payments vendor fallback design",
                    "requested_by": "Priya S.",
                    "requested_at": _iso(12),
                    "status": "pending",
                    "decided_at": None,
                    "decided_by": None,
                },
                {
                    "topic": "Sign off on Q4 legacy export deferral",
                    "requested_by": "Marco R.",
                    "requested_at": _iso(3),
                    "status": "pending",
                    "decided_at": None,
                    "decided_by": None,
                },
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
            **_resource_roster(datetime.now(timezone.utc)),
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
    for source, payload in _build_payloads().items():
        if source in have:
            continue
        db.add(SimulatedDataset(project_id=project_id, source=source, payload=payload))
