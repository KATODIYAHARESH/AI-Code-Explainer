"""API tests for AI Code Explainer (run in demo mode: no LLM_API_KEY)."""

import os

import pytest
from fastapi.testclient import TestClient

os.environ.pop("LLM_API_KEY", None)

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_example():
    res = client.get("/example")
    assert res.status_code == 200
    assert "fibonacci" in res.json()["code"]


def test_explain_demo_mode():
    res = client.post(
        "/explain",
        json={"code": "x = 1\ny = x + 2", "language": "python", "level": "beginner"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["demo"] is True
    assert len(data["line_by_line"]) == 2
    assert data["overview"]


def test_explain_rejects_empty_code():
    res = client.post("/explain", json={"code": "", "language": "python", "level": "beginner"})
    assert res.status_code == 422


def test_explain_rejects_bad_level():
    res = client.post(
        "/explain",
        json={"code": "x = 1", "language": "python", "level": "wizard"},
    )
    assert res.status_code == 422
