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
| /metrics | GET | Prometheus text format |
