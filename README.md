# Prompt Engineering Lab

> 7 runnable experiments to build prompt engineering intuition.  
> Part of [winaykumar.com/ai/hands-on](https://winaykumar.com/ai/hands-on/prompt-engineering-lab/)

## Quick Start

```bash
# 1. Clone
git clone https://github.com/winaykumar/prompt-engineering-lab.git
cd prompt-engineering-lab

# 2. Install
pip install -r requirements.txt

# 3. Run Ollama (or configure your API)
ollama pull llama3.1:8b
ollama serve

# 4. Run any experiment
python 01_zero_few_shot.py
```

## Configuration

Edit `config.py` to switch between:
- **Ollama** (local, free) — default
- **OpenAI** (cloud, paid)
- **EC2 with Ollama** (remote GPU)

## Experiments

| # | File | Technique | What You'll See |
|---|------|-----------|-----------------|
| 01 | `01_zero_few_shot.py` | Zero-shot vs Few-shot | Examples constrain output format |
| 02 | `02_temperature.py` | Temperature | Randomness vs determinism |
| 03 | `03_chain_of_thought.py` | Chain-of-Thought | Step-by-step reasoning |
| 04 | `04_structured_output.py` | Structured Output | JSON extraction + Pydantic |
| 05 | `05_system_prompts.py` | System Prompts | Same question, different personas |
| 06 | `06_self_critique.py` | Self-Critique | Generate → critique → revise |
| 07 | `07_prompt_injection.py` | Prompt Injection | Attack & defence demo |

## Requirements

- Python 3.10+
- Ollama (recommended) or any OpenAI-compatible API
- ~5GB disk for Llama 3.1 8B model

## License

MIT — use freely for learning and experimentation.

