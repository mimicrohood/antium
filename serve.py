#!/usr/bin/env python3
"""Local server for the mirrored Framer site.

Handles two things a plain static server can't:
  1. Clean routes  (/tracks -> /tracks/index.html)
  2. Framer CMS custom range protocol: GET x.framercms?range=a-b,c-d returns
     ONLY the concatenated byte slices (not the whole file).
"""
import os, sys, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8848

MIME = {
    ".html": "text/html; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
    ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8", ".map": "application/json; charset=utf-8",
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
    ".svg": "image/svg+xml", ".webp": "image/webp", ".ico": "image/x-icon",
    ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".otf": "font/otf",
    ".framercms": "application/octet-stream", ".txt": "text/plain; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
}

def guess_mime(path):
    _, ext = os.path.splitext(path)
    return MIME.get(ext.lower(), "application/octet-stream")

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):  # quiet
        pass

    def resolve(self, url_path):
        p = urllib.parse.unquote(url_path.split("?", 1)[0])
        p = p.lstrip("/")
        fs = os.path.join(ROOT, p.replace("/", os.sep))
        if os.path.isdir(fs) or url_path.split("?")[0].endswith("/") or "." not in os.path.basename(p or "x"):
            cand = os.path.join(fs, "index.html")
            if os.path.isfile(cand):
                return cand
        if os.path.isfile(fs):
            return fs
        # try appending index.html for extensionless clean routes
        cand = os.path.join(fs, "index.html")
        if os.path.isfile(cand):
            return cand
        return None

    def do_GET(self):
        self._serve(head=False)

    def do_HEAD(self):
        self._serve(head=True)

    def _serve(self, head):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        fs = self.resolve(self.path)
        if not fs:
            self.send_error(404, "File not found")
            return

        # Framer CMS custom range protocol
        if fs.endswith(".framercms") and "range" in qs:
            try:
                with open(fs, "rb") as f:
                    data = f.read()
                out = bytearray()
                for part in qs["range"][0].split(","):
                    a, b = part.split("-")
                    out += data[int(a):int(b) + 1]  # inclusive end
                body = bytes(out)
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                if not head:
                    self.wfile.write(body)
                return
            except Exception as e:
                self.send_error(500, f"range error: {e}")
                return

        try:
            with open(fs, "rb") as f:
                body = f.read()
        except OSError:
            self.send_error(404, "File not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", guess_mime(fs))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if not head:
            self.wfile.write(body)

if __name__ == "__main__":
    os.chdir(ROOT)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Serving {ROOT} at http://127.0.0.1:{PORT}/  (Ctrl+C to stop)", flush=True)
    srv.serve_forever()
