from __future__ import annotations
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class _01(BaseHTTPRequestHandler):
    def log_message(self, *a):
        return

    def _02(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/v1/users":
            return self._02(200, {
                "users": [
                    {"id": "u_1", "name": "ada", "created": int(time.time())},
                    {"id": "u_2", "name": "grace", "created": int(time.time())},
                ],
                "request_id": "req_demo_123",
            })
        if self.path.startswith("/v1/users/"):
            uid = self.path.rsplit("/", 1)[-1]
            return self._02(200, {
                "id": uid,
                "name": "ada",
                "created": int(time.time()),
                "request_id": "req_demo_456",
            })
        if self.path == "/v1/slow":
            time.sleep(1.5)
            return self._02(200, {"slow": True})
        return self._02(404, {"error": "not found", "path": self.path})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw) if raw else {}
        except Exception:
            payload = {}
        if self.path == "/v1/users":
            return self._02(201, {
                "id": "u_new",
                "name": payload.get("name", "unknown"),
                "created": int(time.time()),
            })
        return self._02(404, {"error": "not found"})


if __name__ == "__main__":
    print("demo upstream on http://localhost:9000")
    HTTPServer(("127.0.0.1", 9000), _01).serve_forever()
