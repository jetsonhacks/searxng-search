#!/usr/bin/env python3
"""Run a minimal OpenAI-compatible tool-calling loop with SearXNG search."""

import argparse
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.searxng.search_searxng import (  # noqa: E402
    build_search_url,
    fetch_search_response,
    get_base_url,
    normalize_results,
    validate_args,
)

TOOL_NAME = "searxng_search"


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Call an OpenAI-compatible model that can use a SearXNG search tool."
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL"),
        help="Base URL for the OpenAI-compatible API. Defaults to OPENAI_BASE_URL.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", "not-needed"),
        help="API key for the OpenAI-compatible API. Defaults to OPENAI_API_KEY or 'not-needed'.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL"),
        help="Model name to call. Defaults to OPENAI_MODEL.",
    )
    parser.add_argument(
        "--searxng-base-url",
        default=os.environ.get("SEARXNG_BASE_URL"),
        help="Base URL for SearXNG. Defaults to SEARXNG_BASE_URL.",
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Prompt to send to the model.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of normalized SearXNG results to return (default: 5).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP timeout for SearXNG requests in seconds (default: 10.0).",
    )
    return parser


def require_openai_client():
    """Import the OpenAI client with a clear fallback message."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The openai Python package is required for this example. "
            "Install dependencies with `uv sync`, or use a virtual environment "
            "and run `python3 -m pip install -e .`."
        ) from exc
    return OpenAI


def validate_model_args(args: argparse.Namespace) -> None:
    """Validate the inputs required to call the model and SearXNG."""
    if not args.base_url:
        raise ValueError(
            "Model base URL is required. Use --base-url or set OPENAI_BASE_URL."
        )
    if not args.model:
        raise ValueError("Model name is required. Use --model or set OPENAI_MODEL.")

    search_args = SimpleNamespace(
        base_url=args.searxng_base_url,
        limit=args.limit,
        timeout=args.timeout,
    )
    validate_args(search_args)
    get_base_url(search_args)


def tool_schema() -> list[dict]:
    """Return the tool schema for the example search tool."""
    return [
        {
            "type": "function",
            "function": {
                "name": TOOL_NAME,
                "description": "Search SearXNG and return compact normalized results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query text.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return.",
                            "minimum": 1,
                        },
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
        }
    ]


def run_searxng_search(
    query: str,
    searxng_base_url: str | None,
    limit: int,
    timeout: float,
) -> dict:
    """Execute the existing SearXNG search flow and return compact structured output."""
    args = SimpleNamespace(
        base_url=searxng_base_url,
        limit=limit,
        timeout=timeout,
    )
    validate_args(args)
    base_url = get_base_url(args)
    search_url = build_search_url(base_url, query)
    payload = fetch_search_response(search_url, timeout)
    results = normalize_results(payload, limit)
    compact_results = [
        {
            "title": result["title"],
            "url": result["url"],
            "engine": result["engine"],
            "content": result["content"],
        }
        for result in results
    ]
    return {
        "ok": True,
        "query": query,
        "base_url": base_url,
        "result_count": len(compact_results),
        "results": compact_results,
    }


def make_client(args: argparse.Namespace):
    """Create the OpenAI-compatible client."""
    OpenAI = require_openai_client()
    return OpenAI(base_url=args.base_url, api_key=args.api_key)


def request_model(client, args: argparse.Namespace, messages: list[dict]):
    """Call the model with the current conversation and tool schema."""
    try:
        return client.chat.completions.create(
            model=args.model,
            messages=messages,
            tools=tool_schema(),
            tool_choice="auto",
        )
    except Exception as exc:
        raise RuntimeError(format_model_error(exc, args)) from exc


def format_model_error(exc: Exception, args: argparse.Namespace) -> str:
    """Convert model client errors into short user-facing messages."""
    message = str(exc).strip() or exc.__class__.__name__
    lowered = message.lower()
    class_name = exc.__class__.__name__.lower()

    if "connection" in class_name or "connect" in lowered:
        return (
            "Could not reach the model endpoint at "
            f"{args.base_url}. Confirm the provider is running and that the "
            "base URL is correct."
        )

    if "notfound" in class_name or "model" in lowered and "not found" in lowered:
        return (
            f"Model {args.model!r} was not found at {args.base_url}. "
            "Query /v1/models and use the exact returned model ID."
        )

    if "404" in lowered and "model" in lowered:
        return (
            f"Model {args.model!r} was not found at {args.base_url}. "
            "Query /v1/models and use the exact returned model ID."
        )

    return f"Model request failed: {message}"


def get_message_text(message) -> str:
    """Extract text content from a completion message."""
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [part.get("text", "") for part in content if isinstance(part, dict)]
        return "".join(parts).strip()
    return ""


def make_assistant_message(message) -> dict:
    """Convert the assistant message to a plain dict for the follow-up request."""
    assistant_message = {
        "role": "assistant",
        "content": get_message_text(message) or "",
    }
    tool_calls = getattr(message, "tool_calls", None) or []
    if tool_calls:
        assistant_message["tool_calls"] = [
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                },
            }
            for tool_call in tool_calls
        ]
    return assistant_message


def parse_tool_arguments(raw_arguments: str) -> dict:
    """Parse JSON tool arguments from the model response."""
    try:
        arguments = json.loads(raw_arguments)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model returned invalid tool arguments: {exc}") from exc

    if not isinstance(arguments, dict):
        raise RuntimeError("Model tool arguments must decode to a JSON object.")

    return arguments


def handle_tool_call(tool_call, args: argparse.Namespace) -> dict:
    """Execute one tool call from the model."""
    if tool_call.function.name != TOOL_NAME:
        raise RuntimeError(f"Model requested an unknown tool: {tool_call.function.name}")

    arguments = parse_tool_arguments(tool_call.function.arguments)
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        raise RuntimeError("Tool call must include a non-empty string query.")

    limit = arguments.get("limit", args.limit)
    if not isinstance(limit, int):
        raise RuntimeError("Tool call limit must be an integer.")

    return run_searxng_search(
        query=query,
        searxng_base_url=args.searxng_base_url,
        limit=limit,
        timeout=args.timeout,
    )


def print_tool_result(tool_call, tool_result: dict) -> None:
    """Print a short learning-oriented trace for the tool call."""
    query = tool_result.get("query", "")
    print(f"Tool call: {tool_call.function.name}({query!r})")
    print(json.dumps(tool_result, indent=2))


def run_tool_calling_loop(args: argparse.Namespace) -> str:
    """Run the minimal tool-calling loop and return the final answer."""
    client = make_client(args)
    messages = [{"role": "user", "content": args.prompt}]

    first_response = request_model(client, args, messages)
    first_message = first_response.choices[0].message
    tool_calls = getattr(first_message, "tool_calls", None) or []
    if not tool_calls:
        raise RuntimeError(
            "Model did not emit a tool call. Try a tool-capable model or a prompt "
            "that clearly asks for web search."
        )

    messages.append(make_assistant_message(first_message))

    for tool_call in tool_calls:
        tool_result = handle_tool_call(tool_call, args)
        print_tool_result(tool_call, tool_result)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result),
            }
        )

    final_response = request_model(client, args, messages)
    final_message = final_response.choices[0].message
    final_answer = get_message_text(final_message).strip()
    if not final_answer:
        raise RuntimeError("Model returned an empty final answer.")
    return final_answer


def main() -> int:
    """Run the example command."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        validate_model_args(args)
        final_answer = run_tool_calling_loop(args)
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("\nFinal answer:\n")
    print(final_answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
