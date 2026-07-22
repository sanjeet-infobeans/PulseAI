"""Team roster + planned leaves for a project (read from the simulated
'resource' connector dataset), plus Resource Risk (#7): the same roster
combined with the rule-based knowledge_map (#12, knowledge_service.py) into
capacity/burnout risk and knowledge-concentration risk, with an LLM
recommendation. Roster summary stats are computed on read rather than
stored, so they never go stale if planned_leaves change. No dedicated
AnalysisKind for the risk view — it's a standalone read, not stored history.
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


async def compute_resource_risk(db: AsyncSession, project_id: uuid.UUID, roster: dict | None = None) -> dict:
    roster = roster if roster is not None else await get_resources(db, project_id)
    resources = roster["resources"]
    knowledge_rows = await latest_knowledge_map(db, project_id)

    sole_holder_modules = [
        {"module": r.module_key, "developer": r.developer, "story_count": r.story_count}
        for r in knowledge_rows if r.is_sole_holder
    ]

    team_size = len(resources) or None
    team_utilization_pct = (
        round(sum(r.get("allocation_percentage", 0) for r in resources) / len(resources))
        if resources else None
    )
    developers = [
        {
            "name": r["name"],
            "skill": ", ".join(r.get("skills", [])) or r.get("designation", ""),
            "utilization_pct": r.get("allocation_percentage", 0),
        }
        for r in resources
    ]

    llm_result: dict = {"burnout_risk": "low", "burnout_reason": "", "recommendations": []}
    if resources or sole_holder_modules:
        try:
            raw = await client.complete(
                feature=LLMFeature.analysis,
                messages=prompts.resource_risk_messages(roster, sole_holder_modules),
                model=settings.llm_model_analysis,
                project_id=project_id,
                temperature=0.2,
                json_mode=True,
            )
            llm_result = {**llm_result, **json.loads(raw)}
        except Exception:  # noqa: BLE001 — recommendation is best-effort
            pass

    return {
        "team_size": team_size,
        "team_utilization_pct": team_utilization_pct,
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
