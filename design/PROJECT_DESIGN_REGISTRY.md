# PROJECT DESIGN REGISTRY — YojanaSetu (UKIS 2026, 10 Nov 2026)

Recorded so the next project can be checked against the last three and
be recognisably different in more than accent colour. Rulebook §1.3.
Previous designs were read from their actual source files and
constitutions on 10 Nov 2026 — nothing below is from memory alone.

## The new project

### YojanaSetu — UKIS 2026 (10 Nov 2026)
- **Concept / metaphor:** the Gazette Ledger. A government gazette
  (nameplate masthead, double rule, dateline, numbered sections, a
  headline that states the finding) over a ruled ledger (tabular
  numerals, hairline rules, one row per enrolment) with file-noting
  as the visible audit trail. The 13 districts stand up as extruded
  blocks on a map plate.
- **Palette:** paper-white `#FDFCF7`, card white, ink navy `#17263B`,
  Himalayan green `#0E3B2E`, green tint `#E6EFEA`, sparing saffron
  `#C2410C` (flag only, max one per viewport), brick `#8C2F26`
  (duplicate/mismatch status word only), hairline rule `#D8D2C4`,
  muted `#5A6470`. No gradients, no blur, no glow, no shadows of any
  kind — separation is by 1px rules, not boxes or shadows.
- **Typography:** Newsreader (serif display, sentence-case headlines)
  + Inter (UI/body) + tabular numerals on every figure (IBM Plex
  Mono for IDs only).
- **Layout:** single-column gazette, `max-width: 1120px` — masthead
  (not sticky) → ruled index line → headline + dek → key-figures
  strip (figures separated by rules, not cards) → district map plate
  (the page's only 7/5 split) → full-width ruled ledger table →
  file-noting section → ruled footer. No sidebar, no sticky bar, no
  two-column app.
- **Hero:** no hero image or split hero. The "hero" is the headline
  itself: a Newsreader sentence stating the finding ("1,214
  enrolments need a second look across 13 districts."), with a
  one-sentence dek. The 3D map comes later, in its own numbered
  section, like a map plate.
- **Signature interaction:** click a district block to filter the
  ledger; click a ledger row to load it into File Noting; record a
  note and watch it appear, dated and attributed, at the top of the
  audit trail. Filters (district / scheme / status / ID search)
  re-write the ledger with a staggered row reveal.
- **Motion:** staggered ledger-row reveal (200ms, 40ms steps, capped
  at 12 rows) + kinetic headline in words (320ms per word, 55ms
  stagger, once on load). Transform + opacity only.
- **3D:** "The District Blocks" — CSS 3D isometric schematic of
  Uttarakhand's 13 districts as extruded blocks (height = enrolment
  volume, saffron outline = open flags), rotation clamped ±20°,
  flat 2D tile grid as a first-class toggle and fallback. No WebGL,
  no library, no canvas.
- **Style:** Swiss Minimalism / Editorial — "Gazette Ledger".

## Previous projects (as actually built / specified)

### NyayaSeal — Walrus Haulout (10 Nov 2026, most recent)
- **Source read:** `~/workspace/hackathons/walrus-haulout/design/DESIGN_CONSTITUTION.md`
  and `~/workspace/hackathons/walrus-haulout/design/PROJECT_DESIGN_REGISTRY.md`.
- **Concept:** the Evidence Board + the Rubber Stamp. Chunky bordered
  dossier panels pinned in a strict grid; the verdict is a physical
  stamp slammed onto the evidence.
- **Palette:** dossier cream `#FFF3D6`, card white, ink `#111111`,
  seal vermilion `#E8380D`, vault teal `#0E7C6B`, seal gold `#FFB000`,
  vault blue `#2547F4`. Flat colour only — no gradients, no blur.
- **Typography:** Archivo Black (900, display/verdict) + Space
  Grotesk (UI/body) + IBM Plex Mono (hashes/evidence).
- **Layout:** sticky chunky top bar (logo block + button nav) → split
  hero (7/5, headline left, live Vault Stack right) → gold "How
  proof works" band (3 panels) → two-panel workbench (Seal / Verify
  side by side) → full-width evidence ledger table → ink footer.
- **Hero:** split hero, giant "PROVE IT. / OR IT DIDN'T / HAPPEN."
  with "PROVE IT." on a gold flat block; live 3D vault beside it.
- **Signature interaction:** the verdict stamp slam (rotated teal /
  vermilion stamp, 180ms overshoot) + click-a-slab-to-inspect in the
  Vault Stack + copy-every-hash controls.
- **Motion:** stamp slam + snap scroll-reveal (transform + opacity
  only).
- **3D:** "The Vault Stack" — Three.js, lazy, orthographic isometric,
  flat-shaded slabs, rotation clamped ±25°, render-on-demand; CSS 3D
  isometric fallback, then a flat 2D stepped stack. One canvas only.
- **Style:** Neo-Brutalism.

### PollPulse — TanStack Start × Convex (10 Nov 2026)
- **Source read:** `~/workspace/hackathons/tanstack-pollpulse/src/styles.css`
  (full file), as recorded in the NyayaSeal registry
  (`~/workspace/hackathons/walrus-haulout/design/PROJECT_DESIGN_REGISTRY.md`,
  read 10 Nov 2026).
- **Concept:** live polls on a deep-indigo night sky. Glassmorphism.
- **Palette:** deep indigo `#0a0f2e` → `#141031` gradient background,
  fuchsia `#d946ef` / cyan `#22d3ee` radial orbs, glass panels
  (`backdrop-filter: blur(18px)`), gradient text (fuchsia → indigo →
  cyan), near-white text `#f4f6ff`.
- **Typography:** system sans (`ui-sans-serif, system-ui, …`); gradient
  text for display.
- **Layout:** glass cards over a fixed gradient sky; staggered card
  entrance; live result bars growing by scaleX.
- **Hero:** glass hero over glowing orbs (gradient + blur treatment).
- **Signature interaction:** live voting with animated result bars;
  floating ambient orbs.
- **Motion:** rise-on-enter (0.7s), slow ambient orb float (9s
  infinite), bar-fill scaleX transitions. Transform + opacity only.
- **3D:** none (depth from glass/blur/orbs, not a scene).
- **Style:** Glassmorphism.

### SchemeSathi — SLAY HACKS 2026 (5 Nov 2026)
- **Source read:** `~/workspace/hackathons/slay-hacks/design/DESIGN_CONSTITUTION.md`,
  `~/workspace/hackathons/slay-hacks/design/PROJECT_DESIGN_REGISTRY.md`,
  and `~/workspace/hackathons/slay-hacks/design/RESEARCH.md`.
- **Concept:** the civic ledger / ration-card modernism. Cream paper,
  ruled structure, stamped verdict chips; the 8 scheme categories as
  a 3D ring ("Scheme Mandala"). A helpful clerk at a village service
  centre, for a citizen asking "am I even allowed to apply?".
- **Palette:** paper `#FBF6EC`, card `#FFFDF7`, ink `#1E2420`,
  green `#14532D` / deep `#0E3B20` / soft `#E4EFE6`, marigold
  `#E8821A` (focus rings, accents, Hindi subhead), line `#D8CDB4`,
  red `#9B2C2C` (NOT ELIGIBLE), amber `#8A6D00` (CLOSE), blue
  `#1D4E89` (NEEDS INFO); a 5px saffron–white–green tricolour rule
  at the very top.
- **Typography:** Georgia serif headings (ledger/gazette feel) +
  system sans body; Hindi subtitles in marigold; no webfonts.
- **Layout:** two-column app, `max-width: 1180px` — intake form
  left (380px: free-text box, example chips, parsed-profile receipt,
  structured form, situation checkboxes), Mandala + summary strip +
  verdict filters + scheme cards + what-if simulator right;
  collapses to one column under 900px.
- **Hero:** no hero treatment — the page opens on the intake form
  ("1 · Tell us about yourself").
- **Signature interaction:** plain-language sentence → parsed-profile
  receipt → rule-by-rule verdict trace → what-if sliders; verdicts
  as plain words (yours / close / not yours) with NEEDS INFO as a
  first-class verdict.
- **Motion:** restrained — 0.7s ease on the Mandala ring rotation
  only; card hover is a background change; auto-turn opt-in only.
- **3D:** "Scheme Mandala" — CSS 3D ring of 9 faces (All + 8
  categories), draggable, keyboard-steppable, flat button list as
  the reduced-motion fallback.
- **Style:** civic ledger / ration-card modernism (warm paper,
  serif, stamped verdicts).

## Comparison — YojanaSetu vs the three most recent

| Dimension | NyayaSeal | PollPulse | SchemeSathi | **YojanaSetu** |
|---|---|---|---|---|
| Style | Neo-Brutalism | Glassmorphism | Civic ledger / ration-card modernism | **Swiss Minimalism / Editorial — "Gazette Ledger"** |
| Canvas | Dossier cream `#FFF3D6`, flat colour blocks | Dark indigo gradient `#0a0f2e → #141031` + glowing orbs | Warm cream paper `#FBF6EC` + tricolour rule | **Paper-white `#FDFCF7`, flat, no blocks, no gradient, no tricolour** |
| Accent logic | Vermilion + teal + gold, each reserved to one meaning | Fuchsia/cyan gradient, decorative | Marigold everywhere (headings, focus, Hindi subhead) + green/red/amber/blue verdicts | **One saffron `#C2410C`, flag-only, max one per viewport; green is the working colour; brick is a status word only** |
| Display type | Archivo Black 900, uppercase, poster | System sans, gradient text | Georgia serif, ledger headings | **Newsreader serif, sentence-case headlines — editorial, not poster, not Georgia** |
| Borders / separation | 3px ink borders + hard `6px 6px 0` offset shadows | 1px glass borders + 18px blur | 1px warm line `#D8CDB4`, stamped chips | **1px hairline rules `#D8D2C4` only; no shadows of any kind; separation by rules, not boxes** |
| Layout | Sticky chunky bar + split hero + 2-panel workbench + ledger | Glass cards over a fixed gradient sky | Two-column citizen app (intake left 380px, results right) | **Single-column gazette: masthead (not sticky) → ruled index → headline → figures strip → map plate → ledger → file noting** |
| Navigation | Sticky bar of chunky buttons (Seal / Verify / Vault / Evidence) | Glass cards, no nav pattern | No nav bar, no tabs — Mandala + verdict chips filter | **One ruled index line of text links under the masthead; active section underlined** |
| Hero | Split hero, gold-block "PROVE IT." + live 3D vault | Glass hero over glowing orbs | No hero — opens on the intake form | **No hero image/split: the headline sentence IS the hero; the 3D map is a numbered map plate later in the issue** |
| Signature interaction | Stamp slam + slab inspection + copy-every-hash | Live voting + animated result bars + floating orbs | Sentence → receipt → rule trace → what-if sliders; 3D ring filters categories | **District block → filtered ledger → row → dated file note; filters re-write the ledger; the note appearing IS the confirmation** |
| Motion | Stamp slam (180ms overshoot) + snap reveal (14px, 60ms steps) | Rise-on-enter 0.7s + 9s ambient orb float | 0.7s Mandala rotation only; hover = background change | **Staggered ledger-row reveal (200ms, 40ms, capped 12 rows) + kinetic headline in *words* (320ms, 55ms, once)** |
| 3D | Vault Stack (Three.js, iso slabs, ±25°, 1 canvas) | None (glass depth) | Scheme Mandala (CSS 3D ring of categories, drag/keys) | **District Blocks (CSS 3D, 13 extruded district blocks, height = volume, outline = flags, ±20°, flat tile grid as first-class fallback) — no WebGL, no library** |
| User / voice | Lawyer/auditor proving a document is real; loud, certain | Poll voter; live, playful, night-sky | Citizen asking "can I apply?"; warm, plain-spoken clerk | **Government officer checking enrolments; quiet, exact, procedural — the gazette, not the clerk and not the stamp** |

## Why YojanaSetu is distinct in more than accent colour

The difference is not the saffron (SchemeSathi has saffron too, in its
tricolour rule and its marigold). It is structural, in at least seven
dimensions at once:

1. **Concept:** a gazette over a ledger, for an officer — versus a
   stamp slammed on evidence (NyayaSeal), a glass night sky for live
   voting (PollPulse), and a warm citizen intake with a category ring
   (SchemeSathi). The user is different (officer, not prover / voter /
   applicant), and the page is organised around that user's question
   ("which records disagree, and what do I note about them?"), not
   around a verdict, a vote, or an application.
2. **Canvas and separation:** paper-white with 1px hairline rules and
   zero shadows — versus flat cream blocks with hard shadows, a dark
   gradient sky with blur, and warm cream with stamped chips. No
   other fleet project separates content with rules alone.
3. **Typography:** Newsreader sentence-case headlines + Inter +
   tabular numerals — versus Archivo Black poster caps, system-sans
   gradient text, and Georgia serif. No other fleet project uses
   tabular numerals as a design feature.
4. **Layout and navigation:** a single-column gazette with a
   non-sticky masthead and a ruled index line — versus a sticky
   chunky bar + split hero + workbench, glass cards over a sky, and
   a two-column intake app. No other fleet project has a masthead
   that does not stick, or navigation that is a contents line.
5. **Hero:** there is no hero treatment at all — the headline
   sentence is the entry — versus a gold-block split hero, a glass
   hero, and an intake form. The 3D is deliberately *not* in the
   hero; it is a numbered map plate in section 02.
6. **Signature interaction:** district → ledger → file note, with the
   recorded note as the visible audit trail — versus stamp-a-verdict,
   vote-and-watch-bars, and sentence-to-trace. No other fleet project
   has file-noting, and no other fleet project makes the officer's
   written decision the product's output.
7. **3D:** 13 CSS-3D extruded district blocks encoding two variables
   (height = volume, outline = flags), with a flat tile grid as a
   first-class view — versus a Three.js vault of document slabs, no
   3D at all, and a CSS 3D ring of categories. The technique (CSS 3D,
   no engine) is shared with SchemeSathi's ring only at the level of
   "CSS 3D, no WebGL"; the object (a schematic district map), the
   encoding (height + outline), and the interaction (filter the
   ledger) are all different.

No hero treatment, card grid, sidebar, sticky bar, gradient, glass
panel, hard shadow, tricolour rule, stamp, ring, or single-column
guard-tool layout is reused from any previous project. The only
deliberately shared DNA is engineering-level, not visual: honest
labelling of sample data, a low-motion toggle +
`prefers-reduced-motion`, transform+opacity-only motion, and real
`<label>`s on every input.
**UI distinctiveness: PASS** under rulebook §1.3. Gate A design half
is satisfied by this registry + `DESIGN_CONSTITUTION.md`.
