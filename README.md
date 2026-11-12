# YojanaSetu — AI-Driven Integrated Beneficiary Data Governance

**UKIS 2026 entry** · Problem: Data Governance & Welfare

> Official problem (verified 10 Nov 2026 from https://www.axocom.in/UKISHackathon):
> "Data Governance & Welfare — AI-Driven Integrated Beneficiary Data Governance: Create a
> privacy-conscious data intelligence platform that connects beneficiary records across
> departments to provide a holistic view of scheme participation while improving inclusion,
> integrity and policy planning."

**Prizes:** State Champion ₹51,000 · Kumaon Champion ₹21,000 · Garhwal Champion ₹21,000 ·
Problem Level ₹10,000 (total ₹1,03,000+). **Stages:** 1 online → 2 evaluation/shortlisting →
3 on-ground (Rudrapur / Roorkee / Dehradun). Programme ends Mon 14 Dec 2026. Solo entry, online Stage 1.

## What it is

A privacy-conscious data-intelligence platform for an officer in Uttarakhand. It connects
(synthetic) beneficiary records across departments into one holistic view per person, flags
duplicate enrolments with evidence, traces eligibility rule-by-rule with source citations,
and surfaces inclusion gaps — people eligible for a scheme they are not enrolled in.

## ⚠️ SYNTHETIC DEMO DATA — no real citizen data

**Every person, ID, enrolment and record on this site is fictional and invented for the demo.**
No real citizen data is used, stored, or fetched. The banner says so on every screen, and this
notice is in the README, the footer, and the `/health` response. Never use this demo for a real
eligibility decision.

Scheme figures are a curated snapshot of widely published headline criteria for real national
schemes (Nov 2026, reused from the SchemeSathi engine — see `app/data.py`). They are NOT an
official source; verify current criteria at https://www.myscheme.gov.in. One scheme
("Hill Transport Support") is clearly labelled **REPRESENTATIVE** — invented to show how a
state scheme plugs into the same governance layer.

## Run locally

```bash
cd ukis-yojanasetu
python3 run.py            # http://127.0.0.1:8771
# or: python3 -m app.server
```

Python 3 stdlib only — no pip installs, no CDN, no external assets, no secrets, no env vars.

## Features

1. **Scheme registry** — 9 schemes (8 real national + 1 labelled representative), searchable
   by name/category, with benefit, department, and criteria source on every card.
2. **Beneficiary lookup** — search by synthetic ID (`YS-1001`), name (`Gita Devi`) or district
   (`Dehradun`) → one holistic view of scheme participation, each enrolment citing its source
   department and record ID.
3. **Duplicate detection** — deterministic matching (name + DOB + district + family ref) with
   confidence score, per-field evidence, and a suggested action. Seeded: 1 exact DUPLICATE
   (Gita Devi, 1.00), 1 LIKELY DUPLICATE (Ramesh Singh / Ramesh Kumar Singh, 0.85), 1 REVIEW
   near-miss (two Sunita Rawats, different DOB, 0.60). Nothing is auto-merged.
4. **Eligibility trace** — pick a person + a scheme → rule-by-rule PASS / FAIL / UNKNOWN trace,
   each rule citing its source record, final verdict ELIGIBLE / NOT ELIGIBLE / NEEDS REVIEW,
   plus an already-enrolled flag.
5. **Officer dashboard** — totals (22 people, 25 enrolments, 9 schemes, 13 districts),
   enrolments by district and scheme, duplicate counts, and 29 inclusion gaps (eligible but
   not enrolled), with a working CSV download and "Trace it" shortcuts.
6. **3D district map** — CSS-3D extruded blocks for all 13 Uttarakhand districts, height =
   enrolment volume. Click / Enter / arrow keys filter the dashboard; a 2D button list is the
   fallback; reduced-motion flattens the map; all blocks are keyboard-focusable.
7. **Duplicate review queue** — see "What's new" below.

## What's new — 12 Nov 2026

**Duplicate Review Queue with officer decisions + audit trail** (built 12 Nov 2026, during the
LaunchPad Hacks window; everything above predates it). Duplicate *detection* is unchanged —
the engine still only flags and suggests. What is new is the human step after the flag:

- A **Review Queue** tab lists every flagged pair (rebuilt live from the same
  `find_duplicates()` engine — no second copy of the logic), each with its evidence,
  confidence, and current decision state.
- For each pair an officer records **Confirmed duplicate** or **Not a duplicate**, with an
  optional note (`POST /api/review-decisions`). Anything else is rejected with a 400;
  an unknown pair ID gets a 404.
- An **audit trail** (`GET /api/audit-trail`) lists every decision newest-first with
  timestamp, pair, decision, and note.
- Decisions live in server memory only (`app/reviews.py`) — the demo's standing pattern:
  no database, no disk writes, a restart clears them, and nothing is ever auto-merged.

## Design

"Gazette Ledger" — Swiss Minimalism / Editorial (design constitution in progress by the design
agent in parallel). Paper-white, deep Himalayan green + ink navy, sparing saffron accent; serif
display headlines + clean sans body; ruled lines, tabular numerals. No glassmorphism, no
Neo-Brutalism, no cream/vermilion stamp aesthetic.

## Tests (real, re-run 12 Nov 2026)

```bash
python3 -m unittest discover -s tests -v
# 45 tests, all PASS — tests/test_governance.py + tests/test_server.py + tests/test_reviews.py
```

Covers: duplicate matching (exact / near-miss / same-name-different-DOB / no-match),
eligibility trace rules, registry + beneficiary search, dashboard totals and gaps, server
smoke (every route returns 200 with the expected JSON shape; 404/400 error paths included),
and the review queue (queue listing, both officer decisions, audit-trail ordering, invalid
decision → 400, unknown pair → 404, malformed JSON → 400).
Live smoke verified with `curl` against `python3 run.py` on port 8771 on 12 Nov 2026,
including a real POST decision round-trip; the Vercel WSGI adapter (api/index.py) was
exercised in-process for the same routes.

## Honest status

- Gates A–D: built and tested locally (see `RELEASE_CARD.md`). Design constitution is being
  written by the design agent in parallel — not yet in this folder.
- Gates E–G **BLOCKED** (by task scope, not by a failure): no GitHub repo, no deployment, no
  demo video, no UKIS registration/submission. See `RELEASE_CARD.md` and
  `deployment/DEPLOYMENT_RUNBOOK.md` (skeleton with nulls — no live URL is claimed).
- Known limitations: in-browser click-through was not possible from this build agent (no live
  browser here) — API + unit verification is done; a live-browser pass is still needed before
  any demo recording. The 3D map is CSS-3D (no WebGL) by design; mobile viewport check is
  code-level (responsive CSS) not device-tested.

## Project layout

```
app/
  data.py        synthetic schemes, 13 districts, 22 fictional beneficiaries
  governance.py  duplicate matching, eligibility trace, dashboard/gaps
  server.py      stdlib http.server — HTML + JSON API
  static/        index.html, style.css, app.js (no external assets)
tests/           unittest suites (governance + server smoke)
qa/              INTERACTION_INVENTORY.md — every visible control
deployment/      DEPLOYMENT_RUNBOOK.md (skeleton, no deploy exists)
run.py           launcher — http://127.0.0.1:8771
```
