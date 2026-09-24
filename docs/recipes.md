# Recipes

## 1. Record once, replay forever

    python examples/demo_upstream.py
    mockrelay serve --mode record
    curl http://localhost:8080/local/v1/users
    mockrelay serve --mode replay --latency 150

## 2. Point a real app at the proxy

    export STRIPE_BASE_URL=http://localhost:8080/stripe

## 3. Test retry/backoff

    routes:
      "/v1/charges":
        error_injection:
          status: 429
          rate: 0.5

## 4. Simulate a slow upstream

    mockrelay replay --latency 2000

## 5. Health checks

    curl http://localhost:8080/_health
