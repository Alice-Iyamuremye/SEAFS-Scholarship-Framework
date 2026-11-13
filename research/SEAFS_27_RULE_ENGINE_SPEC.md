# Experimental 27-combination Mamdani reconstruction

## Status and provenance

This is a provisional research reconstruction, not a verbatim recovery of the submitted thesis implementation. It combines:
- the 25 antecedent/consequent rows transcribed from the supplied appendix;
- two explicitly inferred rows, because the thesis says the omitted combinations map to Reject and Waitlist but does not identify the mapping;
- experimental numerical output membership functions, because the submitted thesis specifies linear triangular/trapezoidal shapes and score bands but does not provide the complete output breakpoints.

## Two inferred antecedents

- GPA Low / Financial Need Low / Recommendations Medium -> Reject.
- GPA Low / Financial Need Medium / Recommendations Medium -> Waitlist.

The first is the conservative outcome for low academic performance and low need. The second is the less exclusionary compensatory outcome for low GPA with moderate need. These are policy inferences, not verified original authorial assignments.

## Output membership functions (experimental)

All output sets are defined over a 0-100 score universe:

| Output | Shape | Parameters |
|---|---|---|
| Reject | Trapezoidal | [0, 0, 30, 50] |
| Waitlist | Triangular | [35, 56.5, 78] |
| Approve | Trapezoidal | [63, 78, 100, 100] |

These overlapping functions are an initial, testable configuration. They are not numerical values recovered from the thesis. The administrative decision bands remain those stated in the thesis: Reject below 45, Waitlist from 45 to below 68, Approve at/above 68. The final decision band is applied to the centroid score, not inferred from the peak of an output membership function.

## Borderline handling

Borderline remains a human-review routing label, not a fourth output fuzzy set. A firing Borderline rule contributes to the Waitlist fuzzy output and independently sets `human_review_required=true`. The API consumer must treat that flag as a referral for committee review, not as an automatic Waitlist decision. This operational mapping is provisional and must be validated with the intended decision-makers.

## Inference operator and Fuzzy AHP

The prototype uses Mamdani min-AND, max aggregation and centroid defuzzification, consistent with the described architecture and the separately reproduced notebook engine. It does **not** apply Fuzzy AHP weights yet. The thesis says weights multiply membership degrees before rule review, but does not provide enough implementation detail to verify the exact weighting operator and how the weighted degrees are combined. Applying the weights without resolving that detail would risk creating an arbitrary method. The weights are therefore recorded but not applied in this version.

## Input scale

The engine accepts GPA, financial need and recommendations on a normalized 0-100 scale. This matches the notebook-style fuzzy universes. The thesis API specification also mentions GPA on a 1.0-4.0 scale; callers must normalize GPA consistently before using this prototype. This scale mismatch must be resolved before an API release.

## Validation

The test suite checks 27 unique antecedent combinations, provenance of the two inferred rows, bounded output memberships, decision boundaries, invalid inputs, rule traces and Borderline review flags. Passing these software tests would establish implementation consistency, not empirical fairness, institutional validity or legal compliance.

## Next research steps

1. Recover or justify output breakpoints with a documented policy elicitation process.
2. Specify and test Fuzzy AHP integration against the thesis methodology.
3. Resolve GPA input normalization and units.
4. Compare the 10-rule notebook engine and this 27-combination reconstruction over a controlled grid and synthetic cohort.
5. Conduct sensitivity analysis for output membership breakpoints, rule inferences and decision thresholds.
6. Seek supervisor/domain-expert review before describing this reconstruction as the thesis's final operational model.
