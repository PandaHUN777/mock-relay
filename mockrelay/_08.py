from __future__ import annotations
from typing import Any, List

_01 = "{{NORMALIZED}}"


def _02(body: Any, paths: List[str]) -> Any:
    if not paths or not isinstance(body, (dict, list)):
        return body
    body = _03(body)
    for p in paths:
        if not p.startswith("$."):
            continue
        _04(body, p[2:].split("."))
    return body


def _04(node: Any, keys: List[str]) -> None:
    if not keys:
        return
    k = keys[0]
    if isinstance(node, dict) and k in node:
        if len(keys) == 1:
            node[k] = _01
        else:
            _04(node[k], keys[1:])
    elif isinstance(node, list):
        for item in node:
            _04(item, keys)


def _03(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _03(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_03(v) for v in obj]
    return obj
