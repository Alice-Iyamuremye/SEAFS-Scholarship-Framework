"""Evaluate the notebook-aligned 10-rule FIS on the synthetic Alpha/Beta cohort."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from seafs_engine import predict_one  # noqa: E402

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
        "financial_need": np.round(rng.normal(85.0, 10.0, n_beta).clip(0, 100), 1),
        "recommendations": np.round(np.clip(rng.normal(80.0, 15.0, n_beta), 0, 100), 1),
    })
    return pd.concat([alpha, beta], ignore_index=True)

def evaluate(cohort: pd.DataFrame, mf_shift: float = 0.0, approval_threshold: float = 68.0) -> pd.DataFrame:
    rows = []
    for row in cohort.itertuples(index=False):
        result = predict_one((row.gpa - 1.0) / 3.0 * 100.0, row.financial_need,
                             row.recommendations, mf_shift=mf_shift)
        rows.append({
            "student_id": row.student_id, "cohort": row.cohort,
            "gpa": row.gpa, "financial_need": row.financial_need,
            "recommendations": row.recommendations,
            "seafs_score": result["score"], "decision": result["decision"],
            "rule_count": len(result["rule_trace"]),
            "fuzzy_pass": bool(np.isfinite(result["score"]) and result["score"] >= approval_threshold),
        })
    return pd.DataFrame(rows)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--threshold", type=float, default=68.0)
    parser.add_argument("--mf-shift", type=float, default=0.0)
    parser.add_argument("--output", type=Path, default=Path("synthetic_cohort_fuzzy_results.csv"))
    args = parser.parse_args()
    results = evaluate(build_cohort(args.seed), args.mf_shift, args.threshold)
    results["legacy_pass"] = results["gpa"] >= 3.0
    results["rescued_vs_legacy"] = (~results["legacy_pass"]) & results["fuzzy_pass"]
    summary = results.groupby("cohort").agg(
        applicants=("student_id", "size"),
        legacy_passes=("legacy_pass", "sum"),
        fuzzy_passes=("fuzzy_pass", "sum"),
        no_rule_cases=("decision", lambda x: int((x == "NoRuleFired").sum())),
        mean_fuzzy_score=("seafs_score", "mean"),
        rescued_vs_legacy=("rescued_vs_legacy", "sum"),
    )
    summary["legacy_pass_rate_pct"] = 100 * summary["legacy_passes"] / summary["applicants"]
    summary["fuzzy_pass_rate_pct"] = 100 * summary["fuzzy_passes"] / summary["applicants"]
    print("Synthetic scenario results only; not real-world fairness evidence.")
    print(summary.round(2).to_string())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(args.output, index=False)
    print(f"Saved case-level results to {args.output}")

if __name__ == "__main__":
    main()
