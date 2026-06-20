# Newsroom Export Adapter Proof v1 - 2026-06-20

Artifact id: `newsroom_export_adapter_proof_v1_2026_06_20`

This proof shows that the fake `newsroom-yt-pipeline` export fixture at commit
`912ce3b` can be deterministically mapped into the existing NLMYTGen normalized
handoff packet shape. It is a diagnostic adapter proof, not a production ingest
adapter and not a real packet acceptance.

This slice does not modify `newsroom-yt-pipeline`, fetch sources, open RSS or
Inoreader flows, access live source material, download media, edit `.ymmp`,
generate YMM4 carriers, render media, approve rights, approve production, or
publish/upload output.

## Artifacts

| Artifact | Path |
| --- | --- |
| adapter module | `src/pipeline/newsroom_export_adapter.py` |
| adapted packet | `samples/_probe/newsroom_handoff/adapted_newsroom_export_packet.json` |
| adapter proof readback | `samples/_probe/newsroom_handoff/newsroom_export_adapter_readback.json` |
| focused tests | `tests/test_newsroom_export_adapter.py` |
| source newsroom fixture | `../newsroom-yt-pipeline/samples/_probe/newsroom_handoff/newsroom_export_fixture_v1.json` |

## Result

| Check | Result |
| --- | --- |
| raw newsroom fixture direct validator | failed as expected; adapter required |
| adapted packet validator | passed |
| adapted packet transfer status | blocked |
| slot-linkage proof | passed_with_warnings |
| transfer-planning proof | blocked |
| real packet accepted | false |
| rights approval | false |
| media approval | false |
| review approval | false |
| production approval | false |
| YMM4 transfer ready | false |

The adapter resolves all required structural fields for NLMYTGen ingest
validation. It intentionally keeps transfer blocked because the fixture is fake,
rights are held for review, media availability is absent, review approval is not
present, and production/YMM4 readiness is not granted.

## Transform / Ownership Matrix

| Field | Newsroom path | NLMYTGen path | Owner | Mapping |
| --- | --- | --- | --- | --- |
| `artifact_id` | `fixture_id` | `artifact_id` | NLMYTGen adapter | rename |
| `contract_version` | `schema_version` | `contract_version` | NLMYTGen adapter | rename |
| `episode_metadata` | `export_metadata` + `localization_notes` + `channel_metadata` | `episode_metadata` | NLMYTGen adapter | compose |
| `source_notes` | `source_notes` | `source_notes` | NLMYTGen adapter | normalize |
| `provenance` | `provenance` + `boundary_assertions` | `provenance` | NLMYTGen adapter | normalize booleans |
| `rights_summary` | `rights_summary` | `rights_summary` | NLMYTGen adapter + human reviewer | preserve hold; never approve |
| `notebooklm_packet` | `notebooklm_packet.transcript_seed.summary` | `notebooklm_packet.transcript_seed` | NLMYTGen adapter | flatten |
| `script_beats` | `script_beats[].summary/source_refs` | `script_beats[].claim/evidence_refs` | NLMYTGen adapter | rename and preserve stable ids |
| `visual_plan` | `visual_plan[].unit_type` | `visual_plan[].visualir_concept/content_slots` | NLMYTGen adapter | map unit type to content slots |
| `g28_slot_hints` | `g28_slot_hints[].hint_type` | `g28_slot_hints[].object_catalog_slot` | NLMYTGen adapter | deterministic alias map |
| `review_warnings` | `review_warnings[].severity` | `review_warnings[].blocks_ymm4_transfer` | NLMYTGen adapter | explicit blocker boolean |
| `downstream_readiness` | `downstream_readiness` | `downstream_readiness` | NLMYTGen adapter | fail-closed booleans and blockers |
| `visual_treatment_preference` | `visual_plan[].unit_type` | optional enrichment | NLMYTGen adapter | derive advisory values |
| `channel_package_metadata` | `channel_metadata` | optional enrichment | NLMYTGen adapter | rename |

## Counts

| Metric | Count |
| --- | ---: |
| direct fields | 9 |
| adapter-owned transforms | 13 |
| held-for-review fields | 8 |
| missing required fields after adapter | 0 |
| transfer-candidate gaps | 3 |
| downstream-only fields | 2 |

## Warnings Preserved

- Raw newsroom fixture requires adapter before validator intake.
- `rights_summary.status=hold_for_review` remains a hold, not approval.
- `rights_summary.media_availability=none_in_fixture` remains a transfer block.
- Quote clearance is still not requested.
- Production and YMM4 readiness remain not approved.
- Slot-linkage passes with expected warnings because some visual content slots
  remain unhinted for transfer planning.

## Downstream Next Use

Use this proof as a seed for a later adapter visibility slice or a real-packet
adapter implementation. The safe next implementation step is to expose the
adapter output/readback in a review surface, or to add a scoped CLI only after
the adapter shape is accepted. Do not use this artifact as production transfer
or YMM4 readiness.
