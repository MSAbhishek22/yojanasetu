"""YojanaSetu — synthetic data layer (UKIS 2026).

ALL data here is SYNTHETIC — fictional people invented for the demo.
No real citizen data is used, stored, or fetched. Every record carries a
synthetic ID (YS-####) and a stated source department *within the fiction*:
the "source" is which (fictional) departmental register the record came
from, so the holistic view can cite it — it is not a real government source.

Scheme rules are a curated snapshot of widely published headline criteria
for real national schemes (as in SchemeSathi, Nov 2026). They are NOT an
official source; verify current criteria at myscheme.gov.in before any
real decision. Two schemes are clearly labelled REPRESENTATIVE (state-level
illustrations, not verified official schemes).
"""
from __future__ import annotations

DISTRICTS = [
    "Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun",
    "Haridwar", "Nainital", "Pauri Garhwal", "Pithoragarh",
    "Rudraprayag", "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi",
]

# Rule fields mirror SchemeSathi's engine (reused, honestly adapted):
# min_age, max_age, max_income, genders, occupations, requires_all,
# requires_any, excludes, needs.
SCHEMES = [
    {
        "id": "pm-kisan", "name": "PM-KISAN Samman Nidhi",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "department": "Agriculture Dept, Uttarakhand",
        "category": "Agriculture",
        "benefit": "₹6,000 per year in three instalments",
        "blurb": "Income support for landholding farmer families.",
        "requires_all": ["landholding"], "occupations": {"farmer"},
        "excludes": {"govt_employee", "income_tax_payer"},
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "pmjay", "name": "Ayushman Bharat PM-JAY",
        "ministry": "Ministry of Health & Family Welfare",
        "department": "Health Dept, Uttarakhand",
        "category": "Health",
        "benefit": "Free hospital treatment up to ₹5 lakh per family per year",
        "blurb": "Health cover for poor and vulnerable families; all Indians 70+ covered.",
        "requires_any": ["bpl", "senior70"],
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "pmay-g", "name": "PM Awas Yojana – Gramin",
        "ministry": "Ministry of Rural Development",
        "department": "Rural Development Dept, Uttarakhand",
        "category": "Housing",
        "benefit": "₹1.20 lakh assistance to build a pucca house",
        "blurb": "A pucca house for rural families in kutcha or dilapidated houses.",
        "requires_all": ["rural", "kutcha_house"],
        "excludes": {"pucca_house", "govt_employee", "income_tax_payer"},
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "pmay-u", "name": "PM Awas Yojana – Urban 2.0",
        "ministry": "Ministry of Housing & Urban Affairs",
        "department": "Urban Development Dept, Uttarakhand",
        "category": "Housing",
        "benefit": "Interest subsidy on home loans for EWS / LIG / MIG first homes",
        "blurb": "Interest subsidy for a first urban home.",
        "max_income": 1800000,
        "requires_all": ["urban", "first_house"], "excludes": {"pucca_house"},
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "ujjwala", "name": "PM Ujjwala Yojana 2.0",
        "ministry": "Ministry of Petroleum & Natural Gas",
        "department": "Food & Civil Supplies Dept, Uttarakhand",
        "category": "Women & Child",
        "benefit": "Free LPG connection (deposit-free) + first refill and stove support",
        "blurb": "Clean cooking fuel for adult women in households without LPG.",
        "min_age": 18, "genders": {"female"}, "requires_all": ["no_lpg"],
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "sukanya", "name": "Sukanya Samriddhi Yojana",
        "ministry": "Ministry of Finance",
        "department": "Women & Child Development Dept, Uttarakhand",
        "category": "Women & Child",
        "benefit": "High-interest savings account for a girl child (matures at 21)",
        "blurb": "Long-term savings for a daughter's education and marriage.",
        "max_age": 10, "genders": {"female"}, "requires_all": ["girl_child"],
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "post-matric-sc", "name": "Post-Matric Scholarship for SC Students",
        "ministry": "Ministry of Social Justice & Empowerment",
        "department": "Social Welfare Dept, Uttarakhand",
        "category": "Education",
        "benefit": "Tuition fees + maintenance allowance after Class 10",
        "blurb": "Scholarship for SC students studying beyond Class 10.",
        "max_income": 250000, "occupations": {"student"},
        "requires_all": ["sc_st", "post_matric"],
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "mudra", "name": "PM Mudra Yojana (PMMY)",
        "ministry": "Ministry of Finance",
        "department": "Industries Dept, Uttarakhand",
        "category": "Business",
        "benefit": "Business loans up to ₹10 lakh (Tarun Plus up to ₹20 lakh)",
        "blurb": "Collateral-free loans to start or grow a small business.",
        "min_age": 18, "occupations": {"entrepreneur", "vendor", "artisan", "self_employed"},
        "requires_any": ["business_idea", "existing_business"],
        "source": "myscheme.gov.in — headline criteria snapshot, Nov 2026",
    },
    {
        "id": "uk-hill-transport", "name": "Hill Transport Support (Representative)",
        "ministry": "Representative state-level illustration — NOT a verified official scheme",
        "department": "Transport Dept, Uttarakhand (representative)",
        "category": "Representative",
        "benefit": "Illustrative fare support for hill-district commuters",
        "blurb": "REPRESENTATIVE scheme invented to show how a state scheme would plug into the same governance layer.",
        "min_age": 18, "requires_all": ["rural"],
        "source": "REPRESENTATIVE — invented for this demo; do not treat as a real scheme",
        "representative": True,
    },
]

SCHEME_BY_ID = {s["id"]: s for s in SCHEMES}

# ---------------------------------------------------------------------------
# Synthetic beneficiaries. Fictional people. Fields:
#   id, name, dob (YYYY-MM-DD), district, gender, age, annual_income,
#   occupation, flags, family_ref (synthetic household ref, shared by
#   duplicates), enrolments: [{scheme, record_id, department, enrolled_on}]
# ---------------------------------------------------------------------------
def _p(pid, name, dob, district, gender, age, income, occupation, flags,
       family_ref, enrolments):
    return {"id": pid, "name": name, "dob": dob, "district": district,
            "gender": gender, "age": age, "annual_income": income,
            "occupation": occupation, "flags": set(flags),
            "family_ref": family_ref, "enrolments": enrolments}

def _e(scheme, record_id, department, enrolled_on):
    return {"scheme": scheme, "record_id": record_id,
            "department": department, "enrolled_on": enrolled_on}

BENEFICIARIES = [
    # --- Seeded EXACT duplicate pair: same name + DOB + district, two IDs ---
    _p("YS-1001", "Gita Devi", "1978-04-12", "Pauri Garhwal", "female", 48,
       120000, "farmer", ["landholding", "rural", "kutcha_house", "no_lpg"],
       "FAM-501",
       [_e("pm-kisan", "AGR-PG-2210", "Agriculture Dept", "2024-03-02"),
        _e("ujjwala", "FCS-PG-1187", "Food & Civil Supplies Dept", "2024-05-19")]),
    _p("YS-1002", "Gita Devi", "1978-04-12", "Pauri Garhwal", "female", 48,
       120000, "farmer", ["landholding", "rural", "kutcha_house", "no_lpg"],
       "FAM-501",
       [_e("pmay-g", "RDD-PG-0344", "Rural Development Dept", "2024-06-11")]),
    # --- Seeded NEAR-MISS pair: name variant + same DOB + district ---
    _p("YS-1003", "Ramesh Singh", "1985-09-03", "Dehradun", "male", 41,
       240000, "vendor", ["street_vendor", "urban", "first_house"],
       "FAM-502",
       [_e("mudra", "IND-DDN-5520", "Industries Dept", "2024-02-14")]),
    _p("YS-1004", "Ramesh Kumar Singh", "1985-09-03", "Dehradun", "male", 41,
       240000, "vendor", ["street_vendor", "urban", "first_house"],
       "FAM-502",
       [_e("pmay-u", "UDD-DDN-7712", "Urban Development Dept", "2024-08-30")]),
    # --- Seeded near-miss: same name + district, DIFFERENT DOB (not a dup) ---
    _p("YS-1005", "Sunita Rawat", "1990-01-25", "Nainital", "female", 36,
       90000, "farmer", ["landholding", "rural", "bpl", "no_lpg"], "FAM-503",
       [_e("pm-kisan", "AGR-NTL-3091", "Agriculture Dept", "2023-11-08"),
        _e("pmjay", "HLT-NTL-6620", "Health Dept", "2024-01-22")]),
    _p("YS-1006", "Sunita Rawat", "1996-07-14", "Nainital", "female", 30,
       150000, "student", ["post_matric", "sc_st"], "FAM-504",
       [_e("post-matric-sc", "SW-NTL-4410", "Social Welfare Dept", "2024-07-05")]),
    # --- Remaining synthetic population (one record each) ---
    _p("YS-1007", "Harish Chandra", "1952-11-30", "Almora", "male", 73,
       80000, "farmer", ["landholding", "rural", "bpl", "senior70"], "FAM-505",
       [_e("pmjay", "HLT-ALM-1023", "Health Dept", "2023-09-17")]),
    _p("YS-1008", "Meena Joshi", "2019-05-06", "Almora", "female", 7,
       180000, "student", ["girl_child"], "FAM-506",
       [_e("sukanya", "WCD-ALM-2088", "Women & Child Development Dept", "2024-04-02")]),
    _p("YS-1009", "Anil Kumar", "1998-02-18", "Haridwar", "male", 28,
       420000, "entrepreneur", ["business_idea", "urban"], "FAM-507",
       [_e("mudra", "IND-HDW-3301", "Industries Dept", "2024-03-25")]),
    _p("YS-1010", "Kavita Bisht", "1988-12-09", "Tehri Garhwal", "female", 37,
       110000, "farmer", ["landholding", "rural", "kutcha_house", "bpl", "no_lpg"],
       "FAM-508",
       [_e("pm-kisan", "AGR-TEH-4102", "Agriculture Dept", "2023-12-01"),
        _e("pmay-g", "RDD-TEH-0921", "Rural Development Dept", "2024-05-08")]),
    _p("YS-1011", "Deepak Negi", "2005-08-21", "Chamoli", "male", 21,
       200000, "student", ["post_matric", "sc_st"], "FAM-509",
       [_e("post-matric-sc", "SW-CHM-5514", "Social Welfare Dept", "2024-06-20")]),
    _p("YS-1012", "Laxmi Devi", "1960-03-15", "Uttarkashi", "female", 66,
       95000, "farmer", ["landholding", "rural", "kutcha_house", "no_lpg", "bpl"],
       "FAM-510",
       [_e("pm-kisan", "AGR-UTK-6710", "Agriculture Dept", "2024-01-30")]),
    _p("YS-1013", "Vikram Singh", "1992-06-27", "Udham Singh Nagar", "male", 34,
       600000, "vendor", ["street_vendor", "urban", "existing_business"], "FAM-511",
       [_e("mudra", "IND-USN-8820", "Industries Dept", "2024-04-12")]),
    _p("YS-1014", "Pooja Rani", "1995-10-02", "Rudraprayag", "female", 31,
       140000, "artisan", ["artisan", "rural", "no_lpg"], "FAM-512",
       [_e("ujjwala", "FCS-RDP-2290", "Food & Civil Supplies Dept", "2024-02-09")]),
    _p("YS-1015", "Suresh Prasad", "1975-01-19", "Bageshwar", "male", 51,
       130000, "farmer", ["landholding", "rural", "kutcha_house"], "FAM-513",
       [_e("pm-kisan", "AGR-BAG-1145", "Agriculture Dept", "2023-10-14")]),
    _p("YS-1016", "Rekha Arya", "2008-04-11", "Pithoragarh", "female", 18,
       160000, "student", ["post_matric", "sc_st"], "FAM-514",
       [_e("post-matric-sc", "SW-PTH-7731", "Social Welfare Dept", "2024-07-19")]),
    _p("YS-1017", "Mohan Lal", "1955-08-08", "Champawat", "male", 71,
       70000, "farmer", ["landholding", "rural", "bpl", "senior70"], "FAM-515",
       [_e("pmjay", "HLT-CHP-3056", "Health Dept", "2024-01-11")]),
    _p("YS-1018", "Anita Sharma", "1983-09-29", "Dehradun", "female", 43,
       900000, "entrepreneur", ["business_idea", "urban", "first_house"], "FAM-516",
       [_e("pmay-u", "UDD-DDN-9042", "Urban Development Dept", "2024-09-03")]),
    _p("YS-1019", "Kishan Singh", "1980-05-23", "Haridwar", "male", 46,
       110000, "farmer", ["landholding", "rural", "bpl"], "FAM-517",
       [_e("pm-kisan", "AGR-HDW-5523", "Agriculture Dept", "2024-02-27"),
        _e("pmjay", "HLT-HDW-1180", "Health Dept", "2024-03-15")]),
    _p("YS-1020", "Nisha Kumari", "2018-12-01", "Nainital", "female", 7,
       210000, "student", ["girl_child"], "FAM-518",
       [_e("sukanya", "WCD-NTL-3370", "Women & Child Development Dept", "2024-05-27")]),
    _p("YS-1021", "Bhupesh Tiwari", "1990-11-12", "Dehradun", "male", 36,
       0, "unemployed", ["urban", "bpl"], "FAM-519",
       []),  # enrolled in nothing — inclusion-gap case (eligible for PM-JAY)
    _p("YS-1022", "Kamla Devi", "1962-02-14", "Almora", "female", 64,
       85000, "farmer", ["landholding", "rural", "kutcha_house", "bpl", "no_lpg"],
       "FAM-520",
       [_e("pm-kisan", "AGR-ALM-9901", "Agriculture Dept", "2024-06-02")]),
]

PERSON_BY_ID = {p["id"]: p for p in BENEFICIARIES}
