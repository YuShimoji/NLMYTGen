# Final Layout Recommendation

selected_candidate: candidate_b_guided_decision_flow

## Why

Candidate B is the next implementation target because the core job is not monitoring. The user needs to identify which situation applies, then receive one safe next action while provenance remains available on demand.

## Next Implementation Target

Build a guided start-to-decision flow: first explain the review purpose in plain language, then ask the minimum situation checks, then show one recommended action and a secondary evidence/gate drawer.

## Known Risks

- If the flow hides too much evidence, expert reviewers may feel slowed down.
- If copy is too assertive, it may look like the tool is approving real input or YMM4 work.
- If tests keep asserting exact card counts, the better layout may be blocked for the wrong reason.

## Test Anti-Goals

Avoid testing exact card counts, exact strings, enum labels in primary copy, and fixed visual section names as success criteria.

Prefer testing that the primary user question exists, the action hierarchy is clear, exactly one final recommendation is selected, source records remain secondary, external dependencies are absent, and all closed gates stay intact.

Copy policy: primary copy should use durable user language, with internal artifact IDs limited to details or machine-readable files.

Layout policy: validate meaning and containment, not one specific grid.
