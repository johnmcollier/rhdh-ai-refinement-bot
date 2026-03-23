import openai
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from .ai import analyze_issue
from .models import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="RHDH AI Refinement Bot", version="0.1.0")


@app.get("/health", tags=["ops"])
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse, tags=["refinement"])
def analyze(request: AnalyzeRequest):
    try:
        return analyze_issue(request.description)
    except (openai.OpenAIError, ValueError, ValidationError) as exc:
        raise HTTPException(status_code=502, detail=f"Model request failed: {exc}") from exc


# IMPORTANT: static mount must be last — API routes defined above take precedence.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
