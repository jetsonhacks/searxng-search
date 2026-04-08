# Validation

## Assumptions

- You are running commands from the repository root.
- Docker is installed and the Docker daemon is reachable.
- Python 3 is available.
- OpenClaw validation is documentation-level unless you have OpenClaw installed locally.
- Use the SearXNG port that matches your install configuration. The install script defaults to `8080` unless you set `SEARXNG_PORT`, and the documented validation history also includes examples on `8081`.

## Milestone 1: Install And Uninstall

Install SearXNG locally:

```bash
bash tools/searxng/install-searxng.sh
```

Confirm the local endpoint responds:

```bash
curl --silent --show-error --fail "http://127.0.0.1:<port>/search?q=smoke+test&format=json"
```

The response should be JSON and include a `results` field.

Remove the local install:

```bash
bash tools/searxng/uninstall-searxng.sh
```

## Milestone 2: Direct Python Search

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

## Milestone 3: MCP Wrapper

First check the Python entry points parse cleanly:

```bash
python3 -m py_compile tools/searxng/search_searxng.py tools/searxng/mcp_server.py
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

## Development History

The development-history documents live under `dev/`.
Use them for milestone history and status tracking, not as the primary reader path through the repository.
