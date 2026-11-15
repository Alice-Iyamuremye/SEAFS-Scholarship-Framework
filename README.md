# SEAFS — Synthesized Explainable Adaptive Fuzzy Scholarship Framework

A research prototype for transparent, fairness-aware scholarship eligibility decision support using Mamdani fuzzy inference and Fuzzy Analytic Hierarchy Process (AHP) criterion weighting.

## Research context

The MSc thesis, **“A Conceptual Fuzzy Logic Framework for Fair and Transparent Scholarship Eligibility Assessment”**, proposes SEAFS as an institution-agnostic decision-support framework. It addresses limitations of rigid GPA-only thresholds by combining academic performance, financial need and recommendations in a continuous fuzzy assessment process.

## Framework overview

- Mamdani-type fuzzy inference with centroid defuzzification.
- Overlapping triangular/trapezoidal membership functions.
- Compensatory rule-based reasoning.
- Fuzzy AHP criterion weights reported in the thesis: financial need 0.50, GPA 0.30, recommendations 0.20.
- Continuous eligibility score with Reject, Waitlist and Approve bands.
- Rule-activation traces, membership activation outputs and structured audit information intended to support human review.

## Implementation and evaluation described in the thesis

The submitted thesis describes a Python/scikit-fuzzy inference engine, FastAPI endpoints, Docker and Docker Compose configuration, Kubernetes deployment manifests, and a pytest suite reported as containing 32 tests.

The reported evaluation uses synthetic cohort backtesting (N=500) and Monte Carlo continuity experiments (N=1,000). The thesis reports a disadvantaged synthetic-cohort approval rate of 86.7% under SEAFS compared with 38.0% under a legacy threshold baseline, and 74 synthetic applicants classified as rescued. These are results from synthetic experiments, not outcomes from a live scholarship programme.

## Thesis

The signed thesis submitted to the University of Europe for Applied Sciences is available here:

[**Read the submitted MSc thesis (PDF)**](Thesis_Submission19_07_signed.pdf)

## Repository contents

- seafs-2.ipynb: research and implementation notebook.
- seafs_architecture.mmd and seafs_architecture.png: architecture diagram and source.
- api_responses.md and execution_outputs.md: API and execution evidence.
- test_cases.py: test suite.
- Docker configuration and supporting implementation evidence.

## Important scope and limitations

SEAFS is a research prototype and decision-support proposal. Synthetic evaluation does not establish real-world effectiveness, fairness, legal compliance or readiness for autonomous scholarship decisions. The framework is intended to support human review; institutional data, stakeholder validation, legal assessment and prospective evaluation would be required before deployment. GDPR and EU AI Act references in the thesis describe design considerations and intended safeguards, not a certification or legal finding of compliance.

## Research methods

Design Science Research; fuzzy set theory; Mamdani fuzzy inference; Fuzzy AHP pairwise weighting; synthetic-data experiments; Monte Carlo simulation; comparative evaluation; software testing and validation.

## Reference

Alice Iyamuremye, *A Conceptual Fuzzy Logic Framework for Fair and Transparent Scholarship Eligibility Assessment*, MSc thesis, University of Europe for Applied Sciences, Potsdam Campus, 20 July 2026.
