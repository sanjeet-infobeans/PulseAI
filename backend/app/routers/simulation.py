import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.what_if_scenario import WhatIfScenario
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services.simulation_service import run_what_if

router = APIRouter(tags=["simulation"])


class WhatIfIn(BaseModel):
    scenario_text: str


class WhatIfOut(BaseModel):
    id: str
    scenario_text: str
    estimated_weeks: float | None
    resources_needed: list
    risk: str
    confidence_delta: float
    summary: str | None
    created_at: str

    @classmethod
    def of(cls, s: WhatIfScenario) -> "WhatIfOut":
        return cls(
            id=str(s.id), scenario_text=s.scenario_text, estimated_weeks=s.estimated_weeks,
            resources_needed=s.resources_needed or [], risk=(s.risk_delta or {}).get("risk", "medium"),
            confidence_delta=s.confidence_delta or 0.0, summary=s.result_summary,
            created_at=s.created_at.isoformat(),
        )


@router.post("/projects/{project_id}/simulate", response_model=WhatIfOut)
async def simulate(
    project_id: uuid.UUID, body: WhatIfIn, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> WhatIfOut:
    await _load_project(db, project_id, user)
    row = await run_what_if(db, project_id, body.scenario_text, requested_by=user.id)
    return WhatIfOut.of(row)
