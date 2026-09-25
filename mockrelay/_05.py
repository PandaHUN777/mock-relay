from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml as _01
    _02 = True
except ImportError:
    _02 = False


class _03:
    def __init__(self, data: Dict[str, Any]):
        self.latency_ms: Optional[int] = data.get("latency_ms")
        self.error_injection: Optional[Dict[str, Any]] = data.get("error_injection")
        self.mode: Optional[str] = data.get("mode")
        self.match_mode: Optional[str] = data.get("match_mode")
        self.fuzzy_threshold: Optional[float] = data.get("fuzzy_threshold")
        self.ignore_case: Optional[bool] = data.get("ignore_case")
        self.match_priority: Optional[Any] = data.get("match_priority")


class _04:
    def __init__(self, name: str, data: Dict[str, Any]):
        self.name = name
        self.base_url: str = data["base_url"]
        self.mode: Optional[str] = data.get("mode")
        self.match_mode: Optional[str] = data.get("match_mode")
        self.fuzzy_threshold: Optional[float] = data.get("fuzzy_threshold")
        self.ignore_case: Optional[bool] = data.get("ignore_case")
        self.match_priority: Optional[Any] = data.get("match_priority")
        self.routes: Dict[str, _03] = {
            k: _03(v) for k, v in (data.get("routes") or {}).items()
        }

    def _05(self, path: str) -> Optional[_03]:
        best = None
        best_len = -1
        for prefix, ov in self.routes.items():
            if path.startswith(prefix) and len(prefix) > best_len:
                best = ov
                best_len = len(prefix)
        return best


class _06:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        d = data or {}
        self.listen: str = d.get("listen", "127.0.0.1:8080")
        self.admin_listen: str = d.get("admin_listen", "127.0.0.1:8081")
        self.fixtures_dir: Path = Path(d.get("fixtures_dir", "./fixtures"))
        self.mode: str = d.get("mode", "record")
        self.latency_ms: int = int(d.get("latency_ms", 0))
        self.error_injection: Optional[Dict[str, Any]] = d.get("error_injection")
        self.metrics_enabled: bool = bool(d.get("metrics_enabled", True))
        self.sequential: bool = bool(d.get("sequential", False))
        self.redact_headers: List[str] = d.get("redact_headers", [
            "authorization", "cookie", "x-api-key", "stripe-secret-key",
        ])
        self.normalize_json_paths: List[str] = d.get("normalize_json_paths", [
            "$.id", "$.created", "$.request_id",
        ])
        self.match_mode: str = str(d.get("match_mode", "auto"))
        self.fuzzy_threshold: float = float(d.get("fuzzy_threshold", 0.86))
        self.ignore_case: bool = bool(d.get("ignore_case", False))
        self.fuzzy_enabled: bool = bool(d.get("fuzzy_enabled", False))
        self.smart_record_paths: bool = bool(d.get("smart_record_paths", False))
        self.match_priority: Optional[Any] = d.get("match_priority")
        self.upstreams: Dict[str, _04] = {
            name: _04(name, u) for name, u in (d.get("upstreams") or {}).items()
        }
        self.fixtures_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _07(cls, path: Path) -> "_06":
        if not path.exists():
            return cls()
        text = path.read_text()
        data = _01.safe_load(text) if _02 else json.loads(text)
        return cls(data or {})

    def _08(self, upstream: str, path: str = "") -> str:
        up = self.upstreams.get(upstream)
        if not up:
            return self.mode
        ov = up._05(path) if path else None
        if ov and ov.mode:
            return ov.mode
        if up.mode:
            return up.mode
        return self.mode

    def _09(self, upstream: str, path: str = "") -> int:
        up = self.upstreams.get(upstream)
        if up:
            ov = up._05(path) if path else None
            if ov and ov.latency_ms is not None:
                return ov.latency_ms
        return self.latency_ms

    def _10(self, upstream: str, path: str = "") -> Optional[Dict[str, Any]]:
        up = self.upstreams.get(upstream)
        if up:
            ov = up._05(path) if path else None
            if ov and ov.error_injection is not None:
                return ov.error_injection
        return self.error_injection

    def _11(self, upstream: str) -> Optional[str]:
        up = self.upstreams.get(upstream)
        return up.base_url if up else None

    def _12(self, upstream: str, path: str = "") -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "match_mode": self.match_mode,
            "fuzzy_threshold": self.fuzzy_threshold,
            "ignore_case": self.ignore_case,
            "fuzzy_enabled": self.fuzzy_enabled,
            "match_priority": self.match_priority,
        }
        up = self.upstreams.get(upstream)
        if up:
            self._13(out, up)
            if path:
                ov = up._05(path)
                if ov:
                    self._13(out, ov)
        return out

    def _13(self, out: Dict[str, Any], src: Any) -> None:
        for k in list(out):
            v = getattr(src, k, None)
            if v is not None:
                out[k] = v
