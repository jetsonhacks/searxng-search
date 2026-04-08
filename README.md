# searxng-search

`searxng-search` is a practical reference project for building an agent-facing search capability on top of [SearXNG](https://github.com/searxng/searxng).

[SearXNG](https://searxng.org/) is a free, self-hostable metasearch engine that can return search results as JSON. That makes it useful when you want private, inspectable web search with structured output, rather than treating search as a black box.

This repository shows the full path from a local SearXNG install to a reusable search capability:

- install and uninstall a local SearXNG instance
- query SearXNG directly from Python
- expose the same search behavior through MCP
- connect that MCP server to OpenClaw
- add a project-owned OpenClaw skill that matches the implemented MCP tool

The goal is to keep each layer small, readable, and easy to validate.

## Quick Start

Bring up a local SearXNG instance:

```bash
SEARXNG_PORT=8081 bash tools/searxng/install-searxng.sh
```

Validate direct search from Python:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:8081 python3 tools/searxng/search_searxng.py "jetson orin"
```

This example uses `8081`. The install script defaults to `8080` unless you set `SEARXNG_PORT`, so use the same port value in both the install and search commands.

When SearXNG is running locally on port `8081`, you can also open the browser interface at `http://localhost:8081/search`.

For the full validation path, including MCP and the OpenClaw example, see `docs/Validation.md`.

## Python Dependencies

This is a normal Python project. Python dependencies are declared in `pyproject.toml`.

Recommended workflow:

- install `uv` if you want to run the Python examples with the recommended workflow
- run `uv sync`
- run repository commands with `uv run ...`

Example:

```bash
uv sync
uv run python3 tools/searxng/search_searxng.py --base-url http://127.0.0.1:8081 "jetson orin"
```

If you prefer standard Python tooling instead, use a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -e .
```

## What This Repository Covers

This repository is organized as a progression:

1. Browser use of local SearXNG
2. Direct Python search with `tools/searxng/search_searxng.py`
3. OpenAI-compatible tool calling under `examples/openai-compatible-tool-calling/`
4. MCP exposure with `tools/searxng/mcp_server.py`
5. OpenClaw example integration under `examples/openclaw/`
6. Project-owned skill definition in `skills/searxng-search/SKILL.md`

The first OpenAI-compatible tool-calling path has been validated end to end against llama.cpp and a local SearXNG instance.

## Reader Guide

- `docs/Architecture.md` explains the implemented structure and boundaries
- `docs/providers/overview.md` explains how provider launch recipes relate to the OpenAI-compatible example
- `docs/Validation.md` shows how to validate the repository end to end
- `dev/README.md` explains what development artifacts live under `dev/`
- `examples/openai-compatible-tool-calling/README.md` outlines the OpenAI-compatible tool-calling example
- `examples/openclaw/README.md` documents the OpenClaw example integration
- `skills/searxng-search/SKILL.md` defines the project-owned OpenClaw skill
- `dev/` contains milestone and development-history documents

`docs/` is reserved for user-facing documentation.
`dev/` contains development artifacts such as plans, status, feature specs, and ADRs.
`AGENTS.md` is the operational guide for coding agents working in this repository.

## Why Use This Repository

This project is useful if you want to:

- understand how to turn SearXNG into a small reusable search component
- keep the core search logic inspectable
- use MCP as a clean integration boundary
- see a controlled OpenClaw example without making the whole project agent-specific

## Notes

- The validated local workflow in this repository used port `8081`, because port `8080` conflicted with NemoClaw in testing.
- Outside the OpenClaw example and skill, the project stays agent-agnostic.

## Releases

### Initial Release (April 2026)

* This release includes the complete reference flow: local SearXNG install and uninstall, direct Python search, MCP exposure, the OpenClaw example, and the project-owned skill.
