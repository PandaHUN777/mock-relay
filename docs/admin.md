# Admin API

The admin server listens on `admin_listen` (default 127.0.0.1:8081).

## Web UI

    http://localhost:8081/

## State

    GET /api/state

Returns current mode, latency, upstreams.

## Recent traffic

    GET /api/recent

Returns the last 50 requests seen by the proxy.

## Fixtures

    GET /api/fixtures
    GET /api/fixtures?upstream=gh
    GET /api/fixtures/<upstream>/<id>
    DELETE /api/fixtures/<upstream>/<id>

## Mode

    POST /api/mode/record
    POST /api/mode/replay
    POST /api/mode/passthrough
    POST /api/mode/hybrid

## Latency

    POST /api/latency/0
    POST /api/latency/500

## Metrics

    GET /metrics

Prometheus text format. Counters:

- mockrelay_requests_total{key}
- mockrelay_responses_total{key}
- mockrelay_mode_total{mode}
