#!/usr/bin/env python3
"""Expose the existing SearXNG search behavior through a small stdio MCP server."""

import json
import sys

from mcp_common import handle_request, make_error


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
