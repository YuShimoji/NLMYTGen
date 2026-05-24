# Real Estate DX Adapter Authorization Gate

Source preflight: `samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.json`

Status: `awaiting_user_or_validator_authorization`

This is an authorization decision gate only. `output_generation_allowed=false` remains in force.
It does not create adapter IR, YMM4 adapter output, YMM4 patch files, `.ymmp` output, render output, production timing, or creative acceptance.

## Candidate Scope

| beat | route types | representation | rights risk |
| --- | --- | --- | --- |
| `RE-02-beginning` | `abstract_ui_route`, `motion_primitive_route` | abstract proxy | low |
| `RE-02-development` | `abstract_ui_route`, `property_card_route`, `motion_primitive_route` | abstract proxy | low |
| `RE-06-beginning` | `property_card_route`, `motion_primitive_route` | abstract proxy | none |
| `RE-06-development` | `document_proxy_route`, `property_card_route`, `risk_marker_route`, `motion_primitive_route` | abstract proxy | none |
| `RE-06-turn` | `document_proxy_route`, `property_card_route`, `motion_primitive_route` | property-document proxy | none |
| `RE-07D-beginning` | `ai_panel_route`, `property_card_route`, `motion_primitive_route` | abstract proxy | none |
| `RE-07D-development` | `risk_marker_route`, `motion_primitive_route` | abstract proxy | low |

## Exclusions

| beat | status | reason |
| --- | --- | --- |
| `RE-02-turn` | `excluded_until_adjusted` | Accepted-with-adjustment proxy has not yet been reflected as a route-planning candidate. |
| `RE-07D-turn` | `deferred_blocks_adapter_planning` | Specialist / cast / silhouette policy remains undecided. |

## Authorization Choices

Recommended response: `authorize_adapter_IR_dry_run_for_7_candidates_only`.

| response | effect |
| --- | --- |
| `authorize_adapter_IR_dry_run_for_7_candidates_only` | Next slice may define and generate adapter IR dry-run artifacts for the 7 route candidates only. YMM4 patch, .ymmp write, render, production timing, and creative acceptance remain forbidden. |
| `hold_for_validator_review` | No downstream dry-run starts. Assistant may prepare a validator-facing review of this gate and the route preflight. |
| `revise_route_candidates_before_authorization` | Return to scene decision, asset/proxy gap report, or route planning candidate correction before any adapter IR dry-run work. |
| `reject_adapter_IR_dry_run` | Close the current adapter route without proceeding to execution-zone dry-run work. |

## Short Return Format

```text
G-27 adapter authorization: authorize_adapter_IR_dry_run_for_7_candidates_only
RE-02-turn: keep excluded_until_adjusted
RE-07D-turn: keep deferred_blocks_adapter_planning
```

## Downstream Boundary

If authorized, the next slice is `adapter_IR_dry_run_contract` for the 7 listed candidates only.
`RE-02-turn` stays excluded until adjusted, and `RE-07D-turn` stays deferred until its specialist / cast / silhouette policy is decided.
YMM4 patch output, `.ymmp` writes, render, production timing, and creative acceptance remain forbidden even after dry-run authorization.
