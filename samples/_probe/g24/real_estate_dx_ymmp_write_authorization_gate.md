# Real Estate DX `.ymmp` Write Authorization Gate

Source dry-run: `samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.json`

Reference compact review: `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json`

Status: `authorized_minimal_patched_ymmp_for_readback_only`

This gate adopts the recommended response for a later minimal patched `.ymmp` readback-only write. It does not perform the write in this slice. `output_generation_allowed=false` and current-slice `ymmp_write_allowed=false` remain in force.

## Candidate Scope

Only the 7 ready candidates may be considered by the next write gate.

| candidate | intended review surface | layer set | duration | placeholder |
| --- | --- | --- | --- | --- |
| `RE-02-beginning` | minimal patched `.ymmp` readback only | 7, 8, 9 | `360`f | `generic_public_search_panel + broker_db_shadow_panel` |
| `RE-02-development` | minimal patched `.ymmp` readback only | 7, 8, 9 | `360`f | `broker_db_panel + public_portal_card + property_card_flow` |
| `RE-06-beginning` | minimal patched `.ymmp` readback only | 7, 8, 9 | `360`f | `property_card_overload_cluster` |
| `RE-06-development` | minimal patched `.ymmp` readback only | 7, 8, 9 | `360`f | `selected_property_sheet + drawback_marker` |
| `RE-06-turn` | minimal patched `.ymmp` readback only | 7, 8, 9 | `360`f | `property_document_editorial_comparison` |
| `RE-07D-beginning` | minimal patched `.ymmp` readback only | 7, 8, 9 | `360`f | `abstract_ai_recommendation_panel + property_card` |
| `RE-07D-development` | minimal patched `.ymmp` readback only | 7, 8, 9 | `360`f | `boundary_inheritance_neighborhood_risk_markers` |

## Exclusions

| candidate | status | reason | required condition |
| --- | --- | --- | --- |
| `RE-02-turn` | `blocked` | Opacity-layer adjustment has not yet been reflected as a route candidate. | Reflect the public information layer / non-public data bundle opacity contrast as a route candidate. |
| `RE-07D-turn` | `deferred` | Specialist / cast / silhouette policy remains undecided. | Choose defer, cut, abstract silhouette, or real asset / cast policy. |

## Boundary

| allowed now | still forbidden |
| --- | --- |
| Read dry-run / compact review evidence | YMM4 adapter output |
| Validate candidate scope consistency | YMM4 patch |
| Prepare the next response choice | `.ymmp` write |
| Update restart state | render / preview capture / production timing / creative acceptance |

Existing compact review and minimal patched probe artifacts remain reference evidence only. They are not regenerated, promoted, rendered, or accepted as production output by this gate.

## Authorization Choices

Selected response: `authorize_minimal_patched_ymmp_for_readback_only`.

| response | effect |
| --- | --- |
| `authorize_minimal_patched_ymmp_for_readback_only` | A later slice may write a minimal patched `.ymmp` for readback only, limited to the 7 candidate set. Render, production timing, and creative acceptance remain forbidden. |
| `hold_for_write_gate_review` | No `.ymmp` write starts. Assistant may refine gate evidence, checker coverage, or the two exclusion plans. |
| `revise_candidate_scope_before_write_gate` | Return to route adjustment or policy decision before any minimal patched `.ymmp` write is authorized. |
| `reject_minimal_patched_ymmp_write` | Close this output path without writing a minimal patched `.ymmp`. |

## Short Return Format

```text
G-27 write authorization: authorize_minimal_patched_ymmp_for_readback_only
Scope: 7 ready candidates only
RE-02-turn: keep blocked until route adjustment
RE-07D-turn: keep deferred until policy decision
```

## Current Selection

- authorization_granted: `true`
- response_selected: `true`
- selected_response: `authorize_minimal_patched_ymmp_for_readback_only`
- selected_response_source: `user_chat_recommended_action`
- output_generation_allowed: `false`
- ymmp_write_allowed: `false`
- actual_ymmp_write_executed: `false`
