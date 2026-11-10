"""Unit tests: duplicate matching, eligibility trace, registry search."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data import BENEFICIARIES, PERSON_BY_ID, SCHEMES, SCHEME_BY_ID
from app.governance import (dashboard, find_duplicates, match_pair,
                            normalise_name, search_beneficiaries,
                            search_schemes, trace_eligibility)


class TestDuplicates(unittest.TestCase):
    def test_exact_duplicate_pair_flagged(self):
        a, b = PERSON_BY_ID["YS-1001"], PERSON_BY_ID["YS-1002"]
        m = match_pair(a, b)
        self.assertEqual(m["verdict"], "DUPLICATE")
        self.assertGreaterEqual(m["confidence"], 0.90)
        fields = {e["field"]: e["match"] for e in m["evidence"]}
        self.assertTrue(fields["name"] and fields["date of birth"]
                        and fields["district"] and fields["family reference"])
        self.assertIn("Merge", m["suggested_action"])

    def test_near_miss_name_variant_is_likely_duplicate(self):
        a, b = PERSON_BY_ID["YS-1003"], PERSON_BY_ID["YS-1004"]
        m = match_pair(a, b)
        self.assertEqual(m["verdict"], "LIKELY DUPLICATE")
        self.assertGreaterEqual(m["confidence"], 0.70)
        self.assertLess(m["confidence"], 0.90)
        self.assertIn("review", m["suggested_action"].lower())

    def test_same_name_different_dob_is_not_a_duplicate(self):
        a, b = PERSON_BY_ID["YS-1005"], PERSON_BY_ID["YS-1006"]
        m = match_pair(a, b)
        self.assertEqual(m["verdict"], "REVIEW")
        self.assertLess(m["confidence"], 0.70)

    def test_unrelated_people_are_no_match(self):
        a, b = PERSON_BY_ID["YS-1007"], PERSON_BY_ID["YS-1013"]
        m = match_pair(a, b)
        self.assertEqual(m["verdict"], "NO MATCH")
        self.assertLess(m["confidence"], 0.50)

    def test_find_duplicates_includes_seeded_pairs(self):
        pairs = find_duplicates()
        keys = {(p["person_a"], p["person_b"]) for p in pairs}
        self.assertIn(("YS-1001", "YS-1002"), keys)
        self.assertIn(("YS-1003", "YS-1004"), keys)
        self.assertTrue(all(p["confidence"] >= 0.50 for p in pairs))
        # Highest confidence first.
        confs = [p["confidence"] for p in pairs]
        self.assertEqual(confs, sorted(confs, reverse=True))

    def test_name_normalisation_is_case_and_punctuation_insensitive(self):
        self.assertEqual(normalise_name("Gita Devi"), normalise_name("gita  devi."))
        self.assertEqual(normalise_name("Ramesh Singh"), normalise_name("RAMESH SINGH"))


class TestEligibilityTrace(unittest.TestCase):
    def test_farmer_with_land_is_eligible_for_pm_kisan(self):
        t = trace_eligibility(PERSON_BY_ID["YS-1001"], SCHEME_BY_ID["pm-kisan"])
        self.assertEqual(t["verdict"], "ELIGIBLE")
        self.assertTrue(all(c["passed"] for c in t["checks"]))
        self.assertTrue(all(c["source"] for c in t["checks"]))

    def test_vendor_is_not_eligible_for_pm_kisan(self):
        t = trace_eligibility(PERSON_BY_ID["YS-1003"], SCHEME_BY_ID["pm-kisan"])
        self.assertEqual(t["verdict"], "NOT ELIGIBLE")
        self.assertTrue(any(c["passed"] is False for c in t["checks"]))

    def test_senior_with_bpl_is_eligible_for_pmjay(self):
        t = trace_eligibility(PERSON_BY_ID["YS-1007"], SCHEME_BY_ID["pmjay"])
        self.assertEqual(t["verdict"], "ELIGIBLE")

    def test_girl_child_under_10_is_eligible_for_sukanya(self):
        t = trace_eligibility(PERSON_BY_ID["YS-1008"], SCHEME_BY_ID["sukanya"])
        self.assertEqual(t["verdict"], "ELIGIBLE")

    def test_adult_is_not_eligible_for_sukanya(self):
        t = trace_eligibility(PERSON_BY_ID["YS-1010"], SCHEME_BY_ID["sukanya"])
        self.assertEqual(t["verdict"], "NOT ELIGIBLE")

    def test_trace_reports_already_enrolled(self):
        t = trace_eligibility(PERSON_BY_ID["YS-1001"], SCHEME_BY_ID["pm-kisan"])
        self.assertTrue(t["already_enrolled"])
        t2 = trace_eligibility(PERSON_BY_ID["YS-1001"], SCHEME_BY_ID["pmjay"])
        self.assertFalse(t2["already_enrolled"])

    def test_every_check_cites_a_source(self):
        for scheme in SCHEMES:
            t = trace_eligibility(PERSON_BY_ID["YS-1010"], scheme)
            self.assertTrue(t["checks"])
            for c in t["checks"]:
                self.assertIn("Synthetic profile", c["source"])
            self.assertIn(t["verdict"], ("ELIGIBLE", "NOT ELIGIBLE", "NEEDS REVIEW"))


class TestRegistryAndSearch(unittest.TestCase):
    def test_registry_has_nine_schemes(self):
        self.assertEqual(len(SCHEMES), 9)

    def test_scheme_search_by_name(self):
        self.assertEqual([s["id"] for s in search_schemes("kisan")], ["pm-kisan"])

    def test_scheme_search_by_category(self):
        self.assertGreaterEqual(len(search_schemes("health")), 1)

    def test_scheme_search_empty_returns_all(self):
        self.assertEqual(len(search_schemes("")), len(SCHEMES))

    def test_beneficiary_search_by_id(self):
        self.assertEqual([p["id"] for p in search_beneficiaries("YS-1001")], ["YS-1001"])

    def test_beneficiary_search_by_name_finds_both_gitas(self):
        ids = {p["id"] for p in search_beneficiaries("gita devi")}
        self.assertEqual(ids, {"YS-1001", "YS-1002"})

    def test_beneficiary_search_by_district(self):
        self.assertTrue(all(p["district"] == "Dehradun"
                            for p in search_beneficiaries("dehradun")))
        self.assertGreaterEqual(len(search_beneficiaries("dehradun")), 2)

    def test_beneficiary_search_empty_returns_nothing(self):
        self.assertEqual(search_beneficiaries(""), [])
        self.assertEqual(search_beneficiaries("zzzz-no-such-name"), [])


class TestDashboard(unittest.TestCase):
    def test_dashboard_totals(self):
        d = dashboard()
        self.assertEqual(d["total_people"], len(BENEFICIARIES))
        self.assertEqual(d["total_schemes"], len(SCHEMES))
        self.assertEqual(d["districts_covered"], 13)
        self.assertEqual(len(d["by_district"]), 13)
        self.assertEqual(d["total_enrolments"],
                         sum(len(p["enrolments"]) for p in BENEFICIARIES))

    def test_dashboard_district_filter(self):
        d = dashboard("Dehradun")
        self.assertEqual(d["district_filter"], "Dehradun")
        dehradun_people = [p for p in BENEFICIARIES if p["district"] == "Dehradun"]
        self.assertEqual(d["total_people"], len(dehradun_people))
        self.assertEqual(d["total_people"], 4)
        self.assertTrue(all(g["district"] == "Dehradun" for g in d["gaps"]))
        self.assertLess(d["total_people"], len(BENEFICIARIES))

    def test_dashboard_by_scheme_is_filtered_by_district(self):
        # Gate D F2: /api/dashboard?district=Almora returned 3 people / 3 enrolments
        # but a by_scheme summing to the global 25. The filtered table must sum
        # to the filtered total_enrolments, and count only that district's schemes.
        for district in ("Almora", "Dehradun", "Rudraprayag"):
            d = dashboard(district)
            self.assertEqual(sum(d["by_scheme"].values()), d["total_enrolments"],
                             f"by_scheme sum != total_enrolments for {district}")
            expected = {}
            for p in BENEFICIARIES:
                if p["district"] != district:
                    continue
                for e in p["enrolments"]:
                    expected[SCHEME_BY_ID[e["scheme"]]["name"]] = \
                        expected.get(SCHEME_BY_ID[e["scheme"]]["name"], 0) + 1
            self.assertEqual(d["by_scheme"], expected)
        self.assertEqual(dashboard("Almora")["total_people"], 3)
        self.assertEqual(dashboard("Almora")["total_enrolments"], 3)
        # Unfiltered table is unchanged (global total).
        self.assertEqual(sum(dashboard()["by_scheme"].values()),
                         dashboard()["total_enrolments"])

    def test_inclusion_gap_case_exists(self):
        d = dashboard()
        self.assertGreater(d["inclusion_gaps"], 0)
        gap = next(g for g in d["gaps"] if g["person_id"] == "YS-1021")
        self.assertEqual(gap["scheme_id"], "pmjay")


if __name__ == "__main__":
    unittest.main()
