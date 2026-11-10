/* YojanaSetu frontend — stdlib API only, no external assets.
   Every visible control below is wired to a real behaviour; see
   qa/INTERACTION_INVENTORY.md for the control-by-control list. */
"use strict";

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => (
  {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const inr = (n) => "₹" + Number(n).toLocaleString("en-IN");

/* ---- Low motion + flat map (constitution §9–§10, Gate D F5–F7) ----
   Low motion: manual masthead toggle, persisted in localStorage; when no
   stored preference exists the OS prefers-reduced-motion setting is the
   default. While low motion is on, the map defaults to the flat list.
   Flat map: manual toggle, persisted; either switch shows the 2D list. */
const LOW_MOTION_KEY = "yojanasetu-low-motion";
const FLAT_MAP_KEY = "yojanasetu-flat-map";
const osReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const storedLowMotion = localStorage.getItem(LOW_MOTION_KEY);
let lowMotion = storedLowMotion === null ? osReducedMotion : storedLowMotion === "true";
let flatMap = localStorage.getItem(FLAT_MAP_KEY) === "true";
let mapRotation = 0; // degrees, clamped to ±20 (constitution §9)

function applyRotation() {
  $("map-3d").style.setProperty("--map-rot", mapRotation + "deg");
}
function setRotation(deg) {
  mapRotation = Math.max(-20, Math.min(20, Math.round(deg)));
  applyRotation();
}
function applyMapView() {
  const flat = flatMap || lowMotion; // low motion forces the flat list
  document.body.classList.toggle("low-motion", lowMotion);
  document.body.classList.toggle("flat-map", flat);
  const lm = $("btn-low-motion");
  lm.textContent = "Low motion: " + (lowMotion ? "On" : "Off");
  lm.setAttribute("aria-pressed", String(lowMotion));
  const fm = $("btn-flat-map");
  fm.textContent = "Flat map: " + (flat ? "On" : "Off");
  fm.setAttribute("aria-pressed", String(flat));
  fm.title = lowMotion ? "Low motion is on, so the flat district list is shown." : "";
  const rv = $("btn-reset-view");
  rv.disabled = flat;
  rv.title = flat ? "Reset view is available in the 3D map view." : "Restore the default map angle.";
  applyRotation();
}
$("btn-low-motion").addEventListener("click", () => {
  lowMotion = !lowMotion;
  localStorage.setItem(LOW_MOTION_KEY, String(lowMotion));
  applyMapView();
  loadDashboard(); // re-render blocks: extrude 0 under low motion, restored otherwise
});
$("btn-flat-map").addEventListener("click", () => {
  flatMap = !flatMap;
  localStorage.setItem(FLAT_MAP_KEY, String(flatMap));
  applyMapView();
});
$("btn-reset-view").addEventListener("click", () => setRotation(0));

/* Drag to rotate the 3D scene (mouse/pen only — touch keeps scroll).
   A drag that moves >6px is a rotate, not a click, so it never also
   selects the district underneath. */
const mapStage = document.querySelector(".map-stage");
let dragStartX = null, dragStartY = null, dragStartRot = 0, mapDragged = false, dragCaptured = false;
/* Press-anchored selection (Gate D re-probe): in this CSS-3D scene the
   mouseup/click hit-test is unreliable right after a press — Chromium
   reports the stage, not the block, for fast presses, so a plain click
   sometimes never reaches the block. The pointerDOWN target is always
   correct, so a press is anchored to the block it started on: if the
   pointer is released with barely any movement, that block is selected.
   Movement in any direction (a drag, or a touch scroll) cancels it. */
let pressBlock = null, pressDistrict = null, pressMoved = false;
let lastPointerSelectDistrict = null, lastPointerSelectAt = 0;
/* Hover anchor: the block the pointer last moved over. Pointermove
   hit-testing is stable in this scene while pointerdown/mouseup are not
   (the press's down can report the stage and its up the block, or vice
   versa — the target flips between the two events), so the press is
   anchored to the block the pointer was over just before the press as
   well as the block the press itself started on. */
let hoverBlock = null, hoverDistrict = null;
function districtOf(block) {
  return block ? block.getAttribute("aria-label").split(":")[0] : null;
}
/* Geometric block lookup: which district block's tile contains the point.
   Hit-testing is unreliable in this CSS-3D scene (the press's target
   flips between the block and the stage), and a second click on the same
   block has NO pointermove before it (the pointer is already there), so
   neither the press target nor the hover anchor can be trusted alone.
   Geometry is deterministic: the point is the face's centre, so among
   the tiles whose box contains the point, the nearest centre wins. */
function blockAtPoint(x, y) {
  let best = null, bestD = Infinity;
  document.querySelectorAll("#map-3d .district-block").forEach((b) => {
    const r = b.getBoundingClientRect();
    if (x >= r.left - 2 && x <= r.right + 2 && y >= r.top - 2 && y <= r.bottom + 2) {
      const d = Math.hypot(x - (r.left + r.width / 2), y - (r.top + r.height / 2));
      if (d < bestD) { bestD = d; best = b; }
    }
  });
  return best;
}
mapStage.addEventListener("pointerdown", (e) => {
  if (lowMotion || flatMap) { pressBlock = null; return; }
  // NOTE: no setPointerCapture here — capturing on pointerdown retargets
  // the following click to the stage, so a plain click would never reach
  // the district block (Gate D re-probe caught this: clicks stopped
  // filtering). Capture only once a real drag has started.
  const block = blockAtPoint(e.clientX, e.clientY) ||
    (e.target.closest ? e.target.closest(".district-block") : null);
  pressBlock = block;
  pressDistrict = districtOf(block);
  pressMoved = false;
  dragStartX = e.clientX; dragStartY = e.clientY; dragStartRot = mapRotation; mapDragged = false; dragCaptured = false;
});
mapStage.addEventListener("pointermove", (e) => {
  // Track the block under the pointer (see hover anchor note above).
  // Only while no press is in progress — during a press the anchor is
  // the press block, and a drag must not re-anchor mid-drag.
  if (dragStartX === null) {
    const block = e.target.closest ? e.target.closest(".district-block") : null;
    hoverBlock = block;
    hoverDistrict = districtOf(block);
  }
  if (dragStartX === null) return;
  const dx = e.clientX - dragStartX, dy = e.clientY - dragStartY;
  if (Math.abs(dx) > 6 || Math.abs(dy) > 6) pressMoved = true;
  if (Math.abs(dx) > 6) {
    mapDragged = true;
    if (e.pointerType !== "touch" && !dragCaptured) {
      try { mapStage.setPointerCapture(e.pointerId); dragCaptured = true; } catch (_) { /* older browsers */ }
    }
  }
  if (e.pointerType !== "touch") setRotation(dragStartRot + dx / 4);
});
function endPress(e) {
  if (dragStartX === null) return;
  // A press that barely moved and was released inside the stage selects
  // the block it started on — or, if the press's own hit-test missed,
  // the block the pointer was hovering just before the press. (The
  // pointerup event's own target is the flaky part, so it is not used.)
  const anchorBlock = pressBlock || hoverBlock;
  const anchorDistrict = pressDistrict || hoverDistrict;
  if (anchorBlock && !pressMoved && e && e.clientX !== undefined) {
    const r = mapStage.getBoundingClientRect();
    if (e.clientX >= r.left - 4 && e.clientX <= r.right + 4 &&
        e.clientY >= r.top - 4 && e.clientY <= r.bottom + 4) {
      lastPointerSelectDistrict = anchorDistrict;
      lastPointerSelectAt = Date.now();
      selectDistrict(anchorDistrict);
    }
  }
  dragStartX = null; dragStartY = null; dragCaptured = false; pressBlock = null;
  // Clear the hover anchor: the map re-renders on selection (detaching
  // the anchored node), and a drag ends with the pointer somewhere the
  // anchor no longer describes — a stale anchor would mis-select.
  hoverBlock = null; hoverDistrict = null;
}
["pointerup", "pointercancel"].forEach((ev) =>
  mapStage.addEventListener(ev, endPress));
window.addEventListener("pointerup", endPress);
mapStage.addEventListener("pointerleave", () => { hoverBlock = null; hoverDistrict = null; });
mapStage.addEventListener("click", (e) => {
  if (mapDragged) { e.stopPropagation(); e.preventDefault(); mapDragged = false; }
}, true);

async function api(path) {
  const res = await fetch(path);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || ("Request failed: " + res.status));
  return data;
}
function showError(el, err) { el.innerHTML = '<p class="error">' + esc(err.message) + "</p>"; }
function clearError(el) { el.innerHTML = ""; }

/* ---- Section tabs ---- */
document.querySelectorAll("nav.tabs button").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll("nav.tabs button").forEach((b) => b.setAttribute("aria-pressed", "false"));
    btn.setAttribute("aria-pressed", "true");
    document.querySelectorAll("section.panel").forEach((p) => p.classList.remove("active"));
    $("panel-" + btn.dataset.panel).classList.add("active");
  });
});

/* ---- Dashboard ---- */
let currentDistrict = null;
let lastGaps = [];

function statCard(value, label, warn) {
  return '<div class="stat' + (warn ? " warn" : "") + '"><b class="num">' + esc(value) +
    "</b><span>" + esc(label) + "</span></div>";
}

async function loadDashboard() {
  const errEl = $("dash-error");
  clearError(errEl);
  try {
    const path = "/api/dashboard" + (currentDistrict ? "?district=" + encodeURIComponent(currentDistrict) : "");
    const { dashboard } = await api(path);
    $("dash-stats").innerHTML =
      statCard(dashboard.total_people, "Synthetic people" + (currentDistrict ? " in " + currentDistrict : " (all districts)")) +
      statCard(dashboard.total_enrolments, "Total enrolments") +
      statCard(dashboard.total_schemes, "Schemes in registry") +
      statCard(dashboard.duplicate_pairs, "Duplicate pairs flagged", dashboard.duplicate_pairs > 0) +
      statCard(dashboard.inclusion_gaps, "Inclusion gaps (eligible, not enrolled)", dashboard.inclusion_gaps > 0);
    // 3D map: height = enrolment volume per district (all-district counts).
    const all = await api("/api/dashboard");
    const counts = all.dashboard.by_district;
    const max = Math.max(1, ...Object.values(counts));
    const stage = $("map-3d");
    stage.innerHTML = "";
    Object.entries(counts).forEach(([district, count]) => {
      const block = document.createElement("button");
      block.type = "button";
      block.className = "district-block";
      block.setAttribute("aria-pressed", String(currentDistrict === district));
      block.setAttribute("aria-label", district + ": " + count + " enrolments. Activate to filter the dashboard.");
      block.style.setProperty("--extrude", (lowMotion ? 0 : 6 + Math.round((count / max) * 42)) + "px");
      block.innerHTML = '<span class="face">' + esc(district) +
        '<span class="count num">' + count + "</span></span>";
      block.addEventListener("click", () => {
        // Guard: a pointer press already selected this district on pointerup
        // (see the stage pointerup handler below) — ignore the duplicate
        // click that follows it. Keyboard activation has no pointerup, so
        // Enter/Space still reach here.
        if (lastPointerSelectDistrict === district &&
            Date.now() - lastPointerSelectAt < 250) return;
        selectDistrict(district);
      });
      stage.appendChild(block);
    });
    // 2D fallback list (same data, same action).
    const list = $("map-2d");
    list.innerHTML = "";
    Object.entries(counts).forEach(([district, count]) => {
      const li = document.createElement("li");
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = district + " (" + count + ")";
      b.setAttribute("aria-pressed", String(currentDistrict === district));
      b.addEventListener("click", () => selectDistrict(district));
      li.appendChild(b);
      list.appendChild(li);
    });
    $("map-filter-note").innerHTML = currentDistrict
      ? "Showing: <b>" + esc(currentDistrict) + "</b> — click the same district again, or Clear district filter, to show all."
      : "Showing: <b>all 13 districts</b>.";
    const rows = Object.entries(dashboard.by_scheme)
      .map(([name, n]) => "<tr><td>" + esc(name) + '</td><td class="num">' + n + "</td></tr>").join("");
    $("dash-by-scheme").innerHTML = rows
      ? '<div class="table-scroll"><table><thead><tr><th>Scheme</th><th>Enrolments</th></tr></thead><tbody>' + rows + "</tbody></table></div>"
      : '<p class="empty">No enrolments in this district yet (synthetic data).</p>';
    lastGaps = dashboard.gaps || [];
    $("dash-gaps").innerHTML = lastGaps.length
      ? '<div class="table-scroll"><table><thead><tr><th>Person</th><th>District</th><th>Eligible for (not enrolled)</th><th></th></tr></thead><tbody>' +
        lastGaps.map((g) => "<tr><td>" + esc(g.person_name) + " <span class='hint'>" + esc(g.person_id) + "</span></td><td>" +
          esc(g.district) + "</td><td>" + esc(g.scheme_name) + "</td><td>" +
          '<button type="button" class="btn secondary" data-trace-person="' + esc(g.person_id) +
          '" data-trace-scheme="' + esc(g.scheme_id) + '">Trace it</button></td></tr>').join("") +
        "</tbody></table></div>"
      : '<p class="empty">No inclusion gaps in this view — everyone eligible is enrolled (synthetic data).</p>';
    // "Trace it" buttons jump to the trace panel with both selects pre-filled.
    document.querySelectorAll("#dash-gaps [data-trace-person]").forEach((b) => {
      b.addEventListener("click", () => {
        $("trace-person").value = b.dataset.tracePerson;
        $("trace-scheme").value = b.dataset.traceScheme;
        document.querySelector('nav.tabs button[data-panel="trace"]').click();
        runTrace();
      });
    });
  } catch (err) { showError(errEl, err); }
}

function selectDistrict(district) {
  currentDistrict = (currentDistrict === district) ? null : district;
  loadDashboard();
}
$("btn-clear-district").addEventListener("click", () => { currentDistrict = null; loadDashboard(); });

$("btn-export-gaps").addEventListener("click", () => {
  const rows = [["person_id", "person_name", "district", "scheme_id", "scheme_name"]];
  lastGaps.forEach((g) => rows.push([g.person_id, g.person_name, g.district, g.scheme_id, g.scheme_name]));
  const csv = rows.map((r) => r.map((c) => '"' + String(c).replace(/"/g, '""') + '"').join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "yojanasetu-inclusion-gaps.csv";
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});

/* Arrow-key navigation across the 3D map blocks; Alt+Arrow rotates the
   scene ±20° instead of moving focus (constitution §9). Plain arrows keep
   the QA-verified focus behaviour; Alt+arrows are the rotation keys. */
$("map-3d").addEventListener("keydown", (e) => {
  if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
  if (e.altKey) {
    if (lowMotion || flatMap) return; // no scene to rotate in the flat view
    e.preventDefault();
    setRotation(mapRotation + (e.key === "ArrowRight" ? 5 : -5));
    return;
  }
  const blocks = [...$("map-3d").querySelectorAll(".district-block")];
  const i = blocks.indexOf(document.activeElement);
  if (i < 0) return;
  e.preventDefault();
  const next = blocks[(i + (e.key === "ArrowRight" ? 1 : -1) + blocks.length) % blocks.length];
  next.focus();
});

/* ---- Lookup ---- */
function personCard(p) {
  const enrol = p.enrolments.length
    ? '<div class="table-scroll"><table><thead><tr><th>Scheme</th><th>Record ID</th><th>Source department</th><th>Enrolled</th></tr></thead><tbody>' +
      p.enrolments.map((e) => "<tr><td>" + esc(e.scheme_name) + "</td><td>" + esc(e.record_id) +
        "</td><td>" + esc(e.department) + "</td><td class='num'>" + esc(e.enrolled_on) + "</td></tr>").join("") +
      "</tbody></table></div>"
    : '<p class="empty">No enrolments on record — check the Eligibility Trace for schemes this person may be eligible for.</p>';
  return '<article class="detail"><h3>' + esc(p.name) + ' <span class="hint">' + esc(p.id) + "</span></h3>" +
    '<div class="kv"><span><b>DOB</b> <span class="num">' + esc(p.dob) + "</span></span>" +
    "<span><b>District</b> " + esc(p.district) + "</span>" +
    "<span><b>Age</b> <span class='num'>" + esc(p.age) + "</span></span>" +
    "<span><b>Gender</b> " + esc(p.gender) + "</span>" +
    "<span><b>Income</b> " + inr(p.annual_income) + "/yr</span>" +
    "<span><b>Occupation</b> " + esc(p.occupation) + "</span>" +
    "<span><b>Family ref</b> " + esc(p.family_ref) + "</span>" +
    "<span><b>Flags</b> " + esc(p.flags.join(", ") || "—") + "</span></div>" +
    "<h3>Scheme participation (" + p.enrolments.length + ")</h3>" + enrol + "</article>";
}
$("lookup-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = $("lookup-q").value.trim();
  const errEl = $("lookup-error"), out = $("lookup-results");
  clearError(errEl);
  if (!q) { out.innerHTML = '<p class="empty">Type a synthetic ID, name or district first.</p>'; return; }
  out.innerHTML = "<p>Searching synthetic records…</p>";
  try {
    const { results } = await api("/api/beneficiaries?q=" + encodeURIComponent(q));
    out.innerHTML = results.length
      ? "<p>" + results.length + " result(s) for “" + esc(q) + "”.</p>" + results.map(personCard).join("")
      : '<p class="empty">No synthetic person matches “' + esc(q) + '”. Try YS-1001, Gita Devi, or Dehradun.</p>';
  } catch (err) { out.innerHTML = ""; showError(errEl, err); }
});
$("btn-lookup-clear").addEventListener("click", () => {
  $("lookup-q").value = ""; $("lookup-results").innerHTML = ""; clearError($("lookup-error"));
  $("lookup-q").focus();
});

/* ---- Duplicates ---- */
function chipFor(v) {
  return v === "DUPLICATE" ? '<span class="chip no">Duplicate</span>'
    : v === "LIKELY DUPLICATE" ? '<span class="chip warn">Likely duplicate</span>'
    : '<span class="chip info">Review</span>';
}
async function loadDuplicates() {
  const errEl = $("dup-error"), out = $("dup-results");
  clearError(errEl);
  out.innerHTML = "<p>Checking synthetic registers…</p>";
  try {
    const { pairs } = await api("/api/duplicates");
    const filter = $("dup-filter").value;
    const shown = filter === "all" ? pairs : pairs.filter((p) => p.verdict === filter);
    out.innerHTML = shown.length
      ? "<p>" + shown.length + " pair(s) flagged" + (filter === "all" ? " (all severities)" : " — " + esc(filter)) + ".</p>" +
        shown.map((p) => '<article class="card"><h4>' + esc(p.name_a) + " ↔ " + esc(p.name_b) + "</h4>" +
          "<p>" + chipFor(p.verdict) + ' <b class="num">Confidence ' + p.confidence.toFixed(2) + "</b></p>" +
          "<p class='hint'>" + esc(p.person_a) + " · " + esc(p.person_b) + "</p>" +
          '<ul class="evidence">' + p.evidence.map((e) => "<li>" + (e.match ? "✓ " : "✗ ") +
            "<b>" + esc(e.field) + ":</b> " + esc(e.detail) + "</li>").join("") + "</ul>" +
          "<p><b>Suggested action:</b> " + esc(p.suggested_action) + "</p></article>").join("")
      : '<p class="empty">No pairs at this severity in the synthetic data.</p>';
    out.className = "cards";
  } catch (err) { out.innerHTML = ""; showError(errEl, err); }
}
$("dup-filter").addEventListener("change", loadDuplicates);
$("btn-dup-refresh").addEventListener("click", loadDuplicates);

/* ---- Eligibility trace ---- */
async function loadTraceOptions() {
  try {
    const schemes = await api("/api/schemes");
    const people = await api("/api/beneficiaries?q=a"); // 'a' matches most names; top-up below
    const allPeople = await api("/api/beneficiaries?q=e");
    const seen = new Map();
    [...people.results, ...allPeople.results].forEach((p) => seen.set(p.id, p));
    // Ensure every seeded person is listed even if the two queries miss one.
    const extra = await api("/api/beneficiaries?q=YS-10");
    extra.results.forEach((p) => seen.set(p.id, p));
    $("trace-person").innerHTML = [...seen.values()].sort((a, b) => a.id.localeCompare(b.id))
      .map((p) => '<option value="' + esc(p.id) + '">' + esc(p.id) + " — " + esc(p.name) + " (" + esc(p.district) + ")</option>").join("");
    $("trace-scheme").innerHTML = schemes.schemes
      .map((s) => '<option value="' + esc(s.id) + '">' + esc(s.name) + "</option>").join("");
  } catch (err) { showError($("trace-error"), err); }
}
async function runTrace() {
  const errEl = $("trace-error"), out = $("trace-result");
  clearError(errEl);
  const person = $("trace-person").value, scheme = $("trace-scheme").value;
  if (!person || !scheme) { out.innerHTML = '<p class="empty">Pick a person and a scheme first.</p>'; return; }
  out.innerHTML = "<p>Running rule trace…</p>";
  try {
    const { trace } = await api("/api/trace?person=" + encodeURIComponent(person) +
      "&scheme=" + encodeURIComponent(scheme));
    const chip = trace.verdict === "ELIGIBLE" ? '<span class="chip ok">Eligible</span>'
      : trace.verdict === "NOT ELIGIBLE" ? '<span class="chip no">Not eligible</span>'
      : '<span class="chip info">Needs review</span>';
    out.innerHTML = '<article class="detail"><h3>' + esc(trace.person_name) + " — " + esc(trace.scheme_name) + "</h3>" +
      "<p>Verdict: " + chip +
      (trace.already_enrolled ? ' <span class="chip info">Already enrolled</span>' : ' <span class="chip warn">Not enrolled</span>') + "</p>" +
      '<div class="table-scroll"><table><thead><tr><th>Rule</th><th>Result</th><th>Detail</th><th>Source</th></tr></thead><tbody>' +
      trace.checks.map((c) => "<tr><td>" + esc(c.label) + "</td><td>" +
        (c.passed === null ? '<span class="chip info">Unknown</span>' : c.passed ? '<span class="chip ok">Pass</span>' : '<span class="chip no">Fail</span>') +
        "</td><td>" + esc(c.detail) + "</td><td>" + esc(c.source) + "</td></tr>").join("") +
      "</tbody></table></div><p class='src'>Scheme criteria source: " + esc(trace.scheme_source) + "</p></article>";
  } catch (err) { out.innerHTML = ""; showError(errEl, err); }
}
$("trace-form").addEventListener("submit", (e) => { e.preventDefault(); runTrace(); });
$("btn-trace-clear").addEventListener("click", () => {
  $("trace-result").innerHTML = ""; clearError($("trace-error"));
});

/* ---- Scheme registry ---- */
async function loadRegistry(q) {
  const errEl = $("registry-error"), out = $("registry-results");
  clearError(errEl);
  out.innerHTML = "<p>Loading registry…</p>";
  try {
    const { schemes } = await api("/api/schemes?q=" + encodeURIComponent(q || ""));
    const cat = $("registry-category").value;
    const shown = cat ? schemes.filter((s) => s.category === cat) : schemes;
    out.innerHTML = shown.length ? shown.map((s) =>
      '<article class="card' + (s.representative ? " rep" : "") + '"><p class="tag">' + esc(s.category) +
      (s.representative ? ' · Representative' : "") + "</p><h4>" + esc(s.name) + "</h4>" +
      "<p>" + esc(s.blurb) + "</p><p><b>Benefit:</b> " + esc(s.benefit) + "</p>" +
      "<p><b>Department:</b> " + esc(s.department) + "</p>" +
      '<p class="src">Source: ' + esc(s.source) + "</p></article>").join("")
      : '<p class="empty">No scheme matches that search.</p>';
  } catch (err) { out.innerHTML = ""; showError(errEl, err); }
}
$("registry-form").addEventListener("submit", (e) => { e.preventDefault(); loadRegistry($("registry-q").value.trim()); });
$("registry-category").addEventListener("change", () => loadRegistry($("registry-q").value.trim()));
$("btn-registry-clear").addEventListener("click", () => {
  $("registry-q").value = ""; $("registry-category").value = ""; loadRegistry("");
});

/* ---- Init: fill category filter, then load all sections ---- */
(async function init() {
  try {
    const { schemes } = await api("/api/schemes");
    const cats = [...new Set(schemes.map((s) => s.category))].sort();
    cats.forEach((c) => {
      const o = document.createElement("option");
      o.value = c; o.textContent = c;
      $("registry-category").appendChild(o);
    });
  } catch (err) { /* registry section shows its own error on load */ }
  applyMapView();
  loadDashboard();
  loadDuplicates();
  loadTraceOptions();
  loadRegistry("");
})();
