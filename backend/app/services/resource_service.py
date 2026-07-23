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

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.llm import client, prompts
from app.models.connector import ConnectorType
from app.models.llm_call_log import LLMFeature
from app.models.project_resource import LeaveStatus, ProjectResource, ResourceLeave
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


def _resource_to_dict(r: ProjectResource) -> dict:
    return {
        "resource_id": str(r.id),
        "employee_code": r.employee_code or "",
        "name": r.name,
        "designation": r.designation or "",
        "email": r.email or "",
        "allocation_percentage": r.allocation_percentage,
        "billable": r.billable,
        "skills": r.skills or [],
        "planned_leaves": [
            {
                "leave_id": str(lv.id),
                "leave_type": lv.leave_type,
                "start_date": lv.start_date.isoformat(),
                "end_date": lv.end_date.isoformat(),
                "total_days": lv.total_days,
                "status": lv.status.value,
            }
            for lv in r.leaves
        ],
    }


async def get_resources(db: AsyncSession, project_id: uuid.UUID) -> dict:
    real_rows = (
        await db.execute(
            select(ProjectResource)
            .options(selectinload(ProjectResource.leaves))
            .where(ProjectResource.project_id == project_id)
        )
    ).scalars().all()

    if real_rows:
        resources = [_resource_to_dict(r) for r in real_rows]
    else:
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


async def _get_resource_or_404(db: AsyncSession, project_id: uuid.UUID, resource_id: uuid.UUID) -> ProjectResource:
    resource = (
        await db.execute(
            select(ProjectResource)
            .options(selectinload(ProjectResource.leaves))
            .where(ProjectResource.id == resource_id, ProjectResource.project_id == project_id)
        )
    ).scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


async def create_resource(
    db: AsyncSession, project_id: uuid.UUID, *,
    name: str, employee_code: str | None = None, designation: str | None = None,
    email: str | None = None, allocation_percentage: float = 100.0,
    billable: bool = True, skills: list[str] | None = None,
) -> ProjectResource:
    resource = ProjectResource(
        project_id=project_id, name=name.strip(), employee_code=employee_code,
        designation=designation, email=email, allocation_percentage=allocation_percentage,
        billable=billable, skills=skills or [],
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource, attribute_names=["leaves"])
    return resource


async def update_resource(db: AsyncSession, project_id: uuid.UUID, resource_id: uuid.UUID, **fields) -> ProjectResource:
    resource = await _get_resource_or_404(db, project_id, resource_id)
    for k, v in fields.items():
        if v is not None:
            setattr(resource, k, v)
    await db.commit()
    await db.refresh(resource, attribute_names=["leaves"])
    return resource


async def delete_resource(db: AsyncSession, project_id: uuid.UUID, resource_id: uuid.UUID) -> None:
    resource = await _get_resource_or_404(db, project_id, resource_id)
    await db.delete(resource)
    await db.commit()


async def add_leave(
    db: AsyncSession, project_id: uuid.UUID, resource_id: uuid.UUID, *,
    leave_type: str, start_date: date, end_date: date, total_days: int,
    status: LeaveStatus = LeaveStatus.pending,
) -> ProjectResource:
    resource = await _get_resource_or_404(db, project_id, resource_id)
    db.add(ResourceLeave(
        resource_id=resource.id, leave_type=leave_type, start_date=start_date,
        end_date=end_date, total_days=total_days, status=status,
    ))
    await db.commit()
    # resource is already in the session's identity map with `leaves` eagerly
    # loaded (as it was before this insert) — a plain re-query reuses that
    # in-memory collection rather than reflecting the new row, so the
    # relationship must be explicitly refreshed.
    await db.refresh(resource, attribute_names=["leaves"])
    return resource


async def update_leave(
    db: AsyncSession, project_id: uuid.UUID, resource_id: uuid.UUID, leave_id: uuid.UUID, **fields
) -> ProjectResource:
    resource = await _get_resource_or_404(db, project_id, resource_id)
    leave = next((lv for lv in resource.leaves if lv.id == leave_id), None)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    for k, v in fields.items():
        if v is not None:
            setattr(leave, k, v)
    await db.commit()
    return await _get_resource_or_404(db, project_id, resource_id)


async def delete_leave(db: AsyncSession, project_id: uuid.UUID, resource_id: uuid.UUID, leave_id: uuid.UUID) -> None:
    resource = await _get_resource_or_404(db, project_id, resource_id)
    leave = next((lv for lv in resource.leaves if lv.id == leave_id), None)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    await db.delete(leave)
    await db.commit()
