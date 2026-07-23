"""Groq + Gemini via LiteLLM call layer, with multi-key fallback. Ported in
shape from AIMS litellm_backend.

Exposes two helpers used by services (not a proxy):
  - complete(): non-streaming, returns text
  - stream():   async iterator of text deltas, logs cost in finally

Golden rule: a single dead key must never fail a request while any other
configured key could have served it. Every configured key (up to 4 Groq + 4
Gemini) is tried in turn — own provider first, then the other provider's
fallback model — before a call is allowed to raise. Every call is metered
into llm_call_logs.
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


def _dedupe(keys: list[str | None]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for k in keys:
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out


def _groq_keys() -> list[str]:
    return _dedupe([*settings.groq_api_keys, settings.groq_api_key])


def _gemini_keys() -> list[str]:
    return _dedupe([*settings.gemini_api_keys, settings.gemini_api_key])


def _candidates(model: str) -> list[tuple[str, str]]:
    """(model, api_key) pairs to try in order: every key configured for the
    requested model's own provider, then every key for the other provider
    (using its configured fallback model). A request only gives up once
    every configured key across both providers has been tried."""
    provider = model.split("/", 1)[0] if "/" in model else ""
    groq_keys, gemini_keys = _groq_keys(), _gemini_keys()

    if provider == "gemini":
        own_candidates = [(model, k) for k in gemini_keys]
        fallback_candidates = [(settings.llm_model_groq_fallback, k) for k in groq_keys]
    else:
        own_candidates = [(model, k) for k in groq_keys]
        fallback_candidates = [(settings.llm_model_gemini_fallback, k) for k in gemini_keys]

    return own_candidates + fallback_candidates


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
    candidates = _candidates(model)
    if not candidates:
        await _log(feature=feature, model=model, project_id=project_id,
                   input_tokens=None, output_tokens=None, status_code=503, start=start)
        raise HTTPException(status_code=503, detail="No LLM API keys configured (GROQ_API_KEYS / GEMINI_API_KEYS)")

    last_exc: Exception | None = None
    for attempt_model, api_key in candidates:
        kwargs: dict = {
            "model": attempt_model,
            "messages": messages,
            "api_key": api_key,
            "temperature": temperature,
            "max_tokens": max_tokens or settings.llm_max_tokens,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        try:
            resp = await litellm.acompletion(**kwargs)
        except Exception as exc:  # noqa: BLE001 — this key/provider is down, try the next one
            last_exc = exc
            logger.warning("LLM call failed on %s (key ...%s): %s — trying next key",
                           attempt_model, api_key[-4:], exc)
            continue

        usage = resp.usage
        await _log(
            feature=feature, model=attempt_model, project_id=project_id,
            input_tokens=usage.prompt_tokens if usage else None,
            output_tokens=usage.completion_tokens if usage else None,
            status_code=200, start=start,
        )
        return resp.choices[0].message.content or ""

    await _log(feature=feature, model=model, project_id=project_id,
               input_tokens=None, output_tokens=None, status_code=502, start=start)
    raise _map_error(last_exc)


async def stream(
    *,
    feature: LLMFeature,
    messages: list[dict],
    model: str,
    project_id: uuid.UUID | None = None,
    max_tokens: int | None = None,
    temperature: float = 0.4,
) -> AsyncIterator[str]:
    """Yield text deltas. Router wraps them as SSE events; cost logged on close.

    Key/provider fallback applies to opening the stream — every configured
    key is tried until one starts successfully. Once the first chunk has
    been yielded to the caller, a fallback would duplicate output already
    sent, so a failure past that point just propagates.
    """
    start = time.monotonic()
    candidates = _candidates(model)
    if not candidates:
        await _log(feature=feature, model=model, project_id=project_id,
                   input_tokens=None, output_tokens=None, status_code=503, start=start)
        raise HTTPException(status_code=503, detail="No LLM API keys configured (GROQ_API_KEYS / GEMINI_API_KEYS)")

    resp = None
    attempt_model = model
    last_exc: Exception | None = None
    for attempt_model, api_key in candidates:
        try:
            resp = await litellm.acompletion(
                model=attempt_model, messages=messages, api_key=api_key,
                temperature=temperature, max_tokens=max_tokens or settings.llm_max_tokens,
                stream=True, stream_options={"include_usage": True},
            )
            break
        except Exception as exc:  # noqa: BLE001 — this key/provider is down, try the next one
            last_exc = exc
            logger.warning("LLM stream open failed on %s (key ...%s): %s — trying next key",
                           attempt_model, api_key[-4:], exc)
            continue

    if resp is None:
        await _log(feature=feature, model=model, project_id=project_id,
                   input_tokens=None, output_tokens=None, status_code=502, start=start)
        raise _map_error(last_exc)

    input_tokens: int | None = None
    output_tokens: int | None = None
    try:
        async for chunk in resp:
            if getattr(chunk, "usage", None):
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield delta
    finally:
        await _log(feature=feature, model=attempt_model, project_id=project_id,
                   input_tokens=input_tokens, output_tokens=output_tokens,
                   status_code=200, start=start)
