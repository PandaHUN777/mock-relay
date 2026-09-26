"""Provides terminal user interface utilities, including text formatting, status logging, and animated loading spinners."""
from __future__ import annotations
import contextlib
import sys
import threading
import time
from typing import Dict, List, Optional

from ._01 import _09 as _01
from ._02 import _05 as _02
from ._03 import _14 as _03
from ._03 import _09 as _04
from ._03 import _15 as _05

_06: Dict[str, List[str]] = {
    "dots": ["\u280b","\u2819","\u2839","\u2838","\u283c","\u2834","\u2826","\u2827","\u2807","\u280f"],
    "bar": ["|","/","-","\\"],
    "arrow": ["\u2190","\u2196","\u2191","\u2197","\u2192","\u2198","\u2193","\u2199"],
    "pulse": ["\u00b7","\u2022","\u25cf","\u2022"],
    "wave": ["\u2581","\u2582","\u2583","\u2584","\u2585","\u2586","\u2587","\u2588","\u2587","\u2586","\u2585","\u2584","\u2583","\u2582"],
    "circle": ["\u25d0","\u25d3","\u25d1","\u25d2"],
    "diamond": ["\u25c7","\u25c8","\u25c6","\u25c8"],
    "orbit": ["\u25d0","\u25d3","\u25d1","\u25d2","\u25d0"],
    "scan": ["\u258f","\u258e","\u258d","\u258c","\u258b","\u258a","\u2589","\u2588","\u2589","\u258a","\u258b","\u258c","\u258d","\u258e"],
}


def _07(name: str) -> List[str]:
    return _06.get(name, _06["dots"])


def _08(name: str = "dots") -> List[str]:
    return _07(name)


def _09() -> float:
    s = str(getattr(_01, "anim_speed", "080")).strip()
    return int(s) / 1000.0 if s.isdigit() else 0.08


def _10(s: str) -> int:
    out, i = 0, 0
    while i < len(s):
        if s[i] == "\x1b":
            j = s.find("m", i)
            i = (j + 1) if j != -1 else i + 1
        else:
            out += 1
            i += 1
    return out


def _11(title: str = "M O C K R E L A Y", theme: Optional[str] = None,
        show_brand: bool = True) -> None:
    if not _01.view:
        return
    inner = int(_01.width)
    pad_l = max(0, (inner - len(title)) // 2)
    pad_r = max(0, inner - len(title) - pad_l)
    line = (" " * pad_l) + title + (" " * pad_r)
    if len(line) > inner:
        line = line[:inner]
    print()
    print("  " + _05("\u256d" + "\u2500" * inner + "\u256e", theme))
    print("  " + _05("\u2502" + line + "\u2502", theme, bold=True))
    print("  " + _05("\u2570" + "\u2500" * inner + "\u256f", theme))
    if show_brand:
        _12()
    print()


def _12(text: Optional[str] = None, theme: Optional[str] = None) -> None:
    if not _01.brand_show or not _01.view:
        return
    label = text or _02()
    print("  " + _05(f"\u00b7 {label} \u00b7", theme))


def _13(text: str, theme: Optional[str] = None) -> None:
    if not _01.view:
        return
    print()
    print(_05(text, theme, bold=True))


def _14(width: Optional[int] = None, char: str = "\u2500",
        theme: Optional[str] = None) -> None:
    if not _01.view:
        return
    print(_05(char * (width or int(_01.width)), theme))


def _15(label: str, width: Optional[int] = None, theme: Optional[str] = None) -> None:
    if not _01.view:
        return
    w = width or int(_01.width)
    l = f" {label} "
    side = max(0, (w - len(l)) // 2)
    print(_05("\u2500" * side + l + "\u2500" * (w - side - len(l)), theme))


def _16(key, value, key_width: int = 16, theme: Optional[str] = None,
        indent: int = 2) -> None:
    if not _01.view:
        return
    pad = " " * max(1, key_width - len(str(key)))
    print(" " * indent + _05(f"{key}{pad}", theme) + str(value))


def _17(headers: List[str], rows: List[List], theme: Optional[str] = None,
        indent: int = 2, gap: int = 2) -> None:
    if not _01.view:
        return
    cols = len(headers)
    widths = [len(str(h)) for h in headers]
    for r in rows:
        for i in range(cols):
            widths[i] = max(widths[i], len(str(r[i] if i < len(r) else "")))
    pad = " " * indent
    print(pad + (" " * gap).join(
        _05(str(headers[i]).ljust(widths[i]), theme, bold=True) for i in range(cols)))
    print(pad + _05("\u2500" * (sum(widths) + gap * (cols - 1)), theme))
    for r in rows:
        cells = [str(r[i] if i < len(r) else "").ljust(widths[i]) for i in range(cols)]
        print(pad + (" " * gap).join(cells))


def _18(kind: str, message: str) -> None:
    if not _01.view:
        return
    g = {"ok": _01.ok_glyph, "run": _01.prefix,
         "info": _01.info_glyph, "warn": _01.warn_glyph,
         "err": _01.err_glyph}.get(kind, _01.info_glyph)
    c = {"ok": "\x1b[32m", "run": "\x1b[35m", "info": "\x1b[36m",
         "warn": "\x1b[33m", "err": "\x1b[31m"}.get(kind, "\x1b[36m")
    print(f"  {c}{g}{_03} {message}" if _04 else f"  {g} {message}")


def _19(content: str, title: Optional[str] = None, width: Optional[int] = None,
        theme: Optional[str] = None) -> None:
    if not _01.view:
        return
    lines = content.splitlines() or [""]
    inner = width or max(int(_01.width), max(_10(l) for l in lines) + 4)
    inner = max(inner, max(_10(l) for l in lines) + 2)
    top = "\u256d" + "\u2500" * inner + "\u256e"
    if title:
        tl = f" {title} "
        pad = inner - len(tl)
        left = pad // 2
        right = pad - left
        top = "\u256d" + "\u2500" * left + tl + "\u2500" * right + "\u256e"
    print("  " + _05(top, theme))
    for ln in lines:
        pad = inner - _10(ln) - 2
        print("  " + _05("\u2502", theme) + " " + ln + " " * pad + " " + _05("\u2502", theme))
    print("  " + _05("\u2570" + "\u2500" * inner + "\u256f", theme))


@contextlib.contextmanager
def _20(label: str = "loading", style: str = "dots", theme: Optional[str] = None):
    frames = _07(style)
    stop = threading.Event()

    def _run():
        i = 0
        while not stop.is_set():
            sys.stdout.write("\r  " + _05(frames[i % len(frames)], theme) + " " + label)
            sys.stdout.flush()
            i += 1
            time.sleep(_09())

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    try:
        yield
    finally:
        stop.set()
        t.join()
        sys.stdout.write("\r  " + _05(_01.ok_glyph, theme) + " " + label + " " * 30 + "\n")
        sys.stdout.flush()
