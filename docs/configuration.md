# Configuration

Full reference for mockrelay.yaml.

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

    normalize_json_paths:
      - "$.id"

    upstreams:
      gh:
        base_url: "https://api.github.com"
        mode: record
