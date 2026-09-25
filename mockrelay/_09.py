"""Smart matching: exact, wildcard, regex, fuzzy and JSON-aware rules."""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from ._06 import _06 as _01

_MODES = ("auto", "exact", "wildcard", "regex", "fuzzy")

_PREFIX: Tuple[Tuple[str, str], ...] = (
    ("exact:", "exact"),
    ("==", "exact"),
    ("wildcard:", "wildcard"),
    ("glob:", "wildcard"),
    ("re:", "regex"),
    ("regex:", "regex"),
    ("~/", "regex"),
    ("fuzzy:", "fuzzy"),
    ("~=", "fuzzy"),
)

_META = "*?["
_OPS = frozenset((
    "$eq", "$ne", "$not", "$gt", "$gte", "$lt", "$lte", "$in", "$nin",
    "$exists", "$regex", "$contains", "$startswith", "$endswith",
    "$len", "$type", "$any", "$all",
))
_BAND = {"exact": 4, "wildcard": 3, "regex": 2, "fuzzy": 1}
_RANK = {"exact": 1000, "case": 960, "path": 950,
         "wildcard": 600, "regex": 400, "fuzzy": 100}
_TYPES: Dict[str, Any] = {
    "string": str, "number": (int, float), "integer": int, "float": float,
    "bool": bool, "null": type(None), "array": (list, tuple), "object": dict,
}
_WS = re.compile(r"\s+")
_INT = re.compile(r"^\d+$")
_SEL = re.compile(r"\[([^\]]*)\]")
_META_RE = re.compile(r"[*?\[]")
_PATH_META_RE = re.compile(r"[*\[]")
_UUID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
_CACHE_MAX = 512

_GLOB: Dict[Tuple[str, bool], Any] = {}
_RX: Dict[Tuple[str, bool], Any] = {}


@dataclass(frozen=True)
class _07:
    mode: str = "auto"
    threshold: float = 0.86
    ignore_case: bool = False
    fuzzy_enabled: bool = False


def _08(s: Any) -> str:
    t = str(s or "")
    for sep in ("#", "?"):
        if sep in t:
            t = t.split(sep, 1)[0]
    t = _WS.sub("", t)
    if t and not t.startswith("/"):
        t = "/" + t
    while "//" in t:
        t = t.replace("//", "/")
    if len(t) > 1:
        t = t.rstrip("/") or "/"
    return t or "/"


def _09(pat: str, ignore_case: bool = False):
    key = (pat, ignore_case)
    hit = _GLOB.get(key)
    if hit is not None:
        return hit
    out: List[str] = []
    i, n = 0, len(pat)
    while i < n:
        c = pat[i]
        if c == "*":
            if i + 1 < n and pat[i + 1] == "*":
                out.append(".*")
                i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[":
            j = pat.find("]", i + 1)
            if j == -1:
                out.append(re.escape(c))
                i += 1
            else:
                out.append("[" + pat[i + 1:j].replace("\\", "\\\\") + "]")
                i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    rx = re.compile("^" + "".join(out) + "$",
                    re.IGNORECASE if ignore_case else 0)
    if len(_GLOB) >= _CACHE_MAX:
        _GLOB.clear()
    _GLOB[key] = rx
    return rx


def _10(pat: str, ignore_case: bool = False):
    key = (pat, ignore_case)
    if key in _RX:
        return _RX[key]
    try:
        rx: Any = re.compile(pat, re.IGNORECASE if ignore_case else 0)
    except re.error:
        rx = False
    if len(_RX) >= _CACHE_MAX:
        _RX.clear()
    _RX[key] = rx
    return rx


def _11(pat: Any, mode: str = "auto") -> Tuple[str, str]:
    s = pat if isinstance(pat, str) else str(pat)
    low = s.lower()
    for pfx, kind in _PREFIX:
        if low.startswith(pfx):
            return kind, s[len(pfx):].strip()
    if mode in _MODES and mode != "auto":
        return mode, s
    if _PATH_META_RE.search(s):
        return "wildcard", s
    return "exact", s


def _12(pat: Any, actual: Any, opts: Optional[_07] = None,
        mode: str = "auto") -> Optional[int]:
    o = opts or _07()
    auto = mode == "auto" and o.mode == "auto"
    kind, body = _11(pat, o.mode if mode == "auto" else mode)
    act = actual if isinstance(actual, str) else str(actual)
    if kind == "exact":
        if body == act:
            return _RANK["exact"]
        if o.ignore_case and body.lower() == act.lower():
            return _RANK["case"]
        if body.startswith("/") and _08(body) == _08(act):
            return _RANK["path"]
    elif kind == "wildcard":
        if auto and body == act:
            return _RANK["exact"]
        rx = _09(body, o.ignore_case)
        if rx.match(act) or (body.startswith("/") and rx.match(_08(act))):
            return _RANK["wildcard"]
    elif kind == "regex":
        rx = _10(body, o.ignore_case)
        if rx and rx.match(act):
            return _RANK["regex"]
    elif _20(body, act) >= o.threshold:
        return _RANK["fuzzy"]
    if o.fuzzy_enabled and kind != "fuzzy" and _20(body, act) >= o.threshold:
        return _RANK["fuzzy"]
    return None


def _13(e: Any, a: Any, opts: Optional[_07] = None,
        mode: str = "auto") -> bool:
    o = opts or _07()
    if isinstance(e, str):
        if not isinstance(a, str):
            return False
        return _12(e, a, o, mode) is not None
    if isinstance(e, bool) or isinstance(a, bool):
        return isinstance(e, bool) and isinstance(a, bool) and e == a
    if isinstance(e, dict):
        return _14(e, a, o, mode)
    if isinstance(e, (list, tuple)):
        return _14(e, a, o, mode)
    if e is None or a is None:
        return e is None and a is None
    if isinstance(e, (int, float)) and isinstance(a, (int, float)):
        return float(e) == float(a)
    if isinstance(e, (int, float)) or isinstance(a, (int, float)):
        return False
    return e == a


def _14(e: Any, a: Any, opts: Optional[_07] = None,
        mode: str = "auto") -> bool:
    o = opts or _07()
    if isinstance(e, dict):
        if e and all(k in _OPS for k in e):
            return all(_18(k, e[k], a, o, mode) for k in e)
        if not isinstance(a, dict):
            return False
        for k, v in e.items():
            if not _15(k, v, a, o, mode):
                return False
        return True
    if isinstance(e, (list, tuple)):
        if not isinstance(a, (list, tuple)):
            return False
        if all(not isinstance(x, (dict, list, tuple)) for x in e):
            if len(e) != len(a):
                return False
            return all(_13(x, y, o, mode) for x, y in zip(e, a))
        return all(any(_13(x, y, o, mode) for y in a) for x in e)
    return _13(e, a, o, mode)


def _15(k: Any, v: Any, a: Any, opts: Optional[_07] = None,
        mode: str = "auto") -> bool:
    o = opts or _07()
    if not isinstance(k, str) or not k or not isinstance(a, dict):
        return False
    want = _19(v)
    if want is not None:
        if k in a:
            return (a[k] is not None) == want
        if _META_RE.search(k):
            rx = _09(k, o.ignore_case)
            return any((av is not None) == want for ak, av in a.items()
                       if rx.match(ak))
        if o.ignore_case:
            return any((av is not None) == want for ak, av in a.items()
                       if ak.lower() == k.lower())
        return not want
    if k in a:
        return _14(v, a[k], o, mode)
    if k in ("*", "$"):
        return any(_14(v, av, o, mode) for av in a.values())
    if k.startswith("$."):
        k = k[2:]
    if k.startswith(".."):
        return _17(k[2:], v, a, o, mode)
    if _META_RE.search(k) and "[" not in k:
        rx = _09(k, o.ignore_case)
        return any(rx.match(ak) and _14(v, av, o, mode)
                   for ak, av in a.items())
    if "." in k or "[" in k:
        return any(_14(v, h, o, mode) for h in _16(a, k))
    if o.ignore_case:
        lk = k.lower()
        return any(ak.lower() == lk and _14(v, av, o, mode)
                   for ak, av in a.items())
    return False


def _16(node: Any, expr: str) -> List[Any]:
    parts = [p for p in expr.split(".") if p]
    if not parts:
        return []
    head, rest = parts[0], ".".join(parts[1:])
    key, idx = head, None
    if "[" in head:
        key = head.split("[", 1)[0]
        for sel in _SEL.findall(head):
            if sel.isdigit():
                idx = int(sel)
    if key:
        if not isinstance(node, dict) or key not in node:
            return []
        node = node[key]
    if idx is not None:
        if not isinstance(node, (list, tuple)) or idx >= len(node):
            return []
        node = (node[idx],)
    if not rest:
        return [node]
    out: List[Any] = []
    for item in (node if isinstance(node, (list, tuple)) else [node]):
        out.extend(_16(item, rest))
    return out


def _17(name: str, v: Any, node: Any, opts: Optional[_07] = None,
        mode: str = "auto", depth: int = 0) -> bool:
    o = opts or _07()
    if depth > 8:
        return False
    if isinstance(node, dict):
        for k, val in node.items():
            if k == name and _14(v, val, o, mode):
                return True
        return any(_17(name, v, val, o, mode, depth + 1)
                   for val in node.values())
    if isinstance(node, (list, tuple)):
        return any(_17(name, v, item, o, mode, depth + 1) for item in node)
    return False


def _18(name: str, arg: Any, a: Any, opts: Optional[_07] = None,
        mode: str = "auto") -> bool:
    o = opts or _07()
    if name == "$eq":
        return _14(arg, a, o, mode)
    if name in ("$ne", "$not"):
        return not _14(arg, a, o, mode)
    if name == "$exists":
        return (a is not None) == bool(arg)
    if name in ("$in", "$nin"):
        args = arg if isinstance(arg, (list, tuple)) else [arg]
        hit = any(_13(x, a, o, mode) for x in args)
        return hit if name == "$in" else not hit
    if name in ("$any", "$all"):
        seq = a if isinstance(a, (list, tuple)) else [a]
        args = arg if isinstance(arg, (list, tuple)) else [arg]
        if name == "$any":
            return any(any(_14(x, item, o, mode) for x in args)
                       for item in seq)
        return all(any(_14(x, item, o, mode) for item in seq) for x in args)
    if name in ("$gt", "$gte", "$lt", "$lte"):
        if a is None or isinstance(a, bool):
            return False
        if isinstance(arg, bool) or not isinstance(arg, (int, float, str)):
            return False
        if isinstance(a, (int, float)) and isinstance(arg, (int, float)):
            x, y = float(a), float(arg)
        elif isinstance(a, str) and isinstance(arg, str):
            x, y = a, arg
        else:
            return False
        if name == "$gt":
            return x > y
        if name == "$gte":
            return x >= y
        if name == "$lt":
            return x < y
        return x <= y
    if name == "$regex":
        pat = arg if isinstance(arg, str) else str(arg)
        rx = _10(pat, o.ignore_case)
        seq = a if isinstance(a, (list, tuple)) else [a]
        return bool(rx) and any(rx.match(x if isinstance(x, str) else str(x))
                                for x in seq)
    if name in ("$contains", "$startswith", "$endswith"):
        hay = arg if isinstance(arg, str) else str(arg)
        seq = a if isinstance(a, (list, tuple)) else [a]
        for item in seq:
            if isinstance(item, str):
                if name == "$contains" and hay in item:
                    return True
                if name == "$startswith" and item.startswith(hay):
                    return True
                if name == "$endswith" and item.endswith(hay):
                    return True
            elif name == "$contains" and isinstance(item, (list, tuple, dict)):
                sub = list(item.keys()) if isinstance(item, dict) else list(item)
                if any(_14(hay, x, o, mode) for x in sub):
                    return True
        return False
    if name == "$len":
        try:
            n = len(a)
        except TypeError:
            return False
        if isinstance(arg, dict) and arg and all(k in _OPS for k in arg):
            return all(_18(k, arg[k], n, o, mode) for k in arg)
        return n == arg
    if name == "$type":
        want = str(arg).lower()
        t = _TYPES.get(want)
        if t is None:
            return False
        if want in ("number", "integer", "float") and isinstance(a, bool):
            return False
        return isinstance(a, t)
    return False


def _19(v: Any) -> Optional[bool]:
    if isinstance(v, dict) and len(v) == 1 and "$exists" in v:
        arg = v["$exists"]
        if isinstance(arg, bool):
            return arg
    return None


def _20(a: str, b: str) -> float:
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0
    if len(a) * len(b) > 250000:
        return 1.0 if (a.startswith(b) or b.startswith(a)) else 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def _21(fx: _01, method: str, path: str, query: Dict[str, List[str]],
        body: Any, opts: Optional[_07] = None) -> Dict[str, Any]:
    base = opts or _07()
    m = fx.match
    o = _23(base, m)
    checks: List[Dict[str, Any]] = []

    want = str(getattr(m, "method", ""))
    m_ok = want.upper() == str(method or "").upper()
    checks.append({"name": "method", "ok": m_ok,
                   "detail": f"{want} vs {method}"})

    pat = getattr(m, "path", "")
    kind, _ = _11(pat, o.mode)
    prank = _12(pat, path, o, o.mode) if isinstance(pat, str) else None
    p_ok = prank is not None
    checks.append({"name": "path", "ok": p_ok,
                   "detail": f"{pat} [{kind}] vs {path}"})

    qs = getattr(m, "query_subset", None) or {}
    q_ok = _24(qs, query or {}, o, o.mode)
    checks.append({"name": "query", "ok": q_ok, "detail": f"{qs} vs {query}"})

    bc = getattr(m, "body_contains", None)
    if not bc:
        b_ok = True
    else:
        b_ok = isinstance(body, (dict, list)) and _14(bc, body, o, o.mode)
    checks.append({"name": "body", "ok": b_ok,
                   "detail": f"{bc} vs {type(body).__name__}"})

    matched = bool(m_ok and p_ok and q_ok and b_ok)
    return {
        "id": fx.id,
        "upstream": fx.upstream,
        "matched": matched,
        "strategy": kind if p_ok else "miss",
        "path_rank": prank or 0,
        "score": _04(fx, base) if matched else 0,
        "status": fx.response.status,
        "checks": checks,
    }


def _22(fixtures: List[_01], method: str, path: str,
        query: Dict[str, List[str]], body: Any,
        opts: Optional[_07] = None) -> List[Dict[str, Any]]:
    rows = [_21(f, method, path, query, body, opts) for f in fixtures]
    rows.sort(key=lambda r: (0 if r["matched"] else 1, -r["score"], r["id"]))
    return rows


def _23(base: Optional[_07], m: Any) -> _07:
    b = base or _07()
    mode = getattr(m, "match_mode", None) or b.mode
    if mode not in _MODES:
        mode = b.mode
    thr = getattr(m, "fuzzy_threshold", None)
    if thr is None:
        thr = b.threshold
    try:
        thr = float(thr)
    except (TypeError, ValueError):
        thr = b.threshold
    ic = getattr(m, "ignore_case", None)
    return _07(
        mode=mode,
        threshold=min(max(thr, b.threshold, 0.0), 1.0),
        ignore_case=b.ignore_case if ic is None else bool(ic),
        fuzzy_enabled=b.fuzzy_enabled or mode == "fuzzy",
    )


def _24(e: Any, a: Any, opts: Optional[_07] = None,
        mode: str = "auto") -> bool:
    o = opts or _07()
    if not isinstance(e, dict) or not e:
        return True
    if not isinstance(a, dict):
        a = {}
    for k, want in e.items():
        got = a.get(k)
        if got is None:
            rx = _09(str(k), o.ignore_case)
            hit = next((ak for ak in a if rx.match(ak)), None)
            if hit is None:
                return False
            got = a[hit]
        if isinstance(got, (str, int, float, bool)):
            got = [got]
        if not isinstance(got, (list, tuple)):
            return False
        if not isinstance(want, (list, tuple)):
            want = [want]
        wl = [x if isinstance(x, str) else str(x) for x in want]
        gl = [x if isinstance(x, str) else str(x) for x in got]
        if not wl:
            if gl:
                return False
            continue
        if not any(_12(w, g, o, mode) is not None for w in wl for g in gl):
            return False
    return True


def _25(path: Any) -> str:
    out: List[str] = []
    for seg in str(path or "").split("/"):
        if _INT.match(seg) or _UUID.match(seg):
            out.append("*")
        else:
            out.append(seg)
    return "/".join(out)


def _28() -> Tuple[str, ...]:
    return _MODES


def _29(d: Optional[Dict[str, Any]] = None) -> _07:
    src = d or {}
    mode = str(src.get("match_mode") or "auto").strip().lower()
    if mode not in _MODES:
        mode = "auto"
    try:
        thr = float(src.get("fuzzy_threshold", 0.86))
    except (TypeError, ValueError):
        thr = 0.86
    return _07(
        mode=mode,
        threshold=min(max(thr, 0.0), 1.0),
        ignore_case=bool(src.get("ignore_case", False)),
        fuzzy_enabled=bool(src.get("fuzzy_enabled", False)) or mode == "fuzzy",
    )


def _02(actual: Any, expected: Dict[str, Any]) -> bool:
    if not isinstance(actual, dict) or not isinstance(expected, dict):
        return False
    return _14(expected, actual, _07(), "auto")


def _03(fx: _01, method: str, path: str, query: Dict[str, List[str]],
        body: Any, opts: Optional[_07] = None) -> bool:
    return bool(_21(fx, method, path, query, body, opts)["matched"])


def _04(fx: _01, opts: Optional[_07] = None) -> int:
    m = fx.match
    o = _23(opts, m)
    kind, body = _11(getattr(m, "path", ""), o.mode)
    lit = len(_META_RE.sub("", body))
    score = _BAND.get(kind, 0) * 1000000
    score += min(len(m.body_contains or {}), 99) * 1000
    score += min(len(m.query_subset or {}), 99) * 10
    score += min(lit, 9)
    return score


def _05(fixtures: List[_01], method: str, path: str,
        query: Dict[str, List[str]], body: Any,
        opts: Optional[_07] = None) -> Optional[_01]:
    cands = [f for f in fixtures if _03(f, method, path, query, body, opts)]
    if not cands:
        return None
    cands.sort(key=lambda f: (-_04(f, opts), f.call_index, f.id))
    return cands[0]


def _06(fixtures: List[_01], method: str, path: str,
        query: Dict[str, List[str]], body: Any, counter: Dict[str, int],
        opts: Optional[_07] = None) -> Optional[_01]:
    cands = [f for f in fixtures if _03(f, method, path, query, body, opts)]
    if not cands:
        return None
    cands.sort(key=lambda f: (f.call_index, f.id))
    key = f"{method.upper()} {path}"
    idx = counter.get(key, 0)
    chosen = cands[idx % len(cands)]
    counter[key] = idx + 1
    return chosen
