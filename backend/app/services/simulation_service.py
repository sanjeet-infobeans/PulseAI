"""What-If Simulation (#14): LLM-only reasoning (no solver/optimizer) against
the project's current baseline confidence/prediction. Logged, not trended —
each run is independent (what_if_scenarios table).

Chat integration (routing free-text "what if" chat questions through this
service) is intentionally out of scope for this build — it would need
intent-detection inside chat_service's streaming pipeline. This ships as its
own endpoint + structured panel instead (see
docs/ai-features-gap-analysis-and-plan.md option (b)), which is verifiable
and doesn't risk destabilizing the existing chat flow.
"""
import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.llm_call_log import LLMFeature
from app.models.what_if_scenario import WhatIfScenario
from app.services.confidence_service import latest_confidence
from app.services.prediction_service import latest_prediction
from app.services.retrieval import build_context


def _clamp(v, lo=-100.0, hi=100.0) -> float:
    try:
        return round(max(lo, min(hi, float(v))), 1)
    except (TypeError, ValueError):
        return 0.0


async def run_what_if(
    db: AsyncSession, project_id: uuid.UUID, scenario_text: str, requested_by: uuid.UUID | None = None
) -> WhatIfScenario:
    context = await build_context(db, project_id)
    confidence = await latest_confidence(db, project_id)
    prediction = await latest_prediction(db, project_id)

    baseline_confidence = (
        {"score": confidence.score, "band": confidence.band.value} if confidence else None
    )
    baseline_prediction = (
        {
            "predicted_completion_date": prediction.predicted_completion_date.isoformat()
            if prediction.predicted_completion_date else None,
            "probability_on_time": prediction.probability_on_time,
        } if prediction else None
    )

    result = {"estimated_weeks": None, "estimated_resources": [], "risk": "medium",
              "confidence_delta": 0.0, "summary": ""}
    try:
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=prompts.what_if_messages(context, baseline_confidence, baseline_prediction, scenario_text),
            model=settings.llm_model_analysis,
            project_id=project_id,
            temperature=0.3,
            json_mode=True,
        )
        result = {**result, **json.loads(raw)}
    except Exception:  # noqa: BLE001 — best-effort; scenario still logged
        pass

    row = WhatIfScenario(
        project_id=project_id, requested_by=requested_by, scenario_text=scenario_text,
        scenario_input={"baseline_confidence": baseline_confidence, "baseline_prediction": baseline_prediction},
        estimated_weeks=result.get("estimated_weeks"),
        resources_needed=result.get("estimated_resources", []),
        risk_delta={"risk": result.get("risk", "medium")},
        confidence_delta=_clamp(result.get("confidence_delta", 0.0)),
        result_summary=result.get("summary", ""),
        model=settings.llm_model_analysis,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row
