# Validation

## Assumptions

- You are running commands from the repository root.
- Docker is installed and the Docker daemon is reachable.
- Python 3 is available.
- Python dependencies are installed from `pyproject.toml`.
- If you want to run the Python examples with the recommended workflow, use `uv sync` followed by `uv run ...`.
- If you prefer standard Python tooling, use a virtual environment before installing dependencies with `pip`.
- OpenClaw validation is documentation-level unless you have OpenClaw installed locally.
- Use the SearXNG port that matches your install configuration. The install script defaults to `8080` unless you set `SEARXNG_PORT`, and the documented validation history also includes examples on `8081`.

## Install, Start, And Uninstall

Install SearXNG locally:

```bash
bash tools/searxng/install-searxng.sh
```

Confirm the local endpoint responds:

```bash
curl --silent --show-error --fail "http://127.0.0.1:<port>/search?q=smoke+test&format=json"
```

The response should be JSON and include a `results` field.

If the container is stopped, start it again:

```bash
bash tools/searxng/start-searxng.sh
```

If stopped containers were pruned after installation, the same command recreates the named container from `.local/searxng/settings.yml` and the local `searxng/searxng:latest` image. Use `SEARXNG_PORT=<port>` when your install used a non-default port.

If you install SearXNG locally on port `8081`, you can also verify the browser-facing interface at:

```text
http://localhost:8081/search
```

Remove the local install:

```bash
bash tools/searxng/uninstall-searxng.sh
```

## Direct Python Search

Validate an explicit base URL:

```bash
python3 tools/searxng/search_searxng.py --base-url http://127.0.0.1:<port> "jetson orin"
```

Validate `SEARXNG_BASE_URL`:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:<port> \
python3 tools/searxng/search_searxng.py "jetson orin"
```

Confirm a clear failure path:

```bash
env -u SEARXNG_BASE_URL \
python3 tools/searxng/search_searxng.py "jetson orin"
```

That failure should return structured JSON with:
- `ok` set to `false`
- `error`

Successful output should include:
- `ok`
- `query`
- `base_url`
- `result_count`
- `results`

## MCP Wrapper

First check the Python entry points parse cleanly:

```bash
python3 -m py_compile \
  tools/searxng/search_searxng.py \
  tools/searxng/mcp_common.py \
  tools/searxng/mcp_server.py \
  tools/searxng/mcp_http_server.py
```

Then start the MCP server:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:<port> python3 tools/searxng/mcp_server.py
```

For a lightweight repository check, confirm the MCP behavior from the implementation and docs:
- `search_searxng`
- required `query`
- optional `base_url`
- optional `limit`
- optional `timeout`
- `ok`
- `query`
- `base_url`
- `result_count`
- `results`

To confirm the failure path without adding extra test machinery:
- start the server without `SEARXNG_BASE_URL`
- use an MCP client or the documented OpenClaw example to call `search_searxng`
- confirm the tool returns structured error output instead of crashing

### HTTP MCP For llama.cpp WebUI

Start the HTTP MCP server:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:<port> \
python3 tools/searxng/mcp_http_server.py --host 127.0.0.1 --port 8765
```

Verify the health endpoint:

```bash
curl --silent --show-error --fail http://127.0.0.1:8765/health
```

Verify the main MCP HTTP endpoint:

```bash
curl --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"0.1.0"}}}' \
  http://127.0.0.1:8765/mcp
```

Verify tool discovery:

```bash
curl --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  http://127.0.0.1:8765/mcp
```

For llama.cpp WebUI registration, use:

```text
http://127.0.0.1:8765/mcp
```

If your local client still expects the older SSE transport, use:

```text
http://127.0.0.1:8765/sse
```

## OpenClaw Example

Validate the OpenClaw example at the documentation level by checking that `examples/openclaw/README.md` matches:
- the command `python3 tools/searxng/mcp_server.py`
- the working directory requirement of the repository root
- the environment expectation `SEARXNG_BASE_URL`
- the tool name `search_searxng`
- the implemented required and optional arguments

## Skill

Validate the skill at the documentation level by checking that `skills/searxng-search/SKILL.md` matches:
- the MCP tool name `search_searxng`
- the implemented inputs `query`, optional `base_url`, optional `limit`, optional `timeout`
- the structured success shape
- the structured error shape
- the `SEARXNG_BASE_URL` expectation when `base_url` is not provided

## OpenAI-Compatible Tool Calling

The first OpenAI-compatible tool-calling path has been validated end to end against a llama.cpp OpenAI-compatible endpoint at `http://127.0.0.1:8080/v1` and a local SearXNG instance at `http://localhost:8081`.

See `examples/openai-compatible-tool-calling/README.md` for the validated command and the manual validation workflow.

The OpenAI-compatible function tool in that example is named `searxng_search`.
This is intentionally separate from the MCP tool name `search_searxng`.

## Standalone Skill Demo

Validate the standalone skill demo at the lightweight level:

```bash
python3 -m py_compile examples/skill-demo/simple_agent.py
```

Then compare `examples/skill-demo/README.md` against the implementation:
- local function tool name `search_searxng`
- model-facing inputs `query` and optional `limit`
- script-level SearXNG settings `--searxng-base-url`, `SEARXNG_BASE_URL`, and `--timeout`
- optional skill loading from `--skill`
- optional model-only comparison from `--no-search-tool`

## llama.cpp WebUI MCP Demo

Validate the llama.cpp WebUI runbook at the documentation level by checking that `examples/llama-cpp-mcp-demo/run-llama-cpp-mcp-demo.md` matches:
- the HTTP MCP command `python3 tools/searxng/mcp_http_server.py --host 127.0.0.1 --port 8765`
- the default MCP URL `http://127.0.0.1:8765/mcp`
- the health endpoint `http://127.0.0.1:8765/health`
- the discovered MCP tool name `search_searxng`
- the CORS preflight headers implemented by `tools/searxng/mcp_http_server.py`

## Development History

The development-history documents live under `dev/`.
Use them for implementation history and status tracking, not as the primary reader path through the repository.
