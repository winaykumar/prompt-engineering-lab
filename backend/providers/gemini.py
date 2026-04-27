"""
Prompt Engineering Lab — Google Gemini Provider
Connects to Google's Generative Language API via direct REST.

Required .env:
    GEMINI_API_KEY=AIza...

Optional .env:
    GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta  (default)

How to get a key:
    1. Go to https://aistudio.google.com/app/apikey
    2. Click "Create API key" and copy it
    3. Paste it into your .env as GEMINI_API_KEY
"""
import json
import os
import time
import urllib.error
import urllib.request

from backend.providers.base import BaseLLMProvider

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL = os.getenv(
    "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
)


class GeminiProvider(BaseLLMProvider):
    name = "Gemini (API)"

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required when LLM_BACKEND=gemini. "
                "Get one at https://aistudio.google.com/app/apikey"
            )

    # ── public API ──────────────────────────────────────────────

    def chat(self, messages, model, temperature=0.0, max_tokens=1000):
        model_name = self._normalize_model(model)
        payload = self._build_payload(messages, temperature, max_tokens)
        body = json.dumps(payload).encode("utf-8")
        url = f"{GEMINI_BASE_URL}/models/{model_name}:generateContent"

        req = urllib.request.Request(
            url=url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY,
            },
        )

        start = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            raise ValueError(f"Gemini API error {e.code}: {err_body}") from e

        latency_ms = int((time.time() - start) * 1000)

        # Extract text from response
        candidates = data.get("candidates") or []
        parts = []
        if candidates:
            parts = (candidates[0].get("content") or {}).get("parts") or []
        text = "".join(p.get("text", "") for p in parts).strip()

        # Extract token usage
        usage = data.get("usageMetadata") or {}
        total = usage.get("totalTokenCount")
        tokens = int(total) if isinstance(total, (int, float)) else 0

        return {
            "text": text,
            "model": model_name,
            "tokens": tokens,
            "latency_ms": latency_ms,
            "backend": self.name,
        }

    # ── helpers ─────────────────────────────────────────────────

    @staticmethod
    def _normalize_model(model: str) -> str:
        """Strip 'models/' prefix if present."""
        return model.split("models/", 1)[1] if model.startswith("models/") else model

    @staticmethod
    def _build_payload(messages: list[dict], temperature: float, max_tokens: int) -> dict:
        """Convert OpenAI-style messages to Gemini generateContent format."""
        contents: list[dict] = []
        system_parts: list[dict] = []

        for msg in messages:
            role = msg.get("role", "user")
            content = str(msg.get("content", ""))
            if not content.strip():
                continue

            if role == "system":
                system_parts.append({"text": content})
            elif role == "assistant":
                contents.append({"role": "model", "parts": [{"text": content}]})
            else:
                contents.append({"role": "user", "parts": [{"text": content}]})

        payload: dict = {
            "contents": contents or [{"role": "user", "parts": [{"text": ""}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        if system_parts:
            payload["systemInstruction"] = {"parts": system_parts}

        return payload

