"""AI Code Explainer — FastAPI app."""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from llm import explain_code
from schemas import ExplainRequest, ExplainResponse

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR

app = FastAPI(title="AI Code Explainer", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/example")
def example() -> dict:
    sample = BASE_DIR / "sample.py"
    return {"code": sample.read_text(), "language": "python"}


@app.post("/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest) -> ExplainResponse:
    return explain_code(req.code.strip(), req.language.strip(), req.level)


@app.exception_handler(Exception)
def unhandled(_request, _exc: Exception) -> JSONResponse:  # noqa: ANN001, ANN202
    return JSONResponse({"detail": "Internal error"}, status_code=500)
