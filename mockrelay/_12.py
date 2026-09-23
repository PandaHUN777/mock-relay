from __future__ import annotations
import json
import ssl
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple

from ._05 import _06 as _01


def _02(raw: bytes, content_type: str) -> Any:
    if not raw:
        return None
    if "application/json" in content_type:
        try:
            return json.loads(raw)
        except Exception:
            return raw.decode("utf-8", "replace")
    if "application/x-www-form-urlencoded" in content_type:
        from urllib.parse import parse_qs
        return {k: v for k, v in parse_qs(raw.decode()).items()}
    return raw.decode("utf-8", "replace")


def _03(body: Any) -> bytes:
    if body is None:
        return b""
    if isinstance(body, (dict, list)):
        return json.dumps(body).encode()
    if isinstance(body, bytes):
        return body
    return str(body).encode()


_04 = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "host", "content-length",
}


def _05(url: str, method: str, headers: Dict[str, str], body: Optional[bytes],
        ) -> Tuple[int, Dict[str, str], bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return resp.status, dict(resp.getheaders()), resp.read()
    except urllib.error.HTTPError as e:
        hdrs = dict(e.headers.items()) if e.headers else {}
        return e.code, hdrs, e.read()


def _06(s: str) -> Tuple[str, int]:
    host, _, port = s.partition(":")
    return (host or "127.0.0.1"), int(port or 8080)
