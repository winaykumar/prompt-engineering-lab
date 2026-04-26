"""
Prompt Engineering Lab — Shared Configuration for CLI Scripts
Delegates to the same provider system used by the web app.
Configure via .env or environment variables.
"""
import os

# Load .env if python-dotenv is available (same as web app)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from backend.llm_client import chat as _llm_chat

# ═══ CONFIGURATION (read from .env) ═══
MODEL = os.getenv("DEFAULT_MODEL", "llama3.1:8b")


def get_client():
    """Legacy compatibility — not needed with provider architecture."""
    raise NotImplementedError(
        "get_client() is deprecated. Use chat() instead, which delegates "
        "to the configured provider via LLM_BACKEND in .env."
    )


def chat(messages: list, temperature: float = 0.0, max_tokens: int = 500) -> str:
    """Send a chat completion request and return the response text."""
    result = _llm_chat(
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return result["text"]
