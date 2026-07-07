# Final Layout Recommendation

selected_candidate: candidate_a_split_view_decision_evidence_pane

## Why

Select split view because the current guided flow proved the value of a user-situation-first entry, but the card/drawer structure hides evidence that the user needs in order to trust the recommendation.

## Next Implementation Target

Build a split-view prototype with a left decision rail and a right evidence/preview pane. The rail should hold current situation, active decision, and one recommended next step. The pane should hold evidence preview, source readiness, and bounded gate context.

## Do Not Carry Forward

- Do not keep a generic evidence drawer as the only source location.
- Do not turn each future source surface into another top-level card.
- Do not return to cockpit inventory as the first screen.

## Test Strategy

- user-situation-first
- visible active path
- evidence is available without becoming a junk drawer
- internal artifact IDs are secondary
- gate details are bounded
- exactly one recommended next step
- no external dependencies
- no production/YMM4/public overclaims

This recommendation is a research checkpoint, not a production UI replacement.
