"""Short-TTL Redis cache for expensive, read-mostly composite endpoints
(dashboard, scope-creep) — these are rebuilt from ~10+ sequential DB round
trips against a remote Supabase pooler, so repeat page views within a short
window are served from cache instead of re-paying that latency.

Not a general-purpose cache: keys are per-project, per-view, and expected to
be invalidated explicitly wherever the underlying data actually changes
(Jira sync, project edits) — the TTL is a correctness backstop for the async
recompute jobs that lag a sync, not the primary invalidation mechanism.
"""
import json
import uuid

from fastapi.encoders import jsonable_encoder

from app.redis import get_redis

_DEFAULT_TTL_SECONDS = 45


def _key(view: str, project_id: uuid.UUID) -> str:
    return f"cache:{view}:{project_id}"


async def get_cached(view: str, project_id: uuid.UUID) -> dict | None:
    redis = await get_redis()
    raw = await redis.get(_key(view, project_id))
    return json.loads(raw) if raw is not None else None


async def set_cached(view: str, project_id: uuid.UUID, payload: dict, ttl: int = _DEFAULT_TTL_SECONDS) -> None:
    redis = await get_redis()
    await redis.set(_key(view, project_id), json.dumps(jsonable_encoder(payload)), ex=ttl)


async def invalidate_project_views(project_id: uuid.UUID) -> None:
    """Call whenever a project's underlying delivery/config data changes
    (Jira sync completing, project fields edited) — clears every cached
    view for that project rather than tracking view names at call sites."""
    redis = await get_redis()
    await redis.delete(_key("dashboard", project_id), _key("scope-creep", project_id))
