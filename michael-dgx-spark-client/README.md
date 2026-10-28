# DGX Spark Python client

Connect Tailscale to the conference network before running. This client uses
Python 3.9 or newer and only the standard library; no package installation is needed.

The two services are:

- Open WebUI: <http://100.69.228.10:3000/> (browser sign-in).
- Model API: <http://100.69.228.10:8000/v1> (used by the Python client).

From this directory:

```sh
python3 dgx_client.py --list-models
python3 dgx_client.py 'What is the Euler characteristic of the complex projective line, and why? Answer in two sentences.'
```

The client discovers the model automatically when the server offers one model.
If it offers several, choose one with `--model MODEL_ID`.

```sh
python3 dgx_client.py --model nvidia/Qwen3.8-Flash-Next-FP4-Local --max-tokens 2048 'Explain the projective line.'
python3 dgx_client.py --json 'Factor x^4 - 1 over the rationals.'
```

`--json` includes the complete server response, including usage and reasoning
fields when provided. `--max-tokens` includes reasoning tokens; increase it if
the model uses the budget before producing a final answer. Requests are not
automatically retried.

Use `--base-url` or `DGX_BASE_URL` if the server address changes. `DGX_MODEL`
sets a default model. If authentication is enabled on the API later, supply its
key through the `DGX_API_KEY` environment variable. The API accepted requests
without a key when checked on October 28, 2026.

The program calls `GET /v1/models` and `POST /v1/chat/completions`, with request
fields checked against the live server's `/openapi.json` schema.
