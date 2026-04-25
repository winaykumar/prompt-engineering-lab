"""
Prompt Engineering Lab — Shared Configuration
Edit the settings below to switch between Ollama, OpenAI, or EC2.
"""
from openai import OpenAI

# ═══ CONFIGURATION ═══

# Option A: Ollama (local, free) — DEFAULT
BASE_URL = "http://localhost:11434/v1"
API_KEY  = "ollama"      # Ollama doesn't need a real key
MODEL    = "llama3.1:8b"

# Option B: OpenAI (cloud, paid)
# BASE_URL = "https://api.openai.com/v1"
# API_KEY  = "sk-..."   # your OpenAI key
# MODEL    = "gpt-4o-mini"

# Option C: EC2 with Ollama (remote GPU)
# BASE_URL = "http://YOUR-EC2-IP:11434/v1"
# API_KEY  = "ollama"
# MODEL    = "llama3.1:8b"


def get_client() -> OpenAI:
    """Create an OpenAI-compatible client pointing to the configured endpoint."""
    return OpenAI(base_url=BASE_URL, api_key=API_KEY)


def chat(messages: list, temperature: float = 0.0, max_tokens: int = 500) -> str:
    """Send a chat completion request and return the response text."""
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
