import re
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.customer import Customer
from app.models.user import User, UserRole
from app.routers.auth import CurrentUser, require_super_admin

router = APIRouter(prefix="/customers", tags=["customers"])


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "customer"


class CustomerIn(BaseModel):
    name: str
    contact_email: str | None = None
    industry: str | None = None


class CustomerOut(BaseModel):
    id: str
    name: str
    slug: str
    contact_email: str | None
    industry: str | None
    is_active: bool

    @classmethod
    def of(cls, c: Customer) -> "CustomerOut":
        return cls(
            id=str(c.id),
            name=c.name,
            slug=c.slug,
            contact_email=c.contact_email,
            industry=c.industry,
            is_active=c.is_active,
        )


def _scope(user: User, stmt):
    """Customers see only their own customer; super admins see all."""
    if user.role == UserRole.customer and user.customer_id:
        return stmt.where(Customer.id == user.customer_id)
    return stmt


@router.get("", response_model=list[CustomerOut])
async def list_customers(
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[CustomerOut]:
    stmt = _scope(user, select(Customer).order_by(Customer.created_at.desc()))
    rows = (await db.execute(stmt)).scalars().all()
    return [CustomerOut.of(c) for c in rows]


@router.get("/{customer_id}", response_model=CustomerOut)
async def get_customer(
    customer_id: uuid.UUID,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CustomerOut:
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if user.role == UserRole.customer and user.customer_id != customer.id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return CustomerOut.of(customer)


@router.post("", response_model=CustomerOut, status_code=201)
async def create_customer(
    body: CustomerIn,
    user: Annotated[User, Depends(require_super_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CustomerOut:
    customer = Customer(
        org_id=user.org_id,
        name=body.name.strip(),
        slug=_slugify(body.name),
        contact_email=body.contact_email,
        industry=body.industry,
        created_by=user.id,
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return CustomerOut.of(customer)
