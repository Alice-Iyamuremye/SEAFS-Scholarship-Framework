# SEAFS 25-rule matrix — transcribed from Appendix pages 45–46

**Source:** Supplementary Framework Matrix Documentation, supplied by the author (Appendix pages 45–46).

This file transcribes the 25 listed rules without changing their antecedents or consequents.

| Rule | GPA | Financial Need | Recommendations | Eligibility Score |
|---:|---|---|---|---|
| 01 | Low | Low | Low | Reject |
| 02 | Low | Low | High | Borderline |
| 03 | Low | Medium | Low | Reject |
| 04 | Low | Medium | High | Borderline |
| 05 | Low | High | Low | Waitlist |
| 06 | Low | High | Medium | Waitlist |
| 07 | Low | High | High | Approve |
| 08 | Medium | Low | Low | Reject |
| 09 | Medium | Low | Medium | Borderline |
| 10 | Medium | Low | High | Waitlist |
| 11 | Medium | Medium | Low | Borderline |
| 12 | Medium | Medium | Medium | Waitlist |
| 13 | Medium | Medium | High | Approve |
| 14 | Medium | High | Low | Waitlist |
| 15 | Medium | High | Medium | Approve |
| 16 | Medium | High | High | Approve |
| 17 | High | Low | Low | Waitlist |
| 18 | High | Low | Medium | Approve |
| 19 | High | Low | High | Approve |
| 20 | High | Medium | Low | Waitlist |
| 21 | High | Medium | Medium | Approve |
| 22 | High | Medium | High | Approve |
| 23 | High | High | Low | Approve |
| 24 | High | High | Medium | Approve |
| 25 | High | High | High | Approve |

## Matrix coverage check

Three inputs with three linguistic terms each define 27 possible antecedent combinations. The supplied list contains 25 unique antecedent combinations. The two combinations not listed are:

1. GPA Low / Financial Need Low / Recommendations Medium.
2. GPA Low / Financial Need Medium / Recommendations Medium.

The supplied pages do not assign outputs to these two combinations. The thesis's earlier statement that two combinations are "logically inconsistent and mapped to Reject/Waitlist respectively" is therefore not demonstrated by this transcribed table. Do not infer which missing combination maps to which output.

## Important implementation clarification

The listed rules use four consequent labels: Reject, Borderline, Waitlist, and Approve. The general description in the final submitted thesis names only Reject, Waitlist, and Approve. The author has confirmed the interpretation that **Borderline is a human-review routing status**, not a fourth fuzzy output category. This interpretation is supported by the earlier thesis draft, which describes scores from 40 to below 70 as being held for committee review; however, those historical cut-offs are not silently substituted for the final thesis decision bands (Reject below 45, Waitlist 45–68, Approve at/above 68).

Accordingly, the 25-rule table is interpreted as a rule-level routing label: a Borderline consequent sends the case to human review rather than making an automated award/rejection decision. This is a documented interpretive reconstruction, not proof that the final submitted thesis fully specified this workflow. The 25-rule matrix still cannot be represented as a fully executable Mamdani model without the final model's numerical output membership functions/aggregation details and an explicit policy for the two unlisted antecedent combinations.

The two unlisted combinations remain unresolved:
- GPA Low / Financial Need Low / Recommendations Medium.
- GPA Low / Financial Need Medium / Recommendations Medium.

Do not infer outcomes for these combinations. The existing notebook-aligned 10-rule engine remains a separate implementation and must not be described as this 25-rule matrix.
