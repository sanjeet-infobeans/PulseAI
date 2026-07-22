"""Writes to metric_snapshots — the generic trend table most Phase 2 features
(prediction, scope creep, volatility, resource, sentiment) read from. Runs on
every Jira sync (see jira_sync.py::_enqueue_recompute) so history accumulates
one data point per sync cycle, the same "needs >=2 points" shape
confidence_service.py's velocity_stability already has.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metric_snapshot import MetricSnapshot
from app.models.sprint import Sprint, SprintState
from app.models.status_ref import StatusCategory
from app.models.story import Story


async def _latest_value(db: AsyncSession, project_id: uuid.UUID, metric_key: str) -> float | None:
    row = (
        await db.execute(
            select(MetricSnapshot)
            .where(MetricSnapshot.project_id == project_id, MetricSnapshot.metric_key == metric_key)
            .order_by(MetricSnapshot.recorded_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    return row.value if row else None


async def append_velocity_snapshot(db: AsyncSession, project_id: uuid.UUID) -> None:
    sprints = (
        await db.execute(select(Sprint).where(Sprint.project_id == project_id))
    ).scalars().all()

    for sprint in sprints:
        if sprint.state != SprintState.closed:
            continue
        # Closed sprints are immutable once closed — one snapshot per sprint, ever.
        existing = (
            await db.execute(
                select(MetricSnapshot).where(
                    MetricSnapshot.project_id == project_id,
                    MetricSnapshot.sprint_id == sprint.id,
                    MetricSnapshot.metric_key == "velocity_completed_points",
                )
            )
        ).scalar_one_or_none()
        if existing:
            continue
        db.add(MetricSnapshot(
            project_id=project_id, sprint_id=sprint.id,
            metric_key="velocity_completed_points", value=sprint.completed_points,
            meta={"committed_points": sprint.committed_points, "sprint_name": sprint.name},
            source="jira_sync",
        ))

    active = next((s for s in sprints if s.state == SprintState.active), None)
    if active:
        # In-flight progress — append every sync so the current sprint's burn-up trends.
        db.add(MetricSnapshot(
            project_id=project_id, sprint_id=active.id,
            metric_key="velocity_completed_points_inflight", value=active.completed_points,
            meta={"committed_points": active.committed_points, "sprint_name": active.name},
            source="jira_sync",
        ))
    await db.commit()


async def append_scope_snapshot(db: AsyncSession, project_id: uuid.UUID) -> None:
    stories = (
        await db.execute(select(Story).where(Story.project_id == project_id))
    ).scalars().all()

    open_count = sum(1 for s in stories if s.status_category != StatusCategory.done)
    point_total = sum(s.story_points or 0.0 for s in stories)

    for metric_key, value in (
        ("scope_story_count_open", float(open_count)),
        ("scope_point_total", point_total),
        ("scope_story_count_total", float(len(stories))),
    ):
        last = await _latest_value(db, project_id, metric_key)
        if last is not None and abs(last - value) < 1e-6:
            continue  # no change — don't spam identical snapshots
        db.add(MetricSnapshot(
            project_id=project_id, metric_key=metric_key, value=value,
            meta={}, source="jira_sync",
        ))
    await db.commit()
