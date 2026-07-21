"""Groq-via-LiteLLM call layer. Ported in shape from AIMS litellm_backend.

Exposes two helpers used by services (not a proxy):
  - complete(): non-streaming, returns (text, usage)
  - stream():   async iterator of text deltas, logs cost in finally
Every call is metered into llm_call_logs.
"""
import logging
import time
import uuid
from typing import AsyncIterator

import litellm
from fastapi import HTTPException

from app.config import settings
from app.database import AsyncSessionLocal
from app.llm.pricing import calculate_cost
from app.models.llm_call_log import LLMCallLog, LLMFeature

logger = logging.getLogger(__name__)
litellm.suppress_debug_info = True


def _api_key() -> str:
    if not settings.groq_api_key:
        raise HTTPException(status_code=503, detail="Groq API key is not configured on this server")
    return settings.groq_api_key


async def _log(
    *, feature: LLMFeature, model: str, project_id: uuid.UUID | None,
    input_tokens: int | None, output_tokens: int | None, status_code: int, start: float,
) -> None:
    try:
        async with AsyncSessionLocal() as db:
            db.add(LLMCallLog(
                project_id=project_id, feature=feature, model=model,
                input_tokens=input_tokens or 0, output_tokens=output_tokens or 0,
                cost_usd=calculate_cost(model, input_tokens, output_tokens),
                status_code=status_code, duration_ms=int((time.monotonic() - start) * 1000),
            ))
            await db.commit()
    except Exception:  # noqa: BLE001 — logging must never break the request
        logger.exception("Failed to write llm_call_log")


def _map_error(exc: Exception) -> HTTPException:
    if isinstance(exc, litellm.exceptions.AuthenticationError):
        return HTTPException(status_code=502, detail="LLM auth error — check GROQ_API_KEY")
    if isinstance(exc, litellm.exceptions.RateLimitError):
        return HTTPException(status_code=429, detail="LLM rate limit — retry shortly")
    if isinstance(exc, litellm.exceptions.BadRequestError):
        return HTTPException(status_code=400, detail=str(exc))
    logger.exception("LiteLLM call failed")
    return HTTPException(status_code=502, detail=f"LLM upstream error: {exc}")


async def complete(
    *,
    feature: LLMFeature,
    messages: list[dict],
    model: str,
    project_id: uuid.UUID | None = None,
    max_tokens: int | None = None,
    temperature: float = 0.3,
    json_mode: bool = False,
) -> str:
    start = time.monotonic()
    kwargs: dict = {
        "model": model,
        "messages": messages,
        "api_key": _api_key(),
        "temperature": temperature,
        "max_tokens": max_tokens or settings.llm_max_tokens,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    try:
        resp = await litellm.acompletion(**kwargs)
    except Exception as exc:  # noqa: BLE001
        await _log(feature=feature, model=model, project_id=project_id,
                   input_tokens=None, output_tokens=None, status_code=502, start=start)
        raise _map_error(exc)

    usage = resp.usage
    await _log(
        feature=feature, model=model, project_id=project_id,
        input_tokens=usage.prompt_tokens if usage else None,
        output_tokens=usage.completion_tokens if usage else None,
        status_code=200, start=start,
    )
    return resp.choices[0].message.content or ""


async def stream(
    *,
    feature: LLMFeature,
    messages: list[dict],
    model: str,
    project_id: uuid.UUID | None = None,
    max_tokens: int | None = None,
    temperature: float = 0.4,
) -> AsyncIterator[str]:
    """Yield text deltas. Router wraps them as SSE events; cost logged on close."""
    start = time.monotonic()
    input_tokens: int | None = None
    output_tokens: int | None = None
    try:
        resp = await litellm.acompletion(
            model=model, messages=messages, api_key=_api_key(),
            temperature=temperature, max_tokens=max_tokens or settings.llm_max_tokens,
            stream=True, stream_options={"include_usage": True},
        )
    except Exception as exc:  # noqa: BLE001
        await _log(feature=feature, model=model, project_id=project_id,
                   input_tokens=None, output_tokens=None, status_code=502, start=start)
        raise _map_error(exc)

    try:
        async for chunk in resp:
            if getattr(chunk, "usage", None):
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield delta
    finally:
        await _log(feature=feature, model=model, project_id=project_id,
                   input_tokens=input_tokens, output_tokens=output_tokens,
                   status_code=200, start=start)
