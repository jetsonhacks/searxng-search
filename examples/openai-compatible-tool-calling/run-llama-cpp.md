# Run With llama.cpp

This is a tested path for running the OpenAI-compatible tool-calling example in this repository.

It assumes:

- llama.cpp is serving an OpenAI-compatible endpoint on `http://127.0.0.1:8080/v1`
- SearXNG is running on `http://localhost:8081`

Run the commands from the repository root with the virtual environment activated.

If you need a llama.cpp server launch example, see `docs/providers/llama-cpp.md`.
If you need the local SearXNG startup step, see the Quick Start section in `README.md`.

If you want the browser-facing MCP path for llama.cpp WebUI instead of the OpenAI-compatible example, this repository now also includes `tools/searxng/mcp_http_server.py`.

## Setup

Create or sync the environment if needed, then activate `.venv`:

```bash
uv sync
. .venv/bin/activate
```

If you are not using `uv`, create the virtual environment and install dependencies first, then activate `.venv`.

## Validate The Endpoints

Verify the model ID:

```bash
curl -s http://127.0.0.1:8080/v1/models | jq -r '.data[0].id'
```

Verify SearXNG:

```bash
curl "http://localhost:8081/search?q=searxng&format=json"
```

Use the exact model ID returned by `/v1/models`.

## Run The Example

From the repository root, with `.venv` activated:

```bash
python examples/openai-compatible-tool-calling/tool_calling_example.py \
  --base-url http://127.0.0.1:8080/v1 \
  --api-key not-needed \
  --model ggml-org/gemma-4-26B-A4B-it-GGUF:Q4_K_M \
  --searxng-base-url http://localhost:8081 \
  --prompt "Use the search tool to look up SearXNG and give me a short summary of the project."
```

## Troubleshooting

- Connection refused:
  Confirm llama.cpp is running and listening on `http://127.0.0.1:8080/v1`.
- Wrong model ID:
  Query `/v1/models` again and use the exact returned model ID.
- No tool call:
  Use a tool-capable model and a prompt that clearly asks for search.

## MCP HTTP Option For WebUI

When you want to register this repository's search tool in llama.cpp WebUI by URL:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:8081 \
python3 tools/searxng/mcp_http_server.py --host 127.0.0.1 --port 8765
```

Then use:

```text
http://127.0.0.1:8765/mcp
```

If your local llama.cpp build still expects the older SSE transport, try:

```text
http://127.0.0.1:8765/sse
```
