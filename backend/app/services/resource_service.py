"""Resource Risk (#7): combines the simulated `resource` connector payload
(team_size/utilization_pct/developers[], see seed_simulated.py) with the
rule-based knowledge_map (#12, knowledge_service.py) into one view — capacity/
burnout risk plus knowledge-concentration risk, with an LLM recommendation.
No dedicated AnalysisKind — this is a standalone read, not stored history yet.
"""
import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.connector import ConnectorType
from app.models.llm_call_log import LLMFeature
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
