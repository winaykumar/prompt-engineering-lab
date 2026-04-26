"""
Prompt Engineering Lab — Ollama Provider (local)
Connects to a locally running Ollama instance via its OpenAI-compatible API.

Required .env:
    OLLAMA_URL=http://localhost:11434/v1   (default, usually no change needed)
"""
import os
import time
from openai import OpenAI
from backend.providers.base import BaseLLMProvider

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")


class OllamaProvider(BaseLLMProvider):
    name = "ollama"

    def __init__(self):
        self._client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")

    def chat(self, messages, model, temperature=0.0, max_tokens=1000):
        start = time.time()
        response = self._client.chat.completions.create(
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
            "backend": self.name,
        }

