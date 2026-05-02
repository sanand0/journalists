#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas>=2.2",
#   "pyarrow>=15",
#   "numpy>=1.26",
# ]
# ///
"""Step 2 — Verify all 6 citizen-survey data cards against the raw survey data.

Re-derives every number shown on each card directly from the parquet (or xlsx)
file and compares it to the expected values documented in the card SOPs.

Provider code reference
-----------------------
b1_most / b7_1 (outpatient):
  1=ASHA  2=SubCentre  3=PHC  4=CHC  5=GovernmentHospital
  6=PrivateClinic  7=PrivateHospital  9=AYUSH  10=TradHealer  11=Chemist

c1_most (inpatient — NOTE: different mapping):
  1=ASHA/PHC-type  2=CHC-type  3=GovernmentHospital  4=PrivateClinic  5=PrivateHospital

Usage
-----
    uv run 02_verify_cards.py
    python 02_verify_cards.py [--data PATH.parquet] [--tolerance 0.01] [--card N]

Exit code  0 = all pass,  1 = one or more fail
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DEFAULT_PARQUET = HERE / "FINAL DATA-CITIZEN_SURVEY_ALL_DATA-FINAL_SKS_09.05.2025.parquet"
DEFAULT_PARQUET2 = HERE / "FINAL DATA-CITIZEN_SURVEY_ALL_DATA-FINAL_SKS_09.05.parquet"
DEFAULT_XLSX    = HERE / "FINAL DATA-CITIZEN_SURVEY_ALL_DATA-FINAL_SKS_09.05.xlsx"

GREEN = "\033[32m"; RED = "\033[31m"; YELLOW = "\033[33m"; BOLD = "\033[1m"; RESET = "\033[0m"
PASS = f"{GREEN}PASS{RESET}"; FAIL = f"{RED}FAIL{RESET}"; WARN = f"{YELLOW}WARN{RESET}"

# b1_most (actual provider) codes
# 1=ASHA 2=SubCentre 3=PHC 4=CHC 5=GovernmentHospital
# 6=PrivateClinic 7=PrivateHospital 8=Doctor-MobileVan 9=AYUSH
# 10=TraditionalHealer/Quack 11=Chemist
B1_CODES = {1,2,3,4,5,6,7,8,9,10,11}

# b7_1 (preferred provider) codes — DIFFERENT numbering to b1_most:
# 1=ASHA 2=SubCentre 3=PHC 4=CHC 5=GovernmentHospital
# 6=PrivateClinic 7=PrivateHospital 8=AYUSH 9=TraditionalHealer/Quack 10=Chemist
# (no Doctor-MobileVan in b7_1)
B7_CODES = {1,2,3,4,5,6,7,8,9,10}

# Cross-map: b1_most code → equivalent b7_1 code
B1_TO_B7 = {
    1: 1,   # ASHA
    2: 2,   # SubCentre
    3: 3,   # PHC
    4: 4,   # CHC
    5: 5,   # GovernmentHospital
    6: 6,   # PrivateClinic
    7: 7,   # PrivateHospital
    8: None, # Doctor-MobileVan — no equivalent in b7_1
    9: 8,   # AYUSH
    10: 9,  # TraditionalHealer/Quack
    11: 10, # Chemist
}

# c1_most inpatient provider codes
IP_GOVT    = 3   # Government hospital (inpatient)
IP_PRIVATE = 5   # Private hospital (inpatient)


# ── helpers ────────────────────────────────────────────────────────────────────

def load_data(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_excel(path, sheet_name="Data")


def check(label: str, got: Any, expected: Any, tol: float = 0.01) -> bool:
    if isinstance(expected, float) or isinstance(got, float):
        try:
            diff = abs(float(got) - float(expected))
            ok = diff <= tol
        except (TypeError, ValueError):
            ok = False
        print(f"  {PASS if ok else FAIL}  {label}")
        if not ok:
            print(f"         card says {expected}, data gives {got}  (diff {diff:.4f})")
        return ok
    else:
        ok = (got == expected)
        print(f"  {PASS if ok else FAIL}  {label}")
        if not ok:
            print(f"         card says {expected!r}, data gives {got!r}")
        return ok


# ── Card 01: Quack-to-hospital dream ──────────────────────────────────────────
# b1_most = actual OP provider, b7_1 = preferred next OP provider
# Code 5 = GovernmentHospital, 10 = TradHealer, 11 = Chemist

def verify_card01(df: pd.DataFrame, tol: float) -> list[bool]:
    print(f"\n{BOLD}Card 01 — Quack-to-hospital dream{RESET}")
    r: list[bool] = []

    if "b1_most" not in df.columns:
        print(f"  {WARN}  b1_most not found"); return [False]
    if "b7_1" not in df.columns:
        print(f"  {WARN}  b7_1 not found"); return [False]

    # b1_most and b7_1 use DIFFERENT code numberings — see B1_TO_B7 map above.
    # Compute net change per provider by mapping b1_most codes to b7_1 equivalents.
    # Use only rows where BOTH b1_most and b7_1 are valid (matches old CSV methodology).
    # This excludes b7_1=88 (DNA, n=165) and b7_1=99 (Other, n=1), giving n=41,659.
    both = df[df["b1_most"].isin(B1_CODES) & df["b7_1"].isin(B7_CODES)]
    n_both = len(both)
    r.append(check("OP respondents with valid current+preferred n ≈ 41,659", n_both, 41659, tol=200))

    current   = both["b1_most"].value_counts()
    preferred = both["b7_1"].value_counts()

    def net(b1_code: int) -> int:
        """Net change: preferred (b7_1 code) - current (b1_most code)."""
        b7_code = B1_TO_B7.get(b1_code)
        if b7_code is None:
            return 0
        return int(preferred.get(float(b7_code), 0) - current.get(float(b1_code), 0))

    r.append(check("GovernmentHospital net = +3,402", net(5),  3402,  tol=50))
    r.append(check("TradHealer/Quack net = −1,761",   net(10), -1761, tol=50))
    r.append(check("Chemist net = −1,283",             net(11), -1283, tol=50))

    # Total OP (all valid b1_most, including those without b7_1 preference)
    op_all = df[df["b1_most"].isin(B1_CODES)]
    informal_pct = (
        (op_all["b1_most"] == 10.0).sum() + (op_all["b1_most"] == 11.0).sum()
    ) / len(op_all) * 100
    r.append(check("Informal share (quack+chemist) ≈ 14%", round(informal_pct, 1), 14.2, tol=1.5))
    return r


# ── Card 02: Insurance / food-shock ───────────────────────────────────────────
# c1_most: 3=GovtHospital, 5=PrivateHospital  (inpatient coding differs from outpatient!)
# Insurance = any 1 across c10a, c10b, c10d, c10e

def verify_card02(df: pd.DataFrame, tol: float) -> list[bool]:
    print(f"\n{BOLD}Card 02 — Insurance: months of food (inpatient){RESET}")
    r: list[bool] = []

    for col in ["c1_most", "oope_total_ip", "a2g_food"]:
        if col not in df.columns:
            print(f"  {WARN}  {col} not found — skipping"); return [False]

    ins_cols = [c for c in ["c10a","c10b","c10d","c10e"] if c in df.columns]
    df2 = df.copy()
    df2["_ins"] = (df2[ins_cols] == 1).any(axis=1) if ins_cols else False

    ip = df2[
        df2["c1_most"].isin([IP_GOVT, IP_PRIVATE]) &
        df2["oope_total_ip"].notna() &
        df2["a2g_food"].notna() &
        (df2["a2g_food"] > 0)
    ].copy()
    ip["_mo"] = ip["oope_total_ip"] / ip["a2g_food"]

    gov = ip[ip["c1_most"] == IP_GOVT]
    pvt = ip[ip["c1_most"] == IP_PRIVATE]
    pvt_ins = pvt[pvt["_ins"]]
    pvt_uni = pvt[~pvt["_ins"]]

    r.append(check("GovtHospital inpatient n = 9,751",         len(gov), 9751, tol=200))
    r.append(check("PrivateHospital inpatient n = 1,844",      len(pvt), 1844, tol=100))
    r.append(check("GovtHospital median OOPE = ₹850",         gov["oope_total_ip"].median(), 850.0,  tol=50))
    r.append(check("PrivateHospital median OOPE = ₹15,000",   pvt["oope_total_ip"].median(), 15000.0,tol=500))
    r.append(check("GovtHospital median months food = 0.162", round(gov["_mo"].median(),6), 0.161538, tol=0.01))
    r.append(check("PrivateHospital all median months = 2.324",round(pvt["_mo"].median(),6), 2.323810, tol=0.05))
    r.append(check("PrivateHospital Insured median months = 1.433",
                   round(pvt_ins["_mo"].median(),3), 1.433, tol=0.05))
    r.append(check("PrivateHospital Uninsured median months = 2.667",
                   round(pvt_uni["_mo"].median(),3), 2.667, tol=0.05))

    cat_ins  = (pvt_ins["_mo"] > 1).mean() * 100
    cat_uni  = (pvt_uni["_mo"] > 1).mean() * 100
    pct_gt3  = (pvt["_mo"] > 3).mean() * 100
    r.append(check("PrivateHospital Insured catastrophic (>1 mo) = 59.2%",  round(cat_ins,1), 59.2, tol=1.5))
    r.append(check("PrivateHospital Uninsured catastrophic (>1 mo) = 77.6%",round(cat_uni,1), 77.6, tol=1.5))
    r.append(check("PrivateHospital pct >3 months = 43.2%",                  round(pct_gt3,1), 43.2, tol=1.5))
    return r


# ── Card 03: Family doctor want vs have ───────────────────────────────────────
# d1a: 1=Yes 2=No 3=CantSay 88=DNA
# b1_most: 1=ASHA (proxy for community worker)

def verify_card03(df: pd.DataFrame, tol: float) -> list[bool]:
    print(f"\n{BOLD}Card 03 — Family doctor: want vs have{RESET}")
    r: list[bool] = []

    if "d1a" not in df.columns:
        print(f"  {WARN}  d1a not found"); return [False]

    valid = df[df["d1a"].isin([1,2,3])]
    want_n = int((valid["d1a"] == 1).sum())
    total  = len(valid)
    want_pct = want_n / total * 100

    r.append(check("d1a valid respondents n = 49,623",          total,   49623, tol=100))
    r.append(check("Want family doctor (d1a=1) n = 43,197",     want_n,  43197, tol=100))
    r.append(check("Want family doctor % = 87.1%",              round(want_pct,1), 87.1, tol=0.5))

    if "b1_most" in df.columns:
        op  = df[df["b1_most"].isin(B1_CODES)]
        pct = (op["b1_most"] == 1).mean() * 100
        r.append(check("ASHA as actual OP provider = 2.8%",     round(pct,1), 2.8, tol=0.3))
    return r


# ── Card 04: Bigger family, smaller plate ────────────────────────────────────
# a2f = household size, a2g_food = monthly food spend

CARD04 = [
    ("1–2",  [1,2], None, 3368,  2500, 1250),
    ("3–4",  [3,4], None, 17609, 5000, 1250),
    ("5–6",  [5,6], None, 19563, 6000, 1000),
    ("7–8",  [7,8], None, 6215,  7000, 1000),
    ("9+",   None,  9,    3245,  10000, 889),
]

def verify_card04(df: pd.DataFrame, tol: float) -> list[bool]:
    print(f"\n{BOLD}Card 04 — Bigger family, smaller plate{RESET}")
    r: list[bool] = []

    if "a2f" not in df.columns or "a2g_food" not in df.columns:
        print(f"  {WARN}  a2f / a2g_food not found"); return [False]

    valid = df[df["a2f"].notna() & df["a2g_food"].notna() & (df["a2g_food"] > 0)].copy()
    valid["_pc"] = valid["a2g_food"] / valid["a2f"]

    for label, members, ge, exp_n, exp_tot, exp_pc in CARD04:
        mask = valid["a2f"].isin(members) if members else (valid["a2f"] >= ge)
        sub  = valid[mask]
        r.append(check(f"[{label}] n = {exp_n}",                      len(sub),                  exp_n,   tol=200))
        r.append(check(f"[{label}] median total food = ₹{exp_tot}",   sub["a2g_food"].median(),  exp_tot, tol=50))
        r.append(check(f"[{label}] median per-capita = ₹{exp_pc}",    sub["_pc"].median(),       exp_pc,  tol=30))

    pc_12 = valid[valid["a2f"].isin([1,2])]["_pc"].median()
    pc_9p = valid[valid["a2f"] >= 9]["_pc"].median()
    r.append(check("Per-capita drop 1–2 → 9+ ≈ 29%",
                   round((pc_12 - pc_9p) / pc_12 * 100, 1), 28.9, tol=1.0))
    r.append(check("Total food ratio 9+ / 1–2 = 4×",
                   round(valid[valid["a2f"]>=9]["a2g_food"].median() /
                         valid[valid["a2f"].isin([1,2])]["a2g_food"].median(), 1), 4.0, tol=0.1))
    return r


# ── Card 05: Educated waiting ─────────────────────────────────────────────────
# a2b_age, rec_a2d (1=Primary…4=HS+), a2e (7=Salaried, 8=AvailableForWork)

CARD05 = [
    (1, "Primary",           3065, 4.5,  1.4),
    (2, "Middle",            2576, 5.5,  1.8),
    (3, "Secondary",         3362, 12.1, 3.7),
    (4, "Higher-Secondary+", 5456, 20.4, 10.3),
]

def verify_card05(df: pd.DataFrame, tol: float) -> list[bool]:
    print(f"\n{BOLD}Card 05 — Educated waiting (education-jobs paradox){RESET}")
    r: list[bool] = []

    df2 = df.copy()
    if "rec_a2d" not in df2.columns:
        if "a2d" in df2.columns:
            df2["rec_a2d"] = np.select(
                [df2["a2d"].isin([1,2]), df2["a2d"]==3, df2["a2d"]==4, df2["a2d"].isin([5,6,7,8])],
                [1, 2, 3, 4], default=np.nan)
        else:
            print(f"  {WARN}  rec_a2d / a2d not found"); return [False]

    if "a2b_age" not in df2.columns or "a2e" not in df2.columns:
        print(f"  {WARN}  a2b_age / a2e not found"); return [False]

    cohort = df2[df2["a2b_age"].between(25,34) & df2["rec_a2d"].isin([1,2,3,4])]

    for edu, label, exp_n, exp_sal, exp_wait in CARD05:
        sub = cohort[cohort["rec_a2d"] == edu]
        r.append(check(f"[{label}] n = {exp_n}",        len(sub),                          exp_n,    tol=150))
        r.append(check(f"[{label}] salaried % = {exp_sal}%",  round((sub["a2e"]==7).mean()*100,1), exp_sal,  tol=0.5))
        r.append(check(f"[{label}] waiting % = {exp_wait}%",  round((sub["a2e"]==8).mean()*100,1), exp_wait, tol=0.5))

    w_pri = (cohort[cohort["rec_a2d"]==1]["a2e"]==8).mean()*100
    w_hs  = (cohort[cohort["rec_a2d"]==4]["a2e"]==8).mean()*100
    r.append(check("Waiting ratio HS+ / Primary = 7.5×", round(w_hs/w_pri,1) if w_pri else 0, 7.5, tol=0.5))
    r.append(check("Total 25–34 cohort n = 14,459", len(cohort), 14459, tol=200))
    return r


# ── Card 06: Private hospital food shock ─────────────────────────────────────
# Same derivation as Card 02 — both verify inpatient food-months.
# Kept separate so the card file's own SOP numbers are cross-checked.

def verify_card06(df: pd.DataFrame, tol: float) -> list[bool]:
    print(f"\n{BOLD}Card 06 — Private hospital food shock{RESET}")
    r: list[bool] = []

    for col in ["c1_most","oope_total_ip","a2g_food"]:
        if col not in df.columns:
            print(f"  {WARN}  {col} not found"); return [False]

    ins_cols = [c for c in ["c10a","c10b","c10d","c10e"] if c in df.columns]
    df2 = df.copy()
    df2["_ins"] = (df2[ins_cols]==1).any(axis=1) if ins_cols else False

    ip = df2[
        df2["c1_most"].isin([IP_GOVT, IP_PRIVATE]) &
        df2["oope_total_ip"].notna() & df2["a2g_food"].notna() & (df2["a2g_food"]>0)
    ].copy()
    ip["_mo"] = ip["oope_total_ip"] / ip["a2g_food"]

    gov = ip[ip["c1_most"]==IP_GOVT]
    pvt = ip[ip["c1_most"]==IP_PRIVATE]
    pvt_ins = pvt[pvt["_ins"]]
    pvt_uni = pvt[~pvt["_ins"]]

    r.append(check("GovtHospital inpatient n = 9,751",              len(gov),                          9751,     tol=200))
    r.append(check("PrivateHospital inpatient n = 1,844",           len(pvt),                          1844,     tol=100))
    r.append(check("GovtHospital median OOPE = ₹850",              gov["oope_total_ip"].median(),      850.0,    tol=50))
    r.append(check("PrivateHospital median OOPE = ₹15,000",        pvt["oope_total_ip"].median(),      15000.0,  tol=500))
    r.append(check("GovtHospital median months food = 0.162",      round(gov["_mo"].median(),6),       0.161538, tol=0.01))
    r.append(check("PrivateHospital all median months = 2.324",    round(pvt["_mo"].median(),6),       2.323810, tol=0.05))
    r.append(check("PrivateHospital Insured median months = 1.433",round(pvt_ins["_mo"].median(),3),   1.433,    tol=0.05))
    r.append(check("PrivateHospital Uninsured median months = 2.667",round(pvt_uni["_mo"].median(),3), 2.667,    tol=0.05))
    r.append(check("PrivateHospital pct >3 months = 43.2%",        round((pvt["_mo"]>3).mean()*100,1), 43.2,    tol=1.5))
    return r


# ── main ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, default=None,
                   help="Path to .parquet or .xlsx. Auto-detected if omitted.")
    p.add_argument("--tolerance", type=float, default=0.01,
                   help="Absolute tolerance for float comparisons (default 0.01)")
    p.add_argument("--card", type=int, choices=range(1,7), default=None,
                   help="Run only this card number 1–6 (default: all)")
    return p.parse_args()


def find_data() -> Path:
    for p in [DEFAULT_PARQUET, DEFAULT_PARQUET2, DEFAULT_XLSX]:
        if p.exists():
            return p
    raise FileNotFoundError(
        "No data file found. Run 01_download_and_prepare.py first, or pass --data PATH."
    )


CARD_FNS = {1:verify_card01, 2:verify_card02, 3:verify_card03,
            4:verify_card04, 5:verify_card05, 6:verify_card06}


def main() -> int:
    args = parse_args()
    path = args.data or find_data()
    print(f"Loading {path.name} …")
    df = load_data(path)
    print(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

    to_run = [args.card] if args.card else list(CARD_FNS)
    all_r: list[bool] = []
    for n in to_run:
        all_r.extend(CARD_FNS[n](df, args.tolerance))

    passed = sum(all_r); total = len(all_r); failed = total - passed
    print(f"\n{'─'*55}")
    print(f"{BOLD}Summary{RESET}  {passed}/{total} checks passed", end="")
    if failed:
        print(f"  {RED}({failed} failed){RESET}")
    else:
        print(f"  {GREEN}✓ all clear{RESET}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
