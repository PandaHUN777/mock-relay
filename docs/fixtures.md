# Fixtures

Fixtures live under fixtures/<upstream>/<id>.json.

## Shape

    {
      "id": "local-get-9ab7c12d3e4f",
      "upstream": "local",
      "match": { "method": "GET", "path": "/v1/users" },
      "request": { "method": "GET", "path": "/v1/users" },
      "response": { "status": 200, "body": {} },
      "recorded_at": "2026-09-23T04:00:00Z"
    }

## Redaction

Headers listed in redact_headers are stored as {{SECRET}}.

## Normalization

Fields listed in normalize_json_paths become {{NORMALIZED}}.

## Matching

Highest-specificity match wins.
