# SEAFS: A Conceptual Fuzzy-Logic Framework for Scholarship Eligibility Assessment

**Research prototype for interpretable, uncertainty-aware scholarship decision support.**

SEAFS explores how fuzzy logic can represent imprecise eligibility criteria and expose the reasoning behind a decision. The project accompanies the MSc thesis *A Conceptual Fuzzy Logic Framework for Fair and Transparent Scholarship Eligibility Assessment*.

> **Research status:** This is a research prototype evaluated using synthetic data. It has not been validated in a live scholarship programme, and it does not establish legal or regulatory compliance.

## Research question

Can an interpretable fuzzy-inference framework combine academic performance, financial need, and recommendation evidence while making the resulting eligibility assessment more transparent than a rigid threshold-based approach?

## Approach

The proposed framework brings together:

- **Mamdani fuzzy inference** to map input criteria to an eligibility assessment.
- **Overlapping triangular and trapezoidal membership functions** to represent gradual transitions and uncertainty.
- **Fuzzy AHP criterion weights** to express the relative importance assigned to the assessment criteria.
- **Interpretable rule activation** so that the rules contributing to an assessment can be inspected.
- **Python implementation**, with scikit-fuzzy used for fuzzy inference and FastAPI explored for API integration.

The thesis assigns the following weights in its described configuration:

| Criterion | Weight |
|---|---:|
| Financial need | 0.50 |
| Academic performance (GPA) | 0.30 |
| Recommendations | 0.20 |

These are design choices in the evaluated framework, not universal or empirically established weights for scholarship selection.

## Evaluation design

The thesis reports evaluation using:

- A synthetic cohort of **500 cases**.
- A Monte Carlo continuity simulation of **1,000 cases**.
- Comparisons with a threshold-based baseline and alternative decision approaches.
- Analysis of simulated eligibility outcomes and changes around decision boundaries.

The thesis reports a simulated disadvantaged-cohort pass rate of 86.7% for SEAFS compared with 38.0% for its legacy threshold baseline. These figures describe the synthetic experimental setup only. They should not be interpreted as evidence of real-world impact or proof of fairness.

## Interpretability and auditability

The framework is designed to make the decision process inspectable through fuzzy membership values, rule activation, and a structured record of the reasoning contributing to an output. Interpretability is a design objective; the usefulness of explanations to actual applicants or scholarship administrators has not yet been established through a user study.

## Repository contents

This repository contains thesis-related research materials and implementation artefacts. Consult the files in the repository for the specific notebooks, source files, diagrams, tests, and deployment configuration available in this version.

## Reproducibility

The experiments use synthetic data. Before reproducing or comparing results, inspect the relevant notebook or script to identify its configuration, random seeds, dependencies, and evaluation procedure. Reported thesis results should not be treated as independently reproduced unless the corresponding run can be executed and its outputs verified.

A complete reproducibility release should specify:

1. Python and package versions.
2. Exact commands and entry points for each experiment.
3. Random seeds and synthetic-data generation settings.
4. Membership-function parameters, rule base, and criterion weights.
5. Baseline definitions and metric calculations.
6. Test commands and expected outputs.

## Limitations

- The evaluation uses synthetic rather than institutional scholarship data.
- Criterion weights are fixed in the evaluated configuration.
- The rule base and criteria represent a simplified model of a complex allocation process.
- Strategic or biased recommendation evidence has not been fully tested.
- No deployment in a real scholarship programme or evaluation with applicants and decision-makers is claimed.
- This project does not certify compliance with GDPR, the EU AI Act, or any other legal framework.

## Research directions

Potential next steps include sensitivity analysis of criterion weights, robustness tests under changes in input distributions, subgroup-focused evaluation, assessment of recommendation manipulation, and user studies examining whether explanations are understandable and useful.

## Citation

If you use this work, cite the associated MSc thesis:

* A Conceptual Fuzzy Logic Framework for Fair and Transparent Scholarship Eligibility Assessment.
* University of Europe for Applied Sciences, 2026.

## Author

**Alice Iyamuremye**  
Research interests: explainable and trustworthy AI, fuzzy decision-support systems, algorithmic fairness, and robust machine learning.
