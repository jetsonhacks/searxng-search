# Architecture

## Purpose

This repository shows how to build a SearXNG-based search capability from first principles and expose it through a small, inspectable stack.

The main goal is to keep the core search behavior understandable on its own, then layer integrations on top without hiding the boundary between them.

## Layers

### Local SearXNG service

The local SearXNG service is the search backend.
It is installed, restarted, and removed with the shell scripts under `tools/searxng/`.
Everything else in the repository depends on this service being reachable.
It is also a browser-facing web application, so when it is running locally on port `8081` you can open `http://localhost:8081/search`.

### `tools/searxng/search_searxng.py`

This is the core capability.
It sends a query to the SearXNG JSON endpoint, normalizes the response, and returns structured JSON for both success and failure cases.

### `examples/openai-compatible-tool-calling/`

This is the direct OpenAI-compatible tool-calling example layer.
It shows how a model using an OpenAI-compatible `chat.completions` API can call a SearXNG-backed local function tool while reusing the existing Python search behavior.
The example tool is named `searxng_search` so it is distinct from the MCP tool boundary.

### `examples/skill-demo/`

This is a standalone skill behavior demo.
It exposes a local OpenAI-compatible function tool named `search_searxng` and can optionally load `skills/searxng-search/SKILL.md` as system guidance.
The demo avoids MCP startup so the comparison stays focused on tool-only behavior versus tool-plus-skill behavior.

### `docs/providers/`

This is the provider documentation area.
It keeps launch recipes and environment-specific model-server notes separate from the core SearXNG feature implementation.

### `tools/searxng/mcp_server.py`

This is the reusable integration boundary.
It exposes one MCP tool named `search_searxng` and reuses the direct Python search helpers instead of reimplementing the search logic.

### `tools/searxng/mcp_http_server.py`

This exposes the same MCP request handling over HTTP for browser-facing clients such as llama.cpp WebUI.
It provides a streamable HTTP endpoint at `/mcp`, a health check at `/health`, and a legacy SSE compatibility endpoint at `/sse`.

### `examples/openclaw/README.md`

This is an example integration layer.
It shows how to point OpenClaw at the MCP server over stdio without changing the core search code.

### `examples/llama-cpp-mcp-demo/`

This is a runbook for connecting llama.cpp WebUI to the HTTP MCP server and validating that the model can discover and invoke `search_searxng`.

### `skills/searxng-search/SKILL.md`

This is project-owned guidance layered on top of the MCP tool.
It describes when to use the search capability, what tool boundary to expect, how to treat snippets, and what structured results the tool returns.

## Boundary Decisions

- Direct Python search is the core capability.
- MCP is the reusable integration boundary, available through stdio and HTTP entry points.
- The OpenAI-compatible examples demonstrate local function-tool behavior without making the core project provider-specific.
- The OpenClaw and llama.cpp WebUI integrations are examples, not the center of the design.
- The skill is guidance on top of the implemented MCP behavior, not a separate implementation.

## Repository Flow

1. Install, restart, or remove the local SearXNG service with the shell scripts under `tools/searxng/`.
2. Open `http://localhost:8081/search` to use the browser-facing SearXNG interface when the local service runs on port `8081`.
3. Validate direct search with `tools/searxng/search_searxng.py`.
4. Follow `examples/openai-compatible-tool-calling/README.md` for the OpenAI-compatible tool-calling example.
5. Follow `examples/skill-demo/README.md` to compare tool-only behavior with tool-plus-skill behavior.
6. Use `docs/providers/overview.md` and the provider notes when you need a compatible model endpoint for the OpenAI-compatible examples.
7. Start or exercise the stdio MCP wrapper with `tools/searxng/mcp_server.py`.
8. Start or exercise the HTTP MCP wrapper with `tools/searxng/mcp_http_server.py`.
9. Follow `examples/openclaw/README.md` for the OpenClaw stdio MCP example.
10. Follow `examples/llama-cpp-mcp-demo/run-llama-cpp-mcp-demo.md` for the llama.cpp WebUI HTTP MCP example.
11. Read `skills/searxng-search/SKILL.md` for the project-owned skill guidance.

## Out Of Scope

This repository does not add production packaging, CI, hosted deployment, or broad multi-agent integration coverage.
The checked-in `pyproject.toml` is dependency metadata for running the Python examples.
Outside the documented examples and skill, the core search path stays agent-agnostic.
