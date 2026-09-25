from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class _01:
    method: str
    path: str
    query_subset: Dict[str, List[str]] = field(default_factory=dict)
    body_contains: Optional[Dict[str, Any]] = None
    match_mode: Optional[str] = None
    fuzzy_threshold: Optional[float] = None
    ignore_case: Optional[bool] = None
    priority: Optional[int] = None

    def _02(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def _03(cls, d: Dict[str, Any]) -> "_01":
        prio = d.get("priority")
        if prio is not None:
            try:
                prio = int(prio)
            except (TypeError, ValueError):
                prio = None
        return cls(
            method=d["method"],
            path=d["path"],
            query_subset=d.get("query_subset") or {},
            body_contains=d.get("body_contains"),
            match_mode=d.get("match_mode"),
            fuzzy_threshold=d.get("fuzzy_threshold"),
            ignore_case=d.get("ignore_case"),
            priority=prio,
        )


@dataclass
class _04:
    method: str
    path: str
    query: Dict[str, List[str]] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None


@dataclass
class _05:
    status: int
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None


@dataclass
class _06:
    id: str
    upstream: str
    match: _01
    request: _04
    response: _05
    normalize: List[str] = field(default_factory=list)
    recorded_at: Optional[str] = None
    call_index: int = 0

    def _07(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "upstream": self.upstream,
            "match": self.match._02(),
            "request": asdict(self.request),
            "response": asdict(self.response),
            "normalize": self.normalize,
            "recorded_at": self.recorded_at,
            "call_index": self.call_index,
        }

    @classmethod
    def _08(cls, d: Dict[str, Any]) -> "_06":
        return cls(
            id=d["id"],
            upstream=d["upstream"],
            match=_01._03(d["match"]),
            request=_04(**d["request"]),
            response=_05(**d["response"]),
            normalize=d.get("normalize") or [],
            recorded_at=d.get("recorded_at"),
            call_index=d.get("call_index", 0),
        )
