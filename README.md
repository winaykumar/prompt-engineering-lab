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
- **Ollama** — local LLM runtime (free, no API key needed)
### Install Ollama
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh
# macOS
brew install ollama
# Or download from https://ollama.com/download
```
### Pull a model
```bash
ollama pull llama3.1:8b
```
---
## Setup
```bash
# 1. Clone the repo
git clone https://github.com/winaykumar/prompt-engineering-lab.git
cd prompt-engineering-lab
# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate     # Windows
# 3. Install dependencies
pip install -r requirements.txt
# 4. Copy environment config
cp .env.example .env
# Edit .env if you want to change backend (default: Ollama)
```
---
## Usage
### Start the lab
```bash
# Terminal 1 — Start Ollama (if not already running)
ollama serve
# Terminal 2 — Start the lab server
uvicorn backend.main:app --reload --port 8000
```
### Open in browser
```
http://localhost:8000           # Overview — all 7 experiments
http://localhost:8000/lab/01    # Experiment 01 — Zero-Shot vs Few-Shot
http://localhost:8000/lab/02    # Experiment 02 — Temperature
...
http://localhost:8000/lab/07    # Experiment 07 — Prompt Injection
```
### How to use each experiment
1. **Read** the experiment description and technique explanation
2. **Edit** the pre-filled prompts — change system/user messages, add/remove messages
3. **Adjust** temperature and max tokens
4. **Click ▶ Run** — sends the prompt to your LLM backend
5. **See** the response with latency (ms), token count, and model info
6. **Compare** variants side by side (e.g., Zero-Shot vs Few-Shot)
### Running standalone scripts (no web UI)
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
## Configuration
### Environment variables (`.env`)
| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BACKEND` | `ollama` | Backend to use: `ollama`, `ec2`, or `openai` |
| `OLLAMA_URL` | `http://localhost:11434/v1` | Ollama API endpoint |
| `EC2_URL` | — | Remote EC2 endpoint (when `LLM_BACKEND=ec2`) |
| `OPENAI_API_KEY` | — | OpenAI API key (when `LLM_BACKEND=openai`) |
| `DEFAULT_MODEL` | `llama3.1:8b` | Model to use for completions |
### Backend options
| Backend | Cost | Setup | Best For |
|---------|------|-------|----------|
| **Ollama** (default) | $0 | `ollama serve` locally | Learning, daily experiments |
| **EC2** | ~$1/hr (GPU) | Run Ollama on EC2, set `EC2_URL` | Larger models (13B+) |
| **OpenAI** | Pay-per-token | Set `OPENAI_API_KEY` | GPT-4o / GPT-4o-mini |
### Switching backends
```bash
# .env — switch to EC2
LLM_BACKEND=ec2
EC2_URL=http://your-ec2-ip:11434/v1
# .env — switch to OpenAI
LLM_BACKEND=openai
OPENAI_API_KEY=sk-...
DEFAULT_MODEL=gpt-4o-mini
```
---
## Project Structure
```
prompt-engineering-lab/
├── backend/
│   ├── main.py                 # FastAPI app — API routes + static serving
│   ├── llm_client.py           # Unified LLM client (Ollama/EC2/OpenAI)
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
## Companion Documentation
Full theory and visual explanations:  
👉 [winaykumar.com/ai/hands-on/prompt-engineering-lab/](https://winaykumar.com/ai/hands-on/prompt-engineering-lab/)
---
## License
Personal learning project by [Vinay Kumar](https://winaykumar.com).
