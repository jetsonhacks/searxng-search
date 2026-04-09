# Feature Spec: llama.cpp MCP HTTP Integration

## Summary

Add an HTTP-accessible MCP server entry point for the existing SearXNG MCP tool so that llama.cpp WebUI can register and use the tool by URL.

The repository already contains a working stdio MCP server. That behavior must remain intact. This feature adds a second transport path for browser-facing and URL-addressable MCP clients, especially llama.cpp WebUI.

## Problem

The current repository implementation exposes SearXNG search through a stdio MCP server. That is suitable for local subprocess clients, but llama.cpp WebUI allows users to add an MCP server by entering a server URL in the browser UI.

Because of that, the current stdio-only MCP server is not sufficient for llama.cpp integration.

We need a transport-compatible MCP server that can be reached over HTTP, while preserving the current stdio MCP implementation and reusing the same search logic.

## Goals

1. Preserve the existing stdio MCP server behavior.
2. Add an HTTP MCP server entry point for the same SearXNG-backed tool.
3. Reuse existing transport-neutral search logic and validation where possible.
4. Support local testing with llama-server and llama.cpp WebUI.
5. Document the launch and validation flow.

## Non-Goals

1. Replacing the existing stdio MCP server.
2. Redesigning the core SearXNG search logic.
3. Introducing packaging or distribution changes.
4. Building a generalized MCP framework for all future transports.
5. Solving every possible remote deployment or authentication scenario.

## User Story

As a developer using llama.cpp WebUI,
I want to add the project’s SearXNG MCP server by URL,
so that prompts in the browser can invoke live search through the repo’s MCP implementation.

## Functional Requirements

### FR1. Existing stdio MCP server remains supported
The current stdio MCP server must continue to work after this feature is added.

### FR2. New HTTP MCP entry point
The repository must provide a second MCP server entry point that is reachable over HTTP.

### FR3. Shared tool behavior
The HTTP MCP server must expose the same SearXNG search capability as the stdio MCP server, using the same underlying search logic, argument validation, and result normalization wherever practical.

### FR4. Localhost-oriented operation
The HTTP MCP server must be runnable locally for development, with a host and port that can be used from llama.cpp WebUI.

### FR5. Browser registration path
The project documentation must describe how to add the MCP server URL in llama.cpp WebUI.

### FR6. Validation path
The feature must include a documented validation flow showing:
- SearXNG is running
- the HTTP MCP server is running
- llama-server is running
- the WebUI can register the MCP server
- a prompt can successfully invoke the search tool

## Technical Requirements

1. Shared search behavior should continue to live in transport-neutral code where possible.
2. The HTTP server implementation should avoid duplicating core search logic.
3. The HTTP transport should be implemented in a way that is compatible with current llama.cpp MCP expectations.
4. The implementation should bind to localhost by default for development.
5. The feature should keep repository structure simple and understandable.

## Constraints

1. Keep the project agent-agnostic except for the llama.cpp example and documentation required by this feature.
2. Do not introduce packaging or distribution work.
3. Do not remove or break current examples that depend on stdio MCP behavior.
4. Prefer a minimal, practical implementation over a broad abstraction layer.

## Proposed Repository Impact

Likely areas of change:

- `tools/searxng/mcp_server.py` if minor refactoring is needed
- `tools/searxng/search_searxng.py` for shared logic cleanup if needed
- `tools/searxng/mcp_http_server.py` as a new HTTP MCP entry point
- repository documentation for llama.cpp usage
- dependency/setup notes if the HTTP MCP path introduces a new runtime dependency

## Acceptance Criteria

1. The existing stdio MCP server still functions as before.
2. A new HTTP MCP server can be started locally from the repository.
3. The HTTP MCP server exposes the same SearXNG-backed tool behavior.
4. llama.cpp WebUI can register the MCP server by URL.
5. A user prompt in llama.cpp WebUI can trigger the tool and receive a search-backed result.
6. The repository documents the steps needed to run and test the integration.

## Test Scenarios

### Scenario 1: Existing stdio path still works
- Start the current stdio MCP server path.
- Run the existing validation flow.
- Confirm behavior is unchanged.

### Scenario 2: HTTP MCP server starts cleanly
- Start SearXNG locally.
- Start the HTTP MCP server locally.
- Confirm the server is reachable at the documented URL.

### Scenario 3: llama.cpp WebUI registration
- Start llama-server with the required WebUI options.
- Open the browser UI.
- Add the MCP server URL.
- Confirm the MCP server registers successfully.

### Scenario 4: End-to-end search invocation
- Prompt the model to perform a web search.
- Confirm the SearXNG MCP tool is invoked.
- Confirm the result is returned through the llama.cpp flow.

## Risks

1. llama.cpp MCP support may still be evolving.
2. HTTP transport compatibility details may differ across llama.cpp revisions.
3. Browser/proxy/CORS behavior may complicate local testing.
4. The MCP HTTP implementation may require a new dependency or runtime pattern.

## Open Questions

1. Which MCP HTTP transport mode should be used first for llama.cpp compatibility?
2. Should the HTTP server support only the main current transport, or also a compatibility fallback?
3. What is the minimum documentation needed to keep this repo practical without over-expanding scope?
```

---

# `dev/features/llama-cpp-mcp-http/Plan.md`

```md
# Feature Plan: llama.cpp MCP HTTP Integration

## Objective

Implement and document an HTTP-accessible MCP server entry point for the existing SearXNG MCP tool so llama.cpp WebUI can register and use it by URL, while preserving the current stdio MCP server.

## Implementation Strategy

Take an additive approach.

Do not replace the existing stdio MCP server. Instead, introduce a second MCP server entry point for HTTP clients and keep the core search behavior shared between both transports.

## Work Plan

### 1. Review the current MCP and search implementation

Inspect the existing files and confirm current boundaries:

- `tools/searxng/mcp_server.py`
- `tools/searxng/search_searxng.py`

Goals of the review:
- identify what is already transport-neutral
- identify any stdio-specific logic mixed into tool behavior
- identify the exact search tool schema currently exposed

### 2. Refactor shared behavior only if needed

If necessary, perform a small refactor so that shared behavior is clearly reusable by both transports.

Possible shared concerns:
- argument validation
- base URL handling
- request construction
- search execution
- result normalization
- response shaping for the tool result

This step should remain minimal. Avoid broad architectural changes.

### 3. Add a new HTTP MCP server entry point

Create a new file:

- `tools/searxng/mcp_http_server.py`

This new entry point should:
- expose the same SearXNG-backed tool as the stdio server
- run locally with host and port configuration
- default to localhost-oriented development usage
- reuse shared search logic

### 4. Decide and implement the HTTP MCP runtime approach

Choose the implementation approach that best fits the repo’s practical goals.

Selection criteria:
- compatibility with current llama.cpp MCP behavior
- minimal complexity
- readable implementation
- small dependency footprint
- clear local run story

Document the choice in code comments or feature notes as appropriate.

### 5. Preserve current stdio behavior

Confirm the existing stdio MCP server remains intact.

If any shared refactoring is performed, verify that it does not change existing behavior or invocation shape for current users.

### 6. Add or update documentation

Document the new workflow in the repository.

Documentation should cover:
- starting SearXNG
- starting the HTTP MCP server
- starting llama-server with the relevant options
- adding the MCP server URL in llama.cpp WebUI
- verifying end-to-end operation

Keep the documentation practical and local-development oriented.

### 7. Validate end-to-end behavior

Perform hands-on validation against the real stack.

Required validation:
- stdio MCP path still works
- HTTP MCP server starts and is reachable
- llama.cpp WebUI accepts the MCP server URL
- a prompt can invoke the search tool successfully

## Deliverables

1. New HTTP MCP server entry point in `tools/searxng/`
2. Any minimal shared-logic refactor needed to support both transports
3. Updated documentation for llama.cpp integration
4. Validation notes captured in the feature workflow or commit history

## Acceptance Checklist

- [ ] Existing stdio MCP flow still works
- [ ] New HTTP MCP server exists and runs locally
- [ ] Shared SearXNG search logic is reused
- [ ] llama.cpp WebUI can register the MCP server by URL
- [ ] End-to-end tool invocation works from the browser UI
- [ ] Documentation is updated

## Testing Approach

### Smoke Test 1: Existing stdio path
- run the current stdio MCP flow
- confirm no regression

### Smoke Test 2: HTTP MCP startup
- start the new HTTP MCP server
- confirm it starts without errors
- confirm the expected endpoint is reachable

### Smoke Test 3: llama.cpp registration
- start llama-server with the required WebUI options
- add the MCP server in the browser UI
- confirm registration succeeds

### Smoke Test 4: Tool invocation
- submit a prompt that requires web search
- confirm the MCP tool is invoked
- confirm results flow back into the model response

## Risks and Mitigations

### Risk: llama.cpp MCP behavior changes upstream
Mitigation:
Keep the feature narrow, document the tested workflow, and avoid overcommitting to unstable optional behavior.

### Risk: HTTP MCP implementation adds complexity
Mitigation:
Prefer the smallest implementation that satisfies the local llama.cpp integration path.

### Risk: CORS or proxy behavior complicates testing
Mitigation:
Document the exact launch configuration used for successful validation.

### Risk: Shared refactor breaks stdio flow
Mitigation:
Refactor only where needed and validate the existing path immediately after changes.

## Suggested Execution Order for Codex Agent

1. inspect current MCP and search files
2. identify minimal shared refactor
3. implement `mcp_http_server.py`
4. verify stdio path still works
5. add llama.cpp integration documentation
6. record exact validation steps and outcomes

## Definition of Done

This feature is complete when the repo supports both:
- the original stdio MCP server path
- a new HTTP MCP server path usable from llama.cpp WebUI by URL

and the full local workflow is documented and validated.

