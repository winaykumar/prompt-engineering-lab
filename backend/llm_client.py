"""
Prompt Engineering Lab — LLM Client
Thin dispatcher that delegates to the configured provider.
Provider implementations live in backend/providers/.
"""
import os
from backend.providers import get_provider

# ═══ CONFIGURATION ═══
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.1:8b")


def chat(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.0,
    max_tokens: int = 1000,
) -> dict:
    """
    Send a chat completion via the configured provider.

    Returns:
        {"text": str, "model": str, "tokens": int, "latency_ms": int, "backend": str}
    """
    provider = get_provider(LLM_BACKEND)
    return provider.chat(
        messages=messages,
        model=model or DEFAULT_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
    )
