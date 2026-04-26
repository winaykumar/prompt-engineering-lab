"""
Prompt Engineering Lab — Provider Registry
Auto-discovers all provider classes and exposes get_provider().
"""
from backend.providers.base import BaseLLMProvider
from backend.providers.ollama import OllamaProvider
from backend.providers.ec2 import EC2Provider
from backend.providers.openai_provider import OpenAIProvider
from backend.providers.gemini import GeminiProvider

# ═══ REGISTRY ═══
_PROVIDERS: dict[str, type[BaseLLMProvider]] = {
    "ollama": OllamaProvider,
    "ec2": EC2Provider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
}

# Cache instantiated providers
_INSTANCES: dict[str, BaseLLMProvider] = {}


def get_provider(name: str) -> BaseLLMProvider:
    """Return a cached provider instance by name."""
    if name not in _INSTANCES:
        cls = _PROVIDERS.get(name)
        if not cls:
            available = ", ".join(sorted(_PROVIDERS.keys()))
            raise ValueError(
                f"Unknown LLM backend: '{name}'. Available: {available}"
            )
        _INSTANCES[name] = cls()
    return _INSTANCES[name]


def list_providers() -> list[str]:
    """Return list of available provider names."""
    return sorted(_PROVIDERS.keys())

