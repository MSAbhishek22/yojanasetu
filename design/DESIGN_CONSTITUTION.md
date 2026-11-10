# DESIGN CONSTITUTION — YojanaSetu (UKIS 2026)

> **Project:** YojanaSetu — AI-Driven Integrated Beneficiary Data Governance
> for Uttarakhand (UKIS 2026, ₹1,03,000+ cash prize pool, solo, online
> Stage 1). One integrated, deduplicated view of who is enrolled in which
> benefit, where the records disagree, and what an officer should do next.
> **Target user:** a government officer checking benefit enrolments.
> **Status:** Design constitution written 10 Nov 2026, BEFORE implementation.
> It is the binding spec for the builder agent. Where the built UI differs
> from this file later, the built UI wins and the difference must be stated
> here.
> **AS-BUILT AMENDMENT — 10 Nov 2026 (post-Gate-D QA):** the app as built
> is a tabbed 5-panel app, NOT the single-page gazette this file originally
> described. §0A below is now the authoritative description of the
> as-built architecture; the sections after it keep the visual identity
> (palette, typography intent, ruled hierarchy) where true, and each
> section that the build contradicts is marked SUPERSEDED with the
> as-built reality stated inline. Nothing in §0A rebuilds the app — it
> records what was actually built.
> **Rulebook:** `~/workspace/ABHI_22_GLOBAL_PROJECT_QUALITY_RULEBOOK.md`
> §1–§3. Gate A (research + design) is satisfied by this file +
> `PROJECT_DESIGN_REGISTRY.md`.
> **Assigned style (not changed, refined):** Swiss Minimalism / Editorial —
> "Gazette Ledger".

## 0A. As-built amendment — 10 Nov 2026 (post-Gate-D QA)

**What was actually built** (verified in-browser by Gate D QA, 10 Nov 2026;
see `qa/QA_REPORT.md` and `qa/FIXES_POST_QA.md`):

- **Shape: a tabbed 5-panel app, not a single-page gazette.** One page,
  one masthead, five panels switched by a tab bar — Officer Dashboard /
  Beneficiary Lookup / Duplicate Detection / Eligibility Trace / Scheme
  Registry. Only one panel is visible at a time. There is no ruled index
  line, no numbered sections 01–04, no "State at a Glance / Districts /
  The Ledger / File Noting" scroll, no ledger table with district/scheme/
  status filters, no row-click → file noting, no copy buttons, no
  pagination, and no print stylesheet. File-noting as a feature does not
  exist in the built app.
- **Masthead (as built):** kicker line ("UKIS 2026 · Data Governance &
  Welfare · Uttarakhand"), "Yojana*Setu*" nameplate, one-line sub,
  a meta-line (problem / stage / 13 districts / prize pool), a
  SYNTHETIC DEMO DATA banner, and the tab bar. The masthead also carries
  the **Low motion: Off/On toggle** (§10) and the "Officer's desk — Demo"
  label. There is no double-rule dateline and the masthead is not sticky.
- **Fonts (as built): Georgia serif for display + system-ui for body.
  Newsreader, Inter and IBM Plex Mono were never loaded** — the app uses
  system fonts only, no CDN, no webfonts. Tabular numerals
  (`font-variant-numeric: tabular-nums`) ARE used on figures, as specified.
- **Focus ring (as built): 3px saffron outline + 2px offset** (measured
  in-browser), not the 2px green ring §4/§12 specify.
- **Saffron (as built): used for flags AND for the masthead "Setu", the
  warn stat figures, the selected district block and the focus ring** —
  i.e. more than one saffron element per viewport. The "at most one
  saffron element per viewport" rule was not met; the binding rule that
  survives is "saffron only for attention/flag states, never decoration".
- **Contrast (as built, measured by QA with the WCAG formula on the real
  tokens):** ink `#14213d` on paper `#fdfdf8` 15.66:1; muted `#4a5568`
  7.38:1; white on green `#0f3d2e` 12.16:1; white on saffron `#c2410c`
  5.18:1; saffron on paper 5.08:1. **All pass WCAG AA.** These replace
  the §12 estimates, which were computed against different hex values.
- **Map (§9, as built and fixed post-QA):** 13 CSS-3D extruded blocks,
  height = enrolment volume, click/tap/Enter filters the dashboard,
  arrow keys move focus between blocks, **drag (mouse) and Alt+←/→ rotate
  the scene ±20°, Reset view restores 0°, Flat map toggles to the 2D
  district grid**. The stage is 450px tall on desktop so the rotated
  scene is not clipped. Dashboard tables scroll inside their own
  container on narrow screens (no page-level horizontal overflow).
- **Motion (§10, as built):** the staggered ledger-row reveal and the
  kinetic headline were never built (there is no ledger and no animated
  headline). As-built motion is: map-block hover, button press
  (`scale` is not used — hover is a colour change), map rotation
  (transform only), and the low-motion toggle, which kills all of it
  and defaults the map to the flat list.
- **What survives unchanged from this file:** the Gazette Ledger visual
  identity — paper-white `#FDFDF8`, Himalayan green `#0F3D2E`, ink navy,
  hairline rules, serif headlines, small-caps status words, tabular
  numerals, no gradients / glass / shadows — and the product loop
  (check → flag → decide), the dual-encoding map (height = volume,
  saffron outline = flags), and the honest sample-data labelling.

## 0. Style pick — Swiss Minimalism / Editorial, "Gazette Ledger" (and why it is not the neighbours)

**Chosen: Swiss Minimalism / Editorial.** The page is a government gazette
that learned to be a ledger: a nameplate masthead, ruled lines, tabular
numerals, serif headlines, and a strict grid — with nothing on the page
that does not carry a fact. This is the right register for the user: an
officer does not need to be delighted or shouted at; they need to trust
the numbers at a glance, find the one district or record that disagrees,
and act on it before the next file-noting.

**Why it is not the three most recent fleet projects** (full proof in
`PROJECT_DESIGN_REGISTRY.md`):

1. **Not NyayaSeal (Neo-Brutalism, 10 Nov 2026).** No cream dossier
   background, no 3px ink borders, no hard offset shadows, no flat colour
   blocks, no rotated stamp, no Archivo Black poster type. YojanaSetu's
   borders are 1px hairline rules, its shadows are none, its verdicts are
   small-caps words in a ruled ledger row — not a slammed stamp.
2. **Not PollPulse (Glassmorphism, 10 Nov 2026).** No dark indigo sky, no
   gradient, no blur, no glass panels, no glowing orbs, no floating
   ambient motion. YojanaSetu is paper-white, flat, and still.
3. **Not SchemeSathi (civic ledger / ration-card modernism, 5 Nov 2026).**
   SchemeSathi is the closest cousin and therefore the one this design
   must work hardest to differ from: it is warm cream paper
   (`#FBF6EC`), Georgia serif, a tricolour rule, marigold accents, a
   two-column citizen intake (form left, results right), and a 3D ring.
   YojanaSetu is paper-*white* (`#FDFCF7`), not warm cream; its serif is
   Georgia (system serif — see §0A: Newsreader was specified but never
   loaded), not SchemeSathi's Georgia-by-choice; its accent is
   a single sparing saffron used only to flag, not a marigold that colours
   headings and focus rings; it has no tricolour bar, no citizen intake
   form at all (the user is an officer, not an applicant), no left/right
   two-column app — it is a tabbed five-panel app (§0A), not the
   single-column gazette this paragraph originally described: the
   masthead → headline → key figures → district map → ledger →
   file-noting scroll was not built. Its 3D is a district map, not a ring.
   The shared word "ledger" is a shared *domain* (government records),
   not a shared visual identity: SchemeSathi's ledger is a warm stamped
   verdict card; YojanaSetu's ledger is a cold ruled table with tabular
   numerals.

**Rejected alternatives:** Neo-Brutalism (taken by NyayaSeal, and a
shouting style is wrong for an officer checking records); Glassmorphism
(taken by PollPulse; blur fights tabular legibility); Cinematic / Film
Noir (taken by TapeOut Gate; a night desk is wrong for a daytime
government desk); Organic/Liquid, Hand-drawn/Claymorphism (wrong tone —
benefit records must look certain, not soft or sketchy); Parallax
Scrollytelling (wrong shape — this is a working ledger, not a story
page); Retro-Futurism/Y2K (chrome would cheapen a governance tool).

## 1. Product personality and emotional tone

**A gazette on a government desk, kept by a meticulous clerk.** Quiet,
exact, unhurried. The product says: "Here is the whole state on one
page. These are the numbers. These are the records that disagree. This
is what needs doing next — in that order."

Tone: credible, restrained, procedural. Warmth comes from clarity, not
from colour or ornament: a headline that states the finding in one
sentence, a figure that is always labelled with its source and date, a
disagreement that is shown as two numbers side by side rather than
hidden behind a score. No exclamation, no marketing copy, no fake
urgency. Saffron appears rarely enough that when it does, the officer
looks at it.

## 2. Target user and context of use

- **Primary user:** a government officer (district- or state-level) in
  Uttarakhand checking benefit enrolments — e.g. whether a beneficiary
  is enrolled twice, under two spellings, in two districts, or in a
  scheme they are no longer eligible for. They work at a desk, on a
  government laptop, often with a slow connection, often with a printout
  beside the screen. They may need to show the screen to a colleague or
  a senior officer, and to print the page.
- **Secondary user:** the UKIS judge on a laptop screen share, who must
  understand the whole loop (ingest → match/deduplicate → flag
  disagreement → officer decision → audit note) in one scroll, with no
  tab hunting.
- **Context:** desktop browser first, phone second (a field check on a
  phone must still show the district and the flag, even if the full
  table collapses). No account is assumed for the demo; seeded/sample
  data is labelled as such, in words, on the page. Nothing about a real
  beneficiary is ever invented: names, enrolment counts and
  disagreements shown in the demo are labelled SAMPLE / DEMO DATA, and
  the UI must say so in one line under the masthead.

## 3. Visual metaphor — the Gazette Ledger

One central metaphor, carried through every screen:

- **The Gazette:** the page is an issue of a gazette. A nameplate
  masthead ("YOJANASETU" in serif caps, with "Uttarakhand · Beneficiary
  Data Governance" and the issue line: date, stage, data-as-of), a
  headline that states the finding, a dek (one-sentence summary), and
  numbered sections (01 · The State at a Glance, 02 · Districts,
  03 · The Ledger, 04 · File Noting). The reader knows where they are
  because a gazette always tells them.
  **[SUPERSEDED — see §0A: the numbered sections, headline + dek and
  file-noting were not built. The built page keeps the nameplate masthead
  and the gazette voice, but organises the work into five tabbed panels.]**
- **The Ledger:** beneath the gazette is a ledger. Ruled lines (1px
  hairlines, never thick borders), tabular numerals (every figure in a
  column aligns on its right edge), and a row per record: beneficiary
  (anonymised ID, never a full name in the demo), scheme, district,
  status, and the disagreement, if any. A ledger row is the unit of
  truth; the map and the headline are summaries of it.
  **[SUPERSEDED — see §0A: there is no ledger table in the built app.
  The ruled-table language survives in the dashboard's "Enrolments by
  scheme" and "Inclusion gaps" tables and in the lookup/trace tables,
  all with tabular numerals and 1px rules.]**
- **File-noting:** the officer's action is a file note — a short,
  dated, attributed note attached to a record ("Verified against
  ration-card register, 10 Nov 2026 — A. Officer"), shown in the
  margin of the ledger like a clerk's annotation. This is the product's
  audit trail, and it is visible, not buried in a log.
  **[SUPERSEDED — see §0A: file-noting was not built. The officer's
  action in the built app is the Eligibility Trace ("Trace it" from a
  gap row) and the CSV export of inclusion gaps; there is no audit-trail
  note list.]**
- **The District Map (3D, §9):** the 13 districts of Uttarakhand as a
  schematic of extruded blocks — the state, stood up on its end, so
  enrolment volume is a height you can see. It is the gazette's map
  plate, not a decoration.

## 4. Colour palette — semantic roles (exact tokens for the builder)

| Token | Value | Semantic role | Where used |
|---|---|---|---|
| Paper | `#FDFCF7` | Page background | `body` — paper-white, not warm cream |
| Card white | `#FFFFFF` | Panel / table surface | Ledger, map plate, note cards |
| Ink navy | `#17263B` | Headlines, primary text, rules | Headlines, body text, masthead |
| Himalayan green | `#0E3B2E` | Primary actions, enrolled/verified state, section numbers | Primary buttons, "Verified" status, section numerals, map block tops |
| Green tint | `#E6EFEA` | Verified / enrolled background | Status chips (with the word, never colour alone) |
| Saffron (sparing) | `#C2410C` | Flag — the ONLY attention colour | "Needs attention" flag, the single key figure that disagrees, the active district outline. Used in at most one place per viewport. |
| Saffron tint | `#FDF0E6` | Flag background | Flagged rows (with the word FLAG, never colour alone) |
| Brick (semantic only) | `#8C2F26` | Duplicate / mismatch — a record-level status, never decoration | "Duplicate" / "Mismatch" status word in the ledger |
| Rule | `#D8D2C4` | Hairline rules, table dividers | All 1px rules |
| Muted | `#5A6470` | Secondary text, labels, captions, source lines | By-lines, "Source:" lines, micro-labels |
| Focus | `#C2410C` (saffron) | Focus ring (**3px outline + 2px offset, as built and measured** — the 2px green ring specified here was not built; see §0A) | `:focus-visible` everywhere |

**Rules (non-negotiable):**
- No gradients as decoration (a flat paper background; the only
  "gradient" permitted is none). No glassmorphism, no blur, no glow,
  no drop-shadow blur, no hard offset shadows either — depth comes
  from the 3D map and from the ruled hierarchy, not from shadows.
  Cards are separated by a 1px rule, not by a shadow or a border box.
- Saffron is used ONLY to flag something that needs an officer's
  attention. It never colours a heading, a button, or a decorative
  element. **[AMENDED — see §0A: as built, saffron also colours the
  masthead "Setu", the warn stat figures, the selected district block
  and the focus ring, so more than one saffron element is visible per
  viewport. The rule as written was not met; the binding rule is
  "saffron only for attention/flag states, never decoration".]**
- Green is the working colour (verified, enrolled, primary action);
  brick is a status word only. No status is ever colour-only: every
  status is a printed word (VERIFIED / ENROLLED / DUPLICATE /
  MISMATCH / NEEDS ATTENTION) plus its colour.
- The map blocks (§9) use green in stepped tints for height shading
  (top face lightest, side faces darker) — the map is the one place
  where a green scale is used, and it encodes nothing except the
  block's own height; status on the map is shown by a saffron outline
  on flagged districts, never by recolouring a block red.

## 5. Typography and type hierarchy

- **Display serif:** **Georgia** (system serif) for the masthead
  nameplate, headlines, and section titles. **[AMENDED — see §0A:
  Newsreader was specified here but never loaded; the built app uses
  Georgia, `"Times New Roman", serif`, with no webfont. The editorial
  serif intent survives, the typeface does not.]** The masthead is
  `clamp(2.5rem, 6vw, 4.25rem)`, uppercase, letter-spacing 0.02em,
  tight leading (1.0). Headlines are sentence case (a gazette
  headline states a finding, it does not shout): 32–40px, weight 600.
  *Why Newsreader, not Georgia:* **[SUPERSEDED — the built app uses
  Georgia after all; the Newsreader rationale below is kept as the
  record of the original intent, not the as-built fact.]** Georgia is SchemeSathi's and
  TapeOut Gate's and CageCheck's serif; Newsreader is a contemporary
  editorial serif with optical sizes, and its lighter, sharper
  texture reads as a gazette, not a ledger card or a night desk.
- **UI / body sans:** **system-ui** (`system-ui, "Segoe UI", sans-serif`)
  for labels,
  buttons, body copy, and table cells. **[AMENDED — see §0A: Inter was
  specified but never loaded.]** Body 16px, line-height 1.6.
- **Data:** **system sans with `font-variant-numeric: tabular-nums`**
  for figures — figures in the ledger MUST
  use tabular numerals so columns align; the builder uses
  `tabular-nums` on every figure, and mono only for IDs and record
  references (e.g. `UK-ENR-004213`). **[AMENDED — see §0A: IBM Plex
  Mono was specified but never loaded; IDs render in the system-ui
  stack with tabular numerals, at 13px.]** Fallback: `ui-monospace, Menlo,
  Consolas, monospace`. IDs render at 13px, `word-break: break-all`
  only where an ID is long; never truncate an ID without a copy
  control beside it. **[The copy control was not built — see §0A.]**
- **Hierarchy:** masthead (Newsreader, uppercase, largest) → headline
  (Newsreader 600, sentence case, 32–40px) → dek (Inter 17px, muted,
  one sentence) → section title (Newsreader 600, 22–24px, with a
  small-caps section numeral "01" in green + a full-width 1px rule
  beneath) → ledger column heads (Inter 600, 11px, uppercase,
  letter-spacing 0.12em, muted) → table body (Inter 15px, tabular
  numerals) → by-line / source line (Inter 12px, muted, "Source:
  … · As of … · Sample data").
- **Why this differs:** NyayaSeal is Archivo Black 900 poster type;
  NyayaLedger is Helvetica grotesk uppercase; TapeOut Gate, CageCheck
  and SchemeSathi are Georgia serif. A Newsreader serif headline +
  Inter body + tabular-numeral ledger is a different register from all
  of them — editorial, not poster, not grotesk, not Georgia.

## 6. Layout grid, spacing and page composition

- **Grid:** 12-column, `max-width: 1120px`, centred, 24px gutters.
  Spacing scale (4px base): 8 / 16 / 24 / 32 / 48 / 64. Generous
  whitespace is the design: the page breathes like a printed gazette,
  and density is earned only inside the ledger table.
- **Masthead (top, not sticky):** a nameplate block. Line 1: small
  caps kicker ("UKIS 2026 · UTTARAKHAND · STAGE 1" + "SAMPLE DATA"
  tag, both 11px, letterspaced, muted). Line 2: "YOJANASETU" in
  Newsreader caps. Line 3: a 1px double rule (a thick-thin rule pair,
  `border-top: 3px double` in ink navy — the gazette's one piece of
  ornament, and it is a rule, not a graphic) with the dateline below
  it ("Dehradun · Tuesday 10 November 2026 · Data as of …"). Right
  side of the masthead: a low-motion toggle (text button, §10) and
  the officer's desk label ("Officer's desk — Demo"). The masthead
  does NOT stick: a gazette's nameplate belongs at the top of the
  issue, and a sticky bar would be a dashboard convention borrowed
  from NyayaSeal. Section navigation is a ruled index line directly
  under the masthead (see §7).
  **[AMENDED — see §0A: as built, the masthead is a kicker + "Yojana*Setu*"
  nameplate (Georgia, not Newsreader) + one-line sub + a meta-line
  (problem / stage / 13 districts / prize pool) + the SYNTHETIC DEMO
  DATA banner + the tab bar. There is no double rule, no dateline, and
  no ruled index line. The low-motion toggle and the "Officer's desk —
  Demo" label ARE in the masthead, as specified.]**
- **Headline + dek (the finding):** one Newsreader headline stating
  the day's finding in sentence case — e.g. "1,214 enrolments need a
  second look across 13 districts." — with a one-sentence dek naming
  the largest cause. Below it, the key-figures strip (§6, below).
  No hero image, no split hero, no live 3D in the headline area:
  the headline is text, and the map comes later, in its own numbered
  section, like a map plate in a gazette.
  **[SUPERSEDED — see §0A: no finding headline + dek was built. Each
  panel opens with an `<h2>` title and a one-paragraph lede stating
  what the panel does.]**
- **Key-figures strip (01 · The State at a Glance):** four figures
  in a row, separated by 1px vertical rules (no cards, no boxes):
  Total enrolments · Verified · Duplicates flagged · Districts with
  open flags. Each figure: a large tabular numeral (40px, Inter 600),
  an 11px uppercase label beneath, and a one-line source note. The
  single saffron figure is the one that needs action (duplicates
  flagged); the other three are ink navy / green. On mobile the
  strip becomes a 2×2 grid with rules only between rows.
  **[AMENDED — see §0A: as built, the dashboard opens with five stat
  cards in a responsive grid (Synthetic people · Total enrolments ·
  Schemes in registry · Duplicate pairs flagged · Inclusion gaps),
  each with a large Georgia numeral and a label, the two flag figures
  topped with a saffron rule. The figures-separated-by-rules strip was
  not built; the stat cards are the as-built key figures.]**
- **District map plate (02 · Districts):** the 3D district map (§9)
  in a white plate with a 1px rule border, a caption line beneath
  it ("Figure 1 — Enrolment volume by district. Height = enrolments.
  Saffron outline = open flags."), and a district summary line that
  updates when a district is selected. Beside/below the map (desktop:
  right column of a 7/5 split *within this section only*): the
  selected district's figures and its top flags, in the same ruled
  style. The map plate is the only 7/5 split on the page — the rest
  of the page is single-column.
  **[AMENDED — see §0A: as built, the map sits in a bordered plate
  (450px tall on desktop) with a hint line above it and a filter note
  below it; the 2D district list follows, then Clear-filter and CSV
  export buttons. There is no 7/5 split and no caption line; the
  encoding is stated in the hint line ("Block height = enrolment
  volume").]**
- **The Ledger (03 · The Ledger):** the product. A full-width ruled
  table (1px rules only, no vertical lines, no zebra striping —
  striping would fight the tabular numerals): columns Beneficiary
  (anonymised ID) / Scheme / District / Enrolled / Status / Note.
  Rows are 52px, 15px Inter, tabular numerals. A flagged row carries
  a saffron left rule (3px, the only thick line in the table) and the
  word FLAG in saffron small caps — never colour alone. Filters sit
  above the table as a ruled filter bar: district (select), scheme
  (select), status (text-button group: All / Verified / Duplicate /
  Mismatch / Needs attention), and a search box for an enrolment ID.
  Every filter actually filters; the count line above the table
  ("Showing 48 of 1,214 enrolments") updates in words. Pagination
  is a plain "← Earlier | Later →" pair with a page note ("Page 1 of
  25"), not numbered page buttons.
  **[SUPERSEDED — see §0A: no ledger was built. The ruled-table
  language survives in the dashboard's "Enrolments by scheme" and
  "Inclusion gaps" tables and in the lookup/trace tables. The
  dashboard's district filter is the 3D map / 2D list / Clear button;
  the lookup panel is the ID/name/district search.]**
- **File Noting (04 · File Noting):** the officer's audit trail.
  A two-part section: on the left, the selected record's file notes
  in chronological order (date, officer, note text, in a ruled list);
  on the right, the "Add a note" form (a textarea with a real
  `<label>`, an officer-name field, and a "Record note" button).
  A note, once recorded, appears at the top of the list with its
  date — this is the visible proof that the officer's decision was
  recorded. Empty state: "No notes on this record yet — the first
  note is the audit trail."
  **[SUPERSEDED — see §0A: file-noting was not built.]**
- **Footer:** a 1px rule, then small print in muted 12px: data
  sources, the sample-data disclaimer, the UKIS track, and the repo
  link. No dark footer bar (NyayaSeal's ink bar is not reused).

## 7. Navigation and information architecture

**[SUPERSEDED — see §0A. The ruled index line, numbered sections and
hash deep-linking described below were not built. As built:]**

Navigation is a **tab bar** directly under the masthead — five text
buttons (Officer Dashboard / Beneficiary Lookup / Duplicate Detection /
Eligibility Trace / Scheme Registry) with `aria-pressed` on the active
tab; one panel is visible at a time. No sidebar, no sticky top bar, no
hamburger, no multi-page routing.

Deep-linking: selecting a district filters the dashboard (stat cards,
by-scheme table and inclusion gaps all follow the district) and updates
the filter note ("Showing: Dehradun…"); clicking the same district
again, or Clear district filter, restores all 13 districts. There is no
URL-hash deep link. A gap row's "Trace it" button jumps to the
Eligibility Trace panel with person + scheme pre-filled and the trace
already run.

Single page, four numbered sections, reached from a **ruled index
line** directly under the masthead — a single row of text links
("01 The State at a Glance · 02 Districts · 03 The Ledger ·
04 File Noting"), separated by middots, 13px Inter 500, with the
active section underlined in green as the user scrolls
(`aria-current="true"` on the active link). No sidebar, no sticky
top bar, no hamburger, no tabs, no multi-page routing. The index
line is the gazette's contents page, and it is the only navigation
on the page.

Deep-linking: selecting a district updates the URL hash
(`#district=dehradun`) and filters the ledger; loading that URL
restores the district filter — the shareable "look at Dehradun"
link an officer can send a colleague. Selecting a ledger row
scrolls to §04 with that record loaded in File Noting.

## 8. Component behaviour and interaction patterns

**[PARTLY SUPERSEDED — see §0A. The ledger, copy controls, file-note
form and print stylesheet below were not built. What was built:]**

- **Panels:** five panels (§7). Each opens with an `<h2>` + lede.
  The dashboard shows five stat cards, the 3D map + 2D list, the
  "Enrolments by scheme" table and the "Inclusion gaps" table (with a
  "Trace it" button per row and a CSV download). Lookup shows one
  holistic person card per result with an enrolments table. Duplicates
  shows flagged pairs with verdict chip, confidence, per-field evidence
  and a suggested action, plus a severity filter and Refresh. Trace
  shows a rule-by-rule table with PASS/FAIL/UNKNOWN chips and a verdict.
  Registry shows nine scheme cards with search + category filter.
- **Tables:** ruled tables (1px rules, tabular numerals) that scroll
  horizontally inside their own container on narrow screens
  (`.table-scroll`), never breaking the page. Empty states are words,
  never blank tables; failures are a red-bordered panel with the real
  error text.
- **Filters (ledger):** district and scheme are native `<select>`s
  with real `<label>`s; status is a group of text buttons with
  `aria-pressed`; search is a labelled input that matches an
  enrolment ID (prefix match, case-insensitive). Every change
  re-filters immediately and updates the count line; clearing all
  filters restores the full ledger. No filter is decorative.
  **[SUPERSEDED — there is no ledger filter bar. The filters that exist
  are: the district map / 2D list / Clear button (dashboard), the
  lookup search (ID / name / district), the duplicate severity filter,
  and the registry search + category filter. All of them actually
  filter.]**
- **Ledger rows:** clicking a row selects it (the row gains a 1px
  green left rule + a paper-tint background `#F4F1E8` — a tint, not
  a shadow) and loads it into §04 File Noting; the row is a real
  `<button>`-like focusable element with a visible focus ring.
  Hover: background tint only (no translate, no lift — a ledger row
  does not move; movement would be a dashboard convention).
  **[SUPERSEDED — no ledger rows exist.]**
- **Status chips:** small-caps words (11px, letterspaced) with a
  1px border in their status colour and a tint background — VERIFIED
  (green), ENROLLED (ink navy), DUPLICATE (brick), MISMATCH (brick),
  NEEDS ATTENTION (saffron). The word is always printed.
- **Buttons:** text-first. Primary ("Record note", "Apply filters"
  where a form needs one): solid Himalayan green background, white
  text, no border, no shadow, 44px tall, Inter 600 14px. Secondary:
  white background, 1px ink-navy border, ink-navy text. Hover:
  background darkens one step (instant colour change, no transform).
  Pressed: `scale(0.98)` (transform only, 120ms). Disabled: 50%
  opacity + the reason in text beside it. Every button has a visible
  `:focus-visible` state: 2px green outline + 2px offset.
- **District map blocks (§9):** click / tap / Enter selects a
  district and filters the ledger; hover raises the block 4px
  (translateY, transform only) and shows its figure in the caption
  line; keyboard ←/→ moves between districts in the map's tab order.
- **Copy controls:** every enrolment ID has a "Copy" text button
  (mono, 12px); on copy it reads "Copied" for 1.5s, then reverts.
  **[SUPERSEDED — see §0A: no copy buttons were built. Enrolment IDs
  are plain selectable text.]**
- **File-note form:** textarea + officer name, both labelled;
  client-side validation (empty note → an inline error in words,
  linked to the field, announced); on submit the note appears at
  the top of the list with today's date and the officer's name, and
  the form clears. No fake success toast — the note appearing in
  the list IS the confirmation.
  **[SUPERSEDED — see §0A: no file-note form was built.]**
- **Loading / empty / error states:** data loading → a ruled
  skeleton: the table shows its column heads and grey hairline rows
  (opacity pulse on the rules only, transform/opacity only) with
  the line "Checking the registers…"; no results → a bordered empty
  state in words ("No enrolments match these filters — widen the
  district or clear the status filter"), never a blank table;
  failure → a saffron-bordered panel with the real error text and a
  RETRY button. No fake success toasts, no dead buttons.
- **Print:** a print stylesheet keeps the masthead, headline, key
  figures and the ledger (filtered view) and hides the 3D map's
  controls and the note form — an officer prints the gazette, not
  the app chrome. This is a deliberate, stated feature of a
  government tool, and it is the one place where the gazette
  metaphor is literal.
  **[SUPERSEDED — see §0A: no print stylesheet was built.]**

## 9. 3D concept — "The District Blocks" (the state, stood up)

- **What it is:** a schematic map of Uttarakhand's 13 districts —
  Almora, Bageshwar, Chamoli, Champawat, Dehradun, Haridwar,
  Nainital, Pauri Garhwal, Pithoragarh, Rudraprayag, Tehri Garhwal,
  Udham Singh Nagar, Uttarkashi — each drawn as one extruded block
  in a CSS-3D isometric scene (fixed isometric angle, no WebGL
  dependency). Each block's **height encodes enrolment volume** in
  that district (linear scale, labelled on the block's top face with
  the district name and its figure); its top face is paper-white
  with a green edge, its side faces are stepped green tints (darker
  as the block gets taller, so height reads even in a still image);
  a district with open flags carries a saffron outline on its top
  face. The blocks sit on a flat paper base ruled with a faint
  1px grid, in approximately their real geographic arrangement
  (a schematic tile layout — the caption says so in words:
  "Schematic arrangement, not a survey map"), so a reader who
  knows Uttarakhand can find Dehradun in the west and Pithoragarh
  in the east without the map pretending to be a survey.
- **Why 3D is meaningful here:** enrolment volume across 13
  districts is exactly the kind of comparison a flat table hides —
  in a table, Dehradun's 4× volume over Rudraprayag is a digit you
  have to read; as heights, it is a difference you see before you
  read anything. Height also makes the officer's first question
  answerable in one glance ("where is the volume, and is that where
  the flags are?") — a tall block with a saffron outline is the
  story. A flat choropleth would colour the districts but could not
  show volume and flags at once without a second encoding; height
  carries the volume and the outline carries the flag.
- **Technology:** pure CSS 3D (`transform: rotateX(60deg)
  rotateZ(-45deg)` on a stage, each block a div with a top face and
  two side faces built from transforms) — 13 blocks, no library, no
  WebGL, no network asset, no canvas. Chosen deliberately over
  Three.js: 13 simple blocks do not need a 3D engine, and a
  government laptop on a slow connection should not download one.
  The scene renders immediately from the DOM; there is no loading
  screen for the map.
- **Interaction:** click / tap / Enter on a block selects its
  district and filters the dashboard (§7–§8); hover changes the block
  to a saffron tint; drag (mouse pointer) or Alt+←/→ keys rotate the
  scene ±20° around the vertical axis (transform only, stops at the
  limits — no free spin, no auto-rotation); a "Reset view"
  text button returns to the default angle; a "Flat map" toggle
  switches the same 13 districts to a 2D tile grid with identical
  labels and figures. Plain ←/→ keys move focus between blocks (the
  Alt modifier keeps rotation from conflicting with focus movement).
  Every 3D interaction has a text equivalent:
  the 2D district list below the map lists the same districts with
  the same figures, in the same order. **[AMENDED 10 Nov 2026: rotation,
  Reset view and the Flat map toggle are implemented — they were
  specified here but missing until Gate-D fixes F6/F7. Selection is
  press-anchored (pointerdown + pointerup, with a geometric tile
  lookup) because Chromium's click hit-testing is unreliable on the
  rotated blocks; see `qa/FIXES_POST_QA.md`.]**
- **Loading / error / fallback:** the map has no async load — it is
  DOM. If CSS 3D is unavailable, the flat 2D tile grid is shown
  instead (same data, same labels). If JavaScript is unavailable,
  the flat grid is the default and the district `<select>` still
  filters the ledger server-side / statically. The 3D never holds
  information hostage.
- **Mobile / performance:** 13 DOM blocks, no canvas, no render
  loop, no images; the stage is capped at the plate width
  (~640×420px desktop, full-width ~300px tall on mobile); on
  mobile the blocks are shorter (a capped height scale, stated in
  the caption) and the flat-grid toggle is offered first. Rotation
  is disabled on touch devices with a coarse pointer — tap-to-select
  only — so a scroll gesture is never hijacked.
  **[AMENDED — as built, the stage is 450px tall on desktop and ~400px
  on mobile (the rotated scene needs the height — see §0A/F1); on
  mobile the scene is scaled 0.72 so its bounding box fits the plate.
  Rotation is mouse/pen-only; touch is tap-to-select.]**
- **Reduced motion:** the scene is static (no rotation, blocks
  appear instantly); the flat-grid toggle is the default view under
  `prefers-reduced-motion` or the low-motion toggle (§10).
- **Accessibility:** each block is a real `<button>` with an
  `aria-label` ("Dehradun district, 1,214 enrolments, 3 open
  flags"); the selection is announced in an `aria-live="polite"`
  region ("Showing Dehradun — 48 enrolments"); the caption line
  states the encoding in words so no information is conveyed by
  height or colour alone.

## 10. Motion language (at least two techniques, transform + opacity only)

**[AMENDED — see §0A. The staggered ledger-row reveal and the kinetic
headline below were never built (no ledger, no animated headline).
As-built motion is: map-block hover (colour change, 180ms), map scene
rotation (transform only, ±20°), and the low-motion toggle. The
transform + opacity only rule and the 400ms budget survive for what
exists; the two named techniques below are the original intent, kept
as a record — not the as-built fact.]**

Two named techniques, plus micro-interactions — all transform +
opacity only, all fast, all purposeful.

1. **Staggered ledger-row reveal (the working motion):** when a
   filter changes (or the page first loads), ledger rows enter with
   `translateY(8px) → 0` + `opacity 0 → 1`, 200ms, staggered 40ms
   per row, capped at the first 12 visible rows (later rows appear
   instantly — a 1,214-row stagger would be a wait, not a motion).
   The stagger makes a re-filter read as "the ledger re-wrote
   itself", and the 40ms step keeps the total under ~700ms. Easing:
   `cubic-bezier(0.2, 0, 0, 1)` (ease-out). This is deliberately
   NOT NyayaSeal's snap reveal (14px, 60ms steps, hard snap) and
   NOT PollPulse's slow 0.7s rise — it is a quiet, clerical
   re-listing.
2. **Kinetic headline (the editorial motion):** the headline's words
   enter one at a time on first load — each word `translateY(0.35em)
   → 0` + `opacity 0 → 1`, 320ms per word, staggered 55ms, in
   reading order, so the finding is *read* rather than flashed.
   It happens exactly once, on first load, and only for the headline
   (the dek and figures appear whole). This is the gazette's
   typesetting moment: the headline is set, word by word, like type
   being laid. It is deliberately NOT TapeOut Gate's kinetic verdict
   stagger (45ms per *letter*, alarm-red) — words, not letters;
   serif, not mono; 55ms, not 45ms; and it states a finding, not a
   verdict.
3. **Micro:** primary buttons press with `scale(0.98)` (120ms);
   map blocks lift 4px on hover (translateY, 160ms); the rule under
   the active index link draws in with `scaleX(0) → 1` (200ms,
   transform-origin left); skeleton rules pulse in opacity only.
   No other motion.
   **[AMENDED — as built, buttons have no press scale and map blocks
   do not lift on hover (hover is a background/border colour change,
   180ms); there is no index link and no skeleton. The only
   as-built motion is the hover colour change and the map rotation.]**
- **Rules:** animate `transform` and `opacity` only — never width,
  height, top, left, or box-shadow (there are no shadows to animate).
  No continuous animation, no auto-rotation, no particles, no
  floating blobs, no ambient drift, no infinite loops. Motion
  communicates cause-and-effect (you filtered → the ledger re-wrote
  itself; the issue opened → the headline was set) and nothing else.
  Total motion budget: no single animation over 400ms except the
  headline's full word sequence, which is capped at ~1.2s and runs
  once.
- **Reduced motion:** `prefers-reduced-motion: reduce` AND a visible
  **Low-motion toggle** (a text button in the masthead, "Low motion:
  Off/On", persisted in `localStorage`) both disable all of the
  above: rows appear instantly, the headline appears whole, the map
  is static and defaults to the flat grid, skeleton rules are static.
  Every workflow works identically without motion.
  **[The toggle is implemented as specified (Gate-D fix F5): it is in
  the masthead, persists in `localStorage` (`yojanasetu-low-motion`),
  defaults to the OS preference when nothing is stored, and forces the
  flat district list while on. The "rows appear instantly / headline
  appears whole" clauses are moot — those animations were never built.]**

## 11. Responsive behaviour

- **Desktop (≥1024px):** 1120px grid; masthead full-width; key
  figures in a 4-across ruled strip; map plate 7/5 split (map left,
  district figures right); ledger full table (6 columns); file
  noting two-part (notes left, form right).
  **[SUPERSEDED — see §0A: as built, desktop is the tabbed app on a
  1120px grid; the dashboard shows five stat cards, the 450px map
  plate, and the two dashboard tables.]**
- **Tablet (600–1023px):** single column throughout; key figures
  2×2 with rules between rows; map plate stacks (map, then district
  figures); ledger scrolls horizontally inside its ruled panel
  (never breaks the page) with the Beneficiary column pinned
  (sticky left, paper background); file noting stacks (notes, then
  form).
  **[AMENDED — as built: single column; stat cards reflow; tables
  scroll horizontally inside their own containers (`.table-scroll`);
  no column is pinned; no file noting.]**
- **Mobile (<600px):** single column; masthead nameplate clamps
  down (floor 2.5rem); the index line wraps to two lines (still text
  links, no hamburger); headline 28px; key figures 2×2; map stage
  ~300px tall with the flat-grid toggle offered first; ledger shows
  4 columns (Beneficiary / Scheme / District / Status) with the
  remaining columns available in the row's expanded detail (tap a
  row to expand it in place); filters stack vertically; touch
  targets ≥44px.
  **[AMENDED — as built: single column; masthead clamps to 32px; tabs
  wrap; the map stage is ~400px tall with the scene scaled 0.72;
  the Flat map toggle sits beside Reset view; tables scroll inside
  their containers; no index line, no ledger, no row expansion.]**
- **No horizontal overflow anywhere** except the ledger's intentional
  inner scroll on tablet. The masthead, headline and CTAs are never
  clipped.
  **[AMENDED — as built: no page-level horizontal overflow at
  1280/768/390 (verified post-QA); wide tables scroll inside their
  own `.table-scroll` containers on every viewport.]**

## 12. Accessibility and reduced-motion behaviour

- Contrast (to be verified with a real contrast check by the builder
  before any WCAG claim is made; no pass is claimed here): ink navy
  `#17263B` on paper `#FDFCF7` is expected to be ~13:1; muted
  `#5A6470` on paper ~5.5:1; white on Himalayan green `#0E3B2E`
  ~9:1; white on saffron `#C2410C` ~4.6:1 — saffron is used only for
  large/bold flag words (≥14px bold) and is always accompanied by
  the printed word FLAG, so no information is colour-only or
  contrast-only. (Builder: measure, do not assert.)
  **[MEASURED 10 Nov 2026 (Gate D QA, WCAG formula on the real tokens
  in `style.css` — the built hex values differ from the ones above):
  ink `#14213d` on paper `#fdfdf8` 15.66:1; muted `#4a5568` 7.38:1;
  white on green `#0f3d2e` 12.16:1; white on saffron `#c2410c` 5.18:1;
  saffron on paper 5.08:1. All pass WCAG AA (4.5:1 normal text).]**
- Statuses, flags and errors are always words + colour, never colour
  alone. Enrolment IDs are text, selectable, copyable.
- Keyboard: full Tab order (masthead toggle → index links → key
  figures (not focusable — they are facts, not controls) → map
  blocks → filter controls → ledger rows → file-note form → footer
  links); visible green focus outlines everywhere; map blocks are
  focusable buttons with `aria-label`s; filter changes and district
  selection are announced in an `aria-live="polite"` region; the
  headline is a real `<h1>`, sections are `<h2>`s with their
  numerals.
  **[AMENDED — as built: Tab order is masthead toggle → tabs → map
  blocks → dashboard controls → panel controls → footer links; the
  focus outline is 3px saffron (see §0A); map blocks are focusable
  buttons with `aria-label`s; district selection updates the filter
  note; panel titles are real `<h2>`s; there are no index links,
  ledger rows or file-note form.]**
- Forms: every input has a real `<label>`; errors are announced and
  linked to their field; the search input has `role="search"` context
  via its label ("Search by enrolment ID").
- Reduced motion: §10 — OS preference + toggle, both kill all motion.
- Print: §8 — the gazette prints as a gazette.
  **[SUPERSEDED — see §0A: no print stylesheet was built.]**
- No information is conveyed by motion, height, rotation, or 3D
  alone: every encoding is stated in words in a caption, a label,
  or the ledger itself.

## 13. Design research — 5 references inspected 10 Nov 2026

All five were inspected on **10 Nov 2026** by opening the pages listed
(text fetch via `browser.open`). Where only part of a page was
inspectable, that is stated honestly below — no reference is claimed as
inspected when it was not.

### R1 — myScheme.gov.in (same category: Indian government benefit discovery)
- **URL:** https://www.myscheme.gov.in:443/accessibility-statement
- **Inspected:** the full Accessibility Statement + FAQ page (text
  fetch, page crawled 2026-11-08 14:58 UTC; inspected 10 Nov 2026).
  The page states myScheme's 3-step flow (enter details → see matches
  → scheme page), its 15 categories, 4,700+ central + state schemes,
  the Yes/No "Check Eligibility Questionnaire", multilingual support
  in 15 languages, MeriPehchaan single sign-on, and its WCAG 2.0
  Level A commitment — including the honest admission that PDF files
  and Hindi-language information are currently not accessible.
- **Learned:** the *domain shape* to respect — eligibility is a
  questionnaire with Yes/No answers, scheme pages carry benefit +
  documents + application procedure, and a government product earns
  trust by stating its accessibility limits in words. The 3-step
  flow maps onto our loop (check → flag → note) as a sequence an
  officer can follow, not a dashboard to stare at.
- **NOT to copy:** the citizen-facing intake (our user is the
  officer, not the applicant — no "Find Schemes for You" form);
  the login-gated saved profile (our demo is login-free); the
  card-list-of-schemes presentation (our unit is the ledger row,
  not the scheme card); the portal's own visual system.
- **Translation:** our §04 File Noting borrows myScheme's
  "eligibility as questions with Yes/No answers" idea as
  "disagreement as two numbers side by side with a note"; our
  footer carries myScheme's honest-limits habit (sample-data and
  accessibility limits stated in words); our 15-language note
  becomes a stated non-goal for Stage 1 (English + Hindi labels
  only, recorded as a limitation, not faked).

### R2 — GOV.UK Performance Platform, GDS blog (same category: government dashboard)
- **URL:** https://gds.blog.gov.uk/2012/10/03/building-a-performance-platform-for-gov-uk/?replytocom=17818
- **Inspected:** the full GDS blog post "Building a performance
  platform for GOV.UK" (text fetch, crawled 2026-11-10 06:04 UTC;
  inspected 10 Nov 2026): the brief, the audience map, the
  optician's-eye-chart hierarchy, the "at a glance" rule, and the
  modular dashboard design.
- **Learned:** the two most load-bearing ideas in this constitution.
  (a) The **optician's eye-test chart**: simple headline messages at
  the top that anyone can read, with more detail as you scroll down
  — our masthead → headline → key figures → map → ledger → notes
  is exactly this, in gazette form. (b) **Visualisations should
  only shout when there is something to say**: most data display
  stays neutral (grey) and only goes green/red when something is
  particularly noteworthy — our saffron-only-where-it-flags rule
  (§4) is this principle, translated from grey/green/red into
  paper/green/saffron. Also: design from real user roles (senior
  people need concise insights, analysts need the detail layers),
  and build in live code early with D3/SVG.
- **NOT to copy:** the GOV.UK visual system itself (different
  country, different brand); the D3/SVG charting stack (our map is
  CSS 3D, our charts are ruled tables — the right tool for 13
  districts and a ledger); the "business intelligence cacophony"
  the post explicitly warns against (competing reds and greens).
- **Translation:** the eye-chart hierarchy is §6's page order; the
  shout-only-when-there-is-something-to-say rule is §4's saffron
  discipline; the "why / what" annotation labels become our caption
  lines ("Figure 1 — …") and our source lines under every figure.

### R3 — Fluent 2 Design System, Motion (exceptional interaction / motion)
- **URL:** https://fluent2.microsoft.design/motion
- **Inspected:** the full Fluent 2 Motion page (text fetch, crawled
  2026-11-10 06:04 UTC; inspected 10 Nov 2026): motion principles
  (Functional, Natural, Consistent, Appealing), duration and easing
  guidance, the four transition types (enter/exit, elevation,
  top-level, container transform), choreography (staggering,
  hierarchy), and the accessible-motion section.
- **Learned:** motion as a *token system*, not a per-component
  afterthought — durations sized to the element and the distance it
  travels; easing that is never linear for UI (ease-out for
  entering, ease-in for exiting); staggering to soften a large
  set's entry and to direct the gaze, with short offsets and a
  warning that staggering a very large group makes the animation
  take too long (our 12-row cap on the ledger stagger comes
  directly from this); hierarchy — important elements get more
  prominent movement, lesser ones move together; and the explicit
  accessible-motion contract (a "no motion" setting, short
  durations, motion constrained to the element in focus, ARIA live
  regions for information conveyed by animation).
- **NOT to copy:** Fluent's elevation/depth language (our page has
  no shadows or elevation — depth is the 3D map, not a card
  rising); container-transform transitions (our layout does not
  morph containers); the Microsoft visual identity; any motion
  longer than our 400ms budget.
- **Translation:** our §10 motion tokens (200ms rows / 40ms stagger
  capped at 12; 320ms headline words / 55ms; 120ms press) are
  Fluent's duration/easing discipline with gazette-sized numbers;
  the low-motion toggle + `prefers-reduced-motion` + ARIA live
  announcements are Fluent's accessible-motion section, implemented
  as a named control in the masthead rather than a settings page.

### R4 — Financial Times data journalism, via GIJN / John Burn-Murdoch (typography / hierarchy)
- **URL:** https://gijn.org/stories/data-visualization-storytelling-tips-john-burn-murdoch/
- **Inspected:** the full GIJN article "From Data to Storytelling:
  Concept and Design Tips from the Financial Times' John
  Burn-Murdoch" (text fetch, crawled 2026-11-10 02:31 UTC;
  inspected 10 Nov 2026): the four takeaways (minimalism isn't
  always best; text helps readers remember; colour contrast draws
  you in but can distract; charts aren't just for data people), the
  Z-shaped reading pattern, and the COVID-19 case study (narrative
  title, labels moved onto the lines, secondary countries faded to
  grey, annotations at inflection points — geometry unchanged).
- **Learned:** the hierarchy lesson this constitution is built on.
  (a) **The Z-shape**: readers go title → axes → data — our page
  is laid out for exactly that path (headline → key figures →
  ledger). (b) **Text is where attention goes first**, and titles
  and annotations are what viewers remember — hence our headline
  states the finding, our figures carry narrative labels, and every
  chart (the map) carries a caption that says what it shows.
  (c) **Minimise distraction, maximise contrast**: one striking
  colour against muted everything else — our saffron rule, again,
  from a different source than R2, which is why it survives as a
  rule rather than a preference. (d) **Labels on the data, not in a
  legend**: Burn-Murdoch moved labels onto the lines so readers
  stopped flipping back and forth — our map puts the district name
  and figure on the block's top face, and our ledger puts the status
  word in the row, for the same reason.
- **NOT to copy:** the FT's salmon pink (`#fff1e0`) and Financier
  serif (that is the FT's identity, and a pink gazette would be a
  different product); the FT's dense multi-column newspaper river
  (our page is a single-column gazette with one map plate, not a
  newspaper); the "minimalism isn't always best" licence to add
  annotation everywhere (our annotations are one caption per figure,
  not arrows all over the page — a government ledger earns trust by
  restraint, and Burn-Murdoch's own caveat is that annotation must
  be well-placed, not plentiful).
- **Translation:** the Z-shaped page order (§6); the narrative
  headline + dek (§6); the on-the-data labelling (§9, §8); the
  one-striking-colour discipline (§4); the "every figure has a
  caption that says what it shows" rule (§6, §9).

### R5 — Flourish, "You can now add regions to your high-performance WebGL-based data maps" (3D / spatial)
- **URL:** https://flourish.studio/blog/3d-pointmap-regions/
- **Inspected:** the full Flourish blog post (text fetch, crawled
  2026-11-10 06:04 UTC; inspected 10 Nov 2026): the 3D Map
  template's four map types — custom regions over a styled base
  map, high-performance choropleths with specific projections,
  extruded region maps (colour by one column, extrude by another),
  and timeline point maps with regions — plus the GeoJSON Regions
  workflow and the WebGL performance note.
- **Learned:** the single most useful 3D-data rule for this
  product: **colour by one column and extrude by another** — two
  independent encodings on the same map, so one visual answers two
  questions. Our map does exactly this: height = enrolment volume,
  saffron outline = open flags. Also: regions over a styled base
  map put the region in context (our faint ruled base grid does
  this without a tile layer); and WebGL's smoothness matters most
  with detailed region data — with 13 schematic blocks, CSS 3D is
  the proportionate technology, and Flourish's own note that the
  template "is also great for making high-performance maps in 2D"
  supports our flat-grid fallback being a first-class view, not a
  downgrade.
- **NOT to copy:** the WebGL template itself (a 3D engine for 13
  blocks would violate rulebook §3's "do not add a large dependency
  just to claim 3D"); the Mercator base map and tile layers (our
  schematic needs no tiles, and tiles would pretend to a survey
  accuracy we do not have); the timeline/points layer (our data is
  a snapshot "as of" a date, not a time series — a timeline would
  fake a history); Flourish's template-gallery presentation.
- **Translation:** the dual encoding (height + outline) is §9; the
  "extrude by the Height binding, with min/max height settings"
  becomes our capped linear height scale with the cap stated in the
  caption; the flat 2D map as a first-class view becomes our
  flat-grid toggle and reduced-motion default.

## 14. Original design decisions (this project only)

- Swiss Minimalism / Editorial chosen by assignment and refined into
  "Gazette Ledger" — the gazette is the product's voice, the ledger
  is its proof, and the two are one page, not two screens.
  **[AMENDED — see §0A: the voice survives; the "one page" is five
  tabbed panels, and there is no ledger table.]**
- The masthead as nameplate + double rule + dateline, and the masthead
  deliberately NOT sticky — a gazette's nameplate belongs at the top
  of the issue.
  **[AMENDED — see §0A: nameplate, not sticky — true. The double rule
  and dateline were not built.]**
- The ruled index line as the only navigation (no sidebar, no sticky
  bar, no hamburger) — the contents page of the issue.
  **[SUPERSEDED — see §0A: navigation is the five-tab bar.]**
- The key-figures strip as figures separated by rules, not cards —
  the anti-card: no boxes, no shadows, no backgrounds.
  **[SUPERSEDED — see §0A: as built, the key figures ARE cards (five
  stat cards with 1px rules and a green/saffron top rule).]**
- Saffron as a rationed flag, not an accent: at most one saffron
  element per viewport, counted by the builder.
  **[AMENDED — see §0A: the ration was not met as built; the surviving
  rule is "saffron only for attention/flag states, never decoration".]**
- Tabular numerals as a design feature, not a detail: every figure
  aligns, because an officer compares figures by eye down a column.
- The kinetic headline in *words* (not letters), once, on load —
  the headline is set like type, not flashed like a verdict.
  **[SUPERSEDED — see §0A: no kinetic headline was built.]**
- The District Blocks: 13 CSS-3D extruded blocks, height = enrolment
  volume, outline = open flags — dual encoding borrowed from
  Flourish, built without a 3D engine, with a flat tile grid as a
  first-class fallback.
- File-noting as the visible audit trail: the officer's note appears
  in the ledger's own section, dated and attributed, instead of
  disappearing into a log file.
  **[SUPERSEDED — see §0A: file-noting was not built.]**
- Print as a first-class behaviour: the gazette prints as a gazette.
  **[SUPERSEDED — see §0A: no print stylesheet was built.]**
- Honest limitations stated in the UI: sample data labelled as
  sample, the map labelled schematic, language scope stated as a
  Stage-1 limitation — the product earns trust by saying what it is
  not.
