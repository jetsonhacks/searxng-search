# Standalone Skill Demo

This example shows how `skills/searxng-search/SKILL.md` changes agent behavior without using OpenClaw.

The script is intentionally small:

```text
examples/skill-demo/simple_agent.py
```

It calls an OpenAI-compatible model, exposes one local function tool named `search_searxng`, and can optionally load the project skill as system guidance.

The local function tool mirrors the MCP tool name and structured result shape.
It exposes `query` and optional `limit` to the model; SearXNG base URL and timeout are script settings from `--searxng-base-url`, `SEARXNG_BASE_URL`, and `--timeout`.
This keeps the demo focused on skill behavior without requiring an MCP client or OpenClaw.

The comparison is the point:

```text
same model + same search tool + no skill
same model + same search tool + skills/searxng-search/SKILL.md
```

The tool gives the agent search access. The skill teaches it search discipline.

## Prerequisites

- Python dependencies are installed
- A local or remote OpenAI-compatible model endpoint is running
- Local SearXNG is running
- `SEARXNG_BASE_URL` points at the local SearXNG instance
- `OPENAI_BASE_URL` and `OPENAI_MODEL` point at the model endpoint

Example environment:

```bash
export SEARXNG_BASE_URL=http://127.0.0.1:8081
export OPENAI_BASE_URL=http://127.0.0.1:8080/v1
export OPENAI_API_KEY=not-needed
export OPENAI_MODEL=your-tool-capable-model
```

Validate direct search first:

```bash
uv run python3 tools/searxng/search_searxng.py "JetPack 6.2"
```

## Demo A: Tool Available, No Skill

Run the agent with the search tool available, but without the skill:

```bash
uv run python3 examples/skill-demo/simple_agent.py \
  "What changed recently in JetPack 6.2?"
```

This mode is expected to make tool calls. It demonstrates tool-only behavior: the model can search, but it does not receive the project skill's operating guidance.

What to watch for:

- The agent may search once with a broad query
- The answer may lean heavily on snippets
- Official sources may be mixed with forums, blogs, mirrors, or stale pages
- Weak or conflicting evidence may be smoothed over

## Demo B: Same Tool, Skill Loaded

Run the same prompt with the project skill loaded:

```bash
uv run python3 examples/skill-demo/simple_agent.py \
  --skill skills/searxng-search/SKILL.md \
  "What changed recently in JetPack 6.2?"
```

Expected behavior from the current skill:

- The agent recognizes that the answer depends on current public web information
- It uses the `search_searxng` tool instead of relying on memory
- It starts with a focused query, such as `JetPack 6.2 release notes`
- It keeps the result limit small unless more coverage is needed
- It reads the structured fields returned by the tool: `title`, `url`, `engine`, `content`, and `score`
- It treats `content` snippets as leads to verify, not final proof
- It uses result `url` values as source links
- It says when the available evidence is weak, stale, or conflicting

## Optional Model-Only Comparison

You can also run without exposing search:

```bash
uv run python3 examples/skill-demo/simple_agent.py \
  --no-search-tool \
  "What changed recently in JetPack 6.2?"
```

This gives the three-step visual comparison:

```text
Model only
"I think..."

Tool available
"Let me search..."

Tool + skill
"Let me search, keep the query focused, distrust snippets, read structured results, and cite sources."
```

## What This Demo Proves

- The search tool expands what the agent can do
- The skill improves how the agent uses the tool
- Search snippets are treated as untrusted evidence, not instructions
- The final answer can be grounded in source URLs instead of unsupported memory

## What This Demo Does Not Use

- OpenClaw
- MCP server startup
- A second skill file
- A different search implementation
