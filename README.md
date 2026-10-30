# Build an AI Agent (Python) — Boot.dev

Toy CLI coding agent from Boot.dev's [Build an AI Agent](https://www.boot.dev/lessons/44e182d7-c2c6-4c7e-9313-1b078e301344) course. A miniature Claude Code / Cursor: you give it a coding task, it picks tool calls (list files, read files, write files, run Python) to work on it.

The calculator app in `./calculator/` is the sandbox project the agent is allowed to inspect and edit.

## Stack migration: Gemini → OpenRouter + OpenAI SDK

This repo started on the old version of the course:

* Old: `google-genai==1.12.1`, model `gemini-2.0-flash-001`, `GEMINI_API_KEY`
* New: `openai==2.44.0`, model `openrouter/free`, `OPENROUTER_API_KEY`, `base_url="https://openrouter.ai/api/v1"`

Why the course switched (July 2026 [Boot.dev Beat](https://www.boot.dev/blog/news/bootdev-beat-2026-07)):

1. `gemini-2.0-flash-001` was deprecated Feb 2026 and **shut down June 1, 2026** ([Google deprecation schedule](https://ai.google.dev/gemini-api/docs/deprecations)). Free-tier quotas were also cut (1500 → 200 RPD) before that.
2. Boot.dev moved AI Agent + RAG courses to OpenRouter via the official OpenAI Python SDK: simpler setup, more transferable SDK, rotating pool of free models with more headroom.

Course status: complete through **Ch3 L4** (system prompt, all four tool schemas, single-step tool dispatch). The agentic loop (Ch4) is next. No Gemini-era code remains; see git history for the lesson-by-lesson rebuild.

## Setup

Requires Python 3.13+, [uv](https://github.com/astral-sh/uv).

```sh
uv venv
# activate: .venv\Scripts\activate on Windows, source .venv/bin/activate on Unix
uv add "openai==2.44.0" "python-dotenv==1.1.0"
```

Create `.env` (never commit it, already in `.gitignore` — see `.env.example`):

```sh
OPENROUTER_API_KEY='your_key_here'
```

Get the key at [openrouter.ai/keys](https://openrouter.ai/keys). Free `:free` models: ~50 req/day, 20/min; a one-time ≥$10 credit purchase raises it to ~1000 req/day. Check usage with `GET /api/v1/key` (`free_model_daily_requests`).

Note: the course assumes a Unix shell — on Windows, run everything from WSL (this repo's `.venv` is Windows-only; use a separate Linux venv, e.g. `UV_PROJECT_ENVIRONMENT=~/.venvs/<name>`).

## Usage

```sh
uv run main.py "read the contents of main.py" --verbose
uv run main.py "fix my calculator app, it's not starting correctly"
```

Without `--verbose`, only tool calls (`Calling function: …`) or the final response print. With it, you also get `User prompt: …`, `Prompt tokens: …`, `Response tokens: …` (from `response.usage`) and each tool result (`-> …`).

Tools exposed to the model (all constrained to `./calculator` via path validation):

* `get_files_info` — list dir + sizes
* `get_file_content` — read file (truncated at 10k chars, see `config.py`)
* `write_file` — create/overwrite file (creates parent dirs)
* `run_python_file` — run `python file.py [args]`, cwd set, 30s timeout, `STDOUT:`/`STDERR:` capture

## Layout

* `main.py` — arg parsing, OpenRouter client, single-step tool dispatch (`--verbose` flag)
* `prompts.py` — system prompt (function-call planner instructions)
* `functions/` — tool implementations + OpenAI dict tool schemas
* `functions/call_function.py` — `available_functions` list + `call_function()` dispatcher (injects `working_directory="./calculator"`, returns `tool` messages)
* `config.py` — `MAX_CHARS = 10_000` truncation limit
* `calculator/` — sandbox target app (JSON-render calculator + tests + `lorem.txt` fixture)
* `test_*.py` — per-lesson manual debug scripts (run directly with `uv run`)
* `.env.example` — env template (`OPENROUTER_API_KEY`, `OPENROUTER_MODEL`)
