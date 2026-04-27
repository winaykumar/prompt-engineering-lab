"""
Prompt Engineering Lab — FastAPI Backend
Run: uvicorn backend.main:app --reload --port 8000
"""
# Load .env BEFORE any other imports so providers pick up env vars
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
from pathlib import Path

from backend.llm_client import chat as llm_chat
from backend.experiments.registry import get_experiment, list_experiments

app = FastAPI(title="Prompt Engineering Lab", version="1.0.0")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══ API Models ═══

class RunRequest(BaseModel):
    messages: list[dict]
    model: str | None = None
    temperature: float = 0.0
    max_tokens: int = 1000


class RunResponse(BaseModel):
    text: str
    model: str
    tokens: int
    latency_ms: int
    backend: str


# ═══ API Endpoints ═══

@app.get("/api/experiments")
def api_list_experiments():
    """List all available experiments."""
    return list_experiments()


@app.get("/api/experiments/{exp_id}")
def api_get_experiment(exp_id: str):
    """Get a single experiment with its variants."""
    exp = get_experiment(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
    return exp


@app.post("/api/run", response_model=RunResponse)
def api_run_prompt(req: RunRequest):
    """Run a prompt against the configured LLM backend."""
    try:
        result = llm_chat(
            messages=req.messages,
            model=req.model,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        return RunResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══ Serve Frontend ═══

# Script file mapping for the "View Code" feature
_SCRIPT_MAP = {
    "01": "01_zero_few_shot.py",
    "02": "02_temperature.py",
    "03": "03_chain_of_thought.py",
    "04": "04_structured_output.py",
    "05": "05_system_prompts.py",
    "06": "06_self_critique.py",
    "07": "07_prompt_injection.py",
}


@app.get("/api/code/{exp_id}")
def api_get_code(exp_id: str):
    """Return the CLI script source code for an experiment."""
    filename = _SCRIPT_MAP.get(exp_id)
    if not filename:
        raise HTTPException(status_code=404, detail=f"No script for experiment {exp_id}")
    script_path = Path(filename)
    if not script_path.exists():
        raise HTTPException(status_code=404, detail=f"Script file {filename} not found")
    return PlainTextResponse(script_path.read_text(encoding="utf-8"))


app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")


@app.get("/lab/{exp_id}")
def serve_lab(exp_id: str):
    return FileResponse("frontend/lab.html")

