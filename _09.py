from __future__ import annotations
from typing import Any, Dict, List, Optional

from ._06 import _06 as _01


def _02(actual: Any, expected: Dict[str, Any]) -> bool:
    if not isinstance(actual, dict):
        return False
    for k, v in expected.items():
        if k not in actual:
            return False
        if isinstance(v, dict) and isinstance(actual[k], dict):
            if not _02(actual[k], v):
                return False
        elif actual[k] != v:
            return False
    return True


def _03(fx: _01, method: str, path: str,
        query: Dict[str, List[str]], body: Any) -> bool:
    m = fx.match
    if m.method.upper() != method.upper():
        return False
    if m.path != path:
        return False
    for k, v in m.query_subset.items():
        if query.get(k) != v:
            return False
    if m.body_contains and not _02(body, m.body_contains):
        return False
    return True


def _04(fx: _01) -> int:
    return len(fx.match.body_contains or {}) * 10 + len(fx.match.query_subset)


def _05(fixtures: List[_01], method: str, path: str,
        query: Dict[str, List[str]], body: Any) -> Optional[_01]:
    cands = [f for f in fixtures if _03(f, method, path, query, body)]
    if not cands:
        return None
    cands.sort(key=lambda f: (-_04(f), f.call_index, f.id))
    return cands[0]


def _06(fixtures: List[_01], method: str, path: str,
        query: Dict[str, List[str]], body: Any,
        counter: Dict[str, int]) -> Optional[_01]:
    cands = [f for f in fixtures if _03(f, method, path, query, body)]
    if not cands:
        return None
    cands.sort(key=lambda f: (f.call_index, f.id))
    key = f"{method.upper()} {path}"
    idx = counter.get(key, 0)
    chosen = cands[idx % len(cands)]
    counter[key] = idx + 1
    return chosen
