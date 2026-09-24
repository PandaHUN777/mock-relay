# Fixtures

Fixtures live under `fixtures/<upstream>/<id>.json`.

## Shape

    {
      "id": "local-get-9ab7c12d3e4f",
      "upstream": "local",
      "match": {
        "method": "GET",
        "path": "/v1/users",
        "query_subset": {},
        "body_contains": null
      },
      "request": {
        "method": "GET",
        "path": "/v1/users",
        "headers": { "Authorization": "{{SECRET}}" }
      },
      "response": {
        "status": 200,
        "headers": { "Content-Type": "application/json" },
        "body": {
          "users": [
            { "id": "u_1", "created": "{{NORMALIZED}}" }
          ]
        }
      },
      "normalize": ["$.created", "$.request_id"],
      "recorded_at": "2026-09-23T04:00:00Z"
    }

## Redaction

Headers listed in `redact_headers` are stored as `{{SECRET}}`. Bodies are
scrubbed for `Bearer`, `sk_live_*`, `sk_test_*`, `ghp_*`.

## Normalization

Fields listed in `normalize_json_paths` become `{{NORMALIZED}}`. That keeps
volatile values from breaking replay matching.

## Matching

- method equals
- path equals
- every key in `query_subset` matches
- every key in `body_contains` matches (recursively)

Highest-specificity match wins.

## Sequential fixtures

Set `sequential: true` in config. The Nth matching call returns the Nth
fixture. Useful for pagination and state machines.
