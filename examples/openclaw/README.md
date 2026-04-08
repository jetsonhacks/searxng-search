# OpenClaw MCP Example

This example shows how to connect OpenClaw to the repository's MCP search server without changing the core search logic.

The integration boundary is `tools/searxng/mcp_server.py`.
OpenClaw talks to that MCP server over stdio, and the MCP server reuses the existing Milestone 2 SearXNG search behavior.

## What This Example Covers

- start the repository MCP server
- point OpenClaw at that server
- call the `search_searxng` MCP tool from OpenClaw
- validate the setup with a simple query

## Prerequisites

- SearXNG is installed and reachable locally
- OpenClaw is installed on your machine
- `SEARXNG_BASE_URL` points at the local SearXNG instance

Example:

```bash
export SEARXNG_BASE_URL=http://127.0.0.1:8081
python3 tools/searxng/search_searxng.py "jetson orin"
```

That command should return structured JSON results before you involve OpenClaw.

## MCP Server Command

Use this command for the MCP server process:

```bash
python3 tools/searxng/mcp_server.py
```

Use this environment for the server:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:8081
```

## OpenClaw Setup

Add a stdio MCP server in OpenClaw that runs:

```bash
python3 tools/searxng/mcp_server.py
```

Set the working directory to the repository root:

```text
/home/jim/searxng-search
```

Set this environment variable for the server process:

```text
SEARXNG_BASE_URL=http://127.0.0.1:8081
```

Once connected, OpenClaw should discover one MCP tool:

```text
search_searxng
```

## Example Tool Call

The MCP tool expects this argument shape:

```json
{
  "query": "jetson orin",
  "limit": 5,
  "timeout": 10.0
}
```

The response content is structured JSON text with the same normalized fields used by the Milestone 2 command-line search:

- `ok`
- `query`
- `base_url`
- `result_count`
- `results`

Each result includes:

- `title`
- `url`
- `engine`
- `content`
- `score`

## Example OpenClaw Prompt

Use a prompt like this after the MCP server is connected:

```text
Use the search_searxng tool to search for "jetson orin" and summarize the top three results.
```

This keeps the OpenClaw-specific behavior in the example only. The search implementation still lives in the reusable Python and MCP layers.

## Practical Validation

1. Confirm local SearXNG works directly:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:8081 \
python3 tools/searxng/search_searxng.py "jetson orin"
```

2. Start or register the MCP server in OpenClaw with:

```bash
python3 tools/searxng/mcp_server.py
```

3. Verify OpenClaw shows the `search_searxng` tool.

4. Ask OpenClaw to call the tool with a small query such as `jetson orin`.

5. Confirm the tool result contains structured JSON text with `ok: true`, `result_count`, and a normalized `results` list.

6. Test an error path by removing `SEARXNG_BASE_URL` from the MCP server environment and reconnecting. Confirm the tool returns structured error output instead of crashing.

## What This Example Does Not Do

- It does not change `tools/searxng/search_searxng.py`
- It does not change `tools/searxng/mcp_server.py`
- It does not add an OpenClaw skill
- It does not introduce packaging or distribution setup
