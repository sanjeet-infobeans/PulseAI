"""User authentication and RBAC.

JWT payload: {sub: user_id, type: "user", role, customer_id, org_id, exp: +8h}
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.user import User, UserRole
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

_bearer = HTTPBearer(auto_error=False)
_TOKEN_HOURS = 8


class LoginBody(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    token: str


class MeOut(BaseModel):
    id: str
    email: str
    name: str
    role: str
    customer_id: str | None
    org_id: str


class ChangePasswordBody(BaseModel):
    current_password: str
    new_password: str


def _create_token(user: User) -> str:
    payload = {
        "sub": str(user.id),
        "type": "user",
        "role": user.role.value,
        "customer_id": str(user.customer_id) if user.customer_id else None,
        "org_id": str(user.org_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=_TOKEN_HOURS),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


async def _get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            credentials.credentials, settings.secret_key, algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "user":
        raise HTTPException(status_code=401, detail="Invalid token type")

    try:
        user_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Malformed token")

    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


CurrentUser = Annotated[User, Depends(_get_current_user)]


def require_role(*roles: UserRole):
    """Dependency factory — enforces the given role set."""
    async def _check(user: CurrentUser) -> User:
        if roles and user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return _check


require_super_admin = require_role(UserRole.super_admin)
require_customer_or_admin = require_role(UserRole.super_admin, UserRole.customer)


@router.post("/login", response_model=TokenOut)
async def login(
    body: LoginBody,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenOut:
    result = await db.execute(
        select(User).where(User.email == body.email.lower().strip())
    )
    user = result.scalar_one_or_none()

    _bad = HTTPException(status_code=401, detail="Invalid email or password")
    if not user or not user.is_active:
        raise _bad
    if not verify_password(body.password, user.password_hash, user.password_salt):
        raise _bad

    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()
    return TokenOut(token=_create_token(user))


@router.get("/me", response_model=MeOut)
async def get_me(user: CurrentUser) -> MeOut:
    return MeOut(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role.value,
        customer_id=str(user.customer_id) if user.customer_id else None,
        org_id=str(user.org_id),
    )


@router.put("/me/password", status_code=204)
async def change_password(
    body: ChangePasswordBody,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    if not verify_password(body.current_password, user.password_hash, user.password_salt):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    user.password_hash, user.password_salt = hash_password(body.new_password)
    await db.commit()
