# Architecture

## Purpose

This repository shows how to build a SearXNG-based search capability from first principles and expose it through a small, inspectable stack.

The main goal is to keep the core search behavior understandable on its own, then layer integrations on top without hiding the boundary between them.

## Layers

### Local SearXNG service

The local SearXNG service is the search backend.
It is installed and removed with the shell scripts under `tools/searxng/`.
Everything else in the repository depends on this service being reachable.

### `tools/searxng/search_searxng.py`

This is the core capability.
It sends a query to the SearXNG JSON endpoint, normalizes the response, and returns structured JSON for both success and failure cases.

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
2. Validate direct search with `tools/searxng/search_searxng.py`.
3. Start or exercise the MCP wrapper with `tools/searxng/mcp_server.py`.
4. Follow `examples/openclaw/README.md` for the OpenClaw example.
5. Read `skills/searxng-search/SKILL.md` for the project-owned skill guidance.

## Out Of Scope

This repository does not add packaging, CI, hosted deployment, or multiple agent integrations.
Outside the OpenClaw example and skill, the project stays agent-agnostic.
