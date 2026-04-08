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

For the full validation path, including MCP and the OpenClaw example, see `docs/Validation.md`.

## What This Repository Covers

This repository is organized as a progression:

1. Local SearXNG install and uninstall with shell scripts under `tools/searxng/`
2. Direct Python search with `tools/searxng/search_searxng.py`
3. MCP exposure with `tools/searxng/mcp_server.py`
4. OpenClaw example integration under `examples/openclaw/`
5. Project-owned skill definition in `skills/searxng-search/SKILL.md`

## Reader Guide

- `docs/Architecture.md` explains the implemented structure and boundaries
- `docs/Validation.md` shows how to validate the repository end to end
- `examples/openclaw/README.md` documents the OpenClaw example integration
- `skills/searxng-search/SKILL.md` defines the project-owned OpenClaw skill
- `docs/development/` contains milestone and development-history documents

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
