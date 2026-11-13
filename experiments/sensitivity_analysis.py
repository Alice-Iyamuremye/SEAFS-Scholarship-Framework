"""One-factor-at-a-time sensitivity analysis for the notebook-aligned 10-rule FIS."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluate_synthetic_cohort import build_cohort, evaluate  # noqa: E402

def main() -> None:
    cohort = build_cohort(42)
    rows = []
    for shift in (-5, 0, 5):
        for threshold in (60, 65, 68, 70, 73, 75, 80):
            evaluated = evaluate(cohort, mf_shift=shift, approval_threshold=threshold)
            for name, group in evaluated.groupby("cohort"):
                rows.append({
                    "mf_boundary_shift": shift,
                    "approval_threshold": threshold,
                    "cohort": name,
                    "n": len(group),
                    "pass_rate_pct": 100 * group["fuzzy_pass"].mean(),
                    "mean_score": group["seafs_score"].mean(),
                    "no_rule_cases": int((group["decision"] == "NoRuleFired").sum()),
                })
    results = pd.DataFrame(rows)
    output = Path("seafs_sensitivity_results.csv")
    results.to_csv(output, index=False)
    print(results.pivot_table(
        index=["mf_boundary_shift", "approval_threshold"],
        columns="cohort", values="pass_rate_pct"
    ).round(1).to_string())
    print(f"Saved sensitivity results to {output}")
    print("This varies membership breakpoints and the decision threshold, not AHP weights.")

if __name__ == "__main__":
    main()
