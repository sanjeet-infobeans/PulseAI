from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Supabase's pooler caps this project to 15 concurrent connections in
# session mode — pool_size/max_overflow here (and uvicorn's single worker,
# and WorkerSettings.max_jobs) are all sized to stay well under that shared
# budget across the api and worker containers combined.
engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=4,
    max_overflow=2,
    pool_pre_ping=True,
    pool_recycle=3600,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
