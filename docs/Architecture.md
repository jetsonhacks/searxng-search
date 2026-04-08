# Architecture

## Purpose

This repository shows how to build a SearXNG-based search capability from first principles and expose it through a small, inspectable stack.

The main goal is to keep the core search behavior understandable on its own, then layer integrations on top without hiding the boundary between them.

## Layers

### Local SearXNG service

The local SearXNG service is the search backend.
It is installed and removed with the shell scripts under `tools/searxng/`.
Everything else in the repository depends on this service being reachable.
It is also a browser-facing web application, so when it is running locally on port `8081` you can open `http://localhost:8081/search`.

### `tools/searxng/search_searxng.py`

This is the core capability.
It sends a query to the SearXNG JSON endpoint, normalizes the response, and returns structured JSON for both success and failure cases.

### `examples/openai-compatible-tool-calling/`

This is the planned OpenAI-compatible tool-calling example layer.
It is intended to show how a model using an OpenAI-compatible API can call a SearXNG-backed search tool while reusing the existing Python search behavior.

### `docs/providers/`

This is the provider documentation area.
It keeps launch recipes and environment-specific model-server notes separate from the core SearXNG feature implementation.

### `tools/searxng/mcp_server.py`

This is the reusable integration boundary.
It exposes one MCP tool named `search_searxng` and reuses the direct Python search helpers instead of reimplementing the search logic.

### `examples/openclaw/README.md`

This is an example integration layer.
It shows how to point OpenClaw at the MCP server over stdio without changing the core search code.

### `skills/searxng-search/SKILL.md`

This is project-owned guidance layered on top of the MCP tool.
It describes when to use the search capability, what tool boundary to expect, and what structured results the tool returns.

## Boundary Decisions

- Direct Python search is the core capability.
- MCP is the reusable integration boundary.
- The OpenClaw integration is an example, not the center of the design.
- The skill is guidance on top of the implemented MCP behavior, not a separate implementation.

## Repository Flow

1. Install or remove the local SearXNG service with the shell scripts under `tools/searxng/`.
2. Open `http://localhost:8081/search` to use the browser-facing SearXNG interface when the local service runs on port `8081`.
3. Validate direct search with `tools/searxng/search_searxng.py`.
4. Follow `examples/openai-compatible-tool-calling/README.md` for the OpenAI-compatible tool-calling example.
5. Use `docs/providers/overview.md` and the provider notes when you need a compatible model endpoint for the OpenAI-compatible example.
6. Start or exercise the MCP wrapper with `tools/searxng/mcp_server.py`.
7. Follow `examples/openclaw/README.md` for the OpenClaw example.
8. Read `skills/searxng-search/SKILL.md` for the project-owned skill guidance.

## Out Of Scope

This repository does not add packaging, CI, hosted deployment, or multiple agent integrations.
Outside the OpenClaw example and skill, the project stays agent-agnostic.
