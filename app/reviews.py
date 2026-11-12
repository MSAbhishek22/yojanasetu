"""Officer review decisions for flagged duplicate pairs — demo state.

The review queue is NOT stored: it is rebuilt from
governance.find_duplicates() on every call, so duplicate detection stays
the single source of truth and this module never re-implements it.

Decisions are kept in a module-level in-memory list, the same way the
rest of this demo keeps its data — in the process, never on disk. A
server restart clears every decision. All records are SYNTHETIC; an
officer decision here is a demo interaction, not a real case outcome.
"""
from __future__ import annotations

import threading
from datetime import datetime, timezone

from app.governance import find_duplicates

# The only two decisions an officer may record on a flagged pair.
DECISIONS = {
    "confirmed_duplicate": "Confirmed duplicate",
    "not_a_duplicate": "Not a duplicate",
}

_lock = threading.Lock()
_audit: list = []  # every decision recorded, oldest first


def pair_id(pair: dict) -> str:
    """Stable identifier for one flagged pair, e.g. 'YS-1001__YS-1003'."""
    return f"{pair['person_a']}__{pair['person_b']}"


def review_queue() -> list:
    """Every flagged pair, each with its latest officer decision (or None)."""
    with _lock:
        latest = {e["pair_id"]: e for e in _audit}
    return [{**pair, "pair_id": pair_id(pair),
             "decision": latest.get(pair_id(pair))}
            for pair in find_duplicates()]


def record_decision(pid: str, decision: str, note: str = "") -> dict | None:
    """Append one officer decision to the audit trail.

    Returns the audit entry, or None when `pid` is not a flagged pair.
    Raises ValueError when `decision` is not one of DECISIONS.
    """
    if decision not in DECISIONS:
        raise ValueError("Decision must be 'confirmed_duplicate' or "
                         "'not_a_duplicate'.")
    pair = {pair_id(p): p for p in find_duplicates()}.get(pid)
    if pair is None:
        return None
    entry = {"pair_id": pid,
             "person_a": pair["person_a"], "person_b": pair["person_b"],
             "name_a": pair["name_a"], "name_b": pair["name_b"],
             "decision": decision, "decision_label": DECISIONS[decision],
             "note": (note or "").strip(),
             "decided_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    with _lock:
        _audit.append(entry)
    return entry


def audit_trail() -> list:
    """All recorded decisions, newest first."""
    with _lock:
        return list(reversed(_audit))
