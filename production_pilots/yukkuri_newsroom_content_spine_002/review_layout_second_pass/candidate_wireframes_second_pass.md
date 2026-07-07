# Candidate Wireframes Second Pass

Selected next implementation target: `candidate_a_split_view_decision_evidence_pane`.

## Split view: decision rail + evidence/preview pane

- status: selected
- pattern family: split_view_master_detail
- evidence handling: evidence_preview_pane
- card-bloat risk: low
- strength: Keeps the active recommendation and the trust evidence visible at the same time without turning evidence into a closet.
- weakness: Needs responsive behavior so the right pane stacks cleanly on narrow screens.

## Spine + detail: active path and selected node

- status: runner_up
- pattern family: spine_detail
- evidence handling: selected_node_detail_with_source_links
- card-bloat risk: medium
- strength: Shows the route through hold, real input, and YMM4 observation without making every option equal.
- weakness: Can become process-heavy if the user only needs a simple current recommendation.

## Start page / service entry + decision board

- status: rejected
- pattern family: service_entry
- evidence handling: summary_then_secondary_panel
- card-bloat risk: medium
- strength: Strong explanation of purpose and first-time user orientation.
- weakness: Still tends to compare choices side by side and can slide back into card-board layout.

## Wizard / step-by-step decision flow

- status: rejected_after_weak_pass
- pattern family: wizard
- evidence handling: deferred_details
- card-bloat risk: medium
- strength: Good for novice input gathering and exactly-one outcome.
- weakness: The weak-pass prototype showed that wizard language can over-trim evidence and hide trust checks.

## Current card/drawer guided flow

- status: weak_pass_do_not_extend
- pattern family: card_drawer
- evidence handling: generic_drawer
- card-bloat risk: high
- strength: Compact, local, dark, and already validates exactly-one recommendation.
- weakness: Cards make options look like equal objects, and the evidence drawer becomes a storage closet.

## Command-center cockpit

- status: rejected
- pattern family: dashboard_cockpit
- evidence handling: status_rows_and_details
- card-bloat risk: high
- strength: Power users can scan many statuses quickly.
- weakness: It centers artifact inventory and repeats the original cockpit weakness for novice decision making.
