"""Prompt builder: one system prompt per detail level.

The model is asked to answer with strict JSON so the API can return
structured sections instead of one big blob of text.
"""

LEVEL_GUIDANCE = {
    "beginner": (
        "Explain like the reader is new to programming. Define every "
        "technical term the first time you use it, keep sentences short, "
        "and avoid jargon without an explanation."
    ),
    "intermediate": (
        "Assume the reader knows programming basics. Focus on what the code "
        "does, why it is written this way, and the trade-offs involved."
    ),
    "expert": (
        "Assume the reader is experienced. Focus on edge cases, complexity, "
        "idioms, and what a senior reviewer would flag."
    ),
}

SYSTEM_PROMPT = """You are a code explanation assistant. You explain source code
clearly and accurately. You never invent behaviour the code does not have.

Return ONLY valid JSON with exactly these keys:
{
  "overview": "2-4 sentence summary of what the code does",
  "line_by_line": [{"line": "<exact code line>", "explanation": "<what it does>"}],
  "key_concepts": ["concept 1", "concept 2"],
  "possible_bugs": ["bug or edge case, or empty list"],
  "improvements": ["suggestion, or empty list"]
}

Rules:
- line_by_line must cover every non-empty line of the snippet.
- Do not add keys, markdown fences, or commentary outside the JSON.
"""


def build_user_prompt(code: str, language: str, level: str) -> str:
    guidance = LEVEL_GUIDANCE.get(level, LEVEL_GUIDANCE["beginner"])
    return (
        f"Language: {language}\n"
        f"Detail level: {level}\n"
        f"{guidance}\n\n"
        f"Explain this code:\n```{language}\n{code}\n```"
    )
