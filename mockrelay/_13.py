from __future__ import annotations
import http.server
import random
import socketserver
import threading
import time
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qsl, urlparse

from ._04 import _18 as _01
from ._05 import _06 as _01cfg
from ._06 import _01 as _02
from ._06 import _04 as _03
from ._06 import _05 as _04
from ._06 import _06 as _05
from ._07 import _05 as _06
from ._07 import _07 as _07
from ._08 import _02 as _08
from ._09 import _21 as _33
from ._09 import _22 as _32
from ._09 import _29 as _34
from ._09 import _25 as _35
from ._09 import _05 as _09
from ._09 import _06 as _10
from ._10 import _04 as _11
from ._11 import _01 as _12
from ._12 import _02 as _13
from ._12 import _03 as _14
from ._12 import _04 as _15
from ._12 import _05 as _16
from ._12 import _06 as _17


class _18:
    def __init__(self, cfg, store, metrics: _12):
        self.cfg = cfg
        self.store = store
        self.metrics = metrics
        self.counter: Dict[str, int] = {}
        self.lock = threading.Lock()


def _19(state: _18):
    cfg = state.cfg
    store = state.store
    metrics = state.metrics

    class _20(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            return

        def _21(self):
            raw_target = urlparse(self.path)
            parts = raw_target.path.lstrip("/").split("/", 1)
            if not parts or not parts[0]:
                return self._26(404, {"error": "missing upstream prefix"})
            upstream = parts[0]
            norm_path = "/" + (parts[1] if len(parts) > 1 else "")

            base_url = cfg._11(upstream)
            if not base_url:
                return self._26(502, {"error": f"unknown upstream '{upstream}'"})

            mode = cfg._08(upstream, norm_path)
            latency = cfg._09(upstream, norm_path)
            err_inj = cfg._10(upstream, norm_path)
            method = self.command
            opts = _34(cfg._12(upstream, norm_path))

            cl = int(self.headers.get("Content-Length", 0) or 0)
            raw = self.rfile.read(cl) if cl else b""

            q_multi: Dict[str, List[str]] = {}
            for k, v in parse_qsl(raw_target.query, keep_blank_values=True):
                q_multi.setdefault(k, []).append(v)
            req_body = _13(raw, self.headers.get("content-type", ""))

            if err_inj and random.random() < float(err_inj.get("rate", 1.0)):
                st = int(err_inj.get("status", 500))
                body = err_inj.get("body") or {"error": "injected", "status": st}
                metrics._06(upstream, st, "inject")
                metrics._07(method, norm_path, st, "inject")
                return self._26(st, body)

            if mode in ("replay", "hybrid"):
                fixtures = list(store._07(upstream))
                if cfg.sequential:
                    with state.lock:
                        hit = _10(fixtures, method, norm_path, q_multi, req_body,
                                  state.counter, opts)
                else:
                    hit = _09(fixtures, method, norm_path, q_multi, req_body, opts)
                if hit:
                    if latency:
                        time.sleep(latency / 1000.0)
                    info = _33(hit, method, norm_path, q_multi, req_body, opts)
                    metrics._06(upstream, hit.response.status, "replay")
                    metrics._07(method, norm_path, hit.response.status, "replay")
                    return self._27(hit.response, hit.id, info)
                if mode == "replay":
                    metrics._06(upstream, 501, "replay")
                    metrics._07(method, norm_path, 501, "replay")
                    miss = _32(fixtures, method, norm_path, q_multi, req_body, opts)
                    return self._26(501, {
                        "error": "no fixture matched",
                        "method": method,
                        "path": norm_path,
                        "match_mode": opts.mode,
                        "nearest": [m["id"] for m in miss[:5]],
                    })

            target_url = base_url.rstrip("/") + norm_path
            if raw_target.query:
                target_url += "?" + raw_target.query
            headers = {k: v for k, v in self.headers.items()
                       if k.lower() not in _15}
            try:
                st, hdrs, rbody = _16(target_url, method, headers,
                                      raw if raw else None)
            except Exception as e:
                metrics._06(upstream, 502, "error")
                metrics._07(method, norm_path, 502, "error")
                return self._26(502, {"error": "upstream failed", "detail": str(e)})

            if mode in ("record", "hybrid"):
                red_req = _06(dict(self.headers), cfg.redact_headers)
                red_resp = {k: v for k, v in hdrs.items() if k.lower() not in _15}
                resp_parsed = _13(rbody, hdrs.get("Content-Type", ""))
                norm_resp = _08(resp_parsed, cfg.normalize_json_paths)

                bc = None
                if isinstance(req_body, dict) and req_body:
                    bc = {k: v for k, v in list(req_body.items())[:5]
                          if not isinstance(v, (dict, list))}

                match_path = _35(norm_path) if cfg.smart_record_paths else norm_path
                match = _02(method=method, path=match_path,
                            query_subset=q_multi, body_contains=bc,
                            match_mode=None if opts.mode == "auto" else opts.mode)
                fixture = _05(
                    id=store._09(upstream, match),
                    upstream=upstream,
                    match=match,
                    request=_03(method=method, path=norm_path, query=q_multi,
                                headers=red_req,
                                body=(req_body if isinstance(req_body, (dict, list))
                                      else (_07(req_body) if isinstance(req_body, str) else None))),
                    response=_04(status=st, headers=red_resp, body=norm_resp),
                    normalize=cfg.normalize_json_paths,
                )
                store._06(upstream, fixture)
                hdrs = dict(hdrs)
                hdrs["X-MockRelay-Match"] = "record"

            if latency:
                time.sleep(latency / 1000.0)
            metrics._06(upstream, st, mode)
            metrics._07(method, norm_path, st, mode)
            self._28(st, rbody, hdrs)

        def _26(self, status: int, body_dict: Any):
            self._28(status, __import__("json").dumps(body_dict).encode(),
                     {"Content-Type": "application/json"})

        def _27(self, rec, fid: str = "", info: Optional[Dict[str, Any]] = None):
            hdrs = {k: v for k, v in rec.headers.items() if k.lower() not in _15}
            if info:
                hdrs["X-MockRelay-Match"] = str(info.get("strategy") or "exact")
                hdrs["X-MockRelay-Fixture"] = str(fid)
                hdrs["X-MockRelay-Score"] = str(info.get("score") or 0)
                if int(info.get("priority") or 0):
                    hdrs["X-MockRelay-Priority"] = str(info["priority"])
            self._28(rec.status, _14(rec.body), hdrs)

        def _28(self, status: int, body: bytes, headers: Dict[str, str]):
            self.send_response(status)
            for k, v in headers.items():
                if k.lower() in _15:
                    continue
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                try:
                    self.wfile.write(body)
                except Exception:
                    pass

        def do_GET(self): self._21()
        def do_POST(self): self._21()
        def do_PUT(self): self._21()
        def do_PATCH(self): self._21()
        def do_DELETE(self): self._21()
        def do_HEAD(self): self._21()
        def do_OPTIONS(self): self._21()

    return _20


class _29(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def _30(state: _18):
    host, port = _17(state.cfg.listen)
    handler = _19(state)
    srv = _29((host, port), handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv
