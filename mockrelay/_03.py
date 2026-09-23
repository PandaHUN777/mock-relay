from __future__ import annotations
import os
import sys
from typing import List, Optional, Tuple

from ._01 import _09 as _01

_02 = {
    "ice": ["#E0F2FE", "#BAE6FD", "#7DD3FC", "#38BDF8", "#0EA5E9", "#0369A1"],
    "fire": ["#FEF3C7", "#FCD34D", "#F59E0B", "#DC2626", "#991B1B"],
    "matrix": ["#D1FAE5", "#6EE7B7", "#10B981", "#047857", "#064E3B"],
    "vapor": ["#F0ABFC", "#E879F9", "#C026D3", "#A21CAF", "#701A75"],
    "sunset": ["#FED7AA", "#FB923C", "#F97316", "#EA580C", "#9A3412"],
}
_03 = dict(_02)
_04 = os.environ.get("SWIVEL_THEME") or _01.theme or "ice"
if _04 not in _03:
    _04 = next(iter(_03))

_05 = bool(os.environ.get("NO_COLOR")) or os.environ.get("TERM") == "dumb"


def _06() -> bool:
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def _07() -> bool:
    if os.environ.get("COLORTERM", "").lower() in ("truecolor", "24bit"):
        return True
    if os.environ.get("WT_SESSION"):
        return True
    if os.environ.get("TERM_PROGRAM", "") in ("vscode", "iTerm.app", "WezTerm", "kitty"):
        return True
    return os.environ.get("TERM", "").endswith("256color")


def _08() -> bool:
    if _05:
        return False
    if os.environ.get("SWIVEL_FORCE_COLOR") == "1":
        return True
    if not bool(_01.color):
        return False
    return _06() or _07()


_09 = _08()


def _10(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _11(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def _12(stops, t: float) -> Tuple[int, int, int]:
    if len(stops) == 1:
        return stops[0]
    seg = t * (len(stops) - 1)
    lo = int(seg // 1)
    hi = min(lo + 1, len(stops) - 1)
    l = seg - lo
    a, b = stops[lo], stops[hi]
    return (_11(a[0], b[0], l), _11(a[1], b[1], l), _11(a[2], b[2], l))


def _13(r: int, g: int, b: int, bold: bool = False) -> str:
    pre = "\x1b[1m" if bold else ""
    return f"{pre}\x1b[38;2;{r};{g};{b}m"


_14 = "\x1b[0m"


def _15(text: str, theme: Optional[str] = None, bold: Optional[bool] = None) -> str:
    if not _09 or len(text) == 0:
        return text
    if bold is None:
        bold = bool(_01.bold_headers)
    name = theme or _04
    stops = [_10(h) for h in _03.get(name, _03[_04])]
    n = max(len(text) - 1, 1)
    out: List[str] = []
    for i, ch in enumerate(text):
        r, g, b = _12(stops, i / n)
        out.append(_13(r, g, b, bold))
        out.append(ch)
    out.append(_14)
    return "".join(out)


def _16(name: str) -> None:
    global _04
    if name not in _03:
        raise ValueError(name)
    _04 = name


def _17() -> List[str]:
    return sorted(_03.keys())


def _18() -> str:
    return _04
