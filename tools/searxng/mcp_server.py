#!/usr/bin/env python3
"""Expose the existing SearXNG search behavior through a small MCP server."""

import json
import sys
from types import SimpleNamespace

from search_searxng import (
    build_search_url,
    fetch_search_response,
    get_base_url,
    normalize_results,
    validate_args,
)

SERVER_NAME = "searxng-search"
SERVER_VERSION = "0.1.0"
TOOL_NAME = "search_searxng"


def read_message() -> dict | None:
    """Read one Content-Length framed JSON-RPC message from stdin."""
    content_length = None

    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break

        header = line.decode("utf-8").strip()
        if not header:
            break

        name, _, value = header.partition(":")
        if name.lower() == "content-length":
            try:
                content_length = int(value.strip())
            except ValueError as exc:
                raise RuntimeError("Invalid Content-Length header.") from exc

    if content_length is None:
        raise RuntimeError("Missing Content-Length header.")

    body = sys.stdin.buffer.read(content_length)
    if len(body) != content_length:
        raise RuntimeError("Incomplete JSON-RPC message body.")

    try:
        message = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON-RPC message: {exc}") from exc

    if not isinstance(message, dict):
        raise RuntimeError("JSON-RPC message must be an object.")

    return message


def write_message(message: dict) -> None:
    """Write one Content-Length framed JSON-RPC message to stdout."""
    encoded = json.dumps(message).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(encoded)}\r\n\r\n".encode("utf-8"))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def make_error(code: int, message: str, request_id=None) -> dict:
    """Build a JSON-RPC error response."""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def make_result(result: dict, request_id) -> dict:
    """Build a JSON-RPC success response."""
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def tool_schema() -> dict:
    """Return the input schema for the SearXNG search tool."""
    return {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query text.",
            },
            "base_url": {
                "type": "string",
                "description": "Optional SearXNG base URL. Falls back to SEARXNG_BASE_URL.",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of normalized results to return.",
                "default": 5,
                "minimum": 1,
            },
            "timeout": {
                "type": "number",
                "description": "HTTP timeout in seconds.",
                "default": 10.0,
                "exclusiveMinimum": 0,
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    }


def make_tool_text(payload: dict) -> str:
    """Render a structured tool payload as formatted JSON text."""
    return json.dumps(payload, indent=2)


def run_search(arguments: dict) -> tuple[bool, dict]:
    """Execute the Milestone 2 search flow using MCP tool arguments."""
    if not isinstance(arguments, dict):
        return False, {"ok": False, "error": "Tool arguments must be an object."}

    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        return False, {"ok": False, "error": "query must be a non-empty string."}

    args = SimpleNamespace(
        base_url=arguments.get("base_url"),
        limit=arguments.get("limit", 5),
        timeout=arguments.get("timeout", 10.0),
    )

    try:
        validate_args(args)
        base_url = get_base_url(args)
        search_url = build_search_url(base_url, query)
        payload = fetch_search_response(search_url, args.timeout)
        results = normalize_results(payload, args.limit)
    except (ValueError, RuntimeError) as exc:
        return False, {"ok": False, "error": str(exc)}

    return True, {
        "ok": True,
        "query": query,
        "base_url": base_url,
        "result_count": len(results),
        "results": results,
    }


def handle_request(message: dict) -> dict | None:
    """Handle one JSON-RPC request object."""
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params", {})

    if method == "notifications/initialized":
        return None

    if method == "initialize":
        return make_result(
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION,
                },
            },
            request_id,
        )

    if method == "ping":
        return make_result({}, request_id)

    if method == "tools/list":
        return make_result(
            {
                "tools": [
                    {
                        "name": TOOL_NAME,
                        "description": "Search a SearXNG instance and return normalized JSON results.",
                        "inputSchema": tool_schema(),
                    }
                ]
            },
            request_id,
        )

    if method == "tools/call":
        if not isinstance(params, dict):
            return make_error(-32602, "tools/call params must be an object.", request_id)

        tool_name = params.get("name")
        if tool_name != TOOL_NAME:
            return make_error(-32602, f"Unknown tool: {tool_name}", request_id)

        ok, payload = run_search(params.get("arguments", {}))
        return make_result(
            {
                "content": [{"type": "text", "text": make_tool_text(payload)}],
                "isError": not ok,
            },
            request_id,
        )

    return make_error(-32601, f"Method not found: {method}", request_id)


def main() -> int:
    """Run the MCP server loop until stdin closes or a fatal protocol error occurs."""
    while True:
        try:
            message = read_message()
            if message is None:
                return 0
            response = handle_request(message)
        except RuntimeError as exc:
            write_message(make_error(-32700, str(exc), None))
            return 1

        if response is not None:
            write_message(response)


if __name__ == "__main__":
    sys.exit(main())
