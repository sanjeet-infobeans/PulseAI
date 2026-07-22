"""Team roster + planned leaves for a project, read from the simulated
'resource' connector dataset. Summary stats are computed on read rather
than stored, so they never go stale if planned_leaves change."""
import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.connector import ConnectorType
from app.models.simulated import SimulatedDataset


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
