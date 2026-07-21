"""Optional sample delivery data (sprints + stories) for the demo project, so the
AI, confidence, and dashboard features work out of the box before a live Jira sync.
Idempotent: skips if the project already has stories. Real Jira sync upserts over this."""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sprint import Sprint, SprintState
from app.models.status_ref import StatusCategory
from app.models.story import IssueType, Story

_NAMES = ["Priya S.", "Marco R.", "Lena K.", "Devon P.", None]


def _story(key, title, cat, pts, itype, assignee, blocked=False):
    return dict(
        external_id=key, title=title, status_category=cat, story_points=pts,
        issue_type=itype, assignee=assignee, is_blocked=blocked, raw_status=cat.value,
        priority="High" if blocked else "Medium", labels=["blocked"] if blocked else [],
    )


_SPRINTS = [
    ("101", "Sprint 40", SprintState.closed, 40, 38),
    ("102", "Sprint 41", SprintState.closed, 42, 44),
    ("103", "Sprint 42", SprintState.active, 45, 28),
]

_STORIES = {
    "103": [
        _story("ATLAS-201", "Checkout API circuit breaker", StatusCategory.in_progress, 8, IssueType.story, "Priya S."),
        _story("ATLAS-202", "Payment vendor timeout handling", StatusCategory.blocked, 5, IssueType.bug, "Marco R.", blocked=True),
        _story("ATLAS-203", "Cart migration to new schema", StatusCategory.done, 8, IssueType.story, "Lena K."),
        _story("ATLAS-204", "Legacy export deprecation", StatusCategory.todo, 5, IssueType.task, None),
        _story("ATLAS-205", "Checkout latency dashboards", StatusCategory.in_review, 3, IssueType.story, "Devon P."),
        _story("ATLAS-206", "Fraud rule regression", StatusCategory.blocked, 8, IssueType.bug, "Priya S.", blocked=True),
        _story("ATLAS-207", "Address validation service", StatusCategory.done, 5, IssueType.story, "Lena K."),
        _story("ATLAS-208", "Order confirmation email revamp", StatusCategory.in_progress, 3, IssueType.story, "Marco R."),
    ],
    "102": [
        _story("ATLAS-180", "Session pooling", StatusCategory.done, 13, IssueType.story, "Priya S."),
        _story("ATLAS-181", "Payment retry queue", StatusCategory.done, 8, IssueType.story, "Marco R."),
        _story("ATLAS-182", "Inventory sync bug", StatusCategory.done, 5, IssueType.bug, "Lena K."),
    ],
    "101": [
        _story("ATLAS-150", "Auth service split", StatusCategory.done, 13, IssueType.story, "Priya S."),
        _story("ATLAS-151", "Catalog caching", StatusCategory.done, 8, IssueType.story, "Devon P."),
    ],
}


async def seed_demo_delivery(db: AsyncSession, project_id: uuid.UUID) -> None:
    existing = await db.scalar(
        select(func.count()).select_from(Story).where(Story.project_id == project_id)
    )
    if existing:
        return

    now = datetime.now(timezone.utc)
    sprint_ids: dict[str, uuid.UUID] = {}
    for i, (ext, name, state, committed, completed) in enumerate(_SPRINTS):
        start = now - timedelta(days=(len(_SPRINTS) - i) * 14)
        sprint = Sprint(
            project_id=project_id, external_id=ext, name=name, state=state,
            goal=f"{name} delivery goal", start_date=start, end_date=start + timedelta(days=14),
            committed_points=committed, completed_points=completed, sequence=i,
        )
        db.add(sprint)
        await db.flush()
        sprint_ids[ext] = sprint.id

    for ext, stories in _STORIES.items():
        for s in stories:
            db.add(Story(project_id=project_id, sprint_id=sprint_ids[ext], **s))
    await db.flush()
