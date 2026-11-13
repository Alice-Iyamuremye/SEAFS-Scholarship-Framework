"""Provisional 27-combination SEAFS Mamdani reconstruction.

This is an experimental reconstruction, not a verbatim recovery of the submitted
thesis implementation. Input scores are normalized to [0, 100]. The 25 appendix
rules are retained; two missing combinations are inferred and provenance-tagged.
Borderline consequents use the Waitlist fuzzy output plus a human-review flag.
Fuzzy AHP weighting is deliberately not applied until its exact operator is verified.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
MATRIX_PATH = ROOT / "research" / "seafs_27_combination_reconstruction.json"
MATRIX = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
TERMS = ("Low", "Medium", "High")
OUTPUT_TERMS = ("Reject", "Waitlist", "Approve")
DECISION_BANDS = {"reject_upper": 45.0, "approve_lower": 68.0}

# Experimental output sets: overlapping linear sets on the 0-100 score universe.
# They are not numerical parameters recovered from the thesis.
OUTPUT_MF_PARAMETERS = {
    "Reject": ("trap", (0.0, 0.0, 30.0, 50.0)),
    "Waitlist": ("tri", (35.0, 56.5, 78.0)),
    "Approve": ("trap", (63.0, 78.0, 100.0, 100.0)),
}

def trapmf(x, p):
    a, b, c, d = p
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (x >= a) & (x < b)
        y[m] = (x[m] - a) / (b - a)
    y[(x >= b) & (x <= c)] = 1.0
    if d > c:
        m = (x > c) & (x <= d)
        y[m] = (d - x[m]) / (d - c)
    return np.clip(y, 0.0, 1.0)

def trimf(x, p):
    a, b, c = p
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (x >= a) & (x <= b)
        y[m] = (x[m] - a) / (b - a)
    if c > b:
        m = (x >= b) & (x <= c)
        y[m] = np.maximum(y[m], (c - x[m]) / (c - b))
    y[x == b] = 1.0
    return np.clip(y, 0.0, 1.0)

def input_mf_parameters():
    return {
        "gpa": {
            "Low": ("trap", (0, 0, 40, 60)),
            "Medium": ("tri", (40, 60, 80)),
            "High": ("trap", (60, 80, 100, 100)),
        },
        "financial_need": {
            "Low": ("trap", (0, 0, 30, 50)),
            "Medium": ("tri", (30, 50, 70)),
            "High": ("trap", (50, 70, 100, 100)),
        },
        "recommendations": {
            "Low": ("trap", (0, 0, 40, 60)),
            "Medium": ("tri", (40, 60, 80)),
            "High": ("trap", (60, 80, 100, 100)),
        },
    }

def _mf(x, kind, params):
    return trapmf(x, params) if kind == "trap" else trimf(x, params)

def _decision(score):
    if score < DECISION_BANDS["reject_upper"]:
        return "Reject"
    if score < DECISION_BANDS["approve_lower"]:
        return "Waitlist"
    return "Approve"

def predict_one(gpa, financial_need, recommendations):
    values = {
        "gpa": float(gpa),
        "financial_need": float(financial_need),
        "recommendations": float(recommendations),
    }
    for name, value in values.items():
        if not np.isfinite(value) or not 0.0 <= value <= 100.0:
            raise ValueError(f"{name} must be finite and within [0, 100]")

    input_params = input_mf_parameters()
    memberships = {}
    for name, value in values.items():
        memberships[name] = {
            term: float(_mf(np.array([value]), *input_params[name][term])[0])
            for term in TERMS
        }

    universe = np.linspace(0.0, 100.0, 1001)
    output_sets = {
        label: _mf(universe, *spec)
        for label, spec in OUTPUT_MF_PARAMETERS.items()
    }
    aggregate = np.zeros_like(universe)
    trace = []
    review_rule_ids = []
    for rule in MATRIX["rules"]:
        antecedents = (
            ("gpa", rule["gpa"]),
            ("financial_need", rule["financial_need"]),
            ("recommendations", rule["recommendations"]),
        )
        firing = min(memberships[name][term] for name, term in antecedents)
        if firing <= 0.0:
            continue
        consequent = rule["consequent"]
        # Borderline is a committee-routing flag, not a fourth output fuzzy set.
        if consequent == "Borderline":
            review_rule_ids.append(rule["id"])
            output_label = "Waitlist"
        else:
            output_label = consequent
        aggregate = np.maximum(aggregate, np.minimum(firing, output_sets[output_label]))
        trace.append({
            "rule_id": rule["id"],
            "antecedents": {name: term for name, term in antecedents},
            "source": rule["provenance"],
            "original_consequent": consequent,
            "fuzzy_output_consequent": output_label,
            "activation": float(firing),
        })

    area = float(aggregate.sum())
    if area <= 0.0:
        return {
            "score": None, "decision_band": "NoRuleFired",
            "human_review_required": False, "rule_trace": trace,
            "memberships": memberships,
        }

    score = float(np.dot(universe, aggregate) / area)
    return {
        "score": score,
        "decision_band": _decision(score),
        "human_review_required": bool(review_rule_ids),
        "human_review_rule_ids": review_rule_ids,
        "rule_trace": trace,
        "memberships": memberships,
        "model_metadata": {
            "rule_count": 27,
            "inferred_rule_count": 2,
            "output_membership_functions": "experimental",
            "fuzzy_ahp_weights_applied": False,
            "decision_thresholds_source": "submitted thesis",
        },
    }
