# Build an AI Agent (Python) — Boot.dev

Toy CLI coding agent from Boot.dev's [Build an AI Agent](https://www.boot.dev/lessons/44e182d7-c2c6-4c7e-9313-1b078e301344) course. A miniature Claude Code / Cursor: you give it a coding task, it loops over LLM + tool calls (list files, read files, write files, run Python) until done.

Test target is the buggy calculator app in `./calculator/`.

## Stack migration: Gemini → OpenRouter + OpenAI SDK

This repo started on the old version of the course:

* Old: `google-genai==1.12.1`, model `gemini-2.0-flash-001`, `GEMINI_API_KEY`
* New: `openai==2.44.0`, model `openrouter/free`, `OPENROUTER_API_KEY`, `base_url="https://openrouter.ai/api/v1"`

Why the course switched (July 2026 [Boot.dev Beat](https://www.boot.dev/blog/news/bootdev-beat-2026-07)):

1. `gemini-2.0-flash-001` was deprecated Feb 2026 and **shut down June 1, 2026** ([Google deprecation schedule](https://ai.google.dev/gemini-api/docs/deprecations)). Free-tier quotas were also cut (1500 → 200 RPD) before that.
2. Boot.dev moved AI Agent + RAG courses to OpenRouter via the official OpenAI Python SDK: simpler setup, more transferable SDK, rotating pool of free models with more headroom.

Migration status: complete through Ch4 L1 — `pyproject.toml`, `main.py`, and all of `functions/*` now use the OpenAI SDK (`chat.completions` + dict tool schemas) via OpenRouter. Dual-provider support (`LLM_PROVIDER=openrouter` default, `opencode-go`/`opencode` via OpenCode Console) lives on top; see `.env.example`.

## Setup (current course, Lessons 2–3)

Requires Python 3.13+, [uv](https://github.com/astral-sh/uv).

```sh
uv venv
# activate: .venv\Scripts\activate on Windows, source .venv/bin/activate on Unix
uv add "openai==2.44.0" "python-dotenv==1.1.0"
```

Create `.env` (never commit it, already in `.gitignore`):

```sh
OPENROUTER_API_KEY='your_key_here'
```

Get the key at [openrouter.ai/keys](https://openrouter.ai/keys). Free tier is ~50 req/day, ~20/min via `openrouter/free`; adding $10 credit raises it to ~1000 req/day.

## Usage

```sh
uv run main.py "fix my calculator app, it's not starting correctly"
uv run main.py "What is the meaning of life?" --verbose
```

`--verbose` prints `User prompt: ...`, `Prompt tokens: ...`, `Response tokens: ...` (from `response.usage`). Without it, only the final response prints.

Tools exposed to the model (constrained to `./calculator`):

* `get_files_info` — list dir + sizes
* `get_file_content` — read file (truncated at 10k chars)
* `write_file` — create/overwrite file
* `run_python_file` — run `python file.py [args]`, 30s timeout

## Layout

* `main.py` — arg parsing, OpenRouter client, agent loop (max 20 steps)
* `functions/` — tool implementations + OpenAI tool schemas
* `calculator/` — sandbox target app the agent is allowed to edit
* `tests.py` — manual scratch tests for the tools
