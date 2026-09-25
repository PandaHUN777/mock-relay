# Admin API

The admin server listens on admin_listen (default 127.0.0.1:8081).

| Endpoint | Method | Purpose |
|---|---|---|
| / | GET | HTML dashboard |
| /api/state | GET | current mode, latency |
| /api/recent | GET | last 50 requests |
| /api/fixtures | GET | list fixtures |
| /api/mode/<mode> | POST | flip mode |
| /api/latency/<ms> | POST | set latency |
| /api/match | GET | preview how a request would match |
| /metrics | GET | Prometheus text format |

## GET /api/match

Returns the ranked candidates for a hypothetical request, with a per-check
breakdown. It does not record, replay, or forward anything.

| Parameter | Default | Purpose |
|---|---|---|
| `method` | `GET` | request method |
| `path` | `/` | request path |
| `query` | empty | query string, e.g. `page=2&sort=asc` |
| `body` | none | JSON body |
| `upstream` | all | limit to one upstream |

    curl "http://127.0.0.1:8081/api/match?method=GET&path=/users/7"

The response carries the resolved settings plus a `results` array ordered best
first. Each result has `matched`, `strategy`, `score`, and a `checks` list
naming the `method`, `path`, `query`, and `body` conditions with a pass or
fail. See [Smart matching](matching.md).
