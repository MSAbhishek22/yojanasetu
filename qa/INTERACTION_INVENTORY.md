# INTERACTION INVENTORY — YojanaSetu (UKIS 2026)

Rulebook §4.1. Every visible control, its expected vs actual behaviour, and status.
Test evidence: `python3 -m unittest discover -s tests -v` → 37/37 PASS (10 Nov 2026),
plus live `curl` smoke against `python3 run.py` on port 8771 (all routes 200, JSON shapes
verified, 404/400 paths verified). No `href="#"`, no dead buttons, no fake toasts —
grep-verified across `app/`.

> **Live-browser QA done 10 Nov 2026 (qa/QA_REPORT.md):** Playwright + headless
> Chromium 1248 at 1280/768/390px + `prefers-reduced-motion` context. 67/73
> browser checks PASS. Every control below was actually clicked in the browser
> except the footer link (target verified, not clicked out). Three controls the
> task/constitution ask for do NOT exist in the built app (see "Controls asked
> for but not present"). Two in-browser defects found: the 3D map stage clips
> blocks at all viewports, and the district filter does not filter the
> by-scheme table — see QA_REPORT.md F1/F2. Unit tests re-run by QA: 37/37 PASS.

## Navigation

| Page / component | Control | Expected | Actual | Status |
|---|---|---|---|---|
| Masthead nav | Officer Dashboard tab | Show dashboard panel, set aria-pressed | Verified in browser: panel shown, `aria-pressed="true"` | PASS |
| Masthead nav | Beneficiary Lookup tab | Show lookup panel | Verified in browser | PASS |
| Masthead nav | Duplicate Detection tab | Show duplicates panel | Verified in browser | PASS |
| Masthead nav | Eligibility Trace tab | Show trace panel | Verified in browser | PASS |
| Masthead nav | Scheme Registry tab | Show registry panel | Verified in browser | PASS |
| Footer | myscheme.gov.in link | Opens official portal in a new context | `href="https://www.myscheme.gov.in"` verified (target not clicked out) | PASS |
| 3D map stage | All 13 district blocks fully visible in the plate | Blocks render inside the stage | **FAIL — 8/13 blocks extend outside the stage at 1280px (stage 168px tall vs 361px content), 3/13 at 768px and 390px** (QA_REPORT.md F1) | FAIL |

## Controls asked for but NOT present in the built app (constitution §9–§10)

| Control | Expected (constitution / task) | Actual | Status |
|---|---|---|---|
| Low-motion toggle (masthead) | Visible "Low motion: Off/On" text button, persisted in `localStorage` | No such element; only OS `prefers-reduced-motion` is honoured (verified: `--extrude: 0px` under reduced-motion) | FAIL |
| "Reset view" button (map) | Return the 3D scene to its default angle | No such button; no drag/rotate interaction exists to reset | FAIL |
| "Flat map" toggle | Switch the 13 districts to a 2D tile grid | No toggle; the 2D district list is always visible below the map, so the data is available | FAIL |

## Officer Dashboard

| Control | Expected | Actual | Status |
|---|---|---|---|
| 3D district block (×13) — click | Filter dashboard to that district; click again clears | Verified in browser: Dehradun filters (people 22→4), click again clears | PASS |
| 3D district block — Enter/Space (keyboard) | Same as click | Verified in browser: Enter filters to Almora; Space filters to Almora | PASS |
| 3D district block — Arrow keys | Move focus to next/previous block | Verified in browser: ArrowRight Almora→Bageshwar, ArrowLeft back | PASS |
| 2D district list button (×13) | Same filter action as the 3D block | Verified in browser: Nainital filters | PASS |
| Clear district filter button | Show all 13 districts again | Verified in browser | PASS |
| Download inclusion gaps (CSV) | Download a real CSV of the current gaps | Verified in browser: real download `yojanasetu-inclusion-gaps.csv`, 2,418 bytes, header + 29 rows | PASS |
| "Trace it" button (per gap row) | Jump to Eligibility Trace with that person + scheme pre-filled and the trace run | Verified in browser: YS-1001 + pmay-g pre-filled, trace ran, verdict shown | PASS |
| Enrolments-by-scheme table under a district filter | Show that district's scheme counts | **FAIL — shows global counts (sums to 25) for every district** (API `by_scheme` unfiltered; QA_REPORT.md F2) | FAIL |

## Beneficiary Lookup

| Control | Expected | Actual | Status |
|---|---|---|---|
| Search input | Accept synthetic ID / name / district | Verified in browser: YS-1001, "Gita Devi", "Dehradun" (4 results) all work | PASS |
| Search button (submit) | Show matching people with enrolments + source citations | Verified in browser: person card + enrolment table rendered; empty query shows guidance; no match shows empty state with examples | PASS |
| Clear button | Empty the query + results, refocus input | Verified in browser: cleared + input refocused | PASS |

## Duplicate Detection

| Control | Expected | Actual | Status |
|---|---|---|---|
| Severity filter select (All / DUPLICATE / LIKELY DUPLICATE / REVIEW) | Filter the flagged pairs | Verified in browser: DUPLICATE → 1 pair, REVIEW → 1 pair | PASS |
| Refresh list button | Re-fetch pairs from the API | Verified in browser: 3 pairs re-rendered | PASS |
| Pair cards (read-only) | Show verdict chip, confidence, per-field evidence, suggested action | Verified in browser: 3 pairs, confidences 1.00 / 0.85 / 0.60, evidence + action shown | PASS |

## Eligibility Trace

| Control | Expected | Actual | Status |
|---|---|---|---|
| Person select (22 synthetic people) | Choose the person to trace | Verified in browser: 22 options | PASS |
| Scheme select (9 schemes) | Choose the scheme to trace | Verified in browser: 9 options | PASS |
| Run trace button (submit) | Show verdict chip + rule table with PASS/FAIL/UNKNOWN and source per rule | Verified in browser: YS-1001 + pm-kisan → ELIGIBLE, "Already enrolled", 4 rule rows with result chips + detail + source | PASS |
| Clear result button | Clear the trace result and error | Verified in browser: result emptied | PASS |

## Scheme Registry

| Control | Expected | Actual | Status |
|---|---|---|---|
| Search input | Filter schemes by name/category/ministry | Verified in browser: "PM-KISAN" → 1 card; "ZZZNOPE" → empty state | PASS |
| Search button (submit) | Show matching scheme cards | Verified in browser | PASS |
| Category select | Filter the shown cards by category | Verified in browser: "Agriculture" → 1 card | PASS |
| Clear button | Reset search + category, show all 9 | Verified in browser: 9 cards restored | PASS |

## Error / empty / loading states (verified in the browser where noted)

| Case | Expected | Actual | Status |
|---|---|---|---|
| Lookup with empty query | Guidance message, no request | Verified in browser: guidance shown | PASS |
| Lookup with no match | Empty state with examples | Verified in browser | PASS |
| Beneficiary ID not found | 404 with message | `/api/beneficiary?id=YS-9999` → 404 (test-verified) | PASS |
| Trace with invalid person/scheme | 400 with message | `/api/trace?person=YS-9999…` → 400 (test-verified) | PASS |
| Unknown route | 404 JSON | `/api/nope` → 404 (test-verified) | PASS |
| Dashboard district with no enrolments | Empty state (not a crash) | `by_scheme` empty → "No enrolments in this district yet" | PASS |
| API failure (server down) | Error box, no fake success | `showError()` renders the message in the section's alert region | PASS |
| Mobile layout (390px) | No horizontal overflow | **FAIL — dashboard scrollWidth 425 vs 390 (gaps table uncontained); lookup results 392 vs 390** (QA_REPORT.md F3/F4) | FAIL |
| Console errors | Zero | **1 — favicon 404** (`GET /favicon.ico`, no `<link rel="icon">`) (QA_REPORT.md F8) | FAIL |

## Controls deliberately NOT present

- No login / sign-up buttons (no accounts by design).
- No "merge duplicates" button — merging is a suggested action for an officer, never an
  auto-action in this demo; the UI intentionally offers no one-click merge.
- No submit-to-UKIS button — submission is out of scope for this build task.
