"""Risk Identifier agent: scans documents + live delivery signal for risks
and upserts them into a persisted, trackable registry (risk_items) — same
persisted-row pattern as judge_service.py, but a registry with a real
active/mitigated/closed lifecycle rather than one-off audit rows. Complements
(does not replace) the existing ephemeral AnalysisKind.risk narrative tab.
"""
import json
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import case, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.llm import client, prompts
from app.models.llm_call_log import LLMFeature
from app.models.risk_item import RiskItem, RiskSeverity, RiskSourceType, RiskStatus
from app.services.retrieval import build_context

# RiskSeverity is stored as a plain string column (native_enum=False), so
# RiskItem.severity.desc() sorts alphabetically ("medium" > "low" > "high")
# rather than by actual severity — this expresses the real high-to-low rank.
_SEVERITY_RANK = case(
    (RiskItem.severity == RiskSeverity.high, 0),
    (RiskItem.severity == RiskSeverity.medium, 1),
    (RiskItem.severity == RiskSeverity.low, 2),
    else_=1,
)


def _severity(value) -> RiskSeverity:
    try:
        return RiskSeverity(value)
    except ValueError:
        return RiskSeverity.medium


async def scan_project_risks(db: AsyncSession, project_id: uuid.UUID) -> list[RiskItem]:
    context = await build_context(db, project_id)
    active = (
        await db.execute(
            select(RiskItem).where(RiskItem.project_id == project_id, RiskItem.status == RiskStatus.active)
        )
    ).scalars().all()
    existing_payload = [{"title": r.title, "severity": r.severity.value} for r in active]

    try:
        raw = await client.complete(
            feature=LLMFeature.analysis,
            messages=prompts.risk_identification_messages(context, existing_payload),
            model=settings.llm_model_analysis,
            project_id=project_id,
            temperature=0.2,
            json_mode=True,
        )
        parsed = json.loads(raw)
    except Exception:  # noqa: BLE001 — a scan failure just leaves the registry unchanged
        parsed = {}

    now = datetime.now(timezone.utc)
    by_title = {r.title: r for r in active}

    for item in parsed.get("risks", []):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        if not title:
            continue
        existing = by_title.get(title)
        if existing:
            existing.last_seen_at = now
            existing.description = item.get("description") or existing.description
            existing.severity = _severity(item.get("severity"))
        else:
            db.add(RiskItem(
                project_id=project_id, title=title, description=item.get("description"),
                severity=_severity(item.get("severity")), status=RiskStatus.active,
                source_type=RiskSourceType.sprint_signal, model=settings.llm_model_analysis,
            ))

    for resolved_title in parsed.get("resolved_titles", []):
        existing = by_title.get(str(resolved_title))
        if existing:
            existing.status = RiskStatus.mitigated
            existing.resolved_at = now

    await db.commit()

    return (
        await db.execute(
            select(RiskItem).where(RiskItem.project_id == project_id)
            .order_by(RiskItem.status, _SEVERITY_RANK, RiskItem.last_seen_at.desc())
        )
    ).scalars().all()


async def get_active_risks(db: AsyncSession, project_id: uuid.UUID) -> list[RiskItem]:
    return (
        await db.execute(
            select(RiskItem).where(RiskItem.project_id == project_id, RiskItem.status == RiskStatus.active)
            .order_by(_SEVERITY_RANK, RiskItem.last_seen_at.desc())
        )
    ).scalars().all()


async def resolve_risk(db: AsyncSession, project_id: uuid.UUID, risk_id: uuid.UUID, status: RiskStatus) -> RiskItem:
    risk = (
        await db.execute(
            select(RiskItem).where(RiskItem.id == risk_id, RiskItem.project_id == project_id)
        )
    ).scalar_one_or_none()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    risk.status = status
    if status in (RiskStatus.mitigated, RiskStatus.closed):
        risk.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(risk)
    return risk
