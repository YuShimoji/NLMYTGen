# G-27 YMM4 Adapter Route Contract

Scope: define the planning-zone route that connects the Real Estate DX
adapter-planning-ready candidate list to a future YMM4 adapter call. This
contract fixes what the adapter is allowed to consume, what proxy / template
primitives it must use, and what representations remain forbidden.

This is a **planning-zone** artifact. `output_generation_allowed=false`. It does
not authorize YMM4 adapter output, YMM4 patch generation, `.ymmp` emission,
render, encode, production timing, or creative acceptance. Those remain blocked
by validator authority and are explicitly outside this contract.

## Source Artifacts

- `samples/_probe/g24/real_estate_dx_thin_scene_decision_packet.json` / `.md`
  — user-confirmed proxy decisions for 9 beats
  (`accepted_proxy` × 7, `accepted_with_adjustment` × 1, `defer` × 1).
- `samples/_probe/g24/real_estate_dx_asset_proxy_gap_report.json` / `.md`
  — `adapter-planning-ready` rollup for 7 beats, `RE-02-turn` adjustment
  requirement, `RE-07D-turn` deferred / still-blocked status.
- `samples/_probe/g24/real_estate_dx_ymm4_adapter_planning_candidates.json` /
  `.md` — narrowed candidate list with planning boundary and forbidden actions.
- `samples/_probe/g24/real_estate_dx_adapter_authorization_gate.json` / `.md`
  — current authorization decision gate for the 7 route-planning candidates.

Validator authority remains
`samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json`
(`status=blocked`,
`allowed_next_actions=[overlay_only_compact_review]`,
`forbidden_next_actions=[cast_motion_ir, ymm4_creative_acceptance, production_timing]`).
This route contract does not open that validator gate.

## 7 Adapter-Planning-Ready Candidates

| beat | route category | required proxy / template primitive |
| --- | --- | --- |
| `RE-02-beginning` | abstract UI | non-official public-search UI vs broker-database abstraction; no service-identifiable branding |
| `RE-02-development` | abstract UI | broker DB panel, public portal card, property-card flow as generic abstractions |
| `RE-06-beginning` | property card | generic property-card overload, density control, subtitle-safe lower band |
| `RE-06-development` | property card + risk marker | selected property sheet plus drawback marker as abstract UI / document shapes |
| `RE-06-turn` | document proxy | property sheet / editorial comparison / document-backed recommendation anchored in property-document structure |
| `RE-07D-beginning` | AI panel + property card | abstract AI recommendation panel plus property card; no identifiable AI service UI |
| `RE-07D-development` | risk marker | boundary / inheritance / neighborhood risk-marker set as abstract symbols |

Motion primitive layer for each candidate stays within the
`enter / move / emphasize / reveal / dim` vocabulary established by the motion
beat plan stage upstream. This contract does not extend that vocabulary.

## Excluded From This Route

| beat | status | reason | re-entry condition (out of scope for this contract) |
| --- | --- | --- | --- |
| `RE-02-turn` | `excluded_until_adjusted` | accepted-with-adjustment state requires opacity-layer contrast (public information layer vs non-public data bundle); prior wall / gate / locked-room / security-facility / conspiracy-coded occlusion language must be removed first | adjustment language reflected in upstream scene decision and gap report by a separate slice |
| `RE-07D-turn` | `deferred_blocks_planning` | specialist / cast / silhouette representation policy is undecided (`asset_proxy_readiness=deferred`, `YMM4_adapter_readiness=still blocked`) | user decision among `abstract silhouette / real asset / cut / defer`; that decision is not made here |

Neither beat is promoted into the candidate list by this contract. Promotion is
an upstream decision recorded in the scene decision packet and gap report, not
in this route contract.

## Forbidden Representation

Across all 7 candidates, the following must not appear in any adapter planning
artifact derived from this contract:

- Real REINS screenshot, logo, or any service-identifiable real-estate search UI
- Real listing photo or externally sourced property image
- Real AI product UI, model screenshots, or identifiable recommendation service branding
- Real maps, registry documents, or identifiable parcel records
- Pure lens / strategy diagram / generic consulting visual treatment as a substitute for the property-document proxy on `RE-06-turn`
- Wall / gate / locked-room / security-facility / conspiracy-coded occlusion language (this also blocks `RE-02-turn` re-entry into the route)
- Real specialist / cast / silhouette representation (`RE-07D-turn` deferred item)
- Any zero-generation pattern (synthesizing YMM4 IR or `.ymmp` content without a tracked source)

Any of these representations entering an adapter planning artifact invalidates
that artifact for adapter consumption.

## Preflight Gate

Before any downstream slice may call the YMM4 adapter against this route
contract, preflight must confirm each of the following. A failure on any item
must be reported with the failing condition; it must not silently degrade to
"planning continues anyway".

1. All 7 candidates remain `adapter-planning-ready` in the latest gap report.
2. `RE-02-turn` remains `excluded_until_adjusted`; no premature promotion into
   the candidate list.
3. `RE-07D-turn` remains `deferred_blocks_planning`; no premature decision on
   specialist / cast / silhouette policy.
4. Validator authority
   `real_estate_dx_background_skit_blueprint_validate.json` still records
   `status=blocked` with `forbidden_next_actions` containing `cast_motion_ir`,
   `ymm4_creative_acceptance`, and `production_timing`.
5. No forbidden representation from the list above has been introduced into the
   upstream artifacts.
6. `output_generation_allowed=false` is preserved. Only an explicit, separately
   authorized user decision may flip this flag; preflight cannot flip it.

## Planning / Execution Boundary

- **Planning zone (in scope for this contract)**: defining the route, candidates
  allowed on that route, proxy / template primitives, forbidden representations,
  and preflight gates.
- **Execution zone (out of scope)**: YMM4 adapter output, adapter IR schema
  definition, YMM4 patch generation, `.ymmp` emission, render, encode,
  production timing, creative acceptance. These remain blocked by validator
  authority. This contract does not unlock them.

`output_generation_allowed=false` is the explicit boundary marker for any
downstream slice that consumes this contract.

## Preflight Report

`scripts/check_g27_adapter_route_preflight.js` machine-checks the six
preflight-gate conditions above against the source artifacts and writes:

- `samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.json`
- `samples/_probe/g24/real_estate_dx_ymm4_adapter_route_preflight.md`

The current report status is `passed_for_planning_preflight`, with 7 route
planning candidates, `RE-02-turn` still `excluded_until_adjusted`, and
`RE-07D-turn` still `deferred_blocks_adapter_planning`.

## Authorization Gate

`scripts/check_g27_adapter_authorization_gate.js` machine-checks the current
authorization surface and writes:

- `samples/_probe/g24/real_estate_dx_adapter_authorization_gate.json`
- `samples/_probe/g24/real_estate_dx_adapter_authorization_gate.md`

The gate status is `awaiting_user_or_validator_authorization`. It may ask for
authorization to start a later adapter IR dry-run contract for the 7 listed
candidates, but it does not grant that authorization and keeps
`output_generation_allowed=false`.

## Next Consumer

The next consumer is the authorization gate above. Adapter IR dry-run work may
start only after a user or validator response authorizes
`authorize_adapter_IR_dry_run_for_7_candidates_only`. YMM4 patch output,
`.ymmp` writes, render, production timing, and creative acceptance remain
forbidden until later gates separately authorize them.
