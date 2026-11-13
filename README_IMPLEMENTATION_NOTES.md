# SEAFS implementation notes

The original Kaggle notebook uses a 10-rule scikit-fuzzy control system for its Monte Carlo section, then switches to a separate weighted arithmetic score for the 500-case cohort. The new review-branch implementation uses one 27-combination fuzzy rule base and the same prediction engine for individual and cohort evaluation.

The criterion weights (financial need 0.50, GPA 0.30, recommendations 0.20) are fixed values reported in the thesis. The notebook does not reproduce a Fuzzy AHP pairwise-comparison calculation, so this code does not claim to calculate Fuzzy AHP weights.

Rule activation uses a weighted geometric conjunction of membership degrees, with configured weights as exponents. Consequents are clipped, aggregated by maximum, and defuzzified using a discrete centroid. This is an explicitly specified weighted fuzzy-AND design, not canonical unweighted min-AND Mamdani inference. The thesis and project description must use this precise terminology.

The 3x3x3 linguistic combinations produce 27 possible rules. The thesis's claim of a 25-rule full factorial is mathematically inconsistent and needs correction or a documented explanation of two intentionally omitted combinations.

## Run

`pip install -r requirements.txt`
`pytest -q`
`python experiments/evaluate_synthetic_cohort.py`

The cohort script reproduces the original synthetic distributions with seed 42, converts GPA from 1.0–4.0 to 0–100, evaluates every case using the fuzzy engine, and reports subgroup pass rates and descriptive pass-rate disparity.

## Limitations

The weights, rule mapping, membership functions, and decision thresholds are design assumptions. The two synthetic cohorts have intentionally different input distributions, so their outcome differences are scenario diagnostics, not proof of fairness or causal effects. No real applicant data, institutional deployment, legal compliance assessment, or user study is included.
