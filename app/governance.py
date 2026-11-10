"""YojanaSetu governance engine — deterministic, explainable, stdlib only.

Three engines, all pure functions over the synthetic data in data.py:
  1. Duplicate detection — normalised name + DOB + district + family-ref
     overlap, with a confidence score and per-field evidence.
  2. Eligibility trace — rule-by-rule PASS/FAIL/UNKNOWN per scheme, each
     check citing the source record it was read from.
  3. Dashboard / inclusion gaps — counts + eligible-but-not-enrolled.

Verdicts: ELIGIBLE / NOT ELIGIBLE / NEEDS REVIEW (missing data).
No ML, no randomness, no network. Same input -> same output, always.
"""
from __future__ import annotations

import re
from collections import Counter

from app.data import BENEFICIARIES, DISTRICTS, SCHEMES, SCHEME_BY_ID

# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------
def normalise_name(name: str) -> str:
    """Lower-case, strip punctuation, collapse spaces, drop honorifics."""
    t = (name or "").lower()
    t = re.sub(r"[^a-z ]", " ", t)
    # Honorifics/suffixes are dropped from BOTH sides, so two spellings of
    # the same name still match; distinct first names still differ.
    words = [w for w in t.split() if w not in ("shri", "smt", "mr", "mrs", "miss", "kumari", "devi", "lal")]
    return " ".join(words)


def _name_tokens(name: str) -> set:
    return set(normalise_name(name).split())


def name_similarity(a: str, b: str) -> float:
    """Jaccard over name tokens; 1.0 = identical token set."""
    ta, tb = _name_tokens(a), _name_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def match_pair(a: dict, b: dict) -> dict:
    """Score one pair. Returns evidence dict with confidence 0..1."""
    evidence = []
    score = 0.0
    sim = name_similarity(a["name"], b["name"])
    if sim == 1.0:
        score += 0.45
        evidence.append({"field": "name", "match": True,
                         "detail": f"Name identical: '{a['name']}'"})
    elif sim >= 0.6:
        score += 0.30
        evidence.append({"field": "name", "match": True,
                         "detail": f"Name variant: '{a['name']}' vs '{b['name']}' "
                                   f"(token overlap {sim:.2f})"})
    else:
        evidence.append({"field": "name", "match": False,
                         "detail": f"Names differ: '{a['name']}' vs '{b['name']}'"})
    if a["dob"] == b["dob"]:
        score += 0.30
        evidence.append({"field": "date of birth", "match": True,
                         "detail": f"DOB identical: {a['dob']}"})
    else:
        evidence.append({"field": "date of birth", "match": False,
                         "detail": f"DOB differs: {a['dob']} vs {b['dob']}"})
    if a["district"] == b["district"]:
        score += 0.15
        evidence.append({"field": "district", "match": True,
                         "detail": f"District identical: {a['district']}"})
    else:
        evidence.append({"field": "district", "match": False,
                         "detail": f"District differs: {a['district']} vs {b['district']}"})
    if a.get("family_ref") and a["family_ref"] == b.get("family_ref"):
        score += 0.10
        evidence.append({"field": "family reference", "match": True,
                         "detail": f"Same synthetic family ref: {a['family_ref']}"})
    else:
        evidence.append({"field": "family reference", "match": False,
                         "detail": "Family refs differ or missing"})
    score = min(round(score, 2), 1.0)
    if score >= 0.90:
        verdict, action = "DUPLICATE", "Merge records — keep the earliest enrolment, retire the later ID, keep both source citations."
    elif score >= 0.70:
        verdict, action = "LIKELY DUPLICATE", "Hold for officer review — verify with the person before merging; do not auto-merge."
    elif score >= 0.50:
        verdict, action = "REVIEW", "Possible relative / namesake — check DOB and family ref; no action unless confirmed."
    else:
        verdict, action = "NO MATCH", "No action — distinct people."
    return {"person_a": a["id"], "person_b": b["id"],
            "name_a": a["name"], "name_b": b["name"],
            "confidence": score, "verdict": verdict,
            "suggested_action": action, "evidence": evidence}


def find_duplicates(threshold: float = 0.50) -> list:
    """All pairs at or above threshold, highest confidence first."""
    out = []
    for i, a in enumerate(BENEFICIARIES):
        for b in BENEFICIARIES[i + 1:]:
            m = match_pair(a, b)
            if m["confidence"] >= threshold:
                out.append(m)
    out.sort(key=lambda m: -m["confidence"])
    return out


# ---------------------------------------------------------------------------
# Eligibility trace (adapted from SchemeSathi's evaluate(); same rule fields)
# ---------------------------------------------------------------------------
def _check(label, passed, detail, source):
    return {"label": label, "passed": passed, "detail": detail, "source": source}


def trace_eligibility(person: dict, scheme: dict) -> dict:
    """Rule-by-rule trace for one person + one scheme.

    Each check cites its source: the synthetic profile record
    (YS-####) or the specific enrolment record where relevant.
    """
    src = f"Synthetic profile {person['id']} ({person['name']}, {person['district']})"
    checks = []
    age, income = person.get("age"), person.get("annual_income")
    gender, occ = person.get("gender"), person.get("occupation")
    flags = person.get("flags") or set()

    if scheme.get("min_age") is not None:
        checks.append(_check(f"Age {scheme['min_age']}+ years",
                             None if age is None else age >= scheme["min_age"],
                             "Age not recorded" if age is None else f"Age: {age}",
                             src))
    if scheme.get("max_age") is not None:
        checks.append(_check(f"Age up to {scheme['max_age']} years",
                             None if age is None else age <= scheme["max_age"],
                             "Age not recorded" if age is None else f"Age: {age}",
                             src))
    if scheme.get("max_income") is not None:
        checks.append(_check(f"Family income up to ₹{scheme['max_income']:,}/yr",
                             None if income is None else income <= scheme["max_income"],
                             "Income not recorded" if income is None else f"Income: ₹{income:,}",
                             src))
    if scheme.get("genders"):
        checks.append(_check("For %s applicants" % "/".join(sorted(scheme["genders"])),
                             None if gender is None else gender in scheme["genders"],
                             "Gender not recorded" if gender is None else f"Gender: {gender}",
                             src))
    if scheme.get("occupations"):
        checks.append(_check("For: %s" % ", ".join(sorted(scheme["occupations"])),
                             None if not occ else occ in scheme["occupations"],
                             "Occupation not recorded" if not occ else f"Occupation: {occ}",
                             src))
    for flag in sorted(scheme.get("requires_all") or []):
        checks.append(_check("Must have: %s" % flag.replace("_", " "),
                             flag in flags,
                             "Present in profile" if flag in flags else "Not present in profile",
                             src))
    if scheme.get("requires_any"):
        opts = sorted(scheme["requires_any"])
        hit = [f for f in opts if f in flags]
        checks.append(_check("Needs at least one of: %s" % ", ".join(f.replace("_", " ") for f in opts),
                             bool(hit),
                             ("Has: %s" % ", ".join(hit)) if hit else "None present",
                             src))
    for flag in sorted(scheme.get("excludes") or []):
        checks.append(_check("Must NOT be: %s" % flag.replace("_", " "),
                             flag not in flags,
                             "Applies — disqualifying" if flag in flags else "Does not apply",
                             src))
    failed = [c for c in checks if c["passed"] is False]
    unknown = [c for c in checks if c["passed"] is None]
    if unknown and not failed:
        verdict = "NEEDS REVIEW"
    elif not failed:
        verdict = "ELIGIBLE"
    else:
        verdict = "NOT ELIGIBLE"
    enrolled = any(e["scheme"] == scheme["id"] for e in person.get("enrolments", []))
    return {"person_id": person["id"], "person_name": person["name"],
            "scheme_id": scheme["id"], "scheme_name": scheme["name"],
            "verdict": verdict, "checks": checks,
            "already_enrolled": enrolled,
            "scheme_source": scheme.get("source", "")}


# ---------------------------------------------------------------------------
# Search / registry / dashboard
# ---------------------------------------------------------------------------
def search_beneficiaries(query: str) -> list:
    q = (query or "").strip().lower()
    if not q:
        return []
    out = []
    for p in BENEFICIARIES:
        if (q in p["id"].lower() or q in p["name"].lower()
                or q in p["district"].lower() or q in p["family_ref"].lower()):
            out.append(p)
    return out


def search_schemes(query: str) -> list:
    q = (query or "").strip().lower()
    if not q:
        return list(SCHEMES)
    return [s for s in SCHEMES
            if q in s["id"] or q in s["name"].lower()
            or q in s["category"].lower() or q in s["ministry"].lower()
            or q in s["department"].lower()]


def public_person(p: dict) -> dict:
    return {"id": p["id"], "name": p["name"], "dob": p["dob"],
            "district": p["district"], "gender": p["gender"], "age": p["age"],
            "annual_income": p["annual_income"], "occupation": p["occupation"],
            "flags": sorted(p["flags"]), "family_ref": p["family_ref"],
            "enrolments": [
                {**e, "scheme_name": SCHEME_BY_ID[e["scheme"]]["name"]
                 if e["scheme"] in SCHEME_BY_ID else e["scheme"]}
                for e in p["enrolments"]]}


def dashboard(district: str | None = None) -> dict:
    people = [p for p in BENEFICIARIES if not district or p["district"] == district]
    enrolments = [e for p in people for e in p["enrolments"]]
    by_district = Counter(p["district"] for p in BENEFICIARIES)
    # by_scheme follows the SAME district filter as total_people/total_enrolments
    # and gaps: it counts only the (filtered) people's enrolments, so a filtered
    # dashboard's scheme table sums to total_enrolments, never the global 25.
    by_scheme = Counter(e["scheme"] for p in people for e in p["enrolments"])
    dups = find_duplicates()
    # Inclusion gaps: eligible but not enrolled (all people, all schemes).
    gaps = []
    for p in people:
        enrolled_ids = {e["scheme"] for e in p["enrolments"]}
        for s in SCHEMES:
            if s["id"] in enrolled_ids:
                continue
            t = trace_eligibility(p, s)
            if t["verdict"] == "ELIGIBLE":
                gaps.append({"person_id": p["id"], "person_name": p["name"],
                             "district": p["district"], "scheme_id": s["id"],
                             "scheme_name": s["name"]})
    return {
        "district_filter": district,
        "total_people": len(people),
        "total_enrolments": len(enrolments),
        "total_schemes": len(SCHEMES),
        "districts_covered": len({p["district"] for p in people}),
        "by_district": {d: by_district.get(d, 0) for d in DISTRICTS},
        "by_scheme": {SCHEME_BY_ID[k]["name"]: v for k, v in sorted(by_scheme.items())},
        "duplicate_pairs": len(dups),
        "duplicate_confirmed": len([d for d in dups if d["verdict"] == "DUPLICATE"]),
        "duplicate_likely": len([d for d in dups if d["verdict"] == "LIKELY DUPLICATE"]),
        "inclusion_gaps": len(gaps),
        "gaps": gaps,
    }
