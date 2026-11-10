# DEPLOYMENT RUNBOOK — YojanaSetu (UKIS 2026)

> Status: **DEPLOY-PREP DONE 10 Nov 2026 — no live deployment exists yet.**
> Vercel adapter (`api/index.py` + `vercel.json` + `.python-version`) is written
> and verified locally (WSGI harness 23/23 PASS, unit tests 38/38 PASS).
> Every field that would describe a real deployment is still `null` below.
> Nothing here claims a live URL. Do not present any URL from this file as live
> until a real deploy is verified from a fresh browser session.

## Release

- Project: YojanaSetu
- Version: 0.1.0 (local build + deploy-prep, 10 Nov 2026)
- GitHub repository URL: `null` — repo MSAbhishek22/yojanasetu does NOT exist yet
  (verified via search_repositories 10 Nov 2026, total_count 0). The GitHub App
  cannot create repos (403, known) — create it in the user's GitHub browser
  session, empty, no README init — see §6.
- Production branch: `main` (planned)
- Deployed commit SHA: `null`
- Production URL: `null` (expected `https://yojanasetu.vercel.app` — confirm the
  actual assigned URL at deploy time; do not assume the slug)
- Deployment provider: Vercel Hobby (planned, NOT deployed) — free tier, no card
- Deployment timestamp (UTC/IST): `null`
- Build/deployment ID: `null`
- Backend/API URL: `null` (same origin as the frontend when deployed)
- Database: none — synthetic data is compiled into `app/data.py`; no persistence
  needed; the app never writes to disk
- Environment variables: **none required** (no secrets, no env vars by design)

## Vercel adaptation (done, verified locally 10 Nov 2026)

- `api/index.py` — WSGI entrypoint, same pattern as NyayaSeal's adapter
  (`~/workspace/hackathons/walrus-haulout/api/index.py`). Route-for-route parity
  with `app/server.py`: `/`, `/static/*`, `/favicon.ico` (204), `/health`,
  `/api/schemes`, `/api/beneficiaries`, `/api/beneficiary`, `/api/duplicates`,
  `/api/trace`, `/api/dashboard` — same JSON shapes, same status codes, same
  error strings. Only GET is served; POST returns 404.
- `vercel.json` — `functions.api/index.py.maxDuration: 60`,
  rewrite `/(.*)` → `/api/index`.
- `.python-version` — `3.12`.
- **Serverless note (unlike NyayaSeal, no caveat applies):** YojanaSetu is fully
  read-only — every route is a GET and the app never writes to disk, so there
  is no per-instance store that can go stale. Serverless behaviour is
  identical to local; no `/tmp` store is needed and no "warm instance"
  assumption is made. Data is compiled into `app/data.py` (22 synthetic
  people, 9 schemes, 13 districts).
- WSGI harness: `/tmp/yojanasetu-wsgi-test.py` — **23/23 PASS** (home, static,
  health 9/22/13, schemes total 9, dashboard 22 people / 25 enrolments,
  district filter + unknown-district 400, duplicates incl. seeded 1.00 pair,
  beneficiary search + lookup + 404, trace ELIGIBLE + bad-ids 400, unknown
  path 404, rewritten `/api/index`, favicon 204, POST rejected).
- Unit tests: `python3 -m unittest discover -s tests` → **38/38 PASS** (0.59s,
  re-run 10 Nov 2026 by the deploy coordinator).
- Secret scan: **0 hits** (only false positives: "token" as in name tokens /
  design tokens in `app/governance.py` and `design/DESIGN_CONSTITUTION.md`).
  All snapshot files UTF-8. Push manifest:
  `~/workspace/hackathons/yojanasetu-paths` (23 paths incl. the manifest below,
  ~215 KB).

## Local run (verified 10 Nov 2026)

```bash
cd ukis-yojanasetu
python3 run.py            # http://127.0.0.1:8771
python3 -m unittest discover -s tests -v   # 38 tests, all PASS
python3 /tmp/yojanasetu-wsgi-test.py       # WSGI harness, 23/23 PASS
```

Health check: `curl http://127.0.0.1:8771/health` → `{"status": "ok", "schemes": 9,
"people": 22, "districts": 13, "data": "SYNTHETIC DEMO DATA — no real citizen data"}`

## Deployment steps (Gate E)

1. **GitHub repo (browser, user's signed-in session):** https://github.com/new →
   name `yojanasetu`, Public, description
   `YojanaSetu — beneficiary data governance for Uttarakhand (UKIS 2026)` →
   do NOT tick README / .gitignore / licence → Create repository (empty).
2. **Push (connector, needs user approval — expected):**
   `github push-files --owner MSAbhishek22 --repo yojanasetu --branch main
   --message "YojanaSetu — UKIS 2026 entry (snapshot 1)" --source-dir
   ~/workspace/hackathons/ukis-yojanasetu --paths-file
   ~/workspace/hackathons/yojanasetu-paths`, then verify head SHA with
   `list_commits` and save the sync record.
3. **Vercel (user's signed-in session, Hobby/free, no card):** Add New → Project →
   Import `MSAbhishek22/yojanasetu`, framework Other, no build command, no env
   vars required → Deploy. If Vercel asks for a card or identity verification,
   follow the NyayaSeal precedent: identity code comes from the user's mail;
   a card request is a hard STOP — report it, do not proceed.
4. **Verify from a fresh browser session** (§3 below) and record provider +
   build ID + timestamp + commit SHA in `deployment/RELEASE_MANIFEST.json`.
   Only then is Gate E PASS.

## Health checks (post-deploy, fresh browser session)

- `GET /` loads the Gazette Ledger home page with the SYNTHETIC DEMO DATA banner.
- `GET /health` returns 200 with `status: "ok"`, schemes 9, people 22, districts 13.
- `GET /api/dashboard` returns 22 people, 25 enrolments, 3 duplicate pairs, 29 gaps.
- `GET /api/duplicates` returns the seeded DUPLICATE (YS-1001/YS-1002, 1.00).
- `GET /api/beneficiary?id=YS-1001` returns Gita Devi's holistic view.
- `GET /api/trace?person=YS-1001&scheme=pm-kisan` returns a rule-by-rule trace.
- No console errors; no horizontal overflow at 1280/768/390px.

## Rollback

- No deployment to roll back yet. Locally: the working tree in
  `~/workspace/hackathons/ukis-yojanasetu/` is the only copy until the first push;
  after the push, `git` history on GitHub is the rollback source. Vercel keeps
  prior deployments — redeploy a previous one from the Vercel dashboard if a
  new deploy regresses.

## Ownership

- Builder: build agent (subagent), 10 Nov 2026.
- Deploy-prep: deploy coordinator (subagent), 10 Nov 2026.
- Owner for deploy/submit decisions: the user (M S Abhishek) — deploy and UKIS
  submission need his explicit approval; neither was requested or given in this
  task.
