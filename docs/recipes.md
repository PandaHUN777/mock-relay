# Recipes

Real workflows you can paste and run.

## 1. Record once, replay forever

Terminal A:

    python examples/demo_upstream.py

Terminal B:

    mockrelay serve --mode record --config examples/mockrelay.demo.yaml

Terminal C:

    curl http://localhost:8080/local/v1/users

You now have `fixtures/local/*.json`. Stop Terminal B, restart in replay:

    mockrelay serve --mode replay --latency 150 --config examples/mockrelay.demo.yaml

Same curl. Same response. No upstream.

## 2. Point a real app at the proxy

    export STRIPE_BASE_URL=http://localhost:8080/stripe
    export GITHUB_API_URL=http://localhost:8080/gh

Run your app. Everything flows through MockRelay.

## 3. Test retry/backoff logic

Add to `mockrelay.yaml` under `upstreams`:

    stripe:
      base_url: "https://api.stripe.com"
      routes:
        "/v1/charges":
          error_injection:
            status: 429
            rate: 0.5
            body: { error: rate_limited, retry_after: 5 }

Half of the calls return 429. Your client should retry.

## 4. Simulate a slow upstream

    mockrelay serve --mode replay --latency 2000

Every response takes 2 seconds. Great for loading states.

## 5. One-off passthrough

    curl -H "X-MockRelay-Mode: passthrough" \
         http://localhost:8080/gh/users/octocat

Bypasses fixtures for that one call.

## 6. Health checks

    curl http://localhost:8080/_health
    curl http://localhost:8080/_ready

Use in Docker or systemd.

## 7. CI replay

Start MockRelay in replay mode, then run:

    python examples/ci_replay.py

Exit code 1 if any request misses a fixture.

## 8. Prune old fixtures

    mockrelay stats
    mockrelay clean --older-than 30
    mockrelay clean --older-than 30 --yes

## 9. Send redacted fixtures to a teammate

    git add fixtures/
    git commit -m "add fixtures"
    git push

Secrets are already `{{SECRET}}`. Volatile IDs are `{{NORMALIZED}}`.
