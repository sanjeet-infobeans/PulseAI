"""Stakeholder Sentiment (#13): real trend version. The `sentiment`
SimulatedDataset payload's static score/trend/series (seed_simulated.py) is
now refreshed nightly by simulated_refresh_service.py, which also appends to
metric_snapshots — this reads that real history instead of just echoing the
static seeded `note`, and reasons over Teams/Slack signals for what's driving
a decline. Live compute, no dedicated table (same pattern as resource_service.py).
"""
import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.connector import ConnectorType
from app.models.llm_call_log import LLMFeature
from app.models.metric_snapshot import MetricSnapshot
from app.services.retrieval import build_context, simulated_signals


async def get_sentiment(db: AsyncSession, project_id: uuid.UUID) -> dict:
    signals = await simulated_signals(db, project_id)
    sentiment_payload = signals.get(ConnectorType.sentiment.value, {})

    history_rows = (
        await db.execute(
            select(MetricSnapshot)
            .where(MetricSnapshot.project_id == project_id, MetricSnapshot.metric_key == "sentiment_score")
            .order_by(MetricSnapshot.recorded_at.asc())
        )
    ).scalars().all()
    sentiment_trend = [
        {"recorded_at": r.recorded_at.isoformat(), "score": r.value} for r in history_rows
    ]

    current_score = sentiment_payload.get("score")
    series = [p["score"] for p in sentiment_trend] or sentiment_payload.get("series", [])

    llm_result = {"trend": sentiment_payload.get("trend", "steady"), "reasons": []}
    if len(sentiment_trend) >= 2 or sentiment_payload:
        try:
            context = await build_context(db, project_id)
            raw = await client.complete(
                feature=LLMFeature.analysis,
                messages=prompts.sentiment_analysis_messages(context, sentiment_trend, signals),
                model=settings.llm_model_analysis,
                project_id=project_id,
                temperature=0.2,
                json_mode=True,
            )
            llm_result = {**llm_result, **json.loads(raw)}
        except Exception:  # noqa: BLE001 — reasoning is best-effort
            pass

    return {
        "current_score": current_score,
        "trend": llm_result.get("trend", "steady"),
        "series": series,
        "reasons": llm_result.get("reasons", []),
        "history_points": len(sentiment_trend),
    }
