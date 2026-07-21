"""Normalized data returned by every connector, regardless of source.

A connector's job is to translate a source-native payload into these shapes so
downstream services (sync, dashboard, AI) never branch on the source system.
"""
from dataclasses import dataclass, field
from datetime import datetime

from app.models.status_ref import StatusCategory
from app.models.sprint import SprintState
from app.models.story import IssueType


@dataclass
class NormalizedStatus:
    raw_name: str
    category: StatusCategory
    order_index: int = 0


@dataclass
class NormalizedStory:
    external_id: str
    title: str
    issue_type: IssueType
    status_category: StatusCategory
    raw_status: str | None = None
    description: str | None = None
    story_points: float | None = None
    assignee: str | None = None
    reporter: str | None = None
    priority: str | None = None
    is_blocked: bool = False
    blocked_reason: str | None = None
    labels: list[str] = field(default_factory=list)
    sprint_external_id: str | None = None
    created_ext: datetime | None = None
    updated_ext: datetime | None = None
    resolved_ext: datetime | None = None


@dataclass
class NormalizedSprint:
    external_id: str
    name: str
    state: SprintState
    goal: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    complete_date: datetime | None = None
    sequence: int = 0


@dataclass
class NormalizedBundle:
    statuses: list[NormalizedStatus] = field(default_factory=list)
    sprints: list[NormalizedSprint] = field(default_factory=list)
    stories: list[NormalizedStory] = field(default_factory=list)
