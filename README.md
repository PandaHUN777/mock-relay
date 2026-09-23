
# MockRelay

## Preview
<img src="https://files.catbox.moe/v9x6sc.png" alt="Image description">

## Install

```bash
pip install -e .
```

Requires **Python 3.10+** and `pyyaml`.

## Quickstart

```bash
mockrelay init
mockrelay serve
```

Point your app at the proxy by swapping the base URL:

| Real | Local |
|---|---|
| `https://api.stripe.com` | `http://localhost:8080/stripe` |
| `https://api.github.com` | `http://localhost:8080/gh` |

```bash
export STRIPE_BASE_URL=http://localhost:8080/stripe
export GITHUB_API_URL=http://localhost:8080/gh
```

## Modes

| Mode | Behavior |
|---|---|
| `record` | Forward to upstream, save every request/response as a fixture |
| `replay` | Serve from fixtures only — never touches the network |
| `passthrough` | Forward only, no recording |
| `hybrid` | Serve from fixtures if matched, otherwise go live and record |

## CLI

```bash
mockrelay serve
mockrelay serve --mode replay
mockrelay serve --latency 200
mockrelay record
mockrelay replay --latency 150
mockrelay list
mockrelay init
mockrelay config
```

## Config

```yaml
listen: "127.0.0.1:8080"
admin_listen: "127.0.0.1:8081"
fixtures_dir: "./fixtures"
mode: record
latency_ms: 0
metrics_enabled: true
sequential: false

redact_headers:
  - authorization
  - cookie
  - x-api-key
  - stripe-secret-key

normalize_json_paths:
  - "$.id"
  - "$.created"
  - "$.request_id"

error_injection: null

upstreams:
  stripe:
    base_url: "https://api.stripe.com"
    mode: record
  gh:
    base_url: "https://api.github.com"
    mode: record
  local:
    base_url: "http://localhost:9000"
    mode: passthrough
    routes:
      "/v1/slow":
        latency_ms: 800
      "/v1/fail":
        error_injection:
          status: 503
          rate: 1.0
```

## Admin UI

Open **http://localhost:8081** for the dashboard.
Prometheus metrics at **`/metrics`**.

## Recipes

**Replay Stripe in CI**
```bash
mockrelay replay --latency 100
pytest
```

**Test retry logic** (in `mockrelay.yaml`)
```yaml
routes:
  "/v1/charges":
    error_injection:
      status: 429
      rate: 0.5
```

**Simulate a slow upstream**
```bash
mockrelay replay --latency 2000
```
