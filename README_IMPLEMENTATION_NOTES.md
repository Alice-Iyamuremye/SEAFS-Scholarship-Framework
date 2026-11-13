# SEAFS implementation and sensitivity notes

Appendix A states that three inputs with three linguistic terms yield 27 possible combinations. It describes two combinations as logically inconsistent and says they are mapped to Reject/Waitlist respectively, leaving 25 effective rules. The appendix extract does not identify those two combinations; its table lists R1-R10 and abbreviates the remaining 15. Do not invent the missing combinations.

The Kaggle notebook implements a condensed 10-rule basis. The thesis itself notes that this condensation may lose granularity near boundary regions. This repository therefore distinguishes the 10-rule notebook implementation from the thesis's 25-rule design.

The reproduced notebook engine uses Mamdani min-AND antecedent firing, max aggregation of clipped output membership functions, and centroid defuzzification. It preserves the notebook membership functions and the ten explicit rules. The thesis reports criterion weights (financial need 0.50, GPA 0.30, recommendations 0.20), but the notebook's 10-rule engine does not apply them; its 500-case section instead uses a separate weighted arithmetic score. This review does not silently blend the methods.

The sensitivity experiment varies input membership-function breakpoints uniformly by -5, 0, and +5 points and varies the administrative pass threshold across 60, 65, 68, 70, 73, 75, and 80. It uses the same 500 synthetic profiles generated with NumPy seed 42 and applies the 10-rule engine to every profile. Criterion-weight sensitivity is not reported because the reproduced notebook engine does not use the thesis weights.

Alpha and Beta are synthetic scenarios generated from different GPA, financial-need, and recommendation distributions. Pass-rate differences are descriptive properties of this constructed scenario, not demographic fairness measurements, real-world impact, or proof of bias mitigation. Any profile for which no rule fires is returned as NoRuleFired/NaN and counted explicitly rather than silently dropped.

Run with: python experiments/evaluate_synthetic_cohort.py; python experiments/sensitivity_analysis.py; pytest -q.
