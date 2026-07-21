"""Real Jira Cloud connector.

Auth: Basic auth = base64(email:api_token). `email` and non-secret config come
from connector.config; the API token is resolved from an env var named by
connector.secret_ref (never stored in the DB).
"""
import base64
import logging
from datetime import datetime

import httpx
from fastapi import HTTPException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.connectors.base import BaseConnector
from app.connectors.schemas import (
    NormalizedBundle,
    NormalizedSprint,
    NormalizedStatus,
    NormalizedStory,
)
from app.models.connector import ConnectorMode, ConnectorType
from app.models.status_ref import StatusCategory
from app.models.sprint import SprintState
from app.models.story import IssueType

logger = logging.getLogger(__name__)

_DEFAULT_SP_FIELD = "customfield_10016"
_PAGE = 50
_TIMEOUT = httpx.Timeout(30.0)

_ISSUE_TYPE_MAP = {
    "story": IssueType.story,
    "bug": IssueType.bug,
    "task": IssueType.task,
    "epic": IssueType.epic,
    "sub-task": IssueType.subtask,
    "subtask": IssueType.subtask,
}

_SPRINT_STATE_MAP = {
    "future": SprintState.future,
    "active": SprintState.active,
    "closed": SprintState.closed,
}


class _RetryableStatus(Exception):
    pass


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _status_category(raw_name: str, category_key: str) -> StatusCategory:
    name = (raw_name or "").lower()
    if "block" in name:
        return StatusCategory.blocked
    if "review" in name:
        return StatusCategory.in_review
    return {
        "new": StatusCategory.todo,
        "indeterminate": StatusCategory.in_progress,
        "done": StatusCategory.done,
    }.get(category_key, StatusCategory.todo)


class JiraConnector(BaseConnector):
    type = ConnectorType.jira
    mode = ConnectorMode.real

    def _client(self) -> httpx.AsyncClient:
        base_url = str(self.config.get("base_url", "")).rstrip("/")
        email = self.config.get("email")
        if not base_url or not email:
            raise HTTPException(status_code=400, detail="Jira connector needs base_url and email in config")
        if not self.secret:
            raise HTTPException(
                status_code=503,
                detail=f"Jira token not found (secret_ref '{self.connector.secret_ref}')",
            )
        token = base64.b64encode(f"{email}:{self.secret}".encode()).decode()
        return httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Basic {token}", "Accept": "application/json"},
            timeout=_TIMEOUT,
        )

    @retry(
        retry=retry_if_exception_type(_RetryableStatus),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _get(self, client: httpx.AsyncClient, path: str, params: dict) -> dict:
        res = await client.get(path, params=params)
        if res.status_code == 429:
            raise _RetryableStatus()
        if res.status_code in (401, 403):
            raise HTTPException(status_code=502, detail="Jira authentication failed — check email/token")
        if res.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"Jira error {res.status_code}: {res.text[:200]}")
        return res.json()

    async def test_connection(self) -> None:
        board_id = self.config.get("board_id")
        async with self._client() as client:
            await self._get(client, f"/rest/agile/1.0/board/{board_id}", {})

    async def fetch_and_normalize(self) -> NormalizedBundle:
        board_id = self.config.get("board_id")
        project_key = self.config.get("project_key")
        sp_field = self.config.get("story_point_field") or _DEFAULT_SP_FIELD
        if not board_id:
            raise HTTPException(status_code=400, detail="Jira connector needs board_id in config")

        bundle = NormalizedBundle()
        async with self._client() as client:
            if project_key:
                bundle.statuses = await self._fetch_statuses(client, project_key)
            bundle.sprints = await self._fetch_sprints(client, board_id)
            membership = await self._sprint_membership(client, bundle.sprints)
            bundle.stories = await self._fetch_board_stories(client, board_id, membership, sp_field)
        return bundle

    async def _fetch_statuses(self, client, project_key: str) -> list[NormalizedStatus]:
        data = await self._get(client, f"/rest/api/3/project/{project_key}/statuses", {})
        seen: dict[str, NormalizedStatus] = {}
        idx = 0
        for issue_type in data if isinstance(data, list) else []:
            for st in issue_type.get("statuses", []):
                name = st.get("name", "")
                if name in seen:
                    continue
                cat_key = st.get("statusCategory", {}).get("key", "new")
                seen[name] = NormalizedStatus(name, _status_category(name, cat_key), idx)
                idx += 1
        return list(seen.values())

    async def _fetch_sprints(self, client, board_id) -> list[NormalizedSprint]:
        sprints: list[NormalizedSprint] = []
        start_at, seq = 0, 0
        while True:
            data = await self._get(
                client, f"/rest/agile/1.0/board/{board_id}/sprint",
                {"startAt": start_at, "maxResults": _PAGE},
            )
            for s in data.get("values", []):
                sprints.append(
                    NormalizedSprint(
                        external_id=str(s["id"]),
                        name=s.get("name", f"Sprint {s['id']}"),
                        state=_SPRINT_STATE_MAP.get(s.get("state", "future"), SprintState.future),
                        goal=s.get("goal"),
                        start_date=_parse_dt(s.get("startDate")),
                        end_date=_parse_dt(s.get("endDate")),
                        complete_date=_parse_dt(s.get("completeDate")),
                        sequence=seq,
                    )
                )
                seq += 1
            if data.get("isLast", True):
                break
            start_at += _PAGE
        return sprints

    async def _sprint_membership(self, client, sprints) -> dict[str, str]:
        """Map issue key → sprint external_id for issues assigned to a sprint."""
        membership: dict[str, str] = {}
        for sprint in sprints:
            start_at = 0
            while True:
                data = await self._get(
                    client, f"/rest/agile/1.0/sprint/{sprint.external_id}/issue",
                    {"startAt": start_at, "maxResults": _PAGE, "fields": "key"},
                )
                for issue in data.get("issues", []):
                    membership[issue.get("key", "")] = sprint.external_id
                total = data.get("total", 0)
                start_at += _PAGE
                if start_at >= total or not data.get("issues"):
                    break
        return membership

    async def _fetch_board_stories(self, client, board_id, membership, sp_field) -> list[NormalizedStory]:
        """Fetch ALL board issues (backlog + sprint), linking each to its sprint if any."""
        stories: list[NormalizedStory] = []
        start_at = 0
        while True:
            data = await self._get(
                client, f"/rest/agile/1.0/board/{board_id}/issue",
                {"startAt": start_at, "maxResults": _PAGE, "fields": "*all"},
            )
            for issue in data.get("issues", []):
                sprint_ext = membership.get(issue.get("key", ""))
                stories.append(self._normalize_issue(issue, sprint_ext, sp_field))
            total = data.get("total", 0)
            start_at += _PAGE
            if start_at >= total or not data.get("issues"):
                break
        return stories

    def _normalize_issue(self, issue: dict, sprint_ext_id: str, sp_field: str) -> NormalizedStory:
        f = issue.get("fields", {})
        status = f.get("status", {}) or {}
        raw_status = status.get("name", "")
        cat_key = status.get("statusCategory", {}).get("key", "new")
        labels = f.get("labels", []) or []
        is_blocked = any("block" in str(l).lower() for l in labels) or "block" in raw_status.lower()
        itype_name = (f.get("issuetype", {}) or {}).get("name", "").lower()
        assignee = (f.get("assignee") or {}).get("displayName")
        reporter = (f.get("reporter") or {}).get("displayName")
        priority = (f.get("priority") or {}).get("name")
        sp = f.get(sp_field)
        return NormalizedStory(
            external_id=issue.get("key", ""),
            title=f.get("summary", ""),
            issue_type=_ISSUE_TYPE_MAP.get(itype_name, IssueType.task),
            status_category=_status_category(raw_status, cat_key),
            raw_status=raw_status,
            description=None,
            story_points=float(sp) if isinstance(sp, (int, float)) else None,
            assignee=assignee,
            reporter=reporter,
            priority=priority,
            is_blocked=is_blocked,
            blocked_reason="Flagged in Jira" if is_blocked else None,
            labels=list(labels),
            sprint_external_id=sprint_ext_id,
            created_ext=_parse_dt(f.get("created")),
            updated_ext=_parse_dt(f.get("updated")),
            resolved_ext=_parse_dt(f.get("resolutiondate")),
        )
