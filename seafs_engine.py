"""SEAFS research prototype: weighted compensatory fuzzy inference.

Criterion weights are fixed configuration values from the thesis. This module
does not calculate Fuzzy AHP pairwise comparisons.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Dict, Tuple
import numpy as np

CRITERIA_WEIGHTS = {"gpa": 0.30, "financial_need": 0.50, "recommendations": 0.20}
LEVELS = ("Low", "Medium", "High")
LEVEL_VALUES = {"Low": 0.0, "Medium": 0.5, "High": 1.0}

def trimf(x: np.ndarray, abc: Tuple[float, float, float]) -> np.ndarray:
    a, b, c = abc
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (x >= a) & (x <= b)
        y[m] = (x[m] - a) / (b - a)
    else:
        y[x == b] = 1.0
    if c > b:
        m = (x >= b) & (x <= c)
        y[m] = np.maximum(y[m], (c - x[m]) / (c - b))
    else:
        y[x == b] = 1.0
    y[x == b] = 1.0
    return np.clip(y, 0.0, 1.0)

def trapmf(x: np.ndarray, abcd: Tuple[float, float, float, float]) -> np.ndarray:
    a, b, c, d = abcd
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

def _membership(value: float, name: str) -> float:
    x = np.array([value], dtype=float)
    if name == "Low":
        return float(trapmf(x, (0, 0, 40, 60))[0])
    if name == "Medium":
        return float(trimf(x, (40, 60, 80))[0])
    if name == "High":
        return float(trapmf(x, (60, 80, 100, 100))[0])
    raise ValueError(f"Unknown linguistic term: {name}")

@dataclass(frozen=True)
class SEAFSResult:
    score: float
    decision: str
    rule_trace: Tuple[dict, ...]
    memberships: Dict[str, Dict[str, float]]

class SEAFSEngine:
    """Three-input fuzzy inference with a complete 3x3x3 rule base.

    Rule firing uses a weighted geometric conjunction of antecedent
    memberships. Consequents are clipped, aggregated by maximum, and
    defuzzified using a discrete centroid. This is an explicit weighted
    fuzzy-AND design, not canonical unweighted min-AND Mamdani inference.
    """
    def __init__(self, weights: Dict[str, float] | None = None, step: float = 1.0):
        self.weights = dict(weights or CRITERIA_WEIGHTS)
        if set(self.weights) != set(CRITERIA_WEIGHTS):
            raise ValueError("Weights must define all three criteria.")
        if any((not np.isfinite(v) or v <= 0) for v in self.weights.values()):
            raise ValueError("All criterion weights must be positive and finite.")
        total = sum(self.weights.values())
        self.weights = {k: v / total for k, v in self.weights.items()}
        if step <= 0 or step > 1:
            raise ValueError("step must be in (0, 1].")
        self.universe = np.arange(0.0, 100.0 + step, step)
        self.output_mfs = {
            "Reject": trapmf(self.universe, (0, 0, 30, 50)),
            "Waitlist": trimf(self.universe, (30, 50, 75)),
            "Approve": trapmf(self.universe, (50, 75, 100, 100)),
        }
        self.rule_base = self._build_rules()
        if len(self.rule_base) != 27:
            raise RuntimeError("Expected a complete 3x3x3 rule base.")

    def _build_rules(self):
        rules = []
        for gpa, need, recs in product(LEVELS, repeat=3):
            support = (self.weights["gpa"] * LEVEL_VALUES[gpa]
                       + self.weights["financial_need"] * LEVEL_VALUES[need]
                       + self.weights["recommendations"] * LEVEL_VALUES[recs])
            consequent = "Reject" if support < 0.35 else ("Waitlist" if support < 0.68 else "Approve")
            rules.append({"gpa": gpa, "financial_need": need,
                          "recommendations": recs, "consequent": consequent})
        return tuple(rules)

    def predict_one(self, gpa: float, financial_need: float, recommendations: float) -> SEAFSResult:
        values = {"gpa": float(gpa), "financial_need": float(financial_need),
                  "recommendations": float(recommendations)}
        for key, value in values.items():
            if not np.isfinite(value) or not 0 <= value <= 100:
                raise ValueError(f"{key} must be finite and within [0, 100].")
        memberships = {key: {level: _membership(value, level) for level in LEVELS}
                       for key, value in values.items()}
        aggregate = np.zeros_like(self.universe)
        trace = []
        for idx, rule in enumerate(self.rule_base, start=1):
            activation = float(np.prod([
                memberships[key][rule[key]] ** self.weights[key]
                for key in self.weights
            ]))
            if activation <= 0:
                continue
            aggregate = np.maximum(
                aggregate,
                np.minimum(activation, self.output_mfs[rule["consequent"]])
            )
            trace.append({"rule": idx, "antecedents": dict(rule),
                          "activation": activation})
        area = float(np.sum(aggregate))
        if area <= 0:
            raise RuntimeError("No fuzzy rule fired; inspect membership coverage.")
        score = float(np.sum(self.universe * aggregate) / area)
        decision = "Reject" if score < 45 else ("Waitlist" if score < 68 else "Approve")
        return SEAFSResult(score, decision, tuple(trace), memberships)

    def predict(self, frame):
        required = ["gpa_0_100", "financial_need", "recommendations"]
        missing = [c for c in required if c not in frame.columns]
        if missing:
            raise ValueError(f"Missing input columns: {missing}")
        rows = [self.predict_one(*row) for row in
                frame[required].itertuples(index=False, name=None)]
        out = frame.copy()
        out["seafs_score"] = [r.score for r in rows]
        out["seafs_decision"] = [r.decision for r in rows]
        out["active_rule_count"] = [len(r.rule_trace) for r in rows]
        return out
