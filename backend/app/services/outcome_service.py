"""Delivery DNA (#11), Phase 3 per docs/ai-features-gap-analysis-and-plan.md:
project_outcomes exists purely so outcomes start accumulating the moment a
project completes — no archetype-matching/probability-of-success logic is
built here. A single org with a handful of projects isn't a corpus; that
logic is explicitly parked until a real multi-project, multi-industry corpus
exists. This is the "mark project outcome" affordance that starts the clock.
"""
import statistics
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metric_snapshot import MetricSnapshot
from app.models.project import Project, ProjectStatus
from app.models.project_outcome import ProjectOutcome
from app.models.status_ref import StatusCategory
from app.models.story import IssueType, Story


async def mark_project_outcome(db: AsyncSession, project_id: uuid.UUID, delivered_on_time: bool) -> ProjectOutcome:
    project = await db.get(Project, project_id)
    if not project:
        raise ValueError("Project not found")

    now = datetime.now(timezone.utc)
    actual_duration_days = None
    if project.start_date:
        start = datetime.combine(project.start_date, datetime.min.time(), tzinfo=timezone.utc)
        actual_duration_days = (now - start).days

    velocity_rows = (
        await db.execute(
            select(MetricSnapshot)
            .where(MetricSnapshot.project_id == project_id, MetricSnapshot.metric_key == "velocity_completed_points")
        )
    ).scalars().all()
    actual_velocity_avg = statistics.mean([r.value for r in velocity_rows if r.value]) if velocity_rows else None

    stories = (
        await db.execute(select(Story).where(Story.project_id == project_id))
    ).scalars().all()
    done = [s for s in stories if s.status_category == StatusCategory.done]
    defect_density = (
        sum(1 for s in done if s.issue_type == IssueType.bug) / len(done) if done else None
    )

    existing = (
        await db.execute(select(ProjectOutcome).where(ProjectOutcome.project_id == project_id))
    ).scalar_one_or_none()

    fields = dict(
        actual_duration_days=actual_duration_days,
        actual_velocity_avg=round(actual_velocity_avg, 1) if actual_velocity_avg is not None else None,
        defect_density=round(defect_density, 3) if defect_density is not None else None,
        delivered_on_time=delivered_on_time,
        closed_at=now,
    )
    if existing:
        for k, v in fields.items():
            setattr(existing, k, v)
        outcome = existing
    else:
        outcome = ProjectOutcome(project_id=project_id, **fields)
        db.add(outcome)

    project.status = ProjectStatus.completed
    await db.commit()
    await db.refresh(outcome)
    return outcome


async def get_outcome(db: AsyncSession, project_id: uuid.UUID) -> ProjectOutcome | None:
    return (
        await db.execute(select(ProjectOutcome).where(ProjectOutcome.project_id == project_id))
    ).scalar_one_or_none()
