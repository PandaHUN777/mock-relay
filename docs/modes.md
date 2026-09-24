# Modes

## record

Forwards every request upstream. Writes a fixture per request/response pair.

    mockrelay serve --mode record

Use when: seeding fixtures, catching up after an API change.

## replay

Serves from fixtures only. Never touches the network.

    mockrelay serve --mode replay

Use when: running tests, CI, offline dev, deterministic demos.

## passthrough

Forwards, never records.

    mockrelay serve --mode passthrough

Use when: you want the proxy for observability without committing fixtures.

## hybrid

Serves fixtures when matched; falls through to upstream and records when not.

    mockrelay serve --mode hybrid

Use when: fixtures are incomplete and you want them to grow organically.

## Per-request override

    curl -H "X-MockRelay-Mode: passthrough" http://localhost:8080/gh/users/octocat

## Per-route override

    upstreams:
      local:
        base_url: "http://localhost:9000"
        mode: record
        routes:
          "/v1/slow":
            latency_ms: 800
          "/v1/fail":
            error_injection:
              status: 503
              rate: 1.0
