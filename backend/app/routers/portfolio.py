from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.routers.auth import require_super_admin
from app.services.portfolio_service import get_portfolio

router = APIRouter(tags=["portfolio"])


@router.get("/portfolio")
async def portfolio(
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    return await get_portfolio(db, user.org_id)
