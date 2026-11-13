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

The listed rules use four consequent labels: Reject, Borderline, Waitlist, and Approve. The general thesis description elsewhere names only Reject, Waitlist, and Approve. The supplied appendix pages do not define a Borderline output membership function, its numerical support/breakpoints, or a final-decision mapping. Therefore this transcription is a documented rule matrix, not yet an executable 25-rule Mamdani model.

Before implementing the 25-rule engine, specify:
- the Borderline output membership function (shape and numerical parameters);
- whether Borderline is a distinct final status or maps to another status;
- how the two unlisted input combinations should be handled, if the intended model assigns them explicit outcomes.

The existing notebook-aligned 10-rule engine remains a separate implementation and must not be described as this 25-rule matrix.
