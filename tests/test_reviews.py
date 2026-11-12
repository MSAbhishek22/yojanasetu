"""Review queue tests: officer decisions on flagged duplicate pairs.

Starts the real server on an ephemeral port in a thread; no mocks.
Decisions live in server memory, so tests never assume an empty trail —
each asserts on the entries it recorded itself (identified by note).
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


def _post(base, path, payload=None, raw=None):
    data = raw if raw is not None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(base + path, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


class TestReviewQueue(unittest.TestCase):
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

    def _pair_ids(self):
        d = self._json("/api/review-queue")
        return [item["pair_id"] for item in d["queue"]]

    def test_queue_lists_every_flagged_pair(self):
        d = self._json("/api/review-queue")
        self.assertTrue(d["ok"])
        dups = self._json("/api/duplicates")
        self.assertEqual(d["total"], len(dups["pairs"]))
        self.assertGreaterEqual(d["total"], 2)
        for item, pair in zip(d["queue"], dups["pairs"]):
            self.assertEqual(item["pair_id"],
                             f"{pair['person_a']}__{pair['person_b']}")
            self.assertEqual(item["confidence"], pair["confidence"])
            self.assertIn("decision", item)

    def test_record_confirmed_duplicate(self):
        pid = self._pair_ids()[0]
        status, d = _post(self.base, "/api/review-decisions",
                          {"pair_id": pid, "decision": "confirmed_duplicate",
                           "note": "test: same person, two IDs"})
        self.assertEqual(status, 200)
        self.assertTrue(d["ok"])
        entry = d["entry"]
        self.assertEqual(entry["pair_id"], pid)
        self.assertEqual(entry["decision"], "confirmed_duplicate")
        self.assertEqual(entry["decision_label"], "Confirmed duplicate")
        self.assertEqual(entry["note"], "test: same person, two IDs")
        self.assertIn("decided_at", entry)
        queue = {i["pair_id"]: i for i in self._json("/api/review-queue")["queue"]}
        self.assertEqual(queue[pid]["decision"]["decision"],
                         "confirmed_duplicate")

    def test_record_not_a_duplicate(self):
        pid = self._pair_ids()[1]
        status, d = _post(self.base, "/api/review-decisions",
                          {"pair_id": pid, "decision": "not_a_duplicate",
                           "note": ""})
        self.assertEqual(status, 200)
        self.assertEqual(d["entry"]["decision"], "not_a_duplicate")
        self.assertEqual(d["entry"]["decision_label"], "Not a duplicate")
        queue = {i["pair_id"]: i for i in self._json("/api/review-queue")["queue"]}
        self.assertEqual(queue[pid]["decision"]["decision"], "not_a_duplicate")

    def test_audit_trail_is_newest_first(self):
        ids = self._pair_ids()
        _post(self.base, "/api/review-decisions",
              {"pair_id": ids[0], "decision": "confirmed_duplicate",
               "note": "ordering probe first"})
        _post(self.base, "/api/review-decisions",
              {"pair_id": ids[1], "decision": "not_a_duplicate",
               "note": "ordering probe second"})
        d = self._json("/api/audit-trail")
        self.assertTrue(d["ok"])
        notes = [e["note"] for e in d["entries"]]
        self.assertLess(notes.index("ordering probe second"),
                        notes.index("ordering probe first"))
        self.assertEqual(d["total"], len(d["entries"]))

    def test_invalid_decision_is_400(self):
        pid = self._pair_ids()[0]
        status, d = _post(self.base, "/api/review-decisions",
                          {"pair_id": pid, "decision": "maybe_duplicate"})
        self.assertEqual(status, 400)
        self.assertFalse(d["ok"])
        self.assertIn("confirmed_duplicate", d["error"])

    def test_unknown_pair_is_404(self):
        status, d = _post(self.base, "/api/review-decisions",
                          {"pair_id": "YS-0000__YS-0001",
                           "decision": "confirmed_duplicate"})
        self.assertEqual(status, 404)
        self.assertFalse(d["ok"])
        self.assertIn("YS-0000__YS-0001", d["error"])

    def test_malformed_json_is_400(self):
        status, d = _post(self.base, "/api/review-decisions",
                          raw=b"{not json")
        self.assertEqual(status, 400)
        self.assertFalse(d["ok"])


if __name__ == "__main__":
    unittest.main()
