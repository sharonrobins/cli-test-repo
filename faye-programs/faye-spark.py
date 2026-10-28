#!/usr/bin/env python3
"""Query the vLLM server on Faye's DGX Spark.

The server speaks the OpenAI-compatible vLLM HTTP API at
http://100.69.228.10:8000/v1 (Tailscale address).

What the default query asks, and why:
FayeJackson.md describes Faye's research on families of algebraic curves over
P^1, viewed as a fibration M^4 -> P^1, and the question of which braids in the
base lift to fiber-preserving diffeomorphisms of M^4. Problem 3 in that file
asks for tools to visualize Deligne-Mostow covers of P^1 branched at n points.
The default prompt ties these together: explain braid lifting, specialize to
cyclic (Deligne-Mostow) covers, and propose a browser visualization of the
lifted monodromy. Pass --prompt to ask something else.

The served model is a reasoning model: vLLM returns its chain of thought in a
separate ``reasoning`` field and the answer in ``content``. The reasoning is
hidden by default; pass --show-reasoning to print it to stderr. Reasoning tokens
count against --max-tokens. Thinking is OFF by default (--thinking off sends the
Qwen ``enable_thinking: false`` chat-template kwarg); --thinking low/medium/high
turns it on and sends ``reasoning_effort`` to bound how long the model thinks.

Standard library only.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

HOST = "100.69.228.10"
PORT = 8000

SYSTEM_PROMPT = (
    "You are a research collaborator of a geometric topologist. Be precise, "
    "use standard terminology, and clearly mark anything you are unsure of as "
    "a guess rather than stating it in the voice of a theorem."
)

DEFAULT_PROMPT = """Consider a family of algebraic curves over P^1, i.e. a fibration M^4 -> P^1 \
with finitely many singular fibers lying over branch points p_1, ..., p_n.

(1) Explain, at the level of a second-year graduate student, what it means for a \
braid on the n branch points to *lift* to a fiber-preserving diffeomorphism of \
M^4, and what can obstruct such a lift.

(2) Specialize to the cyclic cover of P^1 branched at n points (the Deligne-Mostow \
setting). Describe what the monodromy of the lift looks like on H_1 of the fiber, \
mentioning the Burau representation if it is relevant.

(3) Propose one concrete browser visualization (JavaScript) that would help a \
mathematician see the lifted monodromy for n = 4 or 5. Say what is drawn and what \
the user manipulates.

Mark anything you are not sure of as a guess."""


def base_url(host, port):
    return f"http://{host}:{port}/v1"


def http(url, body=None, timeout=600):
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    return urllib.request.urlopen(req, timeout=timeout)


def list_models(host, port):
    with http(f"{base_url(host, port)}/models") as resp:
        return [m["id"] for m in json.load(resp)["data"]]


def chat(host, port, model, prompt, max_tokens, temperature, stream, show_reasoning, thinking):
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
    }
    if thinking == "off":
        body["chat_template_kwargs"] = {"enable_thinking": False}
    else:
        body["reasoning_effort"] = thinking
    url = f"{base_url(host, port)}/chat/completions"
    with http(url, body) as resp:
        if not stream:
            out = json.load(resp)
            choice = out["choices"][0]
            msg = choice["message"]
            if show_reasoning and msg.get("reasoning"):
                print("--- reasoning ---\n" + msg["reasoning"].strip() + "\n--- answer ---", file=sys.stderr)
            content = (msg.get("content") or "").strip()
            if content:
                print(content)
            else:
                print("(model produced no answer text; raise --max-tokens or use --show-reasoning)", file=sys.stderr)
            usage = out.get("usage", {})
            details = usage.get("completion_tokens_details") or {}
            print(
                f"[model={out.get('model')} finish={choice.get('finish_reason')} "
                f"prompt_tokens={usage.get('prompt_tokens')} "
                f"completion_tokens={usage.get('completion_tokens')} "
                f"reasoning_tokens={details.get('reasoning_tokens')}]",
                file=sys.stderr,
            )
            return
        in_reasoning = False
        got_content = False
        for raw in resp:
            line = raw.decode().strip()
            if not line.startswith("data:"):
                continue
            payload = line[len("data:"):].strip()
            if payload == "[DONE]":
                break
            delta = json.loads(payload)["choices"][0].get("delta", {})
            reasoning = delta.get("reasoning") or delta.get("reasoning_content")
            if reasoning and show_reasoning:
                if not in_reasoning:
                    sys.stderr.write("--- reasoning ---\n")
                    in_reasoning = True
                sys.stderr.write(reasoning)
                sys.stderr.flush()
            text = delta.get("content")
            if text:
                if in_reasoning:
                    sys.stderr.write("\n--- answer ---\n")
                    sys.stderr.flush()
                    in_reasoning = False
                if not got_content:
                    text = text.lstrip()
                    got_content = bool(text)
                sys.stdout.write(text)
                sys.stdout.flush()
        print()
        if not got_content:
            print("(model produced no answer text; raise --max-tokens or use --show-reasoning)", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description="Query the vLLM server on the DGX Spark.")
    p.add_argument("--prompt", default=DEFAULT_PROMPT, help="user message (default: braid-lifting question)")
    p.add_argument("--model", default=None, help="model id (default: first model the server lists)")
    p.add_argument("--max-tokens", type=int, default=16000, help="budget shared by reasoning and answer (the model thinks at length on hard questions)")
    p.add_argument("--temperature", type=float, default=0.6)
    p.add_argument("--stream", action="store_true", help="print tokens as they arrive")
    p.add_argument("--show-reasoning", action="store_true", help="also print the model's reasoning to stderr")
    p.add_argument("--thinking", choices=["off", "low", "medium", "high"], default="off",
                   help="off: no chain of thought (default); low/medium/high: think with that reasoning_effort")
    p.add_argument("--host", default=HOST)
    p.add_argument("--port", type=int, default=PORT)
    args = p.parse_args()

    try:
        model = args.model or list_models(args.host, args.port)[0]
        chat(args.host, args.port, model, args.prompt, args.max_tokens, args.temperature, args.stream,
             args.show_reasoning, args.thinking)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} from {args.host}:{args.port}: {e.read().decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(
            f"Could not reach vLLM at {args.host}:{args.port} ({e}). "
            "Check that Tailscale is connected and vLLM is running on the Spark.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
