# SEAFS: Explainable Fuzzy-Logic Scholarship Decision Support

**MSc research prototype exploring fuzzy inference for multi-criteria scholarship eligibility assessment.**

This repository accompanies the thesis *A Conceptual Fuzzy Logic Framework for Fair and Transparent Scholarship Eligibility Assessment* (University of Europe for Applied Sciences, 2026).

> **Research status:** All cohort experiments use synthetic data. This repository does not establish real-world scholarship impact, validated fairness, or legal/regulatory compliance.

## Research motivation

Rigid eligibility cut-offs can create abrupt decisions when applicants have multiple relevant characteristics. SEAFS explores whether fuzzy membership functions and rule-based inference can represent gradual transitions in applicant attributes while making the reasoning more inspectable.

## Research artefacts

- [Original Kaggle notebook](https://www.kaggle.com/code/aliceiyamuremye/seafs)
- Thesis: *A Conceptual Fuzzy Logic Framework for Fair and Transparent Scholarship Eligibility Assessment*

### Original notebook: two distinct experiments

The notebook must be read as containing two separate computational paths.

**A. Mamdani fuzzy-inference experiment**

- Inputs: GPA, financial need, recommendations (each 0–100).
- Overlapping trapezoidal/triangular membership functions.
- Output categories: Reject, Waitlist, Approve.
- Ten explicit rules encoded with scikit-fuzzy.
- Mamdani min-AND rule firing, max aggregation, centroid defuzzification.
- Monte Carlo simulation: 1,000 generated profiles, seed 42.

The saved notebook output reports 950 of 1,000 profiles processed successfully; 50 yielded no usable output and were dropped. The failure cases need to be diagnosed rather than silently excluded.

**B. Synthetic cohort weighted-score exercise**

The notebook separately generates 500 profiles (Alpha: 350; Beta: 150) and calculates a weighted arithmetic score using fixed weights of 0.50 for financial need, 0.30 for normalized GPA, and 0.20 for recommendations. This cohort code does **not** call the fuzzy inference engine and does not derive weights through Fuzzy AHP pairwise comparisons.

The original notebook reports:
- Alpha: 349/350 pass the GPA threshold; 3/350 pass the weighted-score threshold.
- Beta: 57/150 pass the GPA threshold; 130/150 pass the weighted-score threshold.
- 74 Beta profiles fail the GPA threshold but pass the weighted-score threshold.

These figures are outputs of the synthetic weighted-score scenario, not results of the Mamdani engine or evidence of fairness in a real applicant population.

## Rule-base clarification

The supplementary appendix pages 45–46 supplied by the author provide all 25 listed antecedent/consequent rules. The structured transcription is stored in `research/seafs_25_rule_matrix.json`, with coverage and implementation notes in `research/SEAFS_25_RULE_MATRIX_NOTES.md`.

The three inputs with three linguistic terms define 27 possible antecedent combinations. The supplied 25-rule list omits:
- GPA Low / Financial Need Low / Recommendations Medium.
- GPA Low / Financial Need Medium / Recommendations Medium.

The supplied pages do not assign outcomes to these two combinations, despite the thesis's earlier statement that two logically inconsistent combinations are mapped to Reject/Waitlist respectively. The matrix also uses four consequents (Reject, Borderline, Waitlist, Approve), while the general model description elsewhere names only three. Borderline's output membership function and its final-decision mapping are not specified in the supplied pages.

For these reasons, the 25-rule matrix is now documented as source material but is not yet represented as an executable Mamdani model. The Kaggle notebook's ten-rule FIS remains a separate executable implementation. The thesis itself notes that the condensed ten-rule basis may lose granularity around boundary regions.

## Reproducible review implementation

The review branch contains a Python implementation of the **ten-rule notebook FIS** and applies it to the same 500-profile synthetic cohort:

- `seafs_engine.py`: input membership functions, ten rules, Mamdani min-AND, max aggregation, centroid defuzzification and rule traces.
- `experiments/evaluate_synthetic_cohort.py`: regenerates the Alpha/Beta cohort with NumPy seed 42 and evaluates each profile through the fuzzy engine.
- `experiments/sensitivity_analysis.py`: varies input membership-function breakpoints by -5, 0, and +5 points and varies the administrative pass threshold from 60 to 80.
- `tests/test_seafs_engine.py`: input validation, rule trace, and output checks.
- `README_IMPLEMENTATION_NOTES.md`: methodology and limitations.

This is a reproducibility extension of the notebook, not a claim that the original Kaggle notebook already contains the new cohort evaluation.

### Sensitivity analysis: preliminary findings

With the original synthetic cohort (seed 42), the ten-rule FIS, unshifted membership functions, and a 68-point pass threshold:

| Cohort | Applicants | Legacy GPA pass rate | Fuzzy pass rate |
|---|---:|---:|---:|
| Alpha | 350 | 99.7% | 99.4% |
| Beta | 150 | 38.0% | 68.7% |

Two of the 500 profiles produced no firing rule in this implementation and are counted as missing, not as rejects or passes.

Changing membership breakpoints and the pass threshold materially changes Beta's pass rate. For example, at a 68-point threshold, shifting the membership breakpoints uniformly by -5 points gives a Beta pass rate of 85.3%; shifting them by +5 points gives 54.0%. Alpha remains between 97.7% and 99.7% in these runs.

This sensitivity is evidence that outcomes depend strongly on design parameters. It is not a reason to select parameters solely to equalise group pass rates. The cohorts are deliberately generated from different GPA, financial-need, and recommendation distributions; the resulting differences are scenario diagnostics, not demographic fairness measurements or causal evidence.

Criterion-weight sensitivity is not reported for the ten-rule FIS because the notebook implementation does not apply the thesis's fixed AHP weights. That requires a separately specified and validated model variant.

## Run the review implementation

From the repository root:

```bash
pip install -r requirements.txt
pytest -q
python experiments/evaluate_synthetic_cohort.py
python experiments/sensitivity_analysis.py
```

## Limitations and next steps

- The 25-rule thesis configuration and its two omitted combinations need to be transcribed from a complete, authoritative rule table before implementing that variant.
- The ten-rule notebook basis can leave input combinations without a firing rule.
- The Monte Carlo notebook run processes only 950/1,000 profiles in its saved output.
- The original 500-profile cohort experiment is a weighted-sum model, not the fuzzy engine.
- The thesis reports criterion weights, but the notebook does not reproduce their Fuzzy AHP derivation or apply them in its ten-rule inference code.
- Synthetic distributions, thresholds, membership boundaries, and rules require sensitivity analysis and stakeholder calibration.
- Recommendation manipulation, missing inputs, alternate cohort distributions, and multiple random seeds require further study.
- No real institutional deployment, user study, legal compliance assessment, or real-world fairness validation is claimed.

## Research directions

Future work includes reconstructing the complete 25-rule configuration from the thesis source, testing rule coverage, investigating failed Monte Carlo cases, performing broader sensitivity and robustness analyses, validating criterion weights with domain experts, and studying whether explanations are useful to applicants and scholarship committees.

## Citation

*A Conceptual Fuzzy Logic Framework for Fair and Transparent Scholarship Eligibility Assessment.* MSc thesis, University of Europe for Applied Sciences, 2026.

## Author

**Alice Iyamuremye**  
Research interests: explainable and trustworthy AI, fuzzy decision-support systems, algorithmic fairness, and robust machine learning.
