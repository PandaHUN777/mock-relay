# Modes

## record

Forwards every request upstream. Writes a fixture per request/response pair.

## replay

Serves from fixtures only. Never touches the network.

## passthrough

Forwards, never records.

## hybrid

Serves fixtures when matched; falls through to upstream and records when not.

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
