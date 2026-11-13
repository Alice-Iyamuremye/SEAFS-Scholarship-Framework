"""Reproduce the synthetic Alpha/Beta scenario using the SEAFS fuzzy engine."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from seafs_engine import SEAFSEngine  # noqa: E402

def build_cohort(seed: int = 42) -> pd.DataFrame:
    rng = np.random.RandomState(seed)
    n_alpha, n_beta = 350, 150
    alpha = pd.DataFrame({
        "student_id": [f"ALPHA_{i:03d}" for i in range(n_alpha)],
        "cohort": "Alpha",
        "gpa": np.round(np.clip(rng.normal(3.65, 0.25, n_alpha), 1.0, 4.0), 2),
        "financial_need": np.round(np.clip(rng.normal(20.0, 15.0, n_alpha), 0, 100), 1),
        "recommendations": np.round(np.clip(rng.normal(70.0, 15.0, n_alpha), 0, 100), 1),
    })
    beta = pd.DataFrame({
        "student_id": [f"BETA_{i:03d}" for i in range(n_beta)],
        "cohort": "Beta",
        "gpa": np.round(np.clip(rng.normal(2.85, 0.35, n_beta), 1.0, 4.0), 2),
        "financial_need": np.round(np.clip(rng.normal(85.0, 10.0, n_beta), 0, 100), 1),
        "recommendations": np.round(np.clip(rng.normal(80.0, 15.0, n_beta), 0, 100), 1),
    })
    return pd.concat([alpha, beta], ignore_index=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("synthetic_cohort_fuzzy_results.csv"))
    args = parser.parse_args()
    cohort = build_cohort(args.seed)
    cohort["gpa_0_100"] = (cohort["gpa"] - 1.0) / 3.0 * 100.0
    evaluated = SEAFSEngine().predict(cohort)
    evaluated["legacy_pass"] = evaluated["gpa"] >= 3.0
    evaluated["fuzzy_pass"] = evaluated["seafs_score"] >= 68.0
    evaluated["rescued_vs_legacy"] = (~evaluated["legacy_pass"]) & evaluated["fuzzy_pass"]
    summary = evaluated.groupby("cohort").agg(
        applicants=("student_id", "size"),
        legacy_passes=("legacy_pass", "sum"),
        fuzzy_passes=("fuzzy_pass", "sum"),
        mean_fuzzy_score=("seafs_score", "mean"),
        rescued_vs_legacy=("rescued_vs_legacy", "sum"),
    )
    summary["legacy_pass_rate_pct"] = summary.legacy_passes / summary.applicants * 100
    summary["fuzzy_pass_rate_pct"] = summary.fuzzy_passes / summary.applicants * 100
    rates = summary.fuzzy_pass_rate_pct
    gap = float(rates.max() - rates.min())
    ratio = float(rates.min() / rates.max()) if rates.max() else float("nan")
    print("Synthetic scenario results (not real-world fairness evidence)")
    print(summary.round(2).to_string())
    print(f"\nFuzzy pass-rate difference: {gap:.2f} percentage points")
    print(f"Fuzzy pass-rate ratio (lower/higher): {ratio:.3f}")
    print("\nThe cohorts have different generated input distributions; these are descriptive scenario diagnostics.")
    print("They do not establish fairness, causal effects, or suitability for real scholarship decisions.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    evaluated.to_csv(args.output, index=False)
    print(f"\nWrote case-level results to: {args.output}")

if __name__ == "__main__":
    main()
