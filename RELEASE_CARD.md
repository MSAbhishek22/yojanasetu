# RELEASE CARD — YojanaSetu (UKIS 2026)

Rulebook §10 format. Date: 10 Nov 2026. Updated by the coordinator after
in-browser QA + fixes + re-verification. Nothing below claims a deployment,
video, or submission that does not exist.

| Deliverable | Evidence |
|---|---|
| Project identity | YojanaSetu — AI-Driven Integrated Beneficiary Data Governance for Uttarakhand (UKIS 2026). Target user: district/block officer. Design concept: "Gazette Ledger" (Swiss Minimalism / Editorial). |
| Research | Official problem verified 10 Nov 2026 from https://www.axocom.in/UKISHackathon (wording in README). Scheme rules reused from SchemeSathi's verified Nov 2026 snapshot; 1 of 9 schemes labelled REPRESENTATIVE. Design research: 5 real references opened 10 Nov 2026, in `design/DESIGN_CONSTITUTION.md`. |
| Live application | **None — BLOCKED (Gate E).** No deployment exists. Local only: http://127.0.0.1:8771 via `python3 run.py`. |
| GitHub | **None — BLOCKED (Gate E).** No repository created (out of scope for this build task). No commit SHA exists. |
| Deployment | **None — BLOCKED (Gate E).** No provider, no build ID, no timestamp. Runbook skeleton at `deployment/DEPLOYMENT_RUNBOOK.md` with nulls. |
| UI quality | Gazette Ledger UI built (paper-white, Himalayan green + ink navy, saffron accent; serif display + sans body; ruled lines). Design constitution at `design/DESIGN_CONSTITUTION.md` (+ §0A as-built amendment); registry at `design/PROJECT_DESIGN_REGISTRY.md` — distinct from NyayaSeal (Neo-Brutalism), PollPulse (Glassmorphism) and SchemeSathi. Contrast measured in-browser: all pass AA (ink/paper 15.66:1, muted 7.38:1, white-on-green 12.16:1, white-on-saffron 5.18:1). |
| 3D experience | CSS-3D district map: 13 extruded blocks, height = enrolment volume; click/Enter/Space + arrow-key filtering, drag + Alt+←/→ rotation ±20°, Reset view, Flat-map toggle; 2D button-list fallback; low-motion toggle + reduced-motion flattening. Verified in-browser at 1280/768/390px: 0/13 blocks clipped. |
| Functional controls | `qa/INTERACTION_INVENTORY.md` — every visible control listed, statuses updated to browser-observed results by QA. No `href="#"`, no dead buttons, no fake toasts. All 5 tabs, search/filter/lookup/trace/duplicates/dashboard/CSV download verified by clicking in headless Chromium. |
| QA | Unit tests `python3 -m unittest discover -s tests` → **38 tests, 38 PASS, 0 FAIL (0.59s, 10 Nov 2026, re-run by the coordinator)**. In-browser QA (Playwright + headless Chromium, 1280/768/390px): first pass 67/73 PASS, Gate D FAIL (8 fails F1–F8, `qa/QA_REPORT.md`); fixes applied (`qa/FIXES_POST_QA.md`); fix probe 36/36 PASS; QA script re-run 71/1 — the 1 fail is the script's stale expectation of 9 by-scheme rows (correct is 8: 9 schemes exist, only 8 have enrolments). Console errors: 0. |
| Demo video | **None — BLOCKED (Gate F).** No video recorded (requires a live deployment first). |
| Published video | **None — BLOCKED (Gate F).** No upload, no URL. |
| Submission | **Not submitted — BLOCKED (Gate G).** No UKIS registration/submission made (out of scope for this build task). |

## Gate summary

- `LIVE_DEPLOYMENT`: BLOCKED — no deploy; out of scope for this build task.
- `GITHUB_COMMIT_MATCH`: BLOCKED — no repo; out of scope for this build task.
- `ALL_VISIBLE_CONTROLS`: PASS — verified by clicking every control in headless Chromium; inventory updated to browser-observed statuses.
- `3D_EXPERIENCE`: PASS — CSS-3D map verified in-browser (0/13 clipped, rotation + Reset + Flat-map + low-motion all working); 2D fallback verified.
- `UI_DISTINCTIVENESS`: PASS — Gazette Ledger distinct from NyayaSeal, PollPulse and SchemeSathi (registry comparison).
- `RESPONSIVE_AND_ACCESSIBLE`: PASS — 1280/768/390px verified, no horizontal overflow, keyboard focus visible (3px saffron outline), contrast AA measured, reduced-motion + low-motion toggle verified.
- `DEMO_VIDEO_RECORDED_FROM_LIVE`: BLOCKED — no live deployment to record from.
- `VIDEO_PUBLISHED_AND_URL_VERIFIED`: BLOCKED — no video exists.
- `HACKATHON_RULE_COMPLIANCE`: PASS (build scope) — synthetic data only, no real citizen data, free-only stdlib stack, no accounts created; submission itself not yet filed.
- `OVERALL_RELEASE`: **IN_PROGRESS** — Gates A–D PASS; Gates E–G BLOCKED with exact reasons above.

## Deploy-prep (10 Nov 2026, deploy coordinator — Gate E still BLOCKED)

- Vercel adapter written: `api/index.py` (WSGI, route-for-route parity with
  `app/server.py`) + `vercel.json` + `.python-version` (3.12). Same proven
  pattern as NyayaSeal's adapter.
- WSGI harness `/tmp/yojanasetu-wsgi-test.py`: **23/23 PASS**. Unit tests
  re-run: **38/38 PASS**. Secret scan: **0 hits** (only "token" false positives).
- Repo `MSAbhishek22/yojanasetu` does **NOT** exist (search_repositories
  total_count 0, 10 Nov 2026). Connector `create_repository` NOT attempted
  (known GitHub App 403). Push manifest `~/workspace/hackathons/yojanasetu-paths`
  (23 paths, ~220 KB). Runbook + `deployment/RELEASE_MANIFEST.json` updated;
  live URL / commit SHA remain `null` — no deploy exists.
- Serverless note: this app is fully read-only (all GET, no disk writes), so
  unlike NyayaSeal it has no per-instance-store caveat — serverless behaviour
  is identical to local.

## What is still needed (in order)

1. GitHub repo + Vercel (or equivalent free-tier) deploy + fresh-browser verification (Gate E).
2. Demo video recorded from the live URL + published link (Gate F).
3. UKIS registration/submission with user approval (Gate G). Note: stages 2–3 are on-ground in Uttarakhand (Rudrapur / Roorkee / Dehradun) — travel needed only if shortlisted.
