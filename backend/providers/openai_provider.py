"""
Prompt Engineering Lab — OpenAI Provider
Connects to OpenAI's hosted API (GPT-4o, GPT-4o-mini, etc.).

Required .env:
    OPENAI_API_KEY=sk-proj-...
"""
import os
import time
from openai import OpenAI
from backend.providers.base import BaseLLMProvider

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class OpenAIProvider(BaseLLMProvider):
    name = "openai"

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_BACKEND=openai. "
                "Get one at https://platform.openai.com/api-keys"
            )
        self._client = OpenAI(api_key=OPENAI_API_KEY)

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

