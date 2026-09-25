# Configuration

Full reference for mockrelay.yaml.

    listen: "127.0.0.1:8080"
    admin_listen: "127.0.0.1:8081"
    fixtures_dir: "./fixtures"
    mode: record
    latency_ms: 0
    metrics_enabled: true
    sequential: false

    # Smart matching
    match_mode: auto        # auto | exact | wildcard | regex | fuzzy | off
    fuzzy_threshold: 0.86   # 0.0 - 1.0
    ignore_case: false
    fuzzy_enabled: false    # allow fuzzy fallback for bare paths in auto mode
    smart_record_paths: true

    redact_headers:
      - authorization
      - cookie

    normalize_json_paths:
      - "$.id"

    upstreams:
      gh:
        base_url: "https://api.github.com"
        mode: record

## Matching settings

`match_mode`, `fuzzy_threshold`, `ignore_case`, and `fuzzy_enabled` can be set
globally, per upstream, and per route. The most specific definition wins, with
route beating upstream beating global. See [Smart matching](matching.md).

    upstreams:
      gh:
        base_url: "https://api.github.com"
        match_mode: wildcard
        fuzzy_threshold: 0.9
        routes:
          /v1/search:
            match_mode: fuzzy
            fuzzy_threshold: 0.8
            ignore_case: true

`routes` is a mapping of path prefix to overrides. The longest matching prefix
wins.

`smart_record_paths` is global only. When enabled, newly recorded fixtures
store the strategy prefix they matched with.
