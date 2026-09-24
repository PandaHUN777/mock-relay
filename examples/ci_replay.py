from __future__ import annotations
import json
import sys
import urllib.error
import urllib.request


_01 = [
    ("GET", "http://localhost:8080/gh/users/octocat", None),
    ("GET", "http://localhost:8080/local/v1/users", None),
]


def _02(method, url, body):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        print(f"  {method} {url} -> transport error: {e}")
        return 0


def main():
    failed = 0
    for method, url, body in _01:
        st = _02(method, url, body)
        marker = "ok" if st and st < 400 else "MISS"
        print(f"  [{marker}] {st} {method} {url}")
        if not st or st >= 400:
            failed += 1
    if failed:
        print(f"\n{failed} checks failed")
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
