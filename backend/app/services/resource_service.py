"""Resource Risk (#7): combines the simulated `resource` connector payload
(team_size/utilization_pct/developers[], see seed_simulated.py) with the
rule-based knowledge_map (#12, knowledge_service.py) into one view — capacity/
burnout risk plus knowledge-concentration risk, with an LLM recommendation.
No dedicated AnalysisKind — this is a standalone read, not stored history yet.

Also exposes get_resources(): team roster + planned leaves read from the same
simulated `resource` connector payload (resources[] — see seed_simulated.py).
Summary stats are computed on read rather than stored, so they never go stale
if planned_leaves change.
"""
import json
import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.connector import ConnectorType
from app.models.llm_call_log import LLMFeature
from app.models.simulated import SimulatedDataset
from app.services.knowledge_service import latest_knowledge_map
from app.services.retrieval import simulated_signals


async def compute_resource_risk(db: AsyncSession, project_id: uuid.UUID) -> dict:
    signals = await simulated_signals(db, project_id)
    resource_payload = signals.get(ConnectorType.resource.value, {})
    knowledge_rows = await latest_knowledge_map(db, project_id)

    sole_holder_modules = [
        {"module": r.module_key, "developer": r.developer, "story_count": r.story_count}
        for r in knowledge_rows if r.is_sole_holder
    ]

    developers = resource_payload.get("developers", [])
    team_utilization = resource_payload.get("utilization_pct")

    llm_result: dict = {"burnout_risk": "low", "burnout_reason": "", "recommendations": []}
    if resource_payload or sole_holder_modules:
        try:
            raw = await client.complete(
                feature=LLMFeature.analysis,
                messages=prompts.resource_risk_messages(resource_payload, sole_holder_modules),
                model=settings.llm_model_analysis,
                project_id=project_id,
                temperature=0.2,
                json_mode=True,
            )
            llm_result = {**llm_result, **json.loads(raw)}
        except Exception:  # noqa: BLE001 — recommendation is best-effort
            pass

    return {
        "team_size": resource_payload.get("team_size"),
        "team_utilization_pct": team_utilization,
        "developers": developers,
        "knowledge_concentration": [
            {"module": r.module_key, "developer": r.developer, "story_count": r.story_count,
             "is_sole_holder": r.is_sole_holder}
            for r in knowledge_rows
        ],
        "sole_holder_modules": sole_holder_modules,
        "burnout_risk": llm_result.get("burnout_risk", "low"),
        "burnout_reason": llm_result.get("burnout_reason", ""),
        "recommendations": llm_result.get("recommendations", []),
    }


async def get_resources(db: AsyncSession, project_id: uuid.UUID) -> dict:
    row = (
        await db.execute(
            select(SimulatedDataset).where(
                SimulatedDataset.project_id == project_id,
                SimulatedDataset.source == ConnectorType.resource,
            )
        )
    ).scalar_one_or_none()
    resources = (row.payload.get("resources", []) if row else [])

    today = date.today()
    horizon = today + timedelta(days=30)

    all_leaves = [lv for r in resources for lv in r.get("planned_leaves", [])]
    on_leave_today = sum(
        1
        for r in resources
        if any(
            lv["status"] == "Approved" and lv["start_date"] <= today.isoformat() <= lv["end_date"]
            for lv in r.get("planned_leaves", [])
        )
    )
    next_30_days_leaves = [
        lv for lv in all_leaves if today.isoformat() <= lv["start_date"] <= horizon.isoformat()
    ]

    summary = {
        "total_resources": len(resources),
        "active_resources": sum(1 for r in resources if r.get("allocation_percentage", 0) > 0),
        "resources_on_leave_today": on_leave_today,
        "planned_leaves_next_30_days": len(next_30_days_leaves),
        "total_planned_leave_days": sum(lv.get("total_days", 0) for lv in all_leaves),
    }
    return {"resources": resources, "summary": summary}
