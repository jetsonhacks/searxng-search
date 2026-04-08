# llama.cpp Provider Notes

This file documents llama.cpp-style launch artifacts for the OpenAI-compatible examples in this repository.

llama.cpp is documented here because it is the first provider path that has been tested end to end in this repository.

These commands are provider launch recipes. They are not part of the core SearXNG feature implementation, and they are not required to understand the repository's search logic.

Use this page when you want to stand up a llama.cpp-compatible model endpoint that can serve the OpenAI-compatible tool-calling example.

## What Kind Of Artifact This Is

This is a provider runtime note:

- how to launch a compatible model endpoint
- how to point the repository example at that endpoint
- how to keep those runtime details separate from the core feature code

The core feature remains the same regardless of which compatible provider is used.

## Jetson-Oriented Example Launch Recipe

The following command is an example provider runtime artifact for launching a llama.cpp-style server on Jetson with a container image:

```bash
sudo docker run -it --rm --pull always --runtime=nvidia --network host \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  ghcr.io/nvidia-ai-iot/llama_cpp:gemma4-jetson-orin \
  llama-server -hf ggml-org/gemma-4-E2B-it-GGUF:Q8_0
```

Another Jetson-oriented example launch recipe is:

```bash
sudo docker run -it --rm --pull always --runtime=nvidia --network host \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  ghcr.io/nvidia-ai-iot/llama_cpp:gemma4-jetson-orin \
  llama-server -hf ggml-org/gemma-4-26B-A4B-it-GGUF:Q4_K_M
```

Treat this as a provider launch recipe, not as core repository implementation.

## OpenAI-Compatible Boundary

llama.cpp can be used behind an OpenAI-compatible server boundary as well. For this repository, that means the important contract is the exposed API shape, not the internal server stack.

If the launched endpoint exposes an OpenAI-compatible `chat.completions` interface with tool calling, it can be used with the OpenAI-compatible example in this repository.

## Discover The Model ID

Before running the example, confirm the model ID exposed by the endpoint:

```bash
curl -s http://127.0.0.1:8080/v1/models | jq -r '.data[0].id'
```

Use the exact returned model ID when calling the example.

## Point The Example At The Provider

Once the provider endpoint is running, point the example at the provider base URL and the discovered model ID:

```bash
uv run python3 examples/openai-compatible-tool-calling/tool_calling_example.py \
  --base-url http://127.0.0.1:8080/v1 \
  --api-key not-needed \
  --model ggml-org/gemma-4-26B-A4B-it-GGUF:Q4_K_M \
  --searxng-base-url http://localhost:8081 \
  --prompt "Use the search tool to look up SearXNG and give me a short summary of the project."
```

This validated path used:

- llama.cpp OpenAI-compatible endpoint at `http://127.0.0.1:8080/v1`
- local SearXNG at `http://localhost:8081`
- model ID `ggml-org/gemma-4-26B-A4B-it-GGUF:Q4_K_M`

Adjust the base URL, model name, and authentication details only if your validated runtime differs.

For the tested end-to-end run steps, see `examples/openai-compatible-tool-calling/run-llama-cpp.md`.

## Practical Notes

- Different llama.cpp deployments expose different model names and ports.
- Tool calling depends on both the server surface and the selected model.
- Keep provider launch commands here, not in the core feature code or feature planning docs.
