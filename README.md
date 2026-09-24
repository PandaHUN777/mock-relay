# MockRelay

## Preview
<img src="https://files.catbox.moe/v9x6sc.png" alt="MockRelay preview">

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

MIT

