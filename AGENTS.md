# AGENTS.md

This repository is a practical walk through of building a SearXNG-based search tool from first principles.

## Goals

- Install and uninstall SearXNG cleanly
- Demonstrate SearXNG search from Python
- Expose search through MCP
- Show integration with OpenClaw
- Add a project-owned OpenClaw skill

## Constraints

- Keep the project agent-agnostic until the OpenClaw example phase
- Do not introduce packaging or distribution machinery unless explicitly requested
- Prefer simple, readable Python and shell scripts
- Keep functions small and easy to inspect
- Favor structured output over prose when writing tool code
- Add clear error handling
- Do not make unrelated changes

## Workflow

- Work one milestone at a time
- Prefer small diffs
- Explain what was changed and how it was validated
- Keep `docs/development/Status.md` up to date when milestones change or important implementation decisions are made
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

## Current Priority

Implement Milestone 1:
- `tools/searxng/install-searxng.sh`
- `tools/searxng/uninstall-searxng.sh`

These scripts should prepare the system for a clean local SearXNG install and removal, and should be easy to inspect and understand.
