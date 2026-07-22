"""Customer Decision Delay (#6): syncs decision_log from the two sources that
carry decision events — the simulated Teams payload's `pending_decisions`
(see seed_simulated.py) and transcript documents' `decision_events` (see
prompts._DOC_TASK["transcript"]) — and computes delay days.

decided_by/requested_at data is genuinely thin for a POC (most decisions
never got real timestamps until this schema addition), so "who's causing
delays" is reported honestly as "awaiting decision from X days" rather than
attributing blame to an unnamed approver we don't have data for.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.connector import ConnectorType
from app.models.decision_log import DecisionLogEntry, DecisionSource, DecisionStatus
from app.models.document import Document, DocStatus, DocumentExtraction
from app.services.retrieval import simulated_signals


def _parse_dt(value) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _status(value) -> DecisionStatus:
    try:
        return DecisionStatus(value)
    except ValueError:
        return DecisionStatus.pending


async def _upsert(
    db: AsyncSession, project_id: uuid.UUID, *, topic: str, source: DecisionSource,
    requested_at, decided_at, requested_by, decided_by, status: DecisionStatus,
) -> None:
    existing = (
        await db.execute(
            select(DecisionLogEntry).where(
                DecisionLogEntry.project_id == project_id,
                DecisionLogEntry.topic == topic,
                DecisionLogEntry.source == source,
            )
        )
    ).scalar_one_or_none()

    sprint_impact_days = None
    if requested_at and decided_at:
        sprint_impact_days = max(0.0, (decided_at - requested_at).total_seconds() / 86400)

    fields = dict(
        requested_at=requested_at, decided_at=decided_at, requested_by=requested_by,
        decided_by=decided_by, status=status, sprint_impact_days=sprint_impact_days,
    )
    if existing:
        for k, v in fields.items():
            setattr(existing, k, v)
    else:
        db.add(DecisionLogEntry(project_id=project_id, topic=topic, source=source, **fields))


async def sync_decision_log(db: AsyncSession, project_id: uuid.UUID) -> None:
    signals = await simulated_signals(db, project_id)
    teams = signals.get(ConnectorType.teams.value, {})
    for pd in teams.get("pending_decisions", []):
        await _upsert(
            db, project_id, topic=str(pd.get("topic", "")), source=DecisionSource.teams_sim,
            requested_at=_parse_dt(pd.get("requested_at")), decided_at=_parse_dt(pd.get("decided_at")),
            requested_by=pd.get("requested_by"), decided_by=pd.get("decided_by"),
            status=_status(pd.get("status")),
        )

    rows = (
        await db.execute(
            select(Document, DocumentExtraction)
            .join(DocumentExtraction, DocumentExtraction.document_id == Document.id)
            .where(Document.project_id == project_id, Document.status == DocStatus.complete)
        )
    ).all()
    for doc, ext in rows:
        for de in (ext.extraction or {}).get("decision_events", []):
            if not isinstance(de, dict) or not de.get("topic"):
                continue
            await _upsert(
                db, project_id, topic=str(de["topic"]), source=DecisionSource.transcript_doc,
                requested_at=_parse_dt(de.get("requested_at")), decided_at=_parse_dt(de.get("decided_at")),
                requested_by=de.get("requested_by"), decided_by=de.get("decided_by"),
                status=_status(de.get("status")),
            )

    await db.commit()


async def get_decision_summary(db: AsyncSession, project_id: uuid.UUID) -> dict:
    rows = (
        await db.execute(
            select(DecisionLogEntry)
            .where(DecisionLogEntry.project_id == project_id)
            .order_by(DecisionLogEntry.requested_at.desc().nulls_last())
        )
    ).scalars().all()

    now = datetime.now(timezone.utc)
    decided = [r for r in rows if r.sprint_impact_days is not None]
    avg_delay_days = round(sum(r.sprint_impact_days for r in decided) / len(decided), 1) if decided else None

    pending = [
        {
            "topic": r.topic,
            "requested_by": r.requested_by,
            "requested_at": r.requested_at.isoformat() if r.requested_at else None,
            "days_pending": round((now - r.requested_at).total_seconds() / 86400, 1) if r.requested_at else None,
        }
        for r in rows if r.status == DecisionStatus.pending
    ]
    pending.sort(key=lambda d: d["days_pending"] or 0, reverse=True)

    return {
        "avg_delay_days": avg_delay_days,
        "decided_count": len(decided),
        "pending": pending,
        "decisions": [
            {
                "topic": r.topic, "status": r.status.value, "source": r.source.value,
                "requested_at": r.requested_at.isoformat() if r.requested_at else None,
                "decided_at": r.decided_at.isoformat() if r.decided_at else None,
                "requested_by": r.requested_by, "decided_by": r.decided_by,
                "sprint_impact_days": r.sprint_impact_days,
            }
            for r in rows
        ],
    }
