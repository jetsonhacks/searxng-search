# SearXNG Search Controls Map Cleanly To Agent Interfaces

SearXNG uses the same `/search` surface for both browser-facing use and machine-facing use. A person can open a URL such as `http://localhost:8081/search`, fill out the search form, and use the interface interactively. A program can call that same surface with query parameters and request JSON output.

This is a useful design property for this repository. It means the browser experience and the programmatic experience are not separate systems. They are different ways of driving the same search surface.

That is educationally useful here because the repository is meant to teach the progression from first principles. Readers can start with the visible browser interface, then trace the same search surface into Python, tool calling, and MCP without having to learn a different search system at each step.

## Human Syntax Versus Agent Controls

SearXNG already exposes useful controls through query parameters. For example, categories and engines can be selected directly, and time filtering can be represented explicitly. That makes the `/search` endpoint more expressive than a plain free-text search box.

Bang syntax is convenient for humans because it compresses intent into short text. A person can remember a shorthand and type it quickly in the browser. That is a good fit for manual use.

It is not the ideal primary interface for agents. An agent usually does better with explicit structured arguments than with a compact text convention that must be generated and parsed correctly.

What is tedious for humans can become structured control for agents. A person may not want to repeatedly click advanced controls or hand-author long query strings, but an agent can set fields such as `category`, `engines`, and `time_range` directly when those fields are exposed through a tool schema.

## Why This Matters Here

This repository is adding OpenAI-compatible tool-calling examples and already includes an MCP example. In both cases, the important question is not only how to call SearXNG, but how to present SearXNG in a form that matches the strengths of tool-using models.

For OpenAI-compatible tool calling, structured arguments make the tool contract clearer. A model can choose fields intentionally instead of hiding everything inside one search string.

For MCP, the same idea applies. A tool schema with explicit arguments is easier to inspect, validate, and reuse than a tool that expects the model to encode all search intent inside ad hoc text.

## Implications For This Repository

- Keep teaching the progression from browser use to Python, then to OpenAI-compatible tool calling, then to MCP.
- In the Python example, keep the direct search path easy to inspect and leave room for explicit advanced parameters over time.
- In the OpenAI-compatible example, prefer a tool schema with agent-friendly fields such as `category`, `engines`, and `time_range`.
- In the MCP example, expose the same kind of structured controls instead of relying on one free-text query string for everything.
- Treat bang syntax as a useful human shortcut, not as the primary machine interface.
