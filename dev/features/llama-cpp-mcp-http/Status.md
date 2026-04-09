# Status: llama.cpp MCP HTTP Integration

## Current State
Implementation completed and HIL-validated for the target local llama.cpp WebUI flow.

The repository now supports:
- the original stdio MCP server path
- an HTTP MCP server path usable from llama.cpp WebUI by URL

End-to-end validation succeeded:
- llama.cpp WebUI connected to the MCP server
- the WebUI discovered the `search_searxng` tool
- the model invoked the tool successfully
- tool results were returned and summarized in chat

## Completed
- Created feature directory: `dev/features/llama-cpp-mcp-http/`
- Added `Spec.md`
- Added `Plan.md`
- Added `Status.md`
- Added shared MCP logic in `tools/searxng/mcp_common.py`
- Preserved the stdio MCP entry point in `tools/searxng/mcp_server.py`
- Added the HTTP MCP entry point in `tools/searxng/mcp_http_server.py`
- Added `/health` endpoint for smoke testing
- Added legacy `/sse` compatibility path for older MCP HTTP clients
- Updated documentation:
  - `docs/providers/llama-cpp.md`
  - `docs/Validation.md`
  - `examples/openai-compatible-tool-calling/run-llama-cpp.md`

## In Progress
- None

## Next Steps
- Review the implementation against `Spec.md` and `Plan.md` for any final cleanup items
- Decide whether any compatibility behavior should remain exactly as implemented or be simplified
- Determine whether any follow-up documentation polish is needed
- Prepare the feature for commit

## Decisions
- Preserve the existing stdio MCP server
- Add an HTTP MCP server as an additional transport path
- Reuse shared SearXNG search logic where practical through `tools/searxng/mcp_common.py`
- Use `/mcp` as the primary HTTP MCP endpoint
- Include `/health` for smoke testing
- Include `/sse` as a compatibility fallback
- Keep the implementation localhost-oriented for development and HIL testing

## Validation

### Repo-side smoke validation
Passed:
- `python3 -m py_compile tools/searxng/search_searxng.py tools/searxng/mcp_common.py tools/searxng/mcp_server.py tools/searxng/mcp_http_server.py`
- `curl http://127.0.0.1:8765/health` returned `{"ok": true}`
- `POST /mcp initialize` returned the expected MCP initialization response
- `POST /mcp tools/list` returned `search_searxng`
- `POST /mcp tools/call` without `SEARXNG_BASE_URL` returned a structured tool error rather than crashing

### HIL validation timeline

#### 1. Initial browser connection failure
Observed in llama.cpp WebUI:
- transport created for `http://127.0.0.1:8765/mcp`
- transport ready (`streamable_http`)
- initialize attempt failed with `Failed to fetch`

Initial interpretation:
- repo-side MCP server appeared functional from direct `curl`
- failure was likely in browser access or proxy handling

#### 2. CORS preflight issue identified
Browser network inspection showed:
- `OPTIONS http://127.0.0.1:8765/mcp`
- response: `501 Unsupported method ('OPTIONS')`

This established that the HTTP MCP server needed browser CORS preflight support.

#### 3. Added minimal CORS support
The HTTP MCP server was updated to:
- implement `OPTIONS /mcp`
- return `204 No Content` for preflight
- return:
  - `Access-Control-Allow-Origin`
  - `Access-Control-Allow-Methods: POST, OPTIONS`
  - `Access-Control-Allow-Headers`

#### 4. Second CORS issue identified
Browser error then reported:
- request header field `mcp-protocol-version` was not allowed by `Access-Control-Allow-Headers`

The HTTP MCP server was updated again so preflight allowed:
- `content-type`
- `mcp-protocol-version`

Manual verification passed:

curl -i -X OPTIONS http://127.0.0.1:8765/mcp \
  -H 'Origin: http://localhost:8080' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type,mcp-protocol-version'

Observed result included:
- `HTTP/1.0 204 No Content`
- `Access-Control-Allow-Origin: http://localhost:8080`
- `Access-Control-Allow-Methods: POST, OPTIONS`
- `Access-Control-Allow-Headers: content-type, mcp-protocol-version`

#### 5. llama.cpp WebUI registration succeeded
Observed in llama.cpp WebUI:
- connected to `http://127.0.0.1:8765/mcp`
- capabilities exchanged successfully
- tools listed successfully
- connection established with 1 tool
- discovered tool: `search_searxng`

Observed protocol version in the WebUI:
- `2025-06-18`

This demonstrated successful browser-side registration and tool discovery.

#### 6. End-to-end tool invocation succeeded
Test prompt used in llama.cpp WebUI:

`Use the search_searxng tool to search the web for "SearXNG GitHub repository" and summarize the top results.`

Observed behavior:
- the model invoked `search_searxng`
- the MCP server returned normalized search results
- the model summarized the results successfully in chat

This completed HIL validation for the intended local llama.cpp WebUI use case.

## Spec/Plan Reconciliation

### Implemented
- Existing stdio MCP server preserved
- New HTTP MCP server entry point added
- Shared search behavior reused through common logic
- Localhost-oriented HTTP development flow implemented
- llama.cpp WebUI registration by URL validated
- end-to-end tool invocation validated
- documentation updated for llama.cpp and validation workflow

### Pending
- Final review for any small cleanup items
- Final commit and repository integration decisions

### Follow-up Review Items
- Confirm whether the legacy `/sse` compatibility path should remain as-is
- Confirm whether any further CORS hardening or localhost restrictions should be documented
- Confirm whether the documentation should mention the specific browser-origin requirement discovered during HIL testing

## Blockers
- None for the validated local development workflow

## Notes
- The implementation moved ahead of the originally intended milestone sequence and was then brought back under HIL-driven review
- The key integration issue during HIL was browser CORS handling, not MCP protocol logic
- Direct `curl` testing was valuable for separating repo-side MCP behavior from browser/WebUI behavior
- llama.cpp WebUI used Streamable HTTP successfully once CORS requirements were satisfied
