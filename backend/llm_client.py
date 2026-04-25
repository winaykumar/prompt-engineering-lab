"""
Prompt Engineering Lab — LLM Client
Unified client that works with Ollama (local), EC2 (remote), or OpenAI API.
"""
import os
import time
from openai import OpenAI

# ═══ CONFIGURATION (override via .env or environment variables) ═══
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")  # "ollama" | "ec2" | "openai"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
EC2_URL = os.getenv("EC2_URL", "http://localhost:11434/v1")  # Change to your EC2 IP
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.1:8b")


def _get_client() -> OpenAI:
    """Create OpenAI-compatible client for the configured backend."""
    if LLM_BACKEND == "openai":
        return OpenAI(api_key=OPENAI_API_KEY)
    elif LLM_BACKEND == "ec2":
        return OpenAI(base_url=EC2_URL, api_key="ollama")
    else:  # ollama (default)
        return OpenAI(base_url=OLLAMA_URL, api_key="ollama")


def chat(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.0,
    max_tokens: int = 1000,
) -> dict:
    """
    Send a chat completion and return response + metadata.
    Returns: {"text": str, "model": str, "tokens": int, "latency_ms": int}
    """
    client = _get_client()
    model = model or DEFAULT_MODEL
    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    latency_ms = int((time.time() - start) * 1000)
    text = response.choices[0].message.content.strip()
    tokens = response.usage.total_tokens if response.usage else 0

    return {
        "text": text,
        "model": model,
        "tokens": tokens,
        "latency_ms": latency_ms,
        "backend": LLM_BACKEND,
    }

