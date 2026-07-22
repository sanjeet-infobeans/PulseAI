import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.database import engine, get_db
import app.models  # noqa: F401  ensure models are registered
from app.queue import close_arq_pool
from app.redis import close_redis, get_redis
from app.routers import (
    analysis, auth, chat, confidence, connectors, customers, dashboard, decisions, dependencies,
    documents, portfolio, prediction, projects, resources, sentiment, simulation,
)
from app.seed_data import seed_data

logger = logging.getLogger(__name__)


def _run_alembic() -> None:
    """Run migrations synchronously (called from a thread executor)."""
    from alembic.config import Config as AlembicConfig
    from alembic import command as alembic_cmd

    ini = Path(__file__).parent.parent / "alembic.ini"
    cfg = AlembicConfig(str(ini))
    alembic_cmd.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _run_alembic)
    await seed_data()
    yield
    await engine.dispose()
    await close_redis()
    await close_arq_pool()


app = FastAPI(
    title="PulseAI",
    description="AI-powered project delivery intelligence.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(projects.router)
app.include_router(connectors.router)
app.include_router(analysis.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(confidence.router)
app.include_router(dashboard.router)
app.include_router(resources.router)
app.include_router(dependencies.router)
app.include_router(decisions.router)
app.include_router(prediction.router)
app.include_router(sentiment.router)
app.include_router(simulation.router)
app.include_router(portfolio.router)


@app.get("/healthz", tags=["health"])
async def health() -> JSONResponse:
    checks: dict[str, str] = {}

    try:
        async for db in get_db():
            await db.execute(text("SELECT 1"))
            checks["db"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["db"] = f"error: {exc}"

    try:
        redis = await get_redis()
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["redis"] = f"error: {exc}"

    ok = all(v == "ok" for v in checks.values())
    return JSONResponse(
        {"status": "ok" if ok else "degraded", **checks},
        status_code=200 if ok else 503,
    )
