# OpenAI-Compatible Tool-Calling Example

This example shows how a model using an OpenAI-compatible API can call a SearXNG-backed search tool from this repository.

It is intended to stay provider-agnostic where possible. The example code targets the OpenAI-compatible boundary rather than one provider-specific stack.

It has been validated successfully against llama.cpp with a local SearXNG instance. Other OpenAI-compatible providers may work, but llama.cpp is the only provider path documented as tested in this repository right now.

## Files

- `README.md` explains the example and how to run it
- `tool_calling_example.py` implements the minimal tool-calling loop
- `run-llama-cpp.md` captures the tested llama.cpp run path for this example

## What This Example Does

1. Confirm local SearXNG is running on port `8081`
2. Open `http://localhost:8081/search` in a browser to verify the local search interface
3. Confirm direct Python search works with `tools/searxng/search_searxng.py`
4. Run the OpenAI-compatible example against a configured API base URL and model
5. Let the model call `searxng_search`
6. Return the structured search result to the model and print the final answer

The example reuses the existing repository SearXNG search logic instead of reimplementing the HTTP request path.

## Dependencies

- Python 3
- Python dependencies installed from `pyproject.toml`
- A local or remote OpenAI-compatible endpoint
- A reachable SearXNG instance

Recommended workflow with `uv`:

Install `uv` if you want to run this example with the recommended workflow.

```bash
uv sync
```

Then run the example with:

```bash
uv run python3 examples/openai-compatible-tool-calling/tool_calling_example.py \
  --base-url http://127.0.0.1:11434/v1 \
  --api-key not-needed \
  --model your-tool-capable-model \
  --searxng-base-url http://127.0.0.1:8081 \
  --prompt "Search for jetson orin and summarize the top results."
```

If you prefer standard Python tooling instead, use a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -e .
```

## How To Run

Example with a local OpenAI-compatible endpoint and local SearXNG:

```bash
uv run python3 examples/openai-compatible-tool-calling/tool_calling_example.py \
  --base-url http://127.0.0.1:11434/v1 \
  --api-key not-needed \
  --model your-tool-capable-model \
  --searxng-base-url http://127.0.0.1:8081 \
  --prompt "Search for jetson orin and summarize the top results."
```

Validated llama.cpp example:

```bash
uv run python3 examples/openai-compatible-tool-calling/tool_calling_example.py \
  --base-url http://127.0.0.1:8080/v1 \
  --api-key not-needed \
  --model ggml-org/gemma-4-26B-A4B-it-GGUF:Q4_K_M \
  --searxng-base-url http://localhost:8081 \
  --prompt "Use the search tool to look up SearXNG and give me a short summary of the project."
```

For the tested llama.cpp walkthrough, see `examples/openai-compatible-tool-calling/run-llama-cpp.md`.

You can also use environment variables for some inputs:

- `OPENAI_BASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `SEARXNG_BASE_URL`

The script prints a short trace when the model calls `searxng_search`, then prints the final answer.

Use the exact model ID returned by `/v1/models`. Do not guess or shorten the model name.

## Notes On Provider Support

The example intentionally avoids provider-specific branches. If a provider exposes a compatible `chat.completions` tool-calling interface, the same example shape may apply.

Provider launch recipes are documented separately under `docs/providers/` so the example stays focused on the capability rather than on one model-server stack.

## Manual Validation

1. Start local SearXNG and confirm the browser page loads at `http://localhost:8081/search`.
2. Confirm the model endpoint is serving the expected model ID:

```bash
curl -s http://127.0.0.1:8080/v1/models | jq -r '.data[0].id'
```

3. Confirm SearXNG responds directly:

```bash
curl "http://localhost:8081/search?q=searxng&format=json"
```

4. Confirm direct search works:

```bash
SEARXNG_BASE_URL=http://127.0.0.1:8081 \
uv run python3 tools/searxng/search_searxng.py "jetson orin"
```

5. Run the tool-calling example against the local OpenAI-compatible endpoint.
6. Confirm the script prints a `Tool call:` line before the final answer.
7. Confirm the model output reflects the returned search results.
8. Test a failure path by using a model without tool support or a prompt that does not trigger search. The script should fail clearly instead of silently succeeding.
