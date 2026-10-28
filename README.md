# AI Code Explainer

Paste code in any language, get a clear explanation back: an overview,
a line-by-line walkthrough, the key concepts, possible bugs, and
suggested improvements.

Built with Python + FastAPI. The frontend is plain HTML/CSS/JS — no build
step, no framework to install for the UI.

## Features

- Explain code in Python, JavaScript, Java, C++, Go, and more
- Three detail levels: `beginner`, `intermediate`, `expert`
- Line-by-line explanations, not just a summary
- Possible bugs + suggested improvements for every snippet
- Demo mode: works with **no API key** (returns a clearly-marked sample
  explanation) so you can run and demo the whole app immediately
- Pluggable LLM: any OpenAI-compatible chat-completions API
  (OpenAI, Gemini via an OpenAI-compatible endpoint, local models, ...)

## Quick start

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run (demo mode — no key needed)
uvicorn app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000 in your browser.

## Using a real LLM (optional)

```bash
cp .env.example .env
# edit .env and set LLM_API_KEY (and LLM_MODEL / LLM_BASE_URL if needed)
```

With a key set, `/explain` calls your model and returns a real
explanation. Without a key, it returns a demo explanation with
`"demo": true` so the UI still works end to end.

| Variable       | Default                                        | Meaning                              |
| -------------- | ---------------------------------------------- | ------------------------------------ |
| `LLM_API_KEY`  | _(empty = demo mode)_                          | API key for your LLM provider        |
| `LLM_BASE_URL` | `https://api.openai.com/v1`                    | OpenAI-compatible base URL           |
| `LLM_MODEL`    | `gpt-4o-mini`                                  | Model name                           |

## API

### `GET /health`

```json
{"status": "ok"}
```

### `POST /explain`

Request:

```json
{
  "code": "def add(a, b):\n    return a + b",
  "language": "python",
  "level": "beginner"
}
```

Response:

```json
{
  "demo": true,
  "overview": "...",
  "line_by_line": [{"line": "def add(a, b):", "explanation": "..."}],
  "key_concepts": ["functions", "return values"],
  "possible_bugs": [],
  "improvements": ["..."],
  "model": "demo"
}
```

### `GET /example`

Returns a sample Python snippet you can explain with one click.

## Run the tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -q
```

## Project structure

```
ai-code-explainer/
├── app/
│   ├── main.py       # FastAPI app + endpoints
│   ├── schemas.py    # request/response models
│   ├── prompts.py    # prompt builder per detail level
│   └── llm.py        # LLM client + demo-mode fallback
├── static/           # frontend (index.html, app.js, style.css)
├── examples/         # sample snippet for one-click demo
└── tests/            # API tests
```

## License

MIT
