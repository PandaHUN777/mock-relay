from __future__ import annotations
import base64
import os
from typing import Optional

_01 = os.environ.get("SWIVEL_BRAND_KEY", "swivel-ice-v1")
_02 = "EQ5JBRIFWwwP"


def _03(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def _04(plain: str, key: Optional[str] = None) -> str:
    k = (key or _01).encode("utf-8")
    return base64.b64encode(_03(plain.encode("utf-8"), k)).decode("ascii")


def _05(blob: Optional[str] = None, key: Optional[str] = None) -> str:
    b = (blob or _02).strip()
    k = (key or _01).encode("utf-8")
    try:
        return _03(base64.b64decode(b), k).decode("utf-8")
    except Exception:
        return "by swivel"
