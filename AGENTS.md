# AGENTS.md

This repository is a practical walk through of building a SearXNG-based search tool from first principles.

This file is the operational guide for coding agents working in this repository.

## Goals

- Install and uninstall SearXNG cleanly
- Restart a local SearXNG install after the container has stopped or been pruned
- Demonstrate SearXNG search from Python
- Expose search through MCP
- Demonstrate OpenAI-compatible tool calling
- Show integration with OpenClaw
- Add a project-owned search skill

## Constraints

- Keep the project agent-agnostic until the OpenClaw example phase
- Do not introduce packaging or distribution machinery unless explicitly requested
- Prefer simple, readable Python and shell scripts
- Keep functions small and easy to inspect
- Favor structured output over prose when writing tool code
- Add clear error handling
- Do not make unrelated changes

## Workflow

- Work one focused phase at a time
- Prefer small diffs
- Explain what was changed and how it was validated
- Keep `dev/Status.md` up to date when project phases change or important implementation decisions are made
- Preserve the learning value of the repository; do not hide important steps behind unnecessary abstractions

## Coding Style

### Shell scripts
- Use `bash`
- Use `set -euo pipefail`
- Add comments for non-obvious sections
- Print clear status and error messages

### Python
- Target readability first
- Use standard library where practical
- Add docstrings for public functions
- Prefer explicit argument parsing and explicit error handling

## Documentation Style

- Keep documentation direct and practical
- Write for readers who want to understand how the system works
- Avoid marketing language
- Keep the project grounded in first principles
- Keep `docs/` user-facing
- Keep `dev/` for development artifacts such as plans, status, feature specs, and ADRs

## Current Priority

The initial implementation phases are complete.

Current maintenance priority:
- Keep documentation aligned with the implemented code
- Keep examples small, inspectable, and easy to validate
- Preserve the distinction between core search behavior, MCP boundaries, OpenAI-compatible examples, OpenClaw integration, and skill guidance
- Update `dev/Status.md` when important implementation or documentation decisions change
