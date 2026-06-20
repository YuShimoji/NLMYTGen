# Newsroom Export Fixture Compatibility v1 - 2026-06-20

Artifact id: `newsroom_export_fixture_compatibility_v1_2026_06_20`

This readback checks the fake `newsroom-yt-pipeline` export fixture at
commit `912ce3b` against the current NLMYTGen handoff contract, export delta
request, readiness checklist, validator assumptions, G-28 slot-linkage proof,
transfer-planning proof, and Review Console panel assumptions.

It is diagnostic-only. It does not ingest a real packet, fetch sources, open RSS
or Inoreader flows, access live source material, download media, edit `.ymmp`,
generate YMM4 carriers, render media, approve rights, approve production, or
publish/upload output.

## Inputs

| Side | Artifact |
| --- | --- |
| NLMYTGen handoff contract | `docs/integration/NEWSROOM_TO_NLMYTGEN_HANDOFF_CONTRACT.md` |
| NLMYTGen export request | `samples/_probe/newsroom_handoff/upstream_export_delta_request.json` |
| NLMYTGen readiness checklist | `samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json` |
| Newsroom fake fixture | `../newsroom-yt-pipeline/samples/_probe/newsroom_handoff/newsroom_export_fixture_v1.json` |
| Newsroom fixture doc | `../newsroom-yt-pipeline/docs/integration/NEWSROOM_EXPORT_FIXTURE_FOR_NLMYTGEN_V1.md` |
| Compatibility JSON | `samples/_probe/newsroom_handoff/newsroom_export_fixture_compatibility_readback.json` |

## Current Compatibility Result

| Field | Value |
| --- | --- |
| status | passed with adapter warnings; transfer blocked |
| current packet | fake fixture only |
| real packet accepted | false |
| rights approval | false |
| media approval | false |
| review approval | false |
| production approval | false |
| YMM4 transfer ready | false |
| raw fixture direct ingest | not accepted; adapter required |

The newsroom fixture is compatible as an upstream contract probe, not as a raw
NLMYTGen validator input. The next implementation choice is either a narrow
NLMYTGen adapter mapper or a newsroom-side fixture adjustment for fields that
should become direct export fields.

## Status Counts

| Compatibility status | Count |
| --- | ---: |
| direct_match | 9 |
| transform_required | 13 |
| missing_required | 0 |
| missing_transfer_candidate | 3 |
| hold_for_human_review | 8 |
| upstream_only | 10 |
| downstream_only | 2 |
| total checks | 45 |

## Compatibility Matrix

| Area | Newsroom path | NLMYTGen expectation | Status | Next action |
| --- | --- | --- | --- | --- |
| artifact identity | `fixture_id` | `artifact_id` | transform_required | Adapter rename before validator intake. |
| contract version | `schema_version` | `contract_version` | transform_required | Adapter rename or request explicit upstream field. |
| episode identity | `episode_id`, `title`, `topic_summary` | same paths | direct_match | No action for fake fixture shape. |
| episode metadata | `export_metadata`, `localization_notes`, `channel_metadata` | `episode_metadata` | transform_required | Compose adapter field or request direct metadata. |
| source notes | `source_notes` | sanitized `source_notes` | transform_required | Normalize role/title/status fields into NLMYTGen source-note shape. |
| provenance | `provenance` | raw-material and external-fetch booleans | transform_required | Map newsroom safety fields into NLMYTGen provenance booleans. |
| rights summary | `rights_summary.status` | clearance state and blocked uses | hold_for_human_review | Hold; fake fixture does not clear rights. |
| NotebookLM seed | `notebooklm_packet.transcript_seed.summary` | `notebooklm_packet.transcript_seed` | transform_required | Flatten seed summary or request direct string seed. |
| script beats | `script_beats[].summary/source_refs` | `intent`, `claim`, `evidence_refs` | transform_required | Map stable ids and source refs into validator shape. |
| visual plan | `visual_plan[].unit_type/approval_state` | VisualIR fields and content slots | transform_required | Map units to layout candidates and G-28 slots. |
| G-28 hints | `hint_type`, `recommended_role` | `object_catalog_slot` | transform_required | Map semantic intent to allowed G-28 object catalog slots. |
| review warnings | `severity` | `blocks_ymm4_transfer` | transform_required | Convert block/hold severity to explicit transfer blocker booleans. |
| downstream readiness | string readiness states | `ymm4_transfer_ready=false` plus blockers | transform_required | Map block/fail states to fail-closed transfer readiness. |
| transfer gates | rights/media/review/visual states | transfer-candidate gates | missing_transfer_candidate or hold_for_human_review | Keep transfer blocked until real review clears gates. |
| optional enrichments | confidence, priority, notes, localization, channel metadata | optional checklist fields | direct_match or transform_required | Use as advisory metadata only. |
| prohibited assumptions | `boundary_assertions` and fake safety flags | no NLMYTGen source/fetch/render/publish work | upstream_only | Keep these responsibilities out of NLMYTGen. |
| geometry / production readiness | semantic hints and `production_ymm4=fail` | downstream YMM4 gate | downstream_only | Keep geometry and production transfer downstream and blocked. |

Full per-field rows are in
`samples/_probe/newsroom_handoff/newsroom_export_fixture_compatibility_readback.json`.

## Adapter vs Upstream Adjustment

| Lane | Fields |
| --- | --- |
| NLMYTGen adapter mapping | `fixture_id`, `schema_version`, `episode_metadata`, `source_notes`, `provenance`, `notebooklm_packet`, `script_beats`, `visual_plan`, `g28_slot_hints`, `review_warnings`, `downstream_readiness`, `channel_metadata` |
| Upstream fixture adjustment candidate | direct `artifact_id`, direct `contract_version`, direct `episode_metadata`, direct G-28 object catalog slots if newsroom wants fewer adapter rules |
| Human review hold | rights clearance, media availability, review approval, visual approval, ambiguous rights, quote/citation uncertainty, brand risk |
| No action | `episode_id`, `title`, `topic_summary`, explicit no-real-media flags, prohibited-action boundary assertions |

## Validation Readback

- Newsroom fixture path exists and parses as JSON.
- Newsroom fixture has no real URL references.
- Compatibility readback JSON parses.
- Raw newsroom fixture direct validator run fails as expected with adapter
  required: `errors=20`, `transfer_status=blocked`.
- Every NLMYTGen export request item has a compatibility status.
- Compatibility categories are present:
  `direct_match`, `transform_required`, `missing_required`,
  `missing_transfer_candidate`, `hold_for_human_review`, `upstream_only`,
  and `downstream_only`.
- Transfer remains blocked.
- Rights, media, review, production, and YMM4 transfer approvals remain false.
- Focused compatibility test: `6 passed`.
- Combined newsroom focused tests: `35 passed`.

## Downstream Next Use

Use this readback before writing an adapter mapper. The safe default next slice
is an NLMYTGen adapter compatibility proof that converts the fake newsroom
fixture into the existing NLMYTGen validator packet shape without making it a
real packet or transfer candidate.
