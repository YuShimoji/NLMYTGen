# Newsroom Source .ymmp Recreation Import Pack v1

artifact_id: newsroom_source_ymmp_recreation_import_pack_v1_2026_06_26
pack_id: newsroom_source_ymmp_recreation_import_pack_v1_2026_06_26
schema_version: newsroom_source_ymmp_recreation_import_pack.v1
review_status: ready_for_operator_source_ymmp_recreation
production_status: diagnostic_only
recreation_status: csv_ready
diagnostic_only: true

## Why This Exists

The source `.ymmp` is an ignored local artifact, so it is not carried by the remote-tracked repository. This checkout does not have `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`, which blocks the later timing-patch and card-placement regeneration. This pack recreates only the import CSV needed for the user to save that local source project through YMM4 script import.

## Source Evidence

- canonical_speaker: ゆっくり霊夢
- canonical_speaker_unicode_escape: \u3086\u3063\u304f\u308a\u970a\u5922
- confidence: high
- disagreement_or_unknowns: []
- source_readback_paths:
  - samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json
  - samples/_probe/newsroom_handoff/diagnostic_ymmp_probe_packet_v1.json
  - samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv

## CSV Pack

- output_csv_path: samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv
- encoding: UTF-8 BOM
- header: false
- columns: speaker, text
- row_count: 4
- yym4_import_mode: 台本読込
- expected_character_binding: ゆっくり霊夢

| row | speaker | text |
|---:|---|---|
| 1 | ゆっくり霊夢 | Fake topic, review only. |
| 2 | ゆっくり霊夢 | Review-only handoff stays. |
| 3 | ゆっくり霊夢 | A fake claim is shown. |
| 4 | ゆっくり霊夢 | Fake source checks are noted. |

## User Steps

1. Open YMM4.
2. Import `samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv` via 台本読込.
3. Use `ゆっくり霊夢` if speaker binding is requested.
4. Confirm four lines appear.
5. Save as `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`.
6. Do not render yet.

The user observation can stay freeform. No template or structured answer is required for this recreation step.

## Operator Save Target

- target_dir: _tmp/newsroom_manual_probe
- target_source_ymmp: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp
- note: this .ymmp is ignored local only and must not be committed

## Next Codex Continuation

After the user saves the source `.ymmp`, Codex should verify that the local file exists under `_tmp/`, remains ignored and unstaged, then rerun the local regeneration for the timing patch and card placement project copies.

- expected_next_local_outputs:
  - _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
  - _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp

## Safety Boundaries

- ymmp_fabrication: false
- YMM4_launched_by_agent: false
- render_created_by_agent: false
- external_TTS_introduced: false
- audio_generated_by_agent: false
- real_media_imported: false
- external_fetch_performed: false
- production_public_readiness: false
- ymmp_or_media_stage_allowed: false

## Human Burden Hygiene

- user_input: freeform
- template_required: false
- schema_owner: Agent
- user_side_action: YMM4 import/save only after this package
- future_look_for_max_count: 3
- negative_confirmation_checklist: false
- fixed_form_result_template: false

## Boundary Note

This package does not create `.ymmp`, launch YMM4, render, generate audio/TTS, import real media, fetch external sources, or approve production/public use.
