# Status

## Current State

Milestone 6 complete, with follow-up skill and HTTP MCP demonstrations added.

The repository now covers the full learning path from local SearXNG install through Python search, OpenAI-compatible tool calling, MCP exposure over stdio and HTTP, OpenClaw integration, llama.cpp WebUI integration, and the project-owned search skill.

## What Was Completed

### Milestone 1
- Added `tools/searxng/install-searxng.sh`
- Added `tools/searxng/start-searxng.sh`
- Added `tools/searxng/uninstall-searxng.sh`
- Documented a clean local install, restart, and removal path for SearXNG

### Milestone 2
- Added `tools/searxng/search_searxng.py`
- Implemented command-line search against the SearXNG JSON endpoint
- Added support for `--base-url` and `SEARXNG_BASE_URL`
- Normalized results to `title`, `url`, `engine`, `content`, and `score`
- Returned structured JSON output for both success and error cases

### Milestone 3
- Added `tools/searxng/mcp_server.py`
- Exposed one MCP tool named `search_searxng`
- Reused the Milestone 2 search helpers for base URL resolution, request execution, and result normalization
- Returned structured JSON text content for both success and tool-level error cases

### Milestone 4
- Added `examples/openclaw/README.md`
- Documented a controlled OpenClaw integration that uses the MCP server as the boundary
- Kept the core search logic and MCP implementation unchanged for the example

### Milestone 5
- Completed `skills/searxng-search/SKILL.md`
- Matched the skill to the implemented MCP tool name, inputs, and result shape
- Kept the skill aligned with the documented OpenClaw example and MCP boundary

### Milestone 6
- Updated `README.md` to reflect the completed repository progression
- Marked completed milestones accurately in `dev/Plan.md`
- Tightened OpenClaw example documentation to match the implemented required and optional MCP tool arguments
- Added lightweight end-to-end validation guidance without introducing new test infrastructure

### Follow-up Skill Demo
- Added `examples/skill-demo/simple_agent.py`
- Added `examples/skill-demo/README.md`
- Centered the demo on the existing `skills/searxng-search/SKILL.md`
- Documented a before-and-after comparison: same standalone `search_searxng` tool without skill guidance, then with the project skill loaded
- Kept the standalone tool name and result shape aligned with the MCP tool while keeping base URL and timeout as script settings
- Added a run header to `simple_agent.py` so demos show whether the mode is model-only, tool-only, or tool-plus-skill
- Tightened `skills/searxng-search/SKILL.md` with concise source-handling guidance used by the demo
- Removed the skill demo from the OpenClaw example so OpenClaw remains a separate integration path
- Added links from `README.md`

### Documentation Alignment Pass
- Updated `AGENTS.md` so the current priority reflects maintenance after completed milestones
- Updated `docs/Architecture.md` to describe the implemented OpenAI-compatible, skill-demo, stdio MCP, HTTP MCP, OpenClaw, and llama.cpp WebUI layers
- Clarified that `examples/openai-compatible-tool-calling/` uses local function tool name `searxng_search`, while MCP uses `search_searxng`
- Clarified that `examples/skill-demo/` exposes `query` and optional `limit` to the model, while base URL and timeout are script settings
- Added validation notes for the standalone skill demo and llama.cpp WebUI MCP runbook
- Removed milestone terminology from user-facing docs and examples so milestones remain a development-history concept under `dev/`

### llama.cpp WebUI CORS Maintenance
- Updated `tools/searxng/mcp_http_server.py` so browser CORS responses allow both `http://127.0.0.1:8080` and `http://localhost:8080`
- Changed CORS handling to echo the incoming origin only when it is in the local WebUI allowlist
- Updated the llama.cpp WebUI runbook and validation notes to document that browsers treat `127.0.0.1` and `localhost` as different origins

## Validation Notes

- Ran `python3 tools/searxng/search_searxng.py --base-url http://127.0.0.1:8081 "jetson orin"`
- Ran `SEARXNG_BASE_URL=http://127.0.0.1:8081 python3 tools/searxng/search_searxng.py "jetson orin"`
- Confirmed both commands returned normalized JSON results from the local SearXNG instance
- Ran `env -u SEARXNG_BASE_URL python3 tools/searxng/search_searxng.py "jetson orin"`
- Confirmed the missing-base-URL path returned structured JSON error output and exited nonzero
- Ran `python3 -m py_compile tools/searxng/mcp_server.py tools/searxng/search_searxng.py`
- Ran a local JSON-RPC initialize request against `tools/searxng/mcp_server.py`
- Ran a local JSON-RPC `tools/list` request and confirmed one `search_searxng` tool with a structured input schema
- Ran a local JSON-RPC `tools/call` request without `SEARXNG_BASE_URL` and confirmed structured error output with `isError: true`
- Reviewed the OpenClaw example instructions against the implemented MCP tool name, command, working directory, and required environment variable
- Confirmed the example keeps OpenClaw-specific setup inside `examples/openclaw/README.md`
- Compared `skills/searxng-search/SKILL.md` against `tools/searxng/mcp_server.py`
- Compared `skills/searxng-search/SKILL.md` against `examples/openclaw/README.md`
- Confirmed the skill uses the implemented MCP tool name `search_searxng`
- Confirmed the skill lists the implemented tool inputs: `query`, optional `base_url`, optional `limit`, optional `timeout`
- Confirmed the skill reflects the implemented structured result shape and error shape
- Confirmed the skill notes the `SEARXNG_BASE_URL` expectation without promising unsupported behavior
- Confirmed no unsupported claims were added to the skill
- Confirmed the standalone skill demo references the existing `skills/searxng-search/SKILL.md`
- Confirmed the standalone skill demo does not introduce a second skill file
- Confirmed the skill's source-handling guidance uses existing result fields and does not require tool changes
- Ran `python3 -m py_compile examples/skill-demo/simple_agent.py`
- Reviewed `examples/llama-cpp-mcp-demo/run-llama-cpp-mcp-demo.md` against `tools/searxng/mcp_http_server.py`
- Ran `python3 -m py_compile tools/searxng/search_searxng.py tools/searxng/mcp_common.py tools/searxng/mcp_server.py tools/searxng/mcp_http_server.py examples/openai-compatible-tool-calling/tool_calling_example.py examples/skill-demo/simple_agent.py`
- Ran `bash -n tools/searxng/start-searxng.sh tools/searxng/install-searxng.sh tools/searxng/uninstall-searxng.sh`
- Ran `rg -n "Milestone|milestone" README.md docs examples skills AGENTS.md` and confirmed no matches outside development-history docs
- Compared `README.md` against the implemented repository progression: install, restart, or uninstall, Python search, MCP wrapper, OpenClaw example, and project-owned skill
- Compared `dev/Plan.md` against the current completed milestone state
- Compared `dev/Status.md` against the final repository state for Milestone 6
- Compared `examples/openclaw/README.md` against `tools/searxng/mcp_server.py` for tool name, required argument, optional arguments, command, working directory, and environment expectation
- Ran `bash -n tools/searxng/start-searxng.sh tools/searxng/install-searxng.sh tools/searxng/uninstall-searxng.sh`
- Ran `python3 -m py_compile tools/searxng/search_searxng.py tools/searxng/mcp_server.py`
- Confirmed the lightweight validation instructions are practical and consistent with the implemented workflow
- Confirmed the end-to-end learning path is understandable from the repository docs
- Ran `python3 -m py_compile tools/searxng/mcp_http_server.py`
- Ran CORS preflight checks for `Origin: http://127.0.0.1:8080` and `Origin: http://localhost:8080`
- Confirmed each allowed local WebUI origin is echoed in `Access-Control-Allow-Origin`

## Current Focus

Milestones complete. Keep the repository stable, readable, and easy to validate. The current skill demo is standalone and should remain centered on the existing project-owned skill rather than introducing parallel skill examples.

## Next Step

Use the documented smoke-test style checks when making future maintenance updates, and keep docs aligned with the implemented tool behavior.
