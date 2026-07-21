"""First-boot bootstrap: InfoBeans org + super admin, plus an optional demo
customer/project so the happy path is immediately demoable. Idempotent."""
import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.customer import Customer
from app.models.organization import Organization
from app.models.project import Project, ProjectStatus
from app.models.user import User, UserRole
from app.security import hash_password

logger = logging.getLogger(__name__)


async def seed_data() -> None:
    async with AsyncSessionLocal() as db:
        existing = (await db.execute(select(Organization).limit(1))).scalar_one_or_none()
        if existing:
            return

        org = Organization(name="InfoBeans", slug="infobeans")
        db.add(org)
        await db.flush()

        pw_hash, pw_salt = hash_password(settings.super_admin_password)
        admin = User(
            org_id=org.id,
            email=settings.super_admin_email.lower(),
            name="Super Admin",
            password_hash=pw_hash,
            password_salt=pw_salt,
            role=UserRole.super_admin,
        )
        db.add(admin)
        await db.flush()

        if settings.seed_demo_data:
            customer = Customer(
                org_id=org.id,
                name="Acme Corporation",
                slug="acme",
                contact_email="delivery@acme.example",
                industry="Retail",
                created_by=admin.id,
            )
            db.add(customer)
            await db.flush()

            project = Project(
                customer_id=customer.id,
                name="Project Atlas",
                key="ATLAS",
                description="Platform migration and checkout modernization.",
                status=ProjectStatus.active,
                created_by=admin.id,
            )
            db.add(project)
            await db.flush()

            # Customer-role user scoped to this customer (demo customer login)
            cust_hash, cust_salt = hash_password("changeme-customer")
            db.add(User(
                org_id=org.id,
                customer_id=customer.id,
                email="customer@acme.example",
                name="Acme Delivery Lead",
                password_hash=cust_hash,
                password_salt=cust_salt,
                role=UserRole.customer,
            ))

            from app.seed_simulated import seed_simulated_for_project
            from app.seed_demo_delivery import seed_demo_delivery
            await seed_simulated_for_project(db, project.id)
            await seed_demo_delivery(db, project.id)

        try:
            await db.commit()
            logger.info(
                "Seeded org 'InfoBeans' + super admin <%s>%s",
                settings.super_admin_email,
                " + demo customer/project" if settings.seed_demo_data else "",
            )
        except IntegrityError:
            await db.rollback()
            logger.info("Data already seeded by another worker — skipping")
