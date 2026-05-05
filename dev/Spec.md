# Spec

## Purpose

Build a practical reference project that shows how to use SearXNG as the basis for an agent-facing search tool.

## Motivation

SearXNG provides free, private web search with structured JSON output. That makes it a strong fit for AI agents and other automated tools: no advertising, better control of the workflow, and results that are easier to process in code.

## Primary Objectives

- Install and uninstall SearXNG cleanly
- Verify that a local SearXNG instance is running and reachable
- Query SearXNG directly from Python
- Demonstrate OpenAI-compatible tool calling
- Wrap the search capability with MCP
- Provide both stdio and HTTP MCP entry points
- Demonstrate integration with OpenClaw
- Add a project-owned search skill

## Guiding Principles

- Start from first principles
- Keep the implementation readable and inspectable
- Separate core search logic from agent-specific integration
- Delay packaging and distribution concerns beyond the minimal dependency metadata needed to run the examples
- Prefer simple working code over premature abstraction

## Initial Scope

### In scope
- Local installation workflow for SearXNG
- Local uninstallation workflow for SearXNG
- Python search demonstration against a local SearXNG instance
- OpenAI-compatible tool-calling example against a configurable model endpoint
- MCP wrapper for the search capability
- HTTP MCP wrapper for browser-facing clients
- Example integration with OpenClaw
- A checked-in search skill in the repository
- Standalone skill behavior demo

### Out of scope for now
- Packaging and release automation
- Multiple agent integrations beyond OpenClaw
- Exhaustive provider coverage
- Production deployment hardening
- Hosted infrastructure
- User interface work beyond what is needed for demonstration

## Success Criteria

### Milestone 1 is complete when
- Installer script brings up SearXNG successfully
- Uninstaller removes it cleanly
- A smoke test confirms that the local endpoint responds

### Project is meaningfully complete when
- A student can follow the repository from service installation to agent integration
- Each stage is understandable on its own
- The core search capability remains usable outside any single agent framework
- Documentation names the implemented tool boundaries accurately
