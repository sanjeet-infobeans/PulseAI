"""Effort vs estimate: consumed hours = completed story points x 6.5, compared
against Project.total_person_hours. Pure rule computation, no LLM, nothing
stored per-request — same "read-through" pattern as resource_service.py /
scope_service.py. sync_effort_risk() is the one write path: a deterministic,
title-keyed row in the existing risk_items registry (shared with the LLM-
driven Risk Identifier agent in risk_service.py — safe to coexist since that
scanner's upsert-by-title logic only matches within its own currently-active
set, and its prompt is already fed existing active titles to avoid
duplicating them).
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.risk_item import RiskItem, RiskSeverity, RiskSourceType, RiskStatus
from app.models.status_ref import StatusCategory
from app.models.story import Story

_HOURS_PER_POINT = 6.5
_RISK_TITLE = "Effort overshoot risk"


def _band(overshoot_pct: float) -> RiskSeverity:
    if overshoot_pct <= 10:
        return RiskSeverity.low
    if overshoot_pct <= 25:
        return RiskSeverity.medium
    return RiskSeverity.high


async def compute_effort(db: AsyncSession, project_id: uuid.UUID) -> dict:
    done_points, remaining_points = (
        await db.execute(
            select(
                func.coalesce(
                    func.sum(case((Story.status_category == StatusCategory.done, Story.story_points), else_=0.0)), 0.0
                ),
                func.coalesce(
                    func.sum(case((Story.status_category != StatusCategory.done, Story.story_points), else_=0.0)), 0.0
                ),
            ).where(Story.project_id == project_id)
        )
    ).one()

    project = await db.get(Project, project_id)
    estimated_hours = project.total_person_hours if project else None

    consumed_hours = round(done_points * _HOURS_PER_POINT, 1)
    remaining_hours = round(remaining_points * _HOURS_PER_POINT, 1)
    projected_total_hours = round((done_points + remaining_points) * _HOURS_PER_POINT, 1)

    overshoot_pct = None
    overshoot_risk = None
    if estimated_hours and estimated_hours > 0:
        overshoot_pct = round(100 * (projected_total_hours - estimated_hours) / estimated_hours, 1)
        overshoot_risk = _band(overshoot_pct).value

    return {
        "estimated_hours": estimated_hours,
        "consumed_hours": consumed_hours,
        "remaining_hours": remaining_hours,
        "projected_total_hours": projected_total_hours,
        "done_points": round(done_points, 1),
        "remaining_points": round(remaining_points, 1),
        "overshoot_pct": overshoot_pct,
        "overshoot_risk": overshoot_risk,
    }


async def sync_effort_risk(db: AsyncSession, project_id: uuid.UUID) -> None:
    effort = await compute_effort(db, project_id)
    if effort["overshoot_risk"] is None:
        return  # no estimate set — nothing to flag, leave any existing row untouched

    existing = (
        await db.execute(
            select(RiskItem).where(
                RiskItem.project_id == project_id,
                RiskItem.title == _RISK_TITLE,
                RiskItem.status == RiskStatus.active,
            )
        )
    ).scalars().first()

    now = datetime.now(timezone.utc)
    severity = RiskSeverity(effort["overshoot_risk"])

    if severity == RiskSeverity.low:
        if existing:
            existing.status = RiskStatus.mitigated
            existing.resolved_at = now
        await db.commit()
        return

    description = (
        f"At current backlog scope, completing all stories projects to "
        f"{effort['projected_total_hours']}h against a {effort['estimated_hours']}h estimate — "
        f"{effort['overshoot_pct']}% over."
    )
    if existing:
        existing.severity = severity
        existing.description = description
        existing.last_seen_at = now
    else:
        db.add(RiskItem(
            project_id=project_id, title=_RISK_TITLE, description=description,
            severity=severity, status=RiskStatus.active, source_type=RiskSourceType.sprint_signal,
        ))
    await db.commit()
