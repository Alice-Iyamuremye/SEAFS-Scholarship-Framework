"""Explain where the notebook 10-rule and provisional 27-combination models disagree.

Outputs are deterministic diagnostics over a fixed grid, not applicant-level evidence.
"""
from __future__ import annotations
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from seafs_engine import predict_one as predict_10
from seafs_25_rule_engine import predict_one as predict_27

AXES = [0, 20, 30, 40, 45, 50, 56.5, 60, 68, 70, 78, 80, 90, 100]
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)

def finite(value):
    return value is not None and math.isfinite(float(value))

def main():
    rows = []
    for gpa in AXES:
        for need in AXES:
            for rec in AXES:
                a = predict_10(gpa, need, rec)
                b = predict_27(gpa, need, rec)
                a_ok, b_ok = finite(a["score"]), finite(b["score"])
                trace_a, trace_b = a.get("rule_trace", []), b.get("rule_trace", [])
                delta = float(b["score"] - a["score"]) if a_ok and b_ok else None
                rows.append({
                    "gpa": gpa, "financial_need": need, "recommendations": rec,
                    "ten_score": a["score"] if a_ok else "",
                    "ten_decision": a["decision"],
                    "ten_rule_ids": ";".join(str(x.get("rule")) for x in trace_a),
                    "twenty_seven_score": b["score"] if b_ok else "",
                    "twenty_seven_decision": b["decision_band"],
                    "twenty_seven_rule_ids": ";".join(str(x.get("rule_id")) for x in trace_b),
                    "twenty_seven_inferred_rule_ids": ";".join(
                        str(x.get("rule_id")) for x in trace_b if x.get("source") == "reconstructed"),
                    "human_review_required": b.get("human_review_required", False),
                    "score_delta_27_minus_10": delta if delta is not None else "",
                    "jointly_scored": a_ok and b_ok,
                    "decision_agreement": (a["decision"] == b["decision_band"]) if a_ok and b_ok else "",
                })

    csv_path = OUT / "seafs_model_disagreement_diagnostics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    joint = [r for r in rows if r["jointly_scored"]]
    no10 = [r for r in rows if not r["ten_score"] != ""]
    agree = [r for r in joint if r["decision_agreement"]]
    deltas = [float(r["score_delta_27_minus_10"]) for r in joint]
    confusion = Counter((r["ten_decision"], r["twenty_seven_decision"]) for r in joint)
    inferred_active = [r for r in joint if r["twenty_seven_inferred_rule_ids"]]
    review = [r for r in joint if r["human_review_required"]]
    by_gpa = defaultdict(list)
    for r in joint:
        by_gpa[r["gpa"]].append(r)

    lines = [
        "# SEAFS model disagreement diagnostics", "",
        "This is a deterministic diagnostic grid, not a representative applicant sample,",
        "performance benchmark, or fairness evaluation. The 27-combination implementation",
        "uses experimental output membership functions, two inferred rule outcomes, and no",
        "Fuzzy AHP weighting. The 10-rule implementation follows the submitted notebook.", "",
        "## Coverage and overall comparison", "",
        f"- Grid cases: **{len(rows)}**",
        f"- Both models returned scores: **{len(joint)} ({len(joint)/len(rows):.1%})**",
        f"- 10-rule model returned no score: **{len(no10)} ({len(no10)/len(rows):.1%})**",
        f"- Decision agreement among jointly scored cases: **{len(agree)/len(joint):.1%}**",
        f"- Mean score difference (27-rule minus 10-rule): **{sum(deltas)/len(deltas):.2f} points**",
        f"- Median absolute score difference: **{sorted(abs(x) for x in deltas)[len(deltas)//2]:.2f} points**",
        f"- Human-review flag in 27-rule model: **{len(review)} ({len(review)/len(joint):.1%} of jointly scored cases)**",
        f"- At least one inferred rule activated: **{len(inferred_active)} ({len(inferred_active)/len(joint):.1%} of jointly scored cases)**", "",
        "## Decision-band cross-tabulation", "",
        "| 10-rule decision | 27-rule Approve | 27-rule Reject | 27-rule Waitlist |",
        "|---|---:|---:|---:|",
    ]
    labels = ["Approve", "Reject", "Waitlist"]
    for label in labels:
        vals = [confusion[(label, other)] for other in ["Approve", "Reject", "Waitlist"]]
        lines.append(f"| {label} | {vals[0]} | {vals[1]} | {vals[2]} |")
    lines += ["", "## Agreement by GPA grid value", "",
              "| GPA grid value | Joint cases | Agreement | Mean score difference |",
              "|---:|---:|---:|---:|"]
    for gpa in AXES:
        group = by_gpa[gpa]
        if group:
            group_deltas = [float(r["score_delta_27_minus_10"]) for r in group]
            group_agree = sum(bool(r["decision_agreement"]) for r in group)
            lines.append(f"| {gpa:g} | {len(group)} | {group_agree/len(group):.1%} | {sum(group_deltas)/len(group_deltas):.2f} |")
    lines += ["", "## Interpretation and limitations", "",
        "- The largest structural coverage issue in this grid is the 10-rule model's no-rule-fired region.",
        "- Decision disagreements should be reviewed alongside the fired rule IDs and inferred-rule provenance in the CSV.",
        "- The inferred rules are policy assumptions, not recovered thesis rules.",
        "- The 27-rule output membership functions are experimental, and the thesis's Fuzzy AHP weighting operation remains unresolved.",
        "- Neither higher scores, broader coverage, nor higher agreement establishes fairness, validity, or real-world suitability.",
        "- Before treating either implementation as thesis-faithful, resolve the GPA scale mismatch, output membership functions,",
        "  AHP weighting operator, rule-base inconsistency, and the intended handling of Borderline cases.", ""]
    md_path = OUT / "seafs_model_disagreement_summary.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {csv_path} and {md_path}; jointly scored={len(joint)}; agreement={len(agree)/len(joint):.3%}; no-rule-10={len(no10)}")

if __name__ == "__main__":
    main()
