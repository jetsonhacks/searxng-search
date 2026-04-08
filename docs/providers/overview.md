# Provider Overview

The OpenAI-compatible tool-calling example in this repository needs a model endpoint that speaks an OpenAI-compatible API.

This repository integrates against the OpenAI-compatible boundary, not against one provider-specific stack. That is why provider launch recipes are documented separately from the core feature implementation.

The core capability in this repository is:

- SearXNG browser access
- SearXNG programmatic search from Python
- OpenAI-compatible tool calling against a compatible model endpoint
- MCP exposure

Provider-specific runtime artifacts are separate:

- launch commands
- model-server flags
- Jetson-oriented container commands
- model-specific notes
- Docker recipes

Keep using the core examples under `examples/` to understand the repository capability. Use the provider docs under `docs/providers/` when you need to stand up a compatible model endpoint for those examples.

## Current Provider Notes

- `llama-cpp.md` covers the first validated provider path in this repository

Additional provider docs can be added later once they have been tested in this repository.
