#!/usr/bin/env python3
"""Query a local SearXNG instance and print normalized JSON results."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Query the SearXNG JSON search endpoint."
    )
    parser.add_argument("query", help="Search query text")
    parser.add_argument(
        "--base-url",
        help="Base URL for the SearXNG instance. Defaults to SEARXNG_BASE_URL.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of normalized results to print (default: 5).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP timeout in seconds (default: 10).",
    )
    return parser


def get_base_url(args: argparse.Namespace) -> str:
    """Resolve the configured SearXNG base URL."""
    base_url = args.base_url or os.environ.get("SEARXNG_BASE_URL")
    if not base_url:
        raise ValueError(
            "SearXNG base URL is required. Use --base-url or set SEARXNG_BASE_URL."
        )
    return base_url.rstrip("/")


def validate_args(args: argparse.Namespace) -> None:
    """Validate command-line arguments before making the request."""
    if args.limit <= 0:
        raise ValueError("--limit must be greater than 0.")
    if args.timeout <= 0:
        raise ValueError("--timeout must be greater than 0.")


def build_search_url(base_url: str, query: str) -> str:
    """Build the SearXNG JSON search URL."""
    params = urllib.parse.urlencode({"q": query, "format": "json"})
    return f"{base_url}/search?{params}"


def fetch_search_response(search_url: str, timeout: float) -> dict:
    """Fetch and parse the SearXNG JSON response."""
    request = urllib.request.Request(
        search_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "searxng-search-example/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {exc.code} from SearXNG: {body.strip() or exc.reason}"
        ) from exc
    except urllib.error.URLError as exc:
        reason = exc.reason
        raise RuntimeError(f"Could not reach SearXNG: {reason}") from exc

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"SearXNG returned invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise RuntimeError("SearXNG returned an unexpected JSON structure.")

    return data


def normalize_result(result: dict) -> dict:
    """Normalize a single SearXNG result entry."""
    engines = result.get("engines") or []
    engine = engines[0] if engines else None
    return {
        "title": result.get("title"),
        "url": result.get("url"),
        "engine": engine,
        "content": result.get("content"),
        "score": result.get("score"),
    }


def normalize_results(payload: dict, limit: int) -> list[dict]:
    """Normalize the SearXNG results list."""
    results = payload.get("results")
    if not isinstance(results, list):
        raise RuntimeError("SearXNG response did not include a results list.")
    return [normalize_result(result) for result in results[:limit]]


def print_json(data: dict, exit_code: int) -> int:
    """Print JSON output and return the desired exit code."""
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return exit_code


def main() -> int:
    """Run the command-line search tool."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        validate_args(args)
        base_url = get_base_url(args)
        search_url = build_search_url(base_url, args.query)
        payload = fetch_search_response(search_url, args.timeout)
        normalized_results = normalize_results(payload, args.limit)
    except (ValueError, RuntimeError) as exc:
        return print_json({"ok": False, "error": str(exc)}, 1)

    return print_json(
        {
            "ok": True,
            "query": args.query,
            "base_url": base_url,
            "result_count": len(normalized_results),
            "results": normalized_results,
        },
        0,
    )


if __name__ == "__main__":
    sys.exit(main())
