# Spec

## Purpose

Build a practical reference project that shows how to use SearXNG as the basis for an agent-facing search tool.

## Motivation

SearXNG provides free, private web search with structured JSON output. That makes it a strong fit for AI agents and other automated tools: no advertising, better control of the workflow, and results that are easier to process in code.

## Primary Objectives

- Install and uninstall SearXNG cleanly
- Verify that a local SearXNG instance is running and reachable
- Query SearXNG directly from Python
- Wrap the search capability with MCP
- Demonstrate integration with OpenClaw
- Add a project-owned skill for OpenClaw

## Guiding Principles

- Start from first principles
- Keep the implementation readable and inspectable
- Separate core search logic from agent-specific integration
- Delay packaging and distribution concerns until the basic workflow is proven
- Prefer simple working code over premature abstraction

## Initial Scope

### In scope
- Local installation workflow for SearXNG
- Local uninstallation workflow for SearXNG
- Python search demonstration against a local SearXNG instance
- MCP wrapper for the search capability
- Example integration with OpenClaw
- A checked-in OpenClaw skill in the repository

### Out of scope for now
- Packaging and release automation
- Multiple agent integrations beyond OpenClaw
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