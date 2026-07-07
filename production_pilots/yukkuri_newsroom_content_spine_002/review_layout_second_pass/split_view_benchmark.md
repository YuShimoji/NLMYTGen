# Split-View Benchmark

split view: decision rail + evidence/preview pane is the strongest next model because it keeps the user's current situation, active recommendation, evidence preview, and closed gate context visible together.

## Research Basis Applied

- Dashboard/status-board layouts are useful for monitoring, but this task is choosing a next action.
- Progressive disclosure is useful only when secondary information is genuinely secondary.
- Task lists/checklists are heavier than this single next-lane decision requires.
- Split-view, master-detail, and spine-detail patterns better support simultaneous decision and evidence viewing.
- Card grids are suspect unless each card is a primary actionable object and dependency flow remains visible.

## Candidate Comparison

| candidate | score | evidence model | card-bloat risk | verdict |
|---|---:|---|---|---|
| Split view: decision rail + evidence/preview pane | 47 | evidence_preview_pane | low | selected |
| Spine + detail: active path and selected node | 42 | selected_node_detail_with_source_links | medium | runner_up |
| Start page / service entry + decision board | 35 | summary_then_secondary_panel | medium | rejected |
| Wizard / step-by-step decision flow | 34 | deferred_details | medium | rejected_after_weak_pass |
| Current card/drawer guided flow | 26 | generic_drawer | high | weak_pass_do_not_extend |
| Command-center cockpit | 24 | status_rows_and_details | high | rejected |

Selected next implementation target:

`candidate_a_split_view_decision_evidence_pane`
