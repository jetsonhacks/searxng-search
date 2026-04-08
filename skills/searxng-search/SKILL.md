---
name: searxng-search
description: Use SearXNG-backed web search for current public information when local project context is not enough.
---

# SearXNG Search

Use this skill when current public web information is needed and local repository context is not enough.

## When To Use It

Use this SearXNG-backed search capability when:
- the task depends on current public web information
- local files do not already contain the answer
- structured search results are more useful than free-form browsing

## Tool Boundary

This skill uses one MCP tool:
- `search_searxng`

The tool accepts:
- `query` as a required string
- `base_url` as an optional string
- `limit` as an optional integer
- `timeout` as an optional number

If `base_url` is not provided, the MCP server expects `SEARXNG_BASE_URL` to be set in the server environment.

## Expected Result Shape

The tool returns structured JSON text with:
- `ok`
- `query`
- `base_url`
- `result_count`
- `results`

Each item in `results` includes:
- `title`
- `url`
- `engine`
- `content`
- `score`

If the request fails, the tool returns structured JSON text with:
- `ok`
- `error`

## Practical Use

- Start with a focused `query`
- Keep `limit` small unless more coverage is necessary
- Treat `content` snippets as leads to verify, not final proof
- For OpenClaw usage, stay within the MCP boundary described in `examples/openclaw/README.md`