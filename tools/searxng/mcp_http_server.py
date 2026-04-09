#!/usr/bin/env python3
"""Expose the SearXNG MCP tool over HTTP for browser-facing clients."""

from __future__ import annotations

import argparse
import json
import queue
import sys
import threading
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from mcp_common import handle_request, make_error


class SessionRegistry:
    """Track legacy SSE sessions for clients that expect an event stream."""

    def __init__(self) -> None:
        self._sessions: dict[str, queue.Queue[dict | None]] = {}
        self._lock = threading.Lock()

    def create(self) -> tuple[str, queue.Queue[dict | None]]:
        """Create and store a new session queue."""
        session_id = uuid.uuid4().hex
        session_queue: queue.Queue[dict | None] = queue.Queue()
        with self._lock:
            self._sessions[session_id] = session_queue
        return session_id, session_queue

    def get(self, session_id: str) -> queue.Queue[dict | None] | None:
        """Return the session queue for the given ID."""
        with self._lock:
            return self._sessions.get(session_id)

    def close(self, session_id: str) -> None:
        """Remove a session when its SSE connection closes."""
        with self._lock:
            self._sessions.pop(session_id, None)


def build_parser() -> argparse.ArgumentParser:
    """Build command-line arguments for the HTTP MCP server."""
    parser = argparse.ArgumentParser(
        description="Serve the SearXNG MCP tool over HTTP."
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface to bind (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="TCP port to bind (default: 8765).",
    )
    parser.add_argument(
        "--mcp-path",
        default="/mcp",
        help="Path for the streamable HTTP MCP endpoint (default: /mcp).",
    )
    parser.add_argument(
        "--sse-path",
        default="/sse",
        help="Legacy SSE endpoint path for compatibility clients (default: /sse).",
    )
    parser.add_argument(
        "--messages-path",
        default="/messages",
        help="Legacy POST endpoint path for SSE compatibility clients (default: /messages).",
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    """Validate server arguments before starting the listener."""
    if args.port <= 0 or args.port > 65535:
        raise ValueError("--port must be between 1 and 65535.")

    for name in ("mcp_path", "sse_path", "messages_path"):
        value = getattr(args, name)
        if not value.startswith("/"):
            raise ValueError(f"--{name.replace('_', '-')} must start with '/'.")


def make_handler(args: argparse.Namespace):
    """Create a request handler bound to the configured paths."""
    session_registry = SessionRegistry()

    class MCPHTTPRequestHandler(BaseHTTPRequestHandler):
        server_version = "SearXNGMCPHTTP/0.1"

        def log_message(self, format: str, *args) -> None:
            """Write concise HTTP logs to stderr."""
            sys.stderr.write(
                "%s - - [%s] %s\n"
                % (self.address_string(), self.log_date_time_string(), format % args)
            )

        def do_GET(self) -> None:
            """Handle health and compatibility GET endpoints."""
            if self.path == "/health":
                self._write_json(HTTPStatus.OK, {"ok": True})
                return

            if self.path == args.mcp_path:
                self._write_json(
                    HTTPStatus.METHOD_NOT_ALLOWED,
                    {
                        "ok": False,
                        "error": "Use HTTP POST for the MCP endpoint.",
                    },
                )
                return

            if self.path == args.sse_path:
                self._handle_legacy_sse_stream()
                return

            self._write_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found."})

        def do_OPTIONS(self) -> None:
            """Handle browser CORS preflight requests for the MCP endpoint."""
            if self.path == args.mcp_path:
                self.send_response(HTTPStatus.NO_CONTENT)
                self._send_cors_headers()
                self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                self.send_header(
                    "Access-Control-Allow-Headers",
                    "content-type, mcp-protocol-version",
                )
                self.end_headers()
                return

            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()

        def do_POST(self) -> None:
            """Handle streamable HTTP and legacy POST message endpoints."""
            if self.path == args.mcp_path:
                self._handle_json_rpc_response()
                return

            if self.path.startswith(args.messages_path):
                self._handle_legacy_sse_message()
                return

            self._write_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found."})

        def _handle_json_rpc_response(self) -> None:
            """Handle a direct JSON-RPC POST and return a JSON response."""
            message = self._read_json_body()
            if isinstance(message, list):
                if not message:
                    self._write_json(
                        HTTPStatus.BAD_REQUEST,
                        make_error(-32600, "Batch requests must not be empty.", None),
                    )
                    return

                responses = self._handle_message_batch(message)
                if not responses:
                    self.send_response(HTTPStatus.ACCEPTED)
                    self._send_cors_headers()
                    self.end_headers()
                    return

                self._write_json(HTTPStatus.OK, responses)
                return

            if not isinstance(message, dict):
                self._write_json(
                    HTTPStatus.BAD_REQUEST,
                    make_error(-32600, "JSON-RPC payload must be an object.", None),
                )
                return

            response = handle_request(message)
            if response is None:
                self.send_response(HTTPStatus.ACCEPTED)
                self._send_cors_headers()
                self.end_headers()
                return

            self._write_json(HTTPStatus.OK, response)

        def _handle_legacy_sse_stream(self) -> None:
            """Open a small compatibility SSE stream and announce the POST endpoint."""
            session_id, session_queue = session_registry.create()
            endpoint = f"{args.messages_path}?session_id={session_id}"

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            try:
                self._write_sse_event("endpoint", endpoint)
                while True:
                    message = session_queue.get()
                    if message is None:
                        break
                    self._write_sse_event("message", json.dumps(message))
            except (BrokenPipeError, ConnectionResetError):
                return
            finally:
                session_registry.close(session_id)

        def _handle_legacy_sse_message(self) -> None:
            """Handle a JSON-RPC POST for a previously announced SSE session."""
            session_id = self._query_value("session_id")
            if not session_id:
                self._write_json(
                    HTTPStatus.BAD_REQUEST,
                    {"ok": False, "error": "session_id query parameter is required."},
                )
                return

            session_queue = session_registry.get(session_id)
            if session_queue is None:
                self._write_json(
                    HTTPStatus.NOT_FOUND,
                    {"ok": False, "error": "Unknown or expired session_id."},
                )
                return

            message = self._read_json_body()
            if not isinstance(message, dict):
                self._write_json(
                    HTTPStatus.BAD_REQUEST,
                    make_error(-32600, "JSON-RPC payload must be an object.", None),
                )
                return

            response = handle_request(message)
            if response is not None:
                session_queue.put(response)

            self.send_response(HTTPStatus.ACCEPTED)
            self.end_headers()

        def _handle_message_batch(self, messages: list[object]) -> list[dict]:
            """Handle a list of JSON-RPC messages and return the response list."""
            responses: list[dict] = []

            for message in messages:
                if not isinstance(message, dict):
                    responses.append(
                        make_error(-32600, "Each batch item must be an object.", None)
                    )
                    continue

                response = handle_request(message)
                if response is not None:
                    responses.append(response)

            return responses

        def _read_json_body(self) -> object:
            """Read and decode a JSON request body."""
            content_length_text = self.headers.get("Content-Length")
            if content_length_text is None:
                raise ValueError("Missing Content-Length header.")

            try:
                content_length = int(content_length_text)
            except ValueError as exc:
                raise ValueError("Invalid Content-Length header.") from exc

            body = self.rfile.read(content_length)
            try:
                return json.loads(body.decode("utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON request body: {exc}") from exc

        def _query_value(self, name: str) -> str | None:
            """Extract a single query parameter value from the request path."""
            _, _, query_string = self.path.partition("?")
            for pair in query_string.split("&"):
                key, _, value = pair.partition("=")
                if key == name and value:
                    return value
            return None

        def _write_json(self, status: HTTPStatus, payload: object) -> None:
            """Send a JSON response payload."""
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            if self.path == args.mcp_path:
                self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def _send_cors_headers(self) -> None:
            """Send the minimal CORS headers needed for local WebUI testing."""
            origin = self.headers.get("Origin")
            allowed_origin = origin if origin in {"http://localhost:8080"} else "http://localhost:8080"
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Vary", "Origin")

        def _write_sse_event(self, event_name: str, data: str) -> None:
            """Write one SSE event block."""
            encoded = f"event: {event_name}\ndata: {data}\n\n".encode("utf-8")
            self.wfile.write(encoded)
            self.wfile.flush()

        def handle_one_request(self) -> None:
            """Wrap request handling so protocol errors become JSON responses."""
            try:
                super().handle_one_request()
            except ValueError as exc:
                self._write_json(
                    HTTPStatus.BAD_REQUEST,
                    make_error(-32700, str(exc), None),
                )
            except BrokenPipeError:
                return

    return MCPHTTPRequestHandler


def main() -> int:
    """Start the HTTP MCP server and serve until interrupted."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        validate_args(args)
    except ValueError as exc:
        parser.error(str(exc))

    handler = make_handler(args)
    server = ThreadingHTTPServer((args.host, args.port), handler)

    print(
        f"Serving MCP HTTP on http://{args.host}:{args.port}{args.mcp_path}",
        file=sys.stderr,
    )
    print(
        f"Legacy SSE compatibility on http://{args.host}:{args.port}{args.sse_path}",
        file=sys.stderr,
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down MCP HTTP server.", file=sys.stderr)
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
