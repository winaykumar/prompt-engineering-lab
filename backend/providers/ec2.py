"""
Prompt Engineering Lab — EC2 Provider (remote Ollama)
Connects to Ollama running on a remote EC2 GPU instance.

Required .env:
    EC2_URL=http://<EC2_PUBLIC_IP>:11434/v1
"""
import os
import time
from openai import OpenAI
from backend.providers.base import BaseLLMProvider

EC2_URL = os.getenv("EC2_URL", "http://localhost:11434/v1")


class EC2Provider(BaseLLMProvider):
    name = "ec2"

    def __init__(self):
        self._client = OpenAI(base_url=EC2_URL, api_key="ollama")

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

