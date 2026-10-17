"""Tiny self-contained REST API for the API-test practice suite.

Stdlib only — no dependencies. Implements just enough of a /posts
resource to practice status codes, response shapes, and creates:

    GET  /posts        -> 200, JSON array
    GET  /posts/<id>   -> 200 with the post, or 404
    POST /posts        -> 201, echoes the payload with an assigned id
    anything else      -> 404
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

POSTS = [
    {"userId": 1, "id": 1, "title": "learn playwright", "body": "ui tests first"},
    {"userId": 1, "id": 2, "title": "api testing", "body": "status codes matter"},
    {"userId": 2, "id": 3, "title": "ci pipelines", "body": "run on every push"},
]


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/posts":
            return self._send(200, POSTS)
        if self.path.startswith("/posts/"):
            try:
                pid = int(self.path.rsplit("/", 1)[1])
            except ValueError:
                return self._send(404, {"error": "not found"})
            for p in POSTS:
                if p["id"] == pid:
                    return self._send(200, p)
            return self._send(404, {"error": "not found"})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/posts":
            return self._send(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        payload["id"] = max(p["id"] for p in POSTS) + 1
        POSTS.append(payload)
        return self._send(201, payload)

    def log_message(self, *args):  # keep test output clean
        pass


def run(port=0):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    return server


if __name__ == "__main__":
    srv = run(8000)
    print("demo API on http://127.0.0.1:8000")
    srv.serve_forever()
