from __future__ import annotations
import re
from typing import Any, Dict, List

_01 = "{{SECRET}}"
_02 = re.compile(r"Bearer\s+[A-Za-z0-9._\-]+")
_03 = re.compile(r"sk_(live|test)_[A-Za-z0-9]+")
_04 = re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")


def _05(headers: Dict[str, str], redact_list: List[str]) -> Dict[str, str]:
    rl = {h.lower() for h in redact_list}
    return {k: (_01 if k.lower() in rl else v) for k, v in headers.items()}


def _06(text: str) -> str:
    text = _02.sub("Bearer {{SECRET}}", text)
    text = _03.sub("sk_{{SECRET}}", text)
    text = _04.sub("ghp_{{SECRET}}", text)
    return text


def _07(value: Any) -> Any:
    if isinstance(value, str):
        return _06(value)
    if isinstance(value, dict):
        return {k: _07(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_07(v) for v in value]
    return value
