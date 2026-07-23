"""Connector sync: fetch → normalize → upsert into the delivery tables.

Runs as an ARQ job (app.worker.run_jira_sync), so it opens its OWN AsyncSession
(the request session is already closed by the time this runs) — same
open-your-own-session convention as document_service.process_document.
"""
import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from app.connectors.registry import get_connector
from app.connectors.schemas import NormalizedBundle
from app.database import AsyncSessionLocal
from app.models.connector import Connector, ConnectorStatus
from app.models.status_ref import StatusCategory, StatusRef
from app.models.sprint import Sprint
from app.models.story import Story

logger = logging.getLogger(__name__)


async def run_sync(connector_id: uuid.UUID) -> None:
    async with AsyncSessionLocal() as db:
        connector = await db.get(Connector, connector_id)
        if not connector:
            logger.warning("Sync requested for missing connector %s", connector_id)
            return

        connector.status = ConnectorStatus.syncing
        connector.last_error = None
        await db.commit()

        try:
            bundle = await get_connector(connector).fetch_and_normalize()
            await _persist(db, connector, bundle)
            connector.status = ConnectorStatus.connected
            connector.last_synced_at = datetime.now(timezone.utc)
            await db.commit()
            logger.info(
                "Synced connector %s: %d sprints, %d stories",
                connector_id, len(bundle.sprints), len(bundle.stories),
            )
            await _enqueue_recompute(connector.project_id)
        except Exception as exc:  # noqa: BLE001
            await db.rollback()
            connector.status = ConnectorStatus.error
            connector.last_error = str(exc)[:1000]
            await db.commit()
            logger.exception("Sync failed for connector %s", connector_id)


async def _enqueue_recompute(project_id: uuid.UUID) -> None:
    """Cheap/rule-based recompute — safe to run after every sync (LLM-heavy
    jobs like dependency detection are nightly-cron only, see app/worker.py)."""
    from app.queue import get_arq_pool

    pool = await get_arq_pool()
    pid = str(project_id)
    await pool.enqueue_job("append_velocity_snapshot", pid)
    await pool.enqueue_job("append_scope_snapshot", pid)
    await pool.enqueue_job("recompute_knowledge_map", pid)
    await pool.enqueue_job("recompute_confidence", pid)
    await pool.enqueue_job("recompute_prediction", pid)


async def _persist(db, connector: Connector, bundle: NormalizedBundle) -> None:
    project_id = connector.project_id

    # ── Statuses ────────────────────────────────────────────────────────────
    for st in bundle.statuses:
        existing = (
            await db.execute(
                select(StatusRef).where(
                    StatusRef.project_id == project_id, StatusRef.raw_name == st.raw_name
                )
            )
        ).scalar_one_or_none()
        if existing:
            existing.normalized_category = st.category
            existing.order_index = st.order_index
        else:
            db.add(StatusRef(
                project_id=project_id, raw_name=st.raw_name,
                normalized_category=st.category, order_index=st.order_index,
            ))
    await db.flush()

    # ── Sprints (upsert by external_id), track id map for story linkage ───────
    sprint_ids: dict[str, uuid.UUID] = {}
    for s in bundle.sprints:
        existing = (
            await db.execute(
                select(Sprint).where(
                    Sprint.project_id == project_id, Sprint.external_id == s.external_id
                )
            )
        ).scalar_one_or_none()
        if existing:
            existing.name = s.name
            existing.state = s.state
            existing.goal = s.goal
            existing.start_date = s.start_date
            existing.end_date = s.end_date
            existing.complete_date = s.complete_date
            existing.sequence = s.sequence
            existing.connector_id = connector.id
            sprint = existing
        else:
            sprint = Sprint(
                project_id=project_id, connector_id=connector.id, external_id=s.external_id,
                name=s.name, state=s.state, goal=s.goal, start_date=s.start_date,
                end_date=s.end_date, complete_date=s.complete_date, sequence=s.sequence,
            )
            db.add(sprint)
        await db.flush()
        sprint_ids[s.external_id] = sprint.id

    # ── Stories (upsert by external_id) + roll points onto sprints ────────────
    committed: dict[uuid.UUID, float] = {sid: 0.0 for sid in sprint_ids.values()}
    completed: dict[uuid.UUID, float] = {sid: 0.0 for sid in sprint_ids.values()}

    for st in bundle.stories:
        sprint_id = sprint_ids.get(st.sprint_external_id or "")
        existing = (
            await db.execute(
                select(Story).where(
                    Story.project_id == project_id, Story.external_id == st.external_id
                )
            )
        ).scalar_one_or_none()
        fields = dict(
            sprint_id=sprint_id, connector_id=connector.id, title=st.title,
            description=st.description, issue_type=st.issue_type,
            status_category=st.status_category, raw_status=st.raw_status,
            story_points=st.story_points, assignee=st.assignee, reporter=st.reporter,
            priority=st.priority, is_blocked=st.is_blocked, blocked_reason=st.blocked_reason,
            labels=st.labels, created_ext=st.created_ext, updated_ext=st.updated_ext,
            resolved_ext=st.resolved_ext,
        )
        if existing:
            # Requirement-volatility (#5) reopen signal: a story that was done
            # and comes back non-done on a later sync got reopened.
            if (
                existing.status_category == StatusCategory.done
                and st.status_category != StatusCategory.done
            ):
                existing.reopened_count += 1
            # Sprint-timeline carry-forward: snapshot the old sprint before the
            # overwrite below replaces it, same precedent as reopened_count above.
            old_sprint_id = existing.sprint_id
            if (
                old_sprint_id and sprint_id and old_sprint_id != sprint_id
                and st.status_category != StatusCategory.done
            ):
                existing.carried_forward_from_sprint_id = old_sprint_id
            for k, v in fields.items():
                setattr(existing, k, v)
        else:
            db.add(Story(project_id=project_id, external_id=st.external_id, **fields))

        if sprint_id and st.story_points:
            committed[sprint_id] += st.story_points
            if st.status_category == StatusCategory.done:
                completed[sprint_id] += st.story_points

    # Persist rollups
    for sprint_id in sprint_ids.values():
        sprint = await db.get(Sprint, sprint_id)
        if sprint:
            sprint.committed_points = committed.get(sprint_id, 0.0)
            sprint.completed_points = completed.get(sprint_id, 0.0)
    await db.flush()
