"""Server smoke tests: routes return 200 and the expected JSON shapes.

Starts the real server on an ephemeral port in a thread; no mocks.
"""
import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.server import Handler


def _get(base, path):
    with urllib.request.urlopen(base + path, timeout=5) as resp:
        return resp.status, resp.read()


class TestServerSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.base = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _json(self, path, expect=200):
        status, body = _get(self.base, path)
        self.assertEqual(status, expect)
        return json.loads(body.decode("utf-8"))

    def test_homepage_returns_html(self):
        status, body = _get(self.base, "/")
        self.assertEqual(status, 200)
        text = body.decode("utf-8")
        self.assertIn("YojanaSetu", text)
        self.assertIn("SYNTHETIC DEMO DATA", text)
        self.assertIn("/static/app.js", text)

    def test_static_css_and_js(self):
        for path, needle in (("/static/style.css", "Gazette Ledger"),
                             ("/static/app.js", "loadDashboard")):
            status, body = _get(self.base, path)
            self.assertEqual(status, 200)
            self.assertIn(needle, body.decode("utf-8"))

    def test_health(self):
        d = self._json("/health")
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["schemes"], 9)
        self.assertEqual(d["districts"], 13)
        self.assertIn("SYNTHETIC", d["data"])

    def test_schemes_shape(self):
        d = self._json("/api/schemes")
        self.assertTrue(d["ok"])
        self.assertEqual(d["total"], 9)
        self.assertEqual(len(d["schemes"]), 9)
        self.assertTrue(all("name" in s and "benefit" in s for s in d["schemes"]))

    def test_schemes_search(self):
        d = self._json("/api/schemes?q=kisan")
        self.assertEqual(len(d["schemes"]), 1)
        self.assertEqual(d["schemes"][0]["id"], "pm-kisan")

    def test_beneficiary_search_and_detail(self):
        d = self._json("/api/beneficiaries?q=YS-1001")
        self.assertEqual(len(d["results"]), 1)
        self.assertEqual(d["results"][0]["name"], "Gita Devi")
        self.assertEqual(len(d["results"][0]["enrolments"]), 2)
        self.assertIn("record_id", d["results"][0]["enrolments"][0])
        d2 = self._json("/api/beneficiary?id=YS-1001")
        self.assertTrue(d2["ok"])
        self.assertEqual(d2["person"]["id"], "YS-1001")

    def test_beneficiary_not_found_is_404(self):
        try:
            _get(self.base, "/api/beneficiary?id=YS-9999")
            self.fail("expected HTTPError 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)

    def test_duplicates_shape(self):
        d = self._json("/api/duplicates")
        self.assertTrue(d["ok"])
        self.assertGreaterEqual(len(d["pairs"]), 2)
        pair = d["pairs"][0]
        self.assertIn("confidence", pair)
        self.assertIn("evidence", pair)
        self.assertIn("suggested_action", pair)
        self.assertTrue(all("field" in e and "detail" in e for e in pair["evidence"]))

    def test_trace_shape(self):
        d = self._json("/api/trace?person=YS-1001&scheme=pm-kisan")
        self.assertTrue(d["ok"])
        self.assertEqual(d["trace"]["verdict"], "ELIGIBLE")
        self.assertTrue(d["trace"]["checks"])
        self.assertTrue(all("source" in c for c in d["trace"]["checks"]))

    def test_trace_bad_params_is_400(self):
        try:
            _get(self.base, "/api/trace?person=YS-9999&scheme=pm-kisan")
            self.fail("expected HTTPError 400")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)

    def test_dashboard_shape(self):
        d = self._json("/api/dashboard")
        self.assertTrue(d["ok"])
        dash = d["dashboard"]
        self.assertEqual(dash["total_people"], 22)
        self.assertEqual(len(dash["by_district"]), 13)
        self.assertGreater(dash["inclusion_gaps"], 0)
        self.assertEqual(len(d["districts"]), 13)

    def test_dashboard_district_filter(self):
        d = self._json("/api/dashboard?district=Dehradun")
        self.assertEqual(d["dashboard"]["district_filter"], "Dehradun")
        self.assertLess(d["dashboard"]["total_people"], 22)

    def test_unknown_route_is_404(self):
        try:
            _get(self.base, "/api/nope")
            self.fail("expected HTTPError 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)


if __name__ == "__main__":
    unittest.main()
