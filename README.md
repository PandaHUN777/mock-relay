# MockRelay

## Preview

<p align="center">
  <img src="https://files.catbox.moe/v9x6sc.png" alt="MockRelay serving in a terminal">
</p>

## Install

```bash
git clone https://github.com/sswivell/mock-relay.git
cd mock-relay
pip install -e .
```

Requires **Python 3.10+** and `pyyaml`.

## Quickstart

Five steps from zero to a recorded fixture.

### 1. Scaffold a config

```bash
mockrelay init
```

This writes a starter `mockrelay.yaml` in the current directory. It already
contains three example upstreams (`stripe`, `gh`, `local`) you can edit
or delete.

### 2. Edit the config for your upstreams

Open `mockrelay.yaml` and set the base URLs you actually want to proxy.
Each key under `upstreams` becomes a URL prefix.

```yaml
upstreams:
  stripe:
    base_url: "https://api.stripe.com"
    mode: record
  gh:
    base_url: "https://api.github.com"
    mode: record
```

The key name (`stripe`, `gh`) is what appears in the proxy URL. So
`upstreams.stripe` becomes reachable at `http://localhost:8080/stripe/...`.

### 3. Start the proxy

```bash
mockrelay serve
```

You will see the routing table, the fixtures directory, and a health banner.
The admin UI is at http://localhost:8081.

### 4. Point your app at the proxy

Swap the base URL in your app or environment. Only the host and port change;
the path and query string stay the same.

| Real | Local |
|---|---|
| `https://api.stripe.com` | `http://localhost:8080/stripe` |
| `https://api.github.com` | `http://localhost:8080/gh` |

```bash
export STRIPE_BASE_URL=http://localhost:8080/stripe
export GITHUB_API_URL=http://localhost:8080/gh
```

The mapping is 1:1 with the `upstreams` block above:

| Config key | Path prefix | Real base URL |
|---|---|---|
| `stripe` | `/stripe/` | `https://api.stripe.com` |
| `gh` | `/gh/` | `https://api.github.com` |

So `GET https://api.github.com/users/octocat` becomes
`GET http://localhost:8080/gh/users/octocat`.

### 5. Make a request and inspect the fixture

Run any request through the proxy:

```bash
curl http://localhost:8080/gh/users/octocat
```

A JSON fixture is written to `fixtures/gh/`. List what you have:

```bash
mockrelay list
mockrelay list --upstream gh
mockrelay stats
```

Stop the server with Ctrl-C, then restart in replay mode. The same curl now
returns the fixture with no network access:

```bash
mockrelay serve --mode replay --latency 150
```

## How fixtures are stored

Fixtures are plain JSON files on disk. No database, no opaque binary format.

### Location

By default they live under `./fixtures` next to `mockrelay.yaml`. Override
with the `fixtures_dir` key in config.

    fixtures/
      gh/
        gh-get-9ab7c12d3e4f.json
        gh-get-4f2c81e0a1b2.json
      stripe/
        stripe-post-7d8e9f0a1c2d.json
      local/
        local-get-3a4b5c6d7e8f.json

One file per recorded request/response pair. The filename is
`<upstream>-<method>-<hash>.json` where `<hash>` is a short SHA1 of the
match key (method + path + query + body subset). Two requests that would match
the same fixture collide on purpose.

### File shape

    {
      "id": "gh-get-9ab7c12d3e4f",
      "upstream": "gh",
      "match": {
        "method": "GET",
        "path": "/users/octocat",
        "query_subset": {},
        "body_contains": null
      },
      "request": {
        "method": "GET",
        "path": "/users/octocat",
        "query": {},
        "headers": {
          "User-Agent": "curl/8.4.0",
          "Authorization": "{{SECRET}}"
        },
        "body": null
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json",
          "X-RateLimit-Remaining": "59"
        },
        "body": {
          "login": "octocat",
          "id": "{{NORMALIZED}}",
          "created_at": "{{NORMALIZED}}"
        }
      },
      "normalize": ["$.id", "$.created_at"],
      "recorded_at": "2026-09-23T04:12:00Z",
      "call_index": 0
    }

Field notes:

| Field | Meaning |
|---|---|
| `id` | stable hash-based identifier, unique per upstream |
| `upstream` | key from `upstreams` in config |
| `match` | what a live request must satisfy to hit this fixture |
| `request` | original request, headers redacted |
| `response` | original response, volatile fields normalized |
| `normalize` | JSON paths replaced with `{{NORMALIZED}}` |
| `recorded_at` | ISO 8601 UTC timestamp |
| `call_index` | used in sequential mode for Nth-call behavior |

### Redaction

Headers listed under `redact_headers` are stored as `{{SECRET}}`. Bodies
are scanned for `Bearer` tokens, `sk_live_*`, `sk_test_*`, and `ghp_*`
and replaced with `{{SECRET}}`. Commit fixtures to git without leaking keys.

### Normalization

Fields listed under `normalize_json_paths` are replaced with
`{{NORMALIZED}}` at record time. That means volatile values (IDs, timestamps,
nonces, request IDs) do not change the fixture on every record.

### Matching

Replay and hybrid mode match by:

1. HTTP method must be equal.
2. Path must be equal.
3. Every key in `match.query_subset` must be present and equal.
4. Every key in `match.body_contains` must be present and equal
   (recursive for nested objects).

Then the highest-specificity match wins ? more `body_contains` keys beats
fewer, then more query keys beats fewer.

Bodies themselves are not hashed for lookup. Matching is on structure, so a
request with a different order of JSON keys, or with additional fields your
fixture did not pin down, still matches.

### Sequential mode

With `sequential: true` in config, the Nth matching call returns the Nth
fixture (sorted by `call_index`). The counter resets on server restart. Use
it for pagination, polling, or state-machine tests.

### Editing fixtures

They are just JSON. Open one, change a status code to 500, hand-edit a body to
inject an edge case, or delete the file to force a re-record. The proxy reads
from disk on every request, so edits apply immediately without a restart.

### Sharing fixtures

Commit `fixtures/` to git. Teammates get the same replay environment by
pulling. For per-project overrides, use `fixtures_dir` in a project-local
`mockrelay.yaml`.

Full reference: `docs/fixtures.md`.

## Modes

| Mode | Behavior |
|---|---|
| `record` | Forward to upstream, save every request/response as a fixture |
| `replay` | Serve from fixtures only - never touches the network |
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

## License

MIT ? see [LICENSE](LICENSE).



