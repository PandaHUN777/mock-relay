# MockRelay

## Preview

<p align="center">
  <img src="https://files.catbox.moe/v9x6sc.png" alt="MockRelay serving in a terminal">
</p>

<p align="center">
  <a href="https://github.com/sswivell/mock-relay/actions"><img src="https://img.shields.io/github/actions/workflow/status/sswivell/mock-relay/ci.yml?branch=main&label=ci" alt="CI"></a>
  <a href="https://pypi.org/project/mockrelay/"><img src="https://img.shields.io/pypi/v/mockrelay" alt="PyPI"></a>
  <a href="https://pypi.org/project/mockrelay/"><img src="https://img.shields.io/pypi/dm/mockrelay" alt="Downloads"></a>
  <a href="https://github.com/sswivell/mock-relay/stargazers"><img src="https://img.shields.io/github/stars/sswivell/mock-relay" alt="Stars"></a>
  <img src="https://img.shields.io/badge/made%20with-Python-3776AB?logo=python&logoColor=white" alt="Made with Python">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e" alt="License"></a>
</p>

<p align="center">
  <b>Record real HTTP traffic. Replay it forever.</b><br>
  Universal local API mock-and-record reverse proxy.
</p>

---

## Table of contents

- [What it is](#what-it-is)
- [Why](#why)
- [Why not just use X](#why-not-just-use-x)
- [Install](#install)
- [Quickstart](#quickstart)
- [How fixtures are stored](#how-fixtures-are-stored)
- [Normalization](#normalization)
- [Mode precedence](#mode-precedence)
- [Sequential fixtures](#sequential-fixtures)
- [Modes](#modes)
- [CLI](#cli)
- [Config](#config)
- [Admin UI](#admin-ui)
- [Recipes](#recipes)
- [Project layout](#project-layout)
- [Related projects](#related-projects)
- [Acknowledgements](#acknowledgements)
- [Security](#security)
- [License](#license)

---

## What it is

Point your app at MockRelay instead of the real API. Record live traffic into
clean JSON fixtures, then replay it locally with simulated latency and error
states. Language-agnostic - works with any stack that speaks HTTP.

---

## Why

Your tests break when Stripe is down, GitHub rate-limits you, or an internal
microservice is flaky. Hand-written mocks drift from reality. MockRelay
records the real traffic once and replays it forever.

- No hand-written mock servers
- No flaky CI from upstream outages
- No secrets in committed fixtures
- No language lock-in - it is just a proxy

---

## Why not just use X

| Tool | Fits when | MockRelay differs because |
|---|---|---|
| WireMock | Java shop, complex matching | MockRelay records live traffic into fixtures instead of you writing stubs. Single binary, no JVM. |
| Mountebank | Multi-protocol mocking | MockRelay is HTTP-first and starts from recorded reality. |
| Prism | OpenAPI-driven mocks | MockRelay captures what the API actually returns. No spec required. |
| Polly.js | Node browser tests | MockRelay is a proxy - works from any language, any process, any CLI. |
| mitmproxy | General interception | MockRelay is opinionated about the record then replay workflow and fixture format. |

---

## Install

```bash
git clone https://github.com/sswivell/mock-relay.git
cd mock-relay
pip install -e .
```

Requires Python 3.10+ and pyyaml.

---

## Quickstart

Five steps from zero to a recorded fixture.

### 1. Scaffold a config

```bash
mockrelay init
```

This writes a starter mockrelay.yaml in the current directory.

### 2. Edit the config for your upstreams

```yaml
upstreams:
  stripe:
    base_url: "https://api.stripe.com"
    mode: record
  gh:
    base_url: "https://api.github.com"
    mode: record
```

The key name (stripe, gh) is what appears in the proxy URL.

### 3. Start the proxy

```bash
mockrelay serve
```

### 4. Point your app at the proxy

| Real | Local |
|---|---|
| https://api.stripe.com | http://localhost:8080/stripe |
| https://api.github.com | http://localhost:8080/gh |

```bash
export STRIPE_BASE_URL=http://localhost:8080/stripe
export GITHUB_API_URL=http://localhost:8080/gh
```

### 5. Make a request and inspect the fixture

```bash
curl http://localhost:8080/gh/users/octocat
mockrelay list
mockrelay stats
```

Stop with Ctrl-C, then replay:

```bash
mockrelay serve --mode replay --latency 150
```

---

## How fixtures are stored

Fixtures are plain JSON files on disk. No database.

```
fixtures/
  gh/
    gh-get-9ab7c12d3e4f.json
  stripe/
    stripe-post-7d8e9f0a1c2d.json
```

Each file captures the match key, redacted request, normalized response, and
metadata. Full format reference in docs/fixtures.md.

---

## Normalization

Volatile fields (IDs, timestamps, request IDs) change on every real call.
normalize_json_paths replaces them with the placeholder at record time so
re-recording the same endpoint overwrites the same fixture.

Before:

```json
{ "id": 583231, "created_at": "2011-01-25T18:44:36Z", "login": "octocat" }
```

After:

```json
{ "id": "NORMALIZED", "created_at": "NORMALIZED", "login": "octocat" }
```

Full before/after in docs/fixtures.md.

---

## Mode precedence

Five layers. Higher overrides lower.

| Priority | Where | Scope |
|---|---|---|
| 1 | global mode: in config | whole proxy |
| 2 | upstreams.<name>.mode | one upstream |
| 3 | upstreams.<name>.routes.<prefix>.mode | one path prefix |
| 4 | X-MockRelay-Mode request header | one request |
| 5 | admin API POST | runtime flip |

Same rules apply to latency_ms and error_injection.

---

## Sequential fixtures

With sequential: true, the Nth matching call returns the Nth fixture. Useful
for pagination, polling, and state machines. Off by default. Full details in
docs/fixtures.md.

---

## Modes

| Mode | Behavior |
|---|---|
| record | Forward to upstream, save every request/response as a fixture |
| replay | Serve from fixtures only - never touches the network |
| passthrough | Forward only, no recording |
| hybrid | Serve from fixtures if matched, otherwise go live and record |

---

## CLI

```bash
mockrelay serve
mockrelay serve --mode replay
mockrelay serve --latency 200
mockrelay record
mockrelay replay --latency 150
mockrelay list
mockrelay list --upstream gh
mockrelay stats
mockrelay clean --older-than 30 --yes
mockrelay init
mockrelay config
```

Full reference: docs/cli.md.

---

## Config

<details>
<summary>Full mockrelay.yaml example (click to expand)</summary>

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

</details>

Full reference: docs/configuration.md.

---

## Admin UI

The admin server runs on admin_listen (default http://localhost:8081).

| Endpoint | Method | Purpose |
|---|---|---|
| / | GET | HTML dashboard |
| /api/state | GET | current mode, latency, upstreams |
| /api/recent | GET | last 50 requests |
| /api/fixtures | GET | list fixtures |
| /api/fixtures/<upstream>/<id> | GET / DELETE | read or remove |
| /api/mode/<mode> | POST | flip mode |
| /api/latency/<ms> | POST | set latency |
| /metrics | GET | Prometheus text format |

Full reference: docs/admin.md.

---

## Recipes

- Record once, replay forever (docs/recipes.md)
- Point a real app at the proxy (docs/recipes.md)
- Test retry/backoff (docs/recipes.md)
- Simulate a slow upstream (docs/recipes.md)
- One-off passthrough (docs/recipes.md)
- CI replay (docs/recipes.md)
- Prune old fixtures (docs/recipes.md)

Full set: docs/recipes.md.

---

## Project layout

```
mockrelay/
|-- mockrelay/       package
|-- tests/           pytest suite
|-- docs/            documentation
|-- examples/        usage examples
|-- pyproject.toml
|-- mockrelay.yaml
`-- README.md
```

---

## Related projects

- nock - HTTP mocking for Node
- Polly.js - record/replay for JavaScript
- VCR - record/replay for Ruby
- vcrpy - record/replay for Python
- WireMock - HTTP mock server for Java
- Mountebank - multi-protocol mocking
- Prism - OpenAPI-driven mocks
- mitmproxy - interactive HTTPS proxy

MockRelay is the language-agnostic, record-first take on the same problem.

---

## Acknowledgements

- devicon for language icons
- shields.io for badges
- Keep a Changelog for the changelog format
- Contributor Covenant for the code of conduct

---

## Security

See SECURITY.md for the threat model and disclosure process.

---

## License

MIT - see LICENSE.
