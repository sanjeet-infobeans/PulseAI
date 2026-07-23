import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.dependency_edge import DependencyEdge
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services.dependency_service import latest_dependencies

router = APIRouter(tags=["dependencies"])


class DependencyEdgeOut(BaseModel):
    id: str
    from_type: str
    from_ref: str
    to_type: str
    to_ref: str
    relation: str
    confidence: float
    rationale: str | None
    detected_at: str

    @classmethod
    def of(cls, e: DependencyEdge) -> "DependencyEdgeOut":
        return cls(
            id=str(e.id), from_type=e.from_type, from_ref=e.from_ref,
            to_type=e.to_type, to_ref=e.to_ref, relation=e.relation.value,
            confidence=e.confidence, rationale=e.rationale, detected_at=e.detected_at.isoformat(),
        )


@router.get("/projects/{project_id}/dependencies", response_model=list[DependencyEdgeOut])
async def get_dependencies(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[DependencyEdgeOut]:
    await _load_project(db, project_id, user)
    rows = await latest_dependencies(db, project_id)
    return [DependencyEdgeOut.of(r) for r in rows]
