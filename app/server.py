"""YojanaSetu server — Python 3 stdlib only, no dependencies.

Run from the project root:
    python3 run.py            # http://127.0.0.1:8771
    python3 -m app.server

Routes:
  GET  /                     index.html
  GET  /static/<file>        style.css / app.js
  GET  /health               {"status": "ok", ...}
  GET  /api/schemes?q=       scheme registry (searchable)
  GET  /api/beneficiaries?q= beneficiary search (synthetic ID / name / district)
  GET  /api/beneficiary?id=  one holistic view with source citations
  GET  /api/duplicates       duplicate pairs with evidence + confidence
  GET  /api/trace?person=&scheme=  rule-by-rule eligibility trace
  GET  /api/dashboard?district=    officer dashboard (+ inclusion gaps)

All data is SYNTHETIC. No secrets, no env vars, no external assets.
"""
from __future__ import annotations

import json
import mimetypes
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from app.data import BENEFICIARIES, DISTRICTS, PERSON_BY_ID, SCHEMES, SCHEME_BY_ID
from app.governance import (dashboard, find_duplicates, public_person,
                            search_beneficiaries, search_schemes,
                            trace_eligibility)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
PORT = 8771
HOST = "127.0.0.1"


def _public_scheme(s: dict) -> dict:
    return {k: s[k] for k in
            ("id", "name", "ministry", "department", "category", "benefit",
             "blurb", "source") if k in s} | {"representative": bool(s.get("representative"))}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, name: str) -> None:
        safe = os.path.basename(name)
        path = os.path.join(STATIC_DIR, safe)
        if not os.path.exists(path):
            self._json({"ok": False, "error": "Not found."}, 404)
            return
        with open(path, "rb") as fh:
            body = fh.read()
        ctype, _ = mimetypes.guess_type(path)
        self.send_response(200)
        self.send_header("Content-Type", ctype or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path, query = parsed.path, urllib.parse.parse_qs(parsed.query)
        q = (query.get("q") or [""])[0]
        try:
            if path == "/":
                self._static("index.html")
                return
            if path.startswith("/static/"):
                self._static(path[len("/static/"):])
                return
            if path == "/favicon.ico":
                # Browsers request this even with <link rel="icon"> present;
                # answer 204 (no content) so the console stays error-free.
                self.send_response(204)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            if path == "/health":
                self._json({"ok": True, "status": "ok", "app": "yojanasetu",
                            "schemes": len(SCHEMES), "people": len(BENEFICIARIES),
                            "districts": len(DISTRICTS),
                            "data": "SYNTHETIC DEMO DATA — no real citizen data"})
                return
            if path == "/api/schemes":
                self._json({"ok": True, "schemes": [_public_scheme(s) for s in search_schemes(q)],
                            "total": len(SCHEMES)})
                return
            if path == "/api/beneficiaries":
                if not q.strip():
                    self._json({"ok": False, "error": "Type a synthetic ID, name or district to search."}, 400)
                    return
                self._json({"ok": True, "results": [public_person(p) for p in search_beneficiaries(q)]})
                return
            if path == "/api/beneficiary":
                pid = (query.get("id") or [""])[0]
                person = PERSON_BY_ID.get(pid)
                if person is None:
                    self._json({"ok": False, "error": f"No synthetic beneficiary with ID {pid}."}, 404)
                    return
                self._json({"ok": True, "person": public_person(person)})
                return
            if path == "/api/duplicates":
                self._json({"ok": True, "pairs": find_duplicates()})
                return
            if path == "/api/trace":
                pid = (query.get("person") or [""])[0]
                sid = (query.get("scheme") or [""])[0]
                person, scheme = PERSON_BY_ID.get(pid), SCHEME_BY_ID.get(sid)
                if person is None or scheme is None:
                    self._json({"ok": False,
                                "error": "Pick a valid person and a valid scheme."}, 400)
                    return
                self._json({"ok": True, "trace": trace_eligibility(person, scheme)})
                return
            if path == "/api/dashboard":
                district = (query.get("district") or [""])[0] or None
                if district and district not in DISTRICTS:
                    self._json({"ok": False, "error": f"Unknown district: {district}."}, 400)
                    return
                self._json({"ok": True, "dashboard": dashboard(district),
                            "districts": DISTRICTS})
                return
        except Exception as exc:  # never leak a stack trace to the client
            self._json({"ok": False, "error": f"Server error: {exc}"}, 500)
            return
        self._json({"ok": False, "error": "Not found."}, 404)


def main(host: str = HOST, port: int = PORT) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"YojanaSetu listening on http://{host}:{port}")
    print(f"Schemes: {len(SCHEMES)} | Synthetic people: {len(BENEFICIARIES)} | "
          f"Districts: {len(DISTRICTS)} | SYNTHETIC DEMO DATA only")
    server.serve_forever()


if __name__ == "__main__":
    main()
