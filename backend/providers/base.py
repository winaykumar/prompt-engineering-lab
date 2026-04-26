"""
Prompt Engineering Lab — Abstract LLM Provider
All providers must implement this interface.
"""
from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Base class for all LLM backend providers."""

    # Human-readable name, used in API responses
    name: str = "base"

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> dict:
        """
        Send a chat completion and return a normalized response.

        Args:
            messages:    List of {"role": str, "content": str} dicts
            model:       Model identifier (e.g. "llama3.1:8b", "gpt-4o-mini")
            temperature: Sampling temperature (0.0 = deterministic)
            max_tokens:  Maximum tokens in the response

        Returns:
            {
                "text":       str,   # Response text
                "model":      str,   # Model used
                "tokens":     int,   # Total tokens (0 if unavailable)
                "latency_ms": int,   # Round-trip time in milliseconds
                "backend":    str,   # Provider name
            }
        """
        ...

