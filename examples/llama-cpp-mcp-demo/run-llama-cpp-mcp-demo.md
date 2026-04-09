# Run llama.cpp WebUI With MCP

This runbook shows a local end-to-end demo of the repository's HTTP MCP integration.
Run each component in its own terminal from the repository root.

The demo shows:
- SearXNG search exposed through this repository's MCP server
- llama.cpp WebUI connecting to that MCP server by URL
- the model invoking `search_searxng` and using the results in chat

## Prerequisites

- this repository is checked out locally
- Docker is installed and usable
- Python 3 is available
- the repository's local SearXNG workflow is available
- you can run `tools/searxng/mcp_http_server.py`
- you have access to the tested llama.cpp Docker image:
  - `ghcr.io/nvidia-ai-iot/llama_cpp:gemma4-jetson-orin`

Run commands from the repository root.

## 1. Start SearXNG Locally

Open a terminal in the repository root for the SearXNG process.

Use the repository's existing local workflow. This example uses port `8081`:

```bash
SEARXNG_PORT=8081 bash tools/searxng/install-searxng.sh
```

Optional quick check:

```bash
curl --silent --show-error --fail "http://127.0.0.1:8081/search?q=searxng&format=json"
```

## 2. Start The MCP HTTP Server

Open a second terminal in the repository root for the MCP HTTP server.

Start the repository's HTTP MCP server and point it at the local SearXNG instance:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:8081 \
python3 tools/searxng/mcp_http_server.py --host 127.0.0.1 --port 8765
```

Optional quick check:

```bash
curl --silent --show-error --fail http://127.0.0.1:8765/health
```

## 3. Start llama.cpp In Docker

Open a third terminal for the llama.cpp container.

Start llama.cpp WebUI with MCP proxy support enabled:

```bash
sudo docker run -it --rm --pull always --runtime=nvidia --network host \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  ghcr.io/nvidia-ai-iot/llama_cpp:gemma4-jetson-orin \
  llama-server \
  -hf ggml-org/gemma-4-26B-A4B-it-GGUF:Q4_K_M \
  --jinja \
  --webui-mcp-proxy
```

This model is the tested example model for the demo.
On smaller machines, you may prefer:

```text
ggml-org/gemma-4-E2B-it-GGUF:Q8_0
```

`--webui-mcp-proxy` enables llama.cpp's WebUI MCP proxy for trusted local development and testing.

## 4. Open The WebUI

Open this URL in a web browser:

```text
http://127.0.0.1:8080
```

## 5. Add The MCP Server In The Browser UI

In the WebUI MCP server configuration, enter:

```text
http://127.0.0.1:8765/mcp
```

## 6. Expected Connection Result

When the connection succeeds, the expected behavior is:

- connected
- capabilities exchanged successfully
- tools listed successfully
- connection established with 1 tool
- discovered tool: `search_searxng`

## 7. Demo Prompt

Use this exact prompt:

`Use the search_searxng tool to search the web for "SearXNG GitHub repository" and summarize the top results.`

## 8. Expected Demo Outcome

- the model invokes `search_searxng`
- normalized search results are returned by the MCP server
- the model summarizes the results in chat

## Troubleshooting

- Check the health endpoint:

```bash
curl --silent --show-error --fail http://127.0.0.1:8765/health
```

- Check MCP initialize directly:

```bash
curl --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"0.1.0"}}}' \
  http://127.0.0.1:8765/mcp
```

- Check browser CORS preflight with `OPTIONS /mcp`:

```bash
curl -i -X OPTIONS http://127.0.0.1:8765/mcp \
  -H 'Origin: http://localhost:8080' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type,mcp-protocol-version'
```

Expected response headers include:
- `Access-Control-Allow-Origin: http://localhost:8080`
- `Access-Control-Allow-Methods: POST, OPTIONS`
- `Access-Control-Allow-Headers: content-type, mcp-protocol-version`

- If the browser reports a CORS failure:
  Confirm the MCP server is the repository's current `tools/searxng/mcp_http_server.py` implementation and restart it.

- If MCP does not connect from the browser:
  Confirm `llama-server` was started with `--webui-mcp-proxy`.

- If the browser UI still cannot connect:
  Confirm the MCP URL entered in the UI is exactly `http://127.0.0.1:8765/mcp`.
