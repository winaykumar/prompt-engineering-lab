# 🧪 Prompt Engineering Lab
Interactive web app for experimenting with prompt engineering techniques.  
Edit prompts, tweak parameters, run against real LLMs, see results instantly.
---
## Experiments
| # | Technique | What You Learn |
|---|-----------|---------------|
| 01 | Zero-Shot vs Few-Shot | How examples constrain output |
| 02 | Temperature | Randomness vs determinism |
| 03 | Chain-of-Thought | Step-by-step reasoning |
| 04 | Structured Output | JSON extraction + validation |
| 05 | System Prompts | Personas & behaviour control |
| 06 | Self-Critique | Generate → Critique → Revise |
| 07 | Prompt Injection | Attack & defence patterns |
---
## Prerequisites
- **Python 3.11+**
- **An LLM backend** — Ollama (local, free), OpenAI API, or a remote EC2 instance. See [LLM Runtime Options](#llm-runtime-options) below.

---
## Clone the Repo
> Skip this if you've already cloned the repo.
```bash
git clone https://github.com/winaykumar/prompt-engineering-lab.git
cd prompt-engineering-lab
```

---
## Setup Python Environment
> Start here if you already have the repo cloned.
```bash
# 1. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment config
cp .env.example .env
# Edit .env if you want to change backend (default: Ollama)
```
---
## Usage
### Start Ollama
```bash
# Start the Ollama server (runs on http://localhost:11434 by default)
ollama serve

# If it's already running you'll see: "Error: listen tcp 127.0.0.1:11434: bind: address already in use"
# That's fine — just proceed to start the Lab server.

# Check whether Ollama is already running
curl -s http://localhost:11434 && echo "Ollama is running"

# Pull the default model (only needed once)
ollama pull llama3.1:8b
```

### Stop Ollama
```bash
# Option 1 — graceful stop (systemd-managed installs)
sudo systemctl stop ollama

# Option 2 — find and kill the process manually
pkill -f "ollama serve"
# or:
kill $(pgrep -f "ollama serve")

# Verify it has stopped
curl -s http://localhost:11434 || echo "Ollama is not running"
```

### Start the Lab
```bash
# Terminal 1 — Start Ollama (if not already running)
ollama serve
# Terminal 2 — Start the Lab server
uvicorn backend.main:app --reload --port 8000
```
### Open in Browser
```text
http://localhost:8000           # Overview — all 7 experiments
http://localhost:8000/lab/01    # Experiment 01 — Zero-Shot vs Few-Shot
http://localhost:8000/lab/02    # Experiment 02 — Temperature
...
http://localhost:8000/lab/07    # Experiment 07 — Prompt Injection
```
### How to Use Each Experiment
1. **Read** the experiment description and technique explanation
2. **Edit** the pre-filled prompts — change system/user messages, add/remove messages
3. **Adjust** temperature and max tokens
4. **Click ▶ Run** — sends the prompt to your LLM backend
5. **See** the response with latency (ms), token count, and model info
6. **Compare** variants side by side (e.g., Zero-Shot vs Few-Shot)
### Running Standalone Scripts (No Web UI)
The original CLI scripts still work independently:
```bash
python 01_zero_few_shot.py
python 02_temperature.py
python 03_chain_of_thought.py
python 04_structured_output.py
python 05_system_prompts.py
python 06_self_critique.py
python 07_prompt_injection.py
```
> These use `config.py` directly. Edit `BASE_URL`, `API_KEY`, and `MODEL` in `config.py` for CLI scripts.
---
## LLM Runtime Options

Three backends are supported. Pick whichever suits your situation — Ollama is the default and requires no account or API key.

Recommended starter models: local `llama3.1:8b` or `mistral:7b`; API `gpt-4o-mini`; EC2 `qwen2.5:14b` (if you need a larger model).

| Backend | Cost | Best For |
|---------|------|----------|
| **Ollama** (default) | $0 | Learning, daily experiments on your own machine |
| **OpenAI API** | Pay-per-token | GPT-4o / GPT-4o-mini, no local GPU needed |
| **EC2 (remote Ollama)** | ~$0.50–$1/hr (GPU) | Larger models (13B+), shareable with teammates |

---

### 🖥️ Option 1 — Ollama (Local)

Run models 100% locally — no account, no cost, no data leaves your machine.

#### Install
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama
```

#### Pull a Model (Only Once)
```bash
ollama pull llama3.1:8b          # default model (~4.7 GB)
ollama pull llama3.1:70b         # larger, needs ≥40 GB RAM
ollama pull mistral:7b           # alternative lightweight model
```

#### Start / Stop
```bash
# Start
ollama serve

# Check it's running
curl -s http://localhost:11434 && echo "Ollama is running"

# Stop — graceful (systemd)
sudo systemctl stop ollama

# Stop — manual
pkill -f "ollama serve"
```

#### Configure in `.env`
```env
LLM_BACKEND=ollama
OLLAMA_URL=http://localhost:11434/v1
DEFAULT_MODEL=llama3.1:8b
```

---

### 🔑 Option 2 — OpenAI API Keys

Use OpenAI's hosted models (for example: `gpt-4o-mini`, `gpt-4o`, `gpt-4.1-mini`, `gpt-4.1`) — requires an account and billing setup.

#### Step 1 — Create an OpenAI Account
1. Go to [platform.openai.com](https://platform.openai.com) and sign up.
2. Navigate to **Settings → Billing** and add a payment method.
3. Set a **usage limit** (recommended: $5–$10/month for learning) under **Settings → Limits**.

#### Step 2 — Generate an API Key
1. Go to **API Keys** → [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Click **Create new secret key**, give it a name (e.g. `prompt-lab`), and copy it immediately — it won't be shown again.

#### Step 3 — Configure in `.env`
```env
LLM_BACKEND=openai
OPENAI_API_KEY=sk-proj-...        # paste your key here
DEFAULT_MODEL=gpt-4o-mini         # cheapest capable model
# DEFAULT_MODEL=gpt-4o            # best quality, higher cost
```

#### Recommended Models and Approximate Cost
| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| `gpt-4o-mini` | $0.15 / 1M tokens | $0.60 / 1M tokens | Best value for experiments |
| `gpt-4o` | $2.50 / 1M tokens | $10.00 / 1M tokens | Best quality |
| `gpt-4.1-mini` | varies by region/account | varies by region/account | Good coding + instruction-following option |
| `gpt-4.1` | varies by region/account | varies by region/account | Higher quality alternative for complex tasks |

For quick swapping, just change `DEFAULT_MODEL` in `.env` to any model your OpenAI account has access to.

> ⚠️ **Never commit your `.env` to git.** The `.gitignore` already excludes it.

---

### ☁️ Option 3 — EC2 Deployment (Remote Ollama)

Run Ollama on an AWS GPU instance — useful for larger models or when you want a shared endpoint.

#### Recommended Instance Types
| Instance | GPU | RAM | Fits Models | On-Demand Cost |
|----------|-----|-----|-------------|---------------|
| `g4dn.xlarge` | T4 (16 GB) | 16 GB | up to 13B | ~$0.53/hr |
| `g4dn.2xlarge` | T4 (16 GB) | 32 GB | up to 13B comfortably | ~$0.75/hr |
| `g5.xlarge` | A10G (24 GB) | 16 GB | up to 30B | ~$1.01/hr |

Typical model choices on EC2:

| Model | Example Ollama tag | Typical fit |
|-------|---------------------|-------------|
| Llama 3.1 8B | `llama3.1:8b` | `g4dn.xlarge` and above |
| Llama 3.1 70B | `llama3.1:70b` | Multi-GPU / high-memory setups |
| Mistral 7B | `mistral:7b` | `g4dn.xlarge` and above |
| Qwen2.5 14B | `qwen2.5:14b` | `g4dn.2xlarge` and above |

#### Step 1 — Launch an EC2 Instance
1. Open the [EC2 console](https://console.aws.amazon.com/ec2/) → **Launch Instance**.
2. Choose **Ubuntu 22.04 LTS** (or Amazon Linux 2).
3. Select instance type (e.g. `g4dn.xlarge`).
4. Under **Key pair**, create or select one (you'll need it to SSH in).
5. Under **Security group**, add an **Inbound rule**: TCP port **11434**, source = your IP (or `0.0.0.0/0` for open access — not recommended for production).
6. Launch the instance.

#### Step 2 — Install Ollama on EC2
```bash
# SSH into the instance
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull your model
ollama pull llama3.1:8b

# Examples of other models you can run
ollama pull mistral:7b
ollama pull qwen2.5:14b

# Start Ollama, binding to all interfaces so it's reachable remotely
OLLAMA_HOST=0.0.0.0 ollama serve
```

#### Step 3 — Run Ollama as a Background Service (Optional but Recommended)
```bash
# Create a systemd service
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Server
After=network.target

[Service]
ExecStart=/usr/local/bin/ollama serve
Environment=OLLAMA_HOST=0.0.0.0
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

#### Step 4 — Configure in `.env`
```env
LLM_BACKEND=ec2
EC2_URL=http://<EC2_PUBLIC_IP>:11434/v1
DEFAULT_MODEL=llama3.1:8b
```

#### Managing Your EC2 Instance

```bash
# ── Via AWS CLI ────────────────────────────────────────────────
# Start a stopped instance
aws ec2 start-instances --instance-ids i-0123456789abcdef0

# Stop (preserves disk — you can restart it later)
aws ec2 stop-instances --instance-ids i-0123456789abcdef0

# Terminate (permanently deletes instance + ephemeral storage)
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0

# Check instance state
aws ec2 describe-instances --instance-ids i-0123456789abcdef0 \
  --query 'Reservations[0].Instances[0].State.Name' --output text
```

> 💡 **Cost tip:** Always **Stop** the instance when not in use — you only pay for EBS storage (~$0.08/GB/month) while stopped, not for compute. Only **Terminate** when you're done for good.

#### Ollama Service Management on EC2
```bash
# Start / stop / restart the Ollama service on the remote instance
sudo systemctl start ollama
sudo systemctl stop ollama
sudo systemctl restart ollama

# View logs
sudo journalctl -u ollama -f
```

---

## Configuration
### Environment Variables (`.env`)
| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BACKEND` | `ollama` | Backend: `ollama`, `ec2`, `openai`, or `gemini` |
| `OLLAMA_URL` | `http://localhost:11434/v1` | Ollama API endpoint |
| `EC2_URL` | — | Remote EC2 endpoint (when `LLM_BACKEND=ec2`) |
| `OPENAI_API_KEY` | — | OpenAI API key (when `LLM_BACKEND=openai`) |
| `GEMINI_API_KEY` | — | Google Gemini API key (when `LLM_BACKEND=gemini`) |
| `GEMINI_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta` | Gemini API base URL |
| `DEFAULT_MODEL` | `llama3.1:8b` | Model to use for completions |

---
## Project Structure
```text
prompt-engineering-lab/
├── backend/
│   ├── main.py                 # FastAPI app — API routes + static serving
│   ├── llm_client.py           # Thin dispatcher → delegates to providers
│   ├── providers/
│   │   ├── __init__.py         # Provider registry + get_provider()
│   │   ├── base.py             # Abstract BaseLLMProvider class
│   │   ├── ollama.py           # Ollama (local) — OpenAI SDK
│   │   ├── ec2.py              # EC2 (remote Ollama) — OpenAI SDK
│   │   ├── openai_provider.py  # OpenAI API — OpenAI SDK
│   │   └── gemini.py           # Google Gemini — direct REST
│   └── experiments/
│       ├── __init__.py
│       └── registry.py         # All 7 experiment definitions & variants
├── frontend/
│   ├── index.html              # Lab overview page (/)
│   ├── lab.html                # Experiment runner page (/lab/{id})
│   └── style.css               # Dark theme styles
├── 01_zero_few_shot.py         # Standalone CLI script
├── 02_temperature.py           # Standalone CLI script
├── 03_chain_of_thought.py      # Standalone CLI script
├── 04_structured_output.py     # Standalone CLI script
├── 05_system_prompts.py        # Standalone CLI script
├── 06_self_critique.py         # Standalone CLI script
├── 07_prompt_injection.py      # Standalone CLI script
├── config.py                   # Shared config for CLI scripts
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/experiments` | List all experiments |
| `GET` | `/api/experiments/{id}` | Get experiment with variants |
| `POST` | `/api/run` | Run a prompt against LLM |
| `GET` | `/` | Lab overview UI |
| `GET` | `/lab/{id}` | Experiment UI |
### Example: Run a prompt via API
```bash
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What is 2+2?"}],
    "temperature": 0.0,
    "max_tokens": 100
  }'
```
---
## Adding a New Provider

The architecture is model-agnostic — adding a new LLM backend takes **one file** and **one line** in the registry.

#### Step 1 — Create a provider file
Create `backend/providers/your_provider.py`:
```python
import os
import time
from backend.providers.base import BaseLLMProvider

class YourProvider(BaseLLMProvider):
    name = "your_provider"

    def __init__(self):
        self.api_key = os.getenv("YOUR_PROVIDER_API_KEY", "")
        if not self.api_key:
            raise ValueError("YOUR_PROVIDER_API_KEY is required")

    def chat(self, messages, model, temperature=0.0, max_tokens=1000):
        start = time.time()
        # ... call your provider's API here ...
        latency_ms = int((time.time() - start) * 1000)
        return {
            "text": "response text",
            "model": model,
            "tokens": 0,
            "latency_ms": latency_ms,
            "backend": self.name,
        }
```

#### Step 2 — Register in `backend/providers/__init__.py`
```python
from backend.providers.your_provider import YourProvider

_PROVIDERS: dict[str, type[BaseLLMProvider]] = {
    # ...existing providers...
    "your_provider": YourProvider,
}
```

#### Step 3 — Configure in `.env`
```env
LLM_BACKEND=your_provider
YOUR_PROVIDER_API_KEY=...
DEFAULT_MODEL=your-model-name
```

That's it — the UI, API, and CLI scripts will automatically use the new provider.

---
## Companion Documentation
Full theory and visual explanations:  
👉 [winaykumar.com/ai/hands-on/prompt-engineering-lab/](https://winaykumar.com/ai/hands-on/prompt-engineering-lab/)
---
## License
Personal learning project by [Vinay Kumar](https://winaykumar.com).
