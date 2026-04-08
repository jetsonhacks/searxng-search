# Spec

## Problem Statement

The repository currently shows direct Python search, MCP exposure, and an OpenClaw example, but it does not yet show the common middle path where an OpenAI-compatible model calls a local search tool directly through a tool-calling loop.

That gap makes it harder for readers to understand how SearXNG fits both as a browser-facing web application and as a machine-facing search service that can be used before MCP is introduced.

## Why This Matters For Learners

- Show the browser-facing SearXNG interface at `http://localhost:8081/search`
- Show the progression from manual browser use to programmatic search
- Provide a small, inspectable OpenAI-compatible tool-calling example
- Keep the example useful across providers that expose an OpenAI-compatible API
- Reuse the existing repository search behavior instead of introducing a second search implementation

## Scope

In scope:
- A user-facing example under `examples/` for OpenAI-compatible tool calling
- Documentation that explicitly shows browser access to local SearXNG on port `8081`
- A simple tool-calling flow that defines a `searxng_search` tool and runs one tool-calling loop
- Provider-agnostic configuration for API base URL and model name
- Reuse of the existing SearXNG search logic where practical

Out of scope:
- Provider-specific SDK wrappers beyond what is needed for a simple example
- Packaging, distribution, or release changes
- Multiple example implementations for every OpenAI-compatible provider
- Replacing the existing MCP example
- Hosted deployment or production hardening

## Non-Goals

- Do not make the repository provider-specific
- Do not introduce framework-heavy abstractions
- Do not duplicate the SearXNG request and normalization logic if the existing Python code can be reused
- Do not change the core project direction away from first-principles teaching

## Proposed Repository Changes

- Add `dev/features/openai-compatible-tool-calling/Plan.md`
- Add a user-facing example directory under `examples/openai-compatible-tool-calling/`
- Add a small example script that:
  - accepts an OpenAI-compatible API base URL
  - accepts a model name
  - defines a `searxng_search` tool schema
  - sends a prompt and tool schema to the model
  - detects a tool call
  - runs the existing SearXNG search flow
  - returns the tool result to the model
  - prints the final answer
- Add or keep a small example layout under `examples/openai-compatible-tool-calling/` with:
  - `README.md` for setup and walkthrough
  - `tool_calling_example.py` for the minimal tool-calling loop
- Update user-facing docs to show that local SearXNG on port `8081` is available in a browser at `http://localhost:8081/search`
- Update repository docs to teach this progression:
  1. Browser use of SearXNG
  2. Python programmatic use
  3. OpenAI-compatible tool calling
  4. MCP exposure

## Example Flow

1. Start local SearXNG on port `8081`
2. Open `http://localhost:8081/search` in a browser and run a manual search
3. Run the existing Python search example against the same local SearXNG instance
4. Run the OpenAI-compatible tool-calling example with:
   - a configurable LLM API base URL
   - a configurable model name
   - a prompt that may trigger `searxng_search`
5. The example sends the prompt and tool schema to the model
6. If the model requests `searxng_search`, the example runs the existing SearXNG search logic
7. The example returns the structured tool result to the model
8. The model produces a final answer
9. The reader can then compare this flow with the existing MCP example

## Acceptance Criteria

- `dev/features/openai-compatible-tool-calling/Plan.md` exists and matches this spec
- User-facing docs explicitly show `http://localhost:8081/search`
- The repository docs explain SearXNG as both a browser-facing app and a machine-facing service
- The example design stays provider-agnostic across OpenAI-compatible APIs where practical
- The planned example uses a configurable API base URL and model name
- The planned example defines `searxng_search` and follows a standard tool-calling loop
- The planned example reuses existing repository search logic where practical
- The new example lives under `examples/`
- No packaging or distribution changes are introduced
