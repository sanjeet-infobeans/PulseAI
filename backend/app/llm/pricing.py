"""Groq + Gemini pricing (USD per 1M tokens), longest-prefix match. Groq table
ported from AIMS; Gemini entries are approximate paid-tier list prices —
adjust if Google repricing drifts."""
from dataclasses import dataclass


@dataclass(frozen=True)
class _Price:
    input_per_1m: float
    output_per_1m: float


_TABLE: dict[str, _Price] = {
    "llama-3.3-70b": _Price(0.59, 0.79),
    "llama-3.1-8b": _Price(0.05, 0.08),
    "llama-3.1-70b": _Price(0.59, 0.79),
    "openai/gpt-oss-120b": _Price(0.15, 0.75),
    "openai/gpt-oss-20b": _Price(0.10, 0.50),
    "qwen/qwen3-32b": _Price(0.29, 0.59),
    "gemma2-9b": _Price(0.20, 0.20),
    "gemini-2.0-flash": _Price(0.10, 0.40),
    "gemini-1.5-flash": _Price(0.075, 0.30),
}


def _bare(model: str) -> str:
    """Strip the LiteLLM provider prefix: 'groq/llama-3.3-70b-versatile' → 'llama-3.3-70b-versatile'."""
    return model.split("/", 1)[1] if "/" in model else model


def calculate_cost(model: str, input_tokens: int | None, output_tokens: int | None) -> float:
    bare = _bare(model).lower()
    best: _Price | None = None
    best_len = 0
    for prefix, price in _TABLE.items():
        if bare.startswith(prefix) and len(prefix) > best_len:
            best, best_len = price, len(prefix)
    if best is None:
        return 0.0
    in_cost = ((input_tokens or 0) / 1_000_000) * best.input_per_1m
    out_cost = ((output_tokens or 0) / 1_000_000) * best.output_per_1m
    return round(in_cost + out_cost, 8)
