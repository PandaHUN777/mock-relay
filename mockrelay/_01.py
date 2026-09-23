from __future__ import annotations
from typing import Any, Dict

_01: Dict[str, Any] = {
    "theme": "ice", "speed": "000", "view": True, "color": True,
    "width": 56, "progress_width": 32, "bold_headers": True,
    "unicode": True, "prefix": "\u25c7", "ok_glyph": "\u2713", "err_glyph": "\u2717",
    "warn_glyph": "!", "info_glyph": "\u2192",
    "brand": "by swivel", "brand_show": True, "brand_key": "swivel-ice-v1",
    "anim_style": "dots", "anim_speed": "080", "auto_load": True,
}
_02 = {"brand", "brand_key"}


class _03:
    def __init__(self) -> None:
        object.__setattr__(self, "_01", dict(_01))
        object.__setattr__(self, "_02", set(_02))

    def _04(self, k, d=None):
        return self._01.get(k, d)

    def _05(self, k, v):
        if k in self._02:
            raise PermissionError(f"locked: {k}")
        self._01[k] = v

    def _06(self, k):
        self._02.add(k)

    def _07(self, k):
        self._02.discard(k)

    def _08(self):
        return dict(self._01)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        d = object.__getattribute__(self, "_01")
        if name in d:
            return d[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        elif name in self._02:
            raise PermissionError(f"locked: {name}")
        else:
            self._01[name] = value


_09 = _03()


def _10(k: str) -> None:
    _09._07(k)


def _11(k: str) -> None:
    _09._06(k)
