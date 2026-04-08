# searxng-search

This repository is a practical walk through of building a SearXNG-based search tool from first principles.

It covers the full path:
- install and uninstall a local SearXNG instance
- query SearXNG directly from Python
- expose the same search behavior through MCP
- connect that MCP server to OpenClaw
- add a project-owned OpenClaw skill that matches the implemented MCP tool

The goal is to make each step easy to inspect and validate without hiding the moving parts behind extra infrastructure.

## Reader Docs

- `docs/Architecture.md` explains the implemented structure and boundaries
- `docs/Validation.md` shows how to validate the repository end to end
- `docs/development/` contains milestone and development-history documents

## Repository Progression

1. Install and uninstall SearXNG with the shell scripts under `tools/searxng/`
2. Validate direct search with `tools/searxng/search_searxng.py`
3. Start the MCP wrapper with `tools/searxng/mcp_server.py`
4. Follow `examples/openclaw/README.md` for the OpenClaw example
5. Use `skills/searxng-search/SKILL.md` as the project-owned OpenClaw skill definition

## Lightweight Validation

Use these checks to validate the repository end to end:

```bash
python3 -m py_compile tools/searxng/search_searxng.py tools/searxng/mcp_server.py
SEARXNG_BASE_URL=http://127.0.0.1:8081 python3 tools/searxng/search_searxng.py "jetson orin"
```

Then review:
- `examples/openclaw/README.md` for the MCP server command, working directory, and environment setup
- `skills/searxng-search/SKILL.md` for the exact `search_searxng` tool boundary used by the OpenClaw phase
