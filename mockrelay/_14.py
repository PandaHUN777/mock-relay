from __future__ import annotations
import http.server
import json
import socketserver
import threading
from typing import Dict, List
from urllib.parse import parse_qs, parse_qsl, urlparse

from ._13 import _18 as _01
from ._13 import _29 as _02
from ._12 import _06 as _03
from ._09 import _22 as _11
from ._09 import _29 as _12


_04 = """<!doctype html><html><head><title>MockRelay</title>
<style>
 body{font-family:ui-sans-serif,system-ui;margin:2rem;max-width:960px;background:#0b1220;color:#e0f2fe}
 h1{color:#7dd3fc}
 table{border-collapse:collapse;width:100%}
 th,td{border-bottom:1px solid #1e3a5f;padding:.4rem .6rem;text-align:left;font-size:.9rem}
 code{background:#152a47;padding:.1rem .3rem;border-radius:4px;color:#bae6fd}
 .pill{padding:.15rem .5rem;border-radius:999px;background:#152a47;color:#7dd3fc;font-size:.75rem}
</style></head><body>
<h1>MockRelay</h1>
<p>Mode: <span class="pill" id="mode">-</span> &nbsp; Latency: <span class="pill" id="lat">-</span> ms
 &nbsp; Hits: <span class="pill" id="hits">-</span> &nbsp; Misses: <span class="pill" id="miss">-</span>
 &nbsp; Recorded: <span class="pill" id="rec">-</span></p>
<h2>Recent traffic</h2>
<table id="recent"><thead><tr><th>Time</th><th>Method</th><th>Path</th><th>Status</th><th>Mode</th></tr></thead><tbody></tbody></table>
<h2>Fixtures</h2>
<table id="fx"><thead><tr><th>Upstream</th><th>ID</th><th>Method</th><th>Path</th><th>Status</th></tr></thead><tbody></tbody></table>
<script>
async function refresh(){
  const s = await (await fetch('/api/state')).json();
  mode.textContent = s.mode; lat.textContent = s.latency_ms;
  hits.textContent = s.hits; miss.textContent = s.misses; rec.textContent = s.recorded;
  const r = await (await fetch('/api/recent')).json();
  const rb = document.querySelector('#recent tbody'); rb.innerHTML='';
  for (const x of r){ const tr=document.createElement('tr');
    tr.innerHTML=`<td>${x.t}</td><td>${x.m}</td><td>${x.p}</td><td>${x.s}</td><td>${x.mode}</td>`;
    rb.appendChild(tr);}
  const fx = await (await fetch('/api/fixtures')).json();
  const tb = document.querySelector('#fx tbody'); tb.innerHTML = '';
  for (const f of fx){ const tr = document.createElement('tr');
    tr.innerHTML = `<td>${f.upstream}</td><td><code>${f.id}</code></td>
      <td>${f.match.method}</td><td>${f.match.path}</td><td>${f.response.status}</td>`;
    tb.appendChild(tr);}
}
refresh(); setInterval(refresh, 2000);
</script></body></html>"""


def _05(state: _01):
    cfg = state.cfg
    store = state.store
    metrics = state.metrics

    class _06(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            return

        def _07(self, status: int, payload):
            body = json.dumps(payload, default=str).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _08(self, html: str):
            body = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _09(self, body: bytes, ctype: str = "text/plain"):
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                return self._08(_04)
            if self.path == "/metrics":
                return self._09(metrics._08().encode(), "text/plain; version=0.0.4")
            if self.path == "/api/state":
                return self._07(200, {
                    "mode": cfg.mode, "latency_ms": cfg.latency_ms,
                    "upstreams": list(cfg.upstreams.keys()),
                })
            if self.path == "/api/recent":
                return self._07(200, metrics._09())
            if self.path.startswith("/api/match"):
                p = urlparse(self.path)
                q = parse_qs(p.query)
                upstream = (q.get("upstream") or [None])[0]
                method = (q.get("method") or ["GET"])[0].upper()
                path = (q.get("path") or ["/"])[0]
                qq: Dict[str, List[str]] = {}
                for k, v in parse_qsl((q.get("query") or [""])[0],
                                      keep_blank_values=True):
                    qq.setdefault(k, []).append(v)
                body = None
                raw_body = (q.get("body") or [None])[0]
                if raw_body is not None:
                    try:
                        body = json.loads(raw_body)
                    except ValueError:
                        body = raw_body
                opts = _12(cfg._12(upstream or "", path))
                rows = _11(list(store._07(upstream)), method, path, qq,
                           body, opts)
                return self._07(200, {
                    "upstream": upstream,
                    "method": method,
                    "path": path,
                    "match_mode": opts.mode,
                    "fuzzy_threshold": opts.threshold,
                    "ignore_case": opts.ignore_case,
                    "fuzzy_enabled": opts.fuzzy_enabled,
                    "match_priority": list(opts.order),
                    "results": rows,
                })
            if self.path.startswith("/api/fixtures"):
                upstream = None
                if "?" in self.path:
                    q = parse_qs(urlparse(self.path).query)
                    upstream = (q.get("upstream") or [None])[0]
                out: List[Dict] = []
                for f in store._07(upstream):
                    out.append(f._07())
                return self._07(200, out)
            return self._07(404, {"error": "not found"})

        def do_POST(self):
            p = urlparse(self.path).path
            parts = p.strip("/").split("/")
            if len(parts) == 3 and parts[0] == "api" and parts[1] == "mode":
                m = parts[2]
                if m not in ("record", "replay", "passthrough", "hybrid"):
                    return self._07(400, {"error": "invalid mode"})
                cfg.mode = m
                return self._07(200, {"mode": cfg.mode})
            if len(parts) == 3 and parts[0] == "api" and parts[1] == "latency":
                try:
                    cfg.latency_ms = max(0, int(parts[2]))
                except ValueError:
                    return self._07(400, {"error": "bad ms"})
                return self._07(200, {"latency_ms": cfg.latency_ms})
            return self._07(404, {"error": "not found"})

        def do_DELETE(self):
            p = urlparse(self.path).path
            parts = p.strip("/").split("/")
            if len(parts) == 4 and parts[0] == "api" and parts[1] == "fixtures":
                ok = store._08(parts[2], parts[3])
                return self._07(200 if ok else 404, {"deleted": ok})
            return self._07(404, {"error": "not found"})

    return _06


def _10(state: _01):
    host, port = _03(state.cfg.admin_listen)
    handler = _05(state)
    srv = _02((host, port), handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv
