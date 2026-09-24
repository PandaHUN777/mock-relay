# Configuration

`mockrelay.yaml` at the repo root is loaded by default. Pass `--config PATH`
to use a different file.

## Full reference

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

## Keys

| Key | Type | Notes |
|---|---|---|
| listen | host:port | proxy address |
| admin_listen | host:port | admin UI address |
| fixtures_dir | path | where fixtures are written |
| mode | record/replay/passthrough/hybrid | global default |
| latency_ms | int | artificial delay per response |
| metrics_enabled | bool | expose /metrics on admin |
| sequential | bool | Nth call returns Nth matching fixture |
| redact_headers | list | header names replaced with {{SECRET}} |
| normalize_json_paths | list | JSON paths replaced with {{NORMALIZED}} at record time. Dot notation, walks arrays. Example: ["$?.id", "$?.created_at"] |
| error_injection | map | global error injection |
| upstreams | map | name -> {base_url, mode, routes} |

## Route overrides

Longest prefix wins. Each route can override mode, latency_ms,
error_injection.

## Environment variables

| Var | Effect |
|---|---|
| SWIVEL_THEME | pick theme for CLI output |
| NO_COLOR | disable color |
| SWIVEL_FORCE_COLOR | force color even without tty |
| SWIVEL_BRAND_KEY | override the brand blob key |


