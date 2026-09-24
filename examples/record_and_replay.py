from __future__ import annotations
import json
import time
import urllib.request
from pathlib import Path


def _01(url, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, json.loads(r.read())


def _02(name, step):
    print(f"\n=== {name} ===")
    print(step)


def main():
    root = Path(__file__).resolve().parent.parent
    fixtures = root / "fixtures"
    if fixtures.exists():
        for p in fixtures.rglob("*.json"):
            p.unlink()

    _02("1. record", "start `python examples/demo_upstream.py` in another terminal")
    _02("2. record", "start `mockrelay serve --mode record` in another terminal")
    input("press ENTER when both are running...")

    _02("3. record", "hitting mockrelay, which forwards to the demo upstream")
    st, body = _01("http://localhost:8080/local/v1/users")
    print(f"status={st} users={len(body.get('users', []))}")

    _02("4. verify", "fixtures written:")
    for p in sorted(fixtures.rglob("*.json")):
        print("  " + str(p.relative_to(root)))

    _02("5. stop mockrelay", "Ctrl-C in the mockrelay terminal, then run:")
    print("  mockrelay serve --mode replay --latency 150")
    input("press ENTER when replay is running...")

    _02("6. replay", "same request, served from fixture, no upstream")
    t0 = time.time()
    st, body = _01("http://localhost:8080/local/v1/users")
    dt = int((time.time() - t0) * 1000)
    print(f"status={st} users={len(body.get('users', []))} took={dt}ms")

    _02("7. injected error", "add to mockrelay.yaml under upstreams.local.routes:")
    print('  "/v1/users":')
    print("    error_injection:")
    print("      status: 429")
    print("      rate: 1.0")
    print("restart replay and re-run step 6 to see the 429")


if __name__ == "__main__":
    main()
