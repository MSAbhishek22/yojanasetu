"""YojanaSetu on Vercel — WSGI entrypoint (serverless adaptation).

The governance logic is unchanged (app/governance.py + app/data.py:
same duplicate matching, same eligibility trace, same dashboard, same
synthetic data); this file is only a transport adapter. Vercel's Python
runtime calls ``app(environ, start_response)``.

Why this adapter is simpler than NyayaSeal's: the reference data is
compiled into app/data.py and the app never writes to disk (the only
``open()`` calls read static files). The one piece of mutable state is
the officer review-decision store (app/reviews.py): a module-level
in-memory list, identical code to local. On serverless it lives only
for the life of the warm instance — decisions can differ across
instances and vanish on a cold start. That is an accepted demo caveat
(synthetic data, no real cases); locally the behaviour is identical to
app/server.py. The only other difference: no server process — each
request is handled by this WSGI app.

Route-for-route parity with app/server.py (same paths, same JSON
shapes, same status codes, same error strings). No credentials, no
environment variables, no external assets, no secrets.
"""

import json
import mimetypes
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data import (  # noqa: E402
    BENEFICIARIES, DISTRICTS, PERSON_BY_ID, SCHEMES, SCHEME_BY_ID,
)
from app.governance import (  # noqa: E402
    dashboard, find_duplicates, public_person, search_beneficiaries,
    search_schemes, trace_eligibility,
)
from app.reviews import audit_trail, record_decision, review_queue  # noqa: E402

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")


def _public_scheme(s: dict) -> dict:
    # Same public projection as app/server.py.
    return {k: s[k] for k in
            ("id", "name", "ministry", "department", "category", "benefit",
             "blurb", "source") if k in s} | {"representative": bool(s.get("representative"))}


def _json_body(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def _static(name: str):
    safe = os.path.basename(name)
    path = os.path.join(STATIC_DIR, safe)
    if not os.path.exists(path):
        return 404, "application/json", _json_body(
            {"ok": False, "error": "Not found."})
    with open(path, "rb") as f:
        body = f.read()
    ctype, _ = mimetypes.guess_type(path)
    return 200, ctype or "application/octet-stream", body


def handle_get(path: str, query: dict):
    if path == "/":
        return _static("index.html")
    if path.startswith("/static/"):
        return _static(path[len("/static/"):])
    if path == "/favicon.ico":
        return 204, "text/plain", b""
    q = (query.get("q") or [""])[0]
    if path == "/health":
        return 200, "application/json", _json_body({
            "ok": True, "status": "ok", "app": "yojanasetu",
            "schemes": len(SCHEMES), "people": len(BENEFICIARIES),
            "districts": len(DISTRICTS),
            "data": "SYNTHETIC DEMO DATA — no real citizen data"})
    if path == "/api/schemes":
        return 200, "application/json", _json_body(
            {"ok": True,
             "schemes": [_public_scheme(s) for s in search_schemes(q)],
             "total": len(SCHEMES)})
    if path == "/api/beneficiaries":
        if not q.strip():
            return 400, "application/json", _json_body(
                {"ok": False,
                 "error": "Type a synthetic ID, name or district to search."})
        return 200, "application/json", _json_body(
            {"ok": True,
             "results": [public_person(p) for p in search_beneficiaries(q)]})
    if path == "/api/beneficiary":
        pid = (query.get("id") or [""])[0]
        person = PERSON_BY_ID.get(pid)
        if person is None:
            return 404, "application/json", _json_body(
                {"ok": False,
                 "error": f"No synthetic beneficiary with ID {pid}."})
        return 200, "application/json", _json_body(
            {"ok": True, "person": public_person(person)})
    if path == "/api/duplicates":
        return 200, "application/json", _json_body(
            {"ok": True, "pairs": find_duplicates()})
    if path == "/api/trace":
        pid = (query.get("person") or [""])[0]
        sid = (query.get("scheme") or [""])[0]
        person, scheme = PERSON_BY_ID.get(pid), SCHEME_BY_ID.get(sid)
        if person is None or scheme is None:
            return 400, "application/json", _json_body(
                {"ok": False,
                 "error": "Pick a valid person and a valid scheme."})
        return 200, "application/json", _json_body(
            {"ok": True, "trace": trace_eligibility(person, scheme)})
    if path == "/api/dashboard":
        district = (query.get("district") or [""])[0] or None
        if district and district not in DISTRICTS:
            return 400, "application/json", _json_body(
                {"ok": False, "error": f"Unknown district: {district}."})
        return 200, "application/json", _json_body(
            {"ok": True, "dashboard": dashboard(district),
             "districts": DISTRICTS})
    if path == "/api/review-queue":
        queue = review_queue()
        return 200, "application/json", _json_body(
            {"ok": True, "queue": queue, "total": len(queue)})
    if path == "/api/audit-trail":
        entries = audit_trail()
        return 200, "application/json", _json_body(
            {"ok": True, "entries": entries, "total": len(entries)})
    return 404, "application/json", _json_body(
        {"ok": False, "error": "Not found."})


def handle_post(path: str, raw: bytes):
    if path != "/api/review-decisions":
        return 404, "application/json", _json_body(
            {"ok": False, "error": "Not found."})
    try:
        body = json.loads(raw.decode("utf-8")) if raw else {}
    except (ValueError, UnicodeDecodeError):
        return 400, "application/json", _json_body(
            {"ok": False, "error": "Request body must be valid JSON."})
    pid = body.get("pair_id") or ""
    decision = body.get("decision") or ""
    if not pid or not decision:
        return 400, "application/json", _json_body(
            {"ok": False, "error": "pair_id and decision are required."})
    try:
        entry = record_decision(pid, decision, body.get("note") or "")
    except ValueError as exc:
        return 400, "application/json", _json_body(
            {"ok": False, "error": str(exc)})
    if entry is None:
        return 404, "application/json", _json_body(
            {"ok": False,
             "error": f"No flagged duplicate pair with ID {pid}."})
    return 200, "application/json", _json_body({"ok": True, "entry": entry})


_STATUSES = {
    200: "200 OK", 204: "204 No Content", 400: "400 Bad Request",
    404: "404 Not Found", 500: "500 Internal Server Error",
}


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    raw_path = environ.get("PATH_INFO", "/") or "/"
    # Vercel rewrites /(.*) to /api/index: treat the function root as app root.
    path = "/" if raw_path in ("/api/index", "/api") else raw_path
    query = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
    try:
        if method == "GET":
            code, ctype, body = handle_get(path, query)
        elif method == "POST":
            try:
                length = int(environ.get("CONTENT_LENGTH") or 0)
            except ValueError:
                length = 0
            raw = environ["wsgi.input"].read(length) if length > 0 else b""
            code, ctype, body = handle_post(path, raw)
        else:
            code, ctype, body = 404, "application/json", _json_body(
                {"ok": False, "error": "Not found."})
    except Exception as exc:  # never leak a stack trace to the client
        code, ctype, body = 500, "application/json", _json_body(
            {"ok": False, "error": f"Server error: {type(exc).__name__}"})
    start_response(_STATUSES.get(code, "200 OK"),
                   [("Content-Type", ctype),
                    ("Content-Length", str(len(body)))])
    return [body]
