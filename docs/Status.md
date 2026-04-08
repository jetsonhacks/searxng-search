# Status

## Current State

Milestone 2 complete.

## What Was Completed

- Added `tools/searxng/search_searxng.py`
- Implemented command-line search against the SearXNG JSON endpoint
- Added support for `--base-url` and `SEARXNG_BASE_URL`
- Normalized results to `title`, `url`, `engine`, `content`, and `score`
- Returned structured JSON output for both success and error cases

## Validation Notes

- Ran `python3 tools/searxng/search_searxng.py --base-url http://127.0.0.1:8081 "jetson orin"`
- Ran `SEARXNG_BASE_URL=http://127.0.0.1:8081 python3 tools/searxng/search_searxng.py "jetson orin"`
- Confirmed both commands returned normalized JSON results from the local SearXNG instance
- Ran `env -u SEARXNG_BASE_URL python3 tools/searxng/search_searxng.py "jetson orin"`
- Confirmed the missing-base-URL path returned structured JSON error output and exited nonzero

## Current Focus

Prepare for Milestone 3: expose search through MCP.

## Next Step

Implement `tools/searxng/mcp_server.py`
