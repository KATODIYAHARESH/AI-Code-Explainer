"""LLM client with a demo-mode fallback.

With LLM_API_KEY set, this calls any OpenAI-compatible chat-completions
endpoint. Without a key it returns a clearly-marked demo explanation, so
the app (and its tests) run end to end with zero setup.
"""

import json
import os

import httpx

from prompts import SYSTEM_PROMPT, build_user_prompt
from schemas import ExplainResponse, LineExplanation


def _demo_response(code: str, language: str) -> ExplainResponse:
    lines = [ln for ln in code.splitlines() if ln.strip()]
    return ExplainResponse(
        demo=True,
        overview=(
            f"This {language} snippet has {len(lines)} non-empty line(s). "
            "Demo mode is on (no LLM_API_KEY set), so this is a structural "
            "walkthrough, not an AI explanation. Set LLM_API_KEY in .env "
            "for real explanations."
        ),
        line_by_line=[
            LineExplanation(line=ln, explanation="Executes as written (demo mode).")
            for ln in lines
        ],
        key_concepts=["demo mode", "code structure"],
        possible_bugs=[],
        improvements=["Set LLM_API_KEY to get real bug hints and improvements."],
        model="demo",
    )


def explain_code(code: str, language: str, level: str) -> ExplainResponse:
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    if not api_key:
        return _demo_response(code, language)

    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")

    try:
        resp = httpx.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(code, language, level)},
                ],
                "temperature": 0.2,
            },
            timeout=60.0,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        return ExplainResponse(
            demo=False,
            overview=data.get("overview", ""),
            line_by_line=[
                LineExplanation(line=item.get("line", ""), explanation=item.get("explanation", ""))
                for item in data.get("line_by_line", [])
            ],
            key_concepts=data.get("key_concepts", []),
            possible_bugs=data.get("possible_bugs", []),
            improvements=data.get("improvements", []),
            model=model,
        )
    except (httpx.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
        # Never crash the API on an LLM failure: say so, plainly.
        return ExplainResponse(
            demo=False,
            overview=f"LLM call failed: {exc}. Check LLM_API_KEY / LLM_BASE_URL / LLM_MODEL.",
            line_by_line=[],
            key_concepts=[],
            possible_bugs=[],
            improvements=[],
            model=model,
        )
