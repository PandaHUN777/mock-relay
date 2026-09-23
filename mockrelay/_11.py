from __future__ import annotations
import threading
import time
from collections import Counter
from typing import Dict, List


class _01:
    def __init__(self) -> None:
        self._01 = threading.Lock()
        self._02: Counter = Counter()
        self._03: Counter = Counter()
        self._04: Counter = Counter()
        self._05: List[Dict] = []

    def _06(self, key: str, status: int, mode: str) -> None:
        with self._01:
            self._02[key] += 1
            self._03[f"{key}:{status}"] += 1
            self._04[mode] += 1

    def _07(self, method: str, path: str, status: int, mode: str) -> None:
        with self._01:
            self._05.insert(0, {
                "t": time.strftime("%H:%M:%S"),
                "m": method, "p": path, "s": status, "mode": mode,
            })
            del self._05[50:]

    def _08(self) -> str:
        lines: List[str] = []
        with self._01:
            lines.append("# HELP mockrelay_requests_total Total requests")
            lines.append("# TYPE mockrelay_requests_total counter")
            for key, n in self._02.items():
                lines.append(f'mockrelay_requests_total{{key="{key}"}} {n}')
            lines.append("# HELP mockrelay_responses_total Responses by status")
            lines.append("# TYPE mockrelay_responses_total counter")
            for key, n in self._03.items():
                lines.append(f'mockrelay_responses_total{{key="{key}"}} {n}')
            lines.append("# HELP mockrelay_mode_total Requests by mode")
            lines.append("# TYPE mockrelay_mode_total counter")
            for mode, n in self._04.items():
                lines.append(f'mockrelay_mode_total{{mode="{mode}"}} {n}')
        return "\n".join(lines) + "\n"

    def _09(self) -> List[Dict]:
        with self._01:
            return list(self._05)
