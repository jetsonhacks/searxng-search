# Plan

## Implementation Steps

1. Add `examples/openai-compatible-tool-calling/` as the user-facing example directory for this feature.
2. Add a concise example README that explains:
   - the purpose of the example
   - the provider-agnostic OpenAI-compatible assumptions
   - the expected environment and command-line inputs
   - the standard tool-calling loop
3. Add a small Python example script that accepts:
   - an LLM API base URL
   - a model name
   - a prompt
   - optional SearXNG base URL, result limit, and timeout
4. Reuse the existing helpers from `tools/searxng/search_searxng.py` for:
   - SearXNG base URL resolution
   - search URL construction
   - response fetching
   - result normalization
5. Define a `searxng_search` tool schema in the example and implement a single clear tool-calling loop.
6. Update user-facing docs in `docs/` to include the browser-facing SearXNG URL `http://localhost:8081/search`.
7. Update repository guidance so the teaching progression is explicit:
   1. Browser use
   2. Python use
   3. OpenAI-compatible tool calling
   4. MCP

## Expected File-Level Changes

- Add `dev/features/openai-compatible-tool-calling/Spec.md`
- Add `examples/openai-compatible-tool-calling/README.md`
- Add `examples/openai-compatible-tool-calling/tool_calling_example.py`
- Update `README.md`
- Update `docs/Architecture.md`
- Update `docs/Validation.md`

## Validation Steps

- Confirm the browser-facing docs point to `http://localhost:8081/search`
- Confirm the example is documented as OpenAI-compatible rather than provider-specific
- Confirm the example accepts a configurable API base URL and model name
- Confirm the planned tool schema is named `searxng_search`
- Confirm the example reuses the existing repository search logic instead of duplicating the SearXNG request path
- Confirm the repository progression is understandable from browser use through MCP

## Documentation Updates

- Add the browser URL to user-facing docs
- Add the new example to the repository reader path
- Keep `docs/` user-facing and keep feature planning details under `dev/`
- Keep the wording practical, concise, and educational
