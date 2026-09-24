from __future__ import annotations
from typing import Dict

from ._10 import _04 as _01


def _02(store: _01) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    if not store.root.exists():
        return counts
    for d in sorted(store.root.iterdir()):
        if d.is_dir():
            counts[d.name] = sum(1 for _ in d.glob("*.json"))
    return counts
