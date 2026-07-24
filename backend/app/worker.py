"""ARQ worker process — `arq app.worker.WorkerSettings`.

Job functions are thin wrappers: each opens nothing itself (the services they
call open their own AsyncSessionLocal, same convention as jira_sync.run_sync
and document_service.process_document) and are safe to enqueue repeatedly.

Scheduling (see docs/ai-features-gap-analysis-and-plan.md):
- On Jira sync: cheap/rule-based recompute jobs, enqueued from jira_sync.run_sync.
- On document upload complete: requirement-catalog sync, enqueued from
  document_service.process_document.
- Nightly cron: LLM-heavy jobs, gated here to control LLM cost.
"""
import logging
import uuid

from arq.connections import RedisSettings
from arq.cron import cron

from app.queue import redis_settings as _redis_settings

logger = logging.getLogger(__name__)


async def run_jira_sync(ctx, connector_id: str) -> None:
    from app.services.jira_sync import run_sync

    await run_sync(uuid.UUID(connector_id))


async def recompute_confidence(ctx, project_id: str, sprint_id: str | None = None) -> None:
    from app.database import AsyncSessionLocal
    from app.services.confidence_service import compute_confidence

    async with AsyncSessionLocal() as db:
        await compute_confidence(
            db, uuid.UUID(project_id), uuid.UUID(sprint_id) if sprint_id else None
        )


async def append_velocity_snapshot(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.metrics_service import append_velocity_snapshot as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def recompute_effort_risk(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.effort_service import sync_effort_risk

    async with AsyncSessionLocal() as db:
        await sync_effort_risk(db, uuid.UUID(project_id))


async def append_scope_snapshot(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.metrics_service import append_scope_snapshot as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def recompute_knowledge_map(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.knowledge_service import compute_knowledge_map

    async with AsyncSessionLocal() as db:
        await compute_knowledge_map(db, uuid.UUID(project_id))


async def sync_requirement_catalog(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.requirement_service import sync_requirement_catalog as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def sync_decision_log(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.decision_service import sync_decision_log as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def sync_action_items(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.action_item_service import sync_action_items as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def scan_project_risks(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.risk_service import scan_project_risks as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def detect_dependencies(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.dependency_service import detect_dependencies as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def recompute_prediction(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.prediction_service import predict_completion

    async with AsyncSessionLocal() as db:
        await predict_completion(db, uuid.UUID(project_id))


async def compute_requirement_volatility(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.volatility_service import compute_volatility

    async with AsyncSessionLocal() as db:
        await compute_volatility(db, uuid.UUID(project_id))


async def generate_executive_briefing(ctx, project_id: str) -> None:
    from app.database import AsyncSessionLocal
    from app.services.analysis_service import generate_executive_briefing as _run

    async with AsyncSessionLocal() as db:
        await _run(db, uuid.UUID(project_id))


async def refresh_simulated_signals(ctx) -> None:
    from app.database import AsyncSessionLocal
    from app.services.simulated_refresh_service import refresh_all_projects

    async with AsyncSessionLocal() as db:
        await refresh_all_projects(db)


async def nightly_all_projects(ctx) -> None:
    """Fan-out entry point: enqueue the per-project nightly jobs for every project.

    Kept separate from the cron function itself so per-project jobs still show
    up individually in ARQ's job registry/logs.
    """
    from app.database import AsyncSessionLocal
    from app.models.project import Project
    from sqlalchemy import select

    pool = ctx["redis"]
    async with AsyncSessionLocal() as db:
        project_ids = (await db.execute(select(Project.id))).scalars().all()
    for pid in project_ids:
        await pool.enqueue_job("detect_dependencies", str(pid))
        await pool.enqueue_job("recompute_knowledge_map", str(pid))
        await pool.enqueue_job("generate_executive_briefing", str(pid))
        await pool.enqueue_job("compute_requirement_volatility", str(pid))
        # Safety net for projects with no recent document uploads — the
        # primary trigger is document_service.process_document completing.
        await pool.enqueue_job("scan_project_risks", str(pid))


class WorkerSettings:
    functions = [
        run_jira_sync,
        recompute_confidence,
        append_velocity_snapshot,
        recompute_effort_risk,
        append_scope_snapshot,
        recompute_knowledge_map,
        sync_requirement_catalog,
        sync_decision_log,
        sync_action_items,
        scan_project_risks,
        detect_dependencies,
        generate_executive_briefing,
        recompute_prediction,
        compute_requirement_volatility,
        refresh_simulated_signals,
        nightly_all_projects,
    ]
    cron_jobs = [
        cron(refresh_simulated_signals, hour=2, minute=0),
        cron(nightly_all_projects, hour=2, minute=15),
    ]

    @staticmethod
    async def on_startup(ctx):
        logger.info("PulseAI ARQ worker started")

    redis_settings: RedisSettings = _redis_settings()
