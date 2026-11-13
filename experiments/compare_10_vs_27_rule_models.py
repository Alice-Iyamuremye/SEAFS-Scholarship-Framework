"""Grid comparison of the notebook 10-rule model and provisional 27-rule reconstruction."""
import csv
from pathlib import Path
import numpy as np
from seafs_engine import predict_one as predict_10
from seafs_25_rule_engine import predict_one as predict_27

OUT = Path("reports")
OUT.mkdir(exist_ok=True)
axes = [0, 20, 30, 40, 45, 50, 56.5, 60, 68, 70, 78, 80, 90, 100]
rows = []
for gpa in axes:
    for need in axes:
        for rec in axes:
            a = predict_10(gpa, need, rec)
            b = predict_27(gpa, need, rec)
            rows.append({
                "gpa":gpa, "financial_need":need, "recommendations":rec,
                "ten_rule_score":a["score"], "ten_rule_decision":a["decision"],
                "twenty_seven_rule_score":b["score"], "twenty_seven_rule_decision":b["decision_band"],
                "twenty_seven_human_review":b["human_review_required"],
                "ten_rule_fired_count":len(a["rule_trace"]),
                "twenty_seven_rule_fired_count":len(b["rule_trace"]),
            })
path = OUT / "ten_vs_27_rule_grid_comparison.csv"
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
valid = [r for r in rows if r["ten_rule_score"] is not None and np.isfinite(r["ten_rule_score"])
         and r["twenty_seven_rule_score"] is not None]
agreement = sum(r["ten_rule_decision"] == r["twenty_seven_rule_decision"] for r in valid) / len(valid) if valid else float("nan")
summary = OUT / "ten_vs_27_rule_grid_summary.md"
summary.write_text(
    "# 10-rule vs 27-combination reconstruction: grid comparison\n\n"
    f"- Grid cases: {len(rows)}\n- Cases with both models returning scores: {len(valid)}\n"
    f"- Decision-band agreement among jointly scored cases: {agreement:.3%}\n"
    "- This is a deterministic diagnostic grid, not a representative applicant sample or fairness evaluation.\n"
    "- The 27-combination model uses experimental output membership functions, two inferred antecedent outcomes, "
    "and no Fuzzy AHP weighting. Interpret differences as sensitivity to model specification.\n",
    encoding="utf-8"
)
print(f"Wrote {path} and {summary}; jointly scored={len(valid)}; agreement={agreement:.3%}")
