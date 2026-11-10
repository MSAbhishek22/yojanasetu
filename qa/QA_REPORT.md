# QA REPORT — YojanaSetu (UKIS 2026) — Gate D, in-browser verification

**Date:** 10 November 2026 (IST)
**App:** `~/workspace/hackathons/ukis-yojanasetu/`, served via `python3 run.py` on
`http://127.0.0.1:8771` (left running at end of this QA pass)
**Environment:** Python 3.12.3, Playwright 1.65.0 (installed for this pass) driving
headless Chromium 1248 (`~/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome`,
`--no-sandbox`). Viewports: 1280×900, 768×900, 390×844 (touch), plus a
`prefers-reduced-motion: reduce` context at 1280×900.
**QA script:** `/tmp/yojanasetu-qa/qa.py` (re-runnable); raw results
`/tmp/yojanasetu-qa/results.json`; screenshots `/tmp/yojanasetu-qa/*.png`;
downloaded CSV `/tmp/yojanasetu-qa/gaps.csv`.
**Scope:** rulebook §4 (every visible control) and §8 (performance /
accessibility / responsiveness). I fixed nothing. No repo, deploy, video or
submission was created.

## Test counts

| Suite | Result |
|---|---|
| Unit tests (`python3 -m unittest discover -s tests`) — **re-run by QA** | **37/37 PASS** (0.587 s) — confirms the build agent's claim |
| API smoke (coordinator-verified, not re-run here) | All routes 200 as reported |
| In-browser checks (Playwright, this pass) | **67 PASS / 6 FAIL out of 73** in the main run, plus 2 further FAILs found in follow-up probes (map clipping, by-scheme filter) — see Known issues |
| Console errors | **1** (favicon 404 — see F8) |
| Page errors (`window.onerror`) | 0 |
| Failed network requests (HTTP ≥ 400 / requestfailed) | 0 other than the favicon 404 |

## Per-control results (all clicked in a real browser unless noted)

### Navigation (1280px)
| Control | Result |
|---|---|
| Officer Dashboard / Beneficiary Lookup / Duplicate Detection / Eligibility Trace / Scheme Registry tabs | PASS — each shows its panel, sets `aria-pressed="true"` on the active tab |
| Footer myscheme.gov.in link | PASS — `href="https://www.myscheme.gov.in"` (not clicked out; link target verified) |

### Officer Dashboard
| Control | Result |
|---|---|
| 3D district block click (Dehradun) | PASS — filters dashboard, note reads "Showing: Dehradun…"; stats change (people 22 → 4) |
| Click same block again | PASS — clears filter, "all 13 districts" |
| 2D district list button (Nainital) | PASS — same filter action |
| Clear district filter button | PASS — resets to all districts |
| ArrowRight / ArrowLeft on focused block | PASS — focus moves Almora → Bageshwar → back to Almora |
| Enter on focused block | PASS — filters to Almora |
| Space on focused block | PASS — filters to Almora (follow-up probe) |
| Download inclusion gaps (CSV) | PASS — real download `yojanasetu-inclusion-gaps.csv`, 2,418 bytes, header + 29 gap rows |
| "Trace it" button (per gap row) | PASS — jumps to Eligibility Trace, pre-fills person YS-1001 + scheme pmay-g, runs trace, verdict shown |
| By-scheme table (unfiltered) | PASS — 8 rows; the 9th scheme (`uk-hill-transport`, REPRESENTATIVE) has 0 enrolments, so 8 is correct, not a bug |
| By-scheme table **under a district filter** | **FAIL — F2**: still shows the global counts (sums to 25) for every district |

### Beneficiary Lookup
| Control | Result |
|---|---|
| Search YS-1001 | PASS — 1 result, name + enrolments table with record IDs, departments, dates |
| Search "Gita Devi" (name) | PASS |
| Search "Dehradun" (district) | PASS — 4 results |
| Search "ZZZNOPE" (no match) | PASS — empty state with examples |
| Empty query submit | PASS — guidance message, no request |
| Clear button | PASS — empties query + results, refocuses the input |

### Duplicate Detection
| Control | Result |
|---|---|
| 3 pairs render with verdict chip, confidence, per-field evidence, suggested action | PASS — DUPLICATE 1.00, LIKELY 0.85, REVIEW 0.60 |
| Severity filter DUPLICATE / REVIEW | PASS — narrows to 1 pair each |
| Refresh list button | PASS — re-fetches, 3 pairs again |

### Eligibility Trace
| Control | Result |
|---|---|
| Person select (22 options) / Scheme select (9 options) | PASS |
| Run trace YS-1001 + pm-kisan | PASS — verdict ELIGIBLE + "Already enrolled" chip, 4 rule rows with PASS/FAIL/UNKNOWN chips, detail + source per rule |
| Clear result button | PASS — result emptied |

### Scheme Registry
| Control | Result |
|---|---|
| 9 scheme cards render | PASS |
| Search "PM-KISAN" | PASS — 1 card |
| Search "ZZZNOPE" | PASS — "No scheme matches" empty state |
| Category filter ("Agriculture") | PASS — narrows 9 → 1 |
| Clear button | PASS — restores all 9, resets search + category |

### Controls the task asked for that do NOT exist in the built app
| Control | Result |
|---|---|
| Low-motion toggle (masthead text button, constitution §10) | **FAIL — F5**: no element matching "Low motion" anywhere; only OS `prefers-reduced-motion` is honoured |
| "Reset view" button (map, constitution §9) | **FAIL — F6**: absent; there is also no drag/rotate interaction to reset |
| "Flat map" toggle (constitution §9) | **FAIL — F7**: absent; the 2D district list exists and is always visible, so the information is available, but there is no toggle |

## Viewport results

| Viewport | Result |
|---|---|
| 1280×900 desktop | No horizontal overflow (scrollWidth = clientWidth = 1280). All panels work. **But F1: the 3D map stage clips 8 of 13 blocks** (see below). Screenshot `1280-dashboard.png` confirms blocks cut at the plate's bottom edge. |
| 768×900 tablet | No horizontal overflow on dashboard, lookup, lookup results, trace. Map clips 3/13 blocks (F1). |
| 390×844 mobile (touch) | **FAIL — F3**: dashboard overflows to 425 px (gaps table 405 px uncontained; `.map-3d` 461 px wide). Lookup results overflow to 392 px (F4, 2 px). Tap on a district block filters correctly; lookup and duplicates work. Screenshot `390-dashboard.png`. |
| Reduced motion (`prefers-reduced-motion: reduce`, 1280) | Page loads, all 13 blocks render, `--extrude` is `0px` (flat), click-filter still works. The OS preference path works; the missing piece is only the manual toggle (F5). |

## Console / network results

- **1 console error:** `Failed to load resource: the server responded with a status of 404 (Not Found)`.
  Root cause confirmed: `GET /favicon.ico → 404`; there is no `<link rel="icon">` in
  `index.html` and no favicon file is served. Cosmetic, but Gate D asks for zero
  console errors (F8).
- 0 page errors, 0 failed API requests, 0 console warnings across all four contexts.
- No external requests at all (system fonts only, no CDN) — verified by the absence
  of any non-local request in the run.

## Keyboard / focus / contrast

- Tab order is logical (tabs → map blocks → controls). Focus is visible: the first
  Tab lands on a tab button with a `3px solid rgb(194,65,12)` (saffron) outline.
  Note: constitution §4/§12 specifies a 2 px green focus ring; the built CSS uses a
  3 px saffron ring — visible and passing, but a constitution drift (see below).
- Contrast **measured** (WCAG formula applied to the actual tokens in `style.css`,
  not the constitution's expected values): ink `#14213d` on paper `#fdfdf8` **15.66:1**;
  muted `#4a5568` on paper **7.38:1**; white on green `#0f3d2e` **12.16:1**; white on
  saffron `#c2410c` **5.18:1**; saffron on paper **5.08:1**; red/amber/blue chips on
  their tints 7.79 / 6.25 / 7.29:1. **All pass WCAG AA** (4.5:1 normal text).
  The constitution's "expected" ratios (~13:1, ~5.5:1, ~9:1, ~4.6:1) were computed
  against different hex values than the built CSS uses — the built values are
  equal or better in every case.

## Known issues

| # | Severity | Issue | Evidence / fix for the builder |
|---|---|---|---|
| F1 | **Medium** | **3D map stage clips district blocks at every viewport.** `.map-stage` has `overflow: hidden` and its content is taller than the stage after the isometric transform: at 1280 px, stage clientHeight 168 vs scrollHeight 361, **8 of 13 blocks** extend outside the plate (Almora, Bageshwar, Chamoli, Haridwar, Nainital, Pauri Garhwal, Pithoragarh, Rudraprayag); 3/13 at 768 px; 3/13 at 390 px. Blocks remain clickable (partially visible) but the signature 3D feature is visibly cut off. | Give `.map-stage` enough height for the rotated `.map-3d` (or remove the fixed-height squeeze / set an explicit stage height per breakpoint) and re-verify with the bounding-box probe. |
| F2 | **Medium** | **District filter does not filter "Enrolments by scheme".** `GET /api/dashboard?district=Almora` returns `total_people: 3, total_enrolments: 3` but `by_scheme` identical to the global table (sums to 25); same for Rudraprayag (1 person, same by_scheme). The filtered dashboard therefore shows contradictory numbers: "3 people in Almora" next to a scheme table totalling 25 enrolments. Stat cards and gaps *do* filter (gaps 29 → 6 for Almora). | Filter `by_scheme` by district server-side in `app/governance.py` / `app/server.py` (same as `total_people`/`gaps`), or hide the table under a district filter. |
| F3 | **Medium** | **Horizontal overflow at 390 px, dashboard: scrollWidth 425 vs clientWidth 390.** Culprits measured in-browser: the inclusion-gaps `<table>` (405 px, no scroll wrapper) and `.map-3d` (461 px wide). Rulebook §8 forbids horizontal overflow. | Wrap dashboard tables in a horizontally scrollable container (as the constitution prescribes for tablet) and cap `.map-3d` width at the stage. |
| F4 | Low | **Horizontal overflow at 390 px, lookup results: scrollWidth 392 vs 390** (2 px, enrolment table). | Same table-scroll wrapper; trivial. |
| F5 | Medium | **No low-motion toggle.** Constitution §10 requires a visible masthead "Low motion: Off/On" toggle persisted in `localStorage`. Only the OS media query is implemented (`app.js` `reducedMotion`, verified working). A user who needs reduced motion but has no OS setting cannot switch it off. | Add the toggle button per §10 (persist in `localStorage`, default the map to the flat list when on). |
| F6 | Low | **No "Reset view" button and no scene rotation at all** (constitution §9: drag / ←/→ rotate ±20°, Reset view). Arrow keys move *focus* between blocks, which is implemented and good, but there is no rotation to reset. | Either implement rotation + Reset view, or amend the constitution to drop rotation (the fixed isometric angle is defensible for 13 blocks). |
| F7 | Low | **No "Flat map" toggle** (constitution §9). The 2D district list is always visible below the map, so no information is hidden — this is a missing toggle, not missing data. | Add the toggle, or amend the constitution to record the always-visible 2D list as the flat view. |
| F8 | Low | **1 console error: favicon 404** (`GET /favicon.ico → 404`, no `<link rel="icon">`). | Add a favicon (inline SVG data URI is enough for a stdlib server) or a route returning 204. |

### Design-constitution drift (observations, not functional FAILs)

The built app is a **tabbed 5-panel app** (Officer Dashboard / Lookup / Duplicates /
Trace / Registry). `design/DESIGN_CONSTITUTION.md` describes a **different page
shape**: a single-column gazette with a ruled index line, numbered sections
01–04 (State at a Glance / Districts / The Ledger / File Noting), a ledger table
with district/scheme/status filters, row-click → file noting, copy buttons,
and a print stylesheet. None of those gazette structures exist in the built app,
and conversely the built app's tabs, duplicate-detection panel and eligibility
trace are not in the constitution's §6–§7. The inventory (`qa/INTERACTION_INVENTORY.md`)
matches the built app, not the constitution. Other drifts: fonts are Georgia +
system-ui, not Newsreader / Inter / IBM Plex Mono (§5); focus ring is 3 px
saffron, not 2 px green (§4/§12); saffron appears in more than one place per
viewport (banner border, "Setu" in the masthead, warn stat figures, selected
block, focus ring) against the "at most one saffron element per viewport" rule
(§4); no print stylesheet (§8/§12). The built visual identity is coherent and
the contrast numbers above are strong — but the constitution should be amended
to describe the app that was actually built, or the app brought into line,
before Gate A/C are claimed as fully passed. This does not change the Gate D
verdict, which is about the built app's behaviour.

## Gate D verdict: **FAIL**

The core workflows all work in a real browser — every inventoried control
passes, 37/37 unit tests re-verified, zero page errors, zero failed API calls,
AA contrast measured, reduced-motion OS path working. But Gate D requires the
desktop/tablet/mobile checks to pass and no critical console errors, and this
pass has three blocking defects in the built product: the signature 3D map is
visibly clipped at all three viewports (F1), the district filter shows
contradictory scheme totals (F2), and the dashboard overflows horizontally on
mobile (F3), plus one console error (F8). Fix F1–F3 (+F8, one line) and re-run
this QA script; F5–F7 are constitution-compliance items that should be fixed
or the constitution amended before the release is called complete.
