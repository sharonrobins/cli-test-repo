#!/usr/bin/env python3
"""Query the DGX Spark's OpenAI-compatible API on port 8000 (Python 3.9+)."""

import argparse
import json
import math
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "http://100.69.228.10:8000/v1"


class APIError(Exception):
    """A connection, HTTP, or response-format error."""


def request_json(base_url, endpoint, api_key=None, timeout=120, payload=None):
    """GET an endpoint, or POST a JSON payload when one is supplied."""
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    request = Request(f"{base_url}/{endpoint}", data=data, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.load(response)
    except HTTPError as exc:
        detail = exc.read(2048).decode("utf-8", errors="replace")
        raise APIError(f"HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise APIError(
            f"Could not reach {base_url}: {exc}. "
            "Check that Tailscale is connected to the conference network "
            "and the server is running on port 8000."
        ) from exc
    except (ValueError, UnicodeError) as exc:
        raise APIError("The server returned an invalid JSON response.") from exc
    if not isinstance(result, dict):
        raise APIError("Expected a JSON object from the server.")
    return result


def model_ids(response):
    data = response.get("data")
    if not isinstance(data, list):
        raise APIError("The model list has no 'data' array.")
    ids = [item.get("id") for item in data if isinstance(item, dict)]
    ids = [model for model in ids if isinstance(model, str) and model]
    if not ids:
        raise APIError("The server reports no available models.")
    return ids


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", help="Prompt to send to the model")
    parser.add_argument("--base-url", default=os.getenv("DGX_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=os.getenv("DGX_MODEL"), help="Default: discover the single served model")
    parser.add_argument("--list-models", action="store_true", help="Print available model IDs and exit")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Maximum generated tokens, including reasoning (default: 1024)")
    parser.add_argument("--timeout", type=float, default=120, help="Network timeout in seconds (default: 120)")
    parser.add_argument("--json", action="store_true", help="Print the complete JSON response")
    args = parser.parse_args(argv)
    if not args.list_models and (args.prompt is None or not args.prompt.strip()):
        parser.error("provide a prompt or --list-models")
    if args.max_tokens < 1:
        parser.error("--max-tokens must be positive")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be a positive finite number")

    base_url = args.base_url.rstrip("/")
    parsed = urlsplit(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.query or parsed.fragment or parsed.username:
        parser.error("--base-url must be an HTTP(S) URL without credentials, query, or fragment")
    if not base_url.endswith("/v1"):
        base_url += "/v1"
    api_key = os.getenv("DGX_API_KEY")

    try:
        model = args.model
        if args.list_models or not model:
            models = request_json(base_url, "models", api_key, args.timeout)
            ids = model_ids(models)
            if args.list_models:
                print(json.dumps(models, indent=2) if args.json else "\n".join(ids))
                return 0
            if len(ids) != 1:
                raise APIError("Multiple models are available; select one with --model: " + ", ".join(ids))
            model = ids[0]

        response = request_json(
            base_url,
            "chat/completions",
            api_key,
            args.timeout,
            {
                "model": model,
                "messages": [{"role": "user", "content": args.prompt}],
                "max_completion_tokens": args.max_tokens,
                "stream": False,
            },
        )
        if args.json:
            print(json.dumps(response, indent=2, ensure_ascii=False))
            return 0
        try:
            choice = response["choices"][0]
            content = choice["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise APIError("The server returned no chat completion; use --json to inspect it.") from exc
        if not isinstance(content, str) or not content.strip():
            raise APIError("No final answer was returned. Try a larger --max-tokens value, or --json to inspect reasoning.")
        print(content)
        if choice.get("finish_reason") == "length":
            print("Warning: token limit reached; the answer may be incomplete. Increase --max-tokens.", file=sys.stderr)
        return 0
    except APIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
