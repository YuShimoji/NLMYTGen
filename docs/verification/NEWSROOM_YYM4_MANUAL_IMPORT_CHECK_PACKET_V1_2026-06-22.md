# Newsroom YMM4 Manual Import Check Packet v1

artifact_id: newsroom_yym4_manual_import_check_packet_v1_2026_06_22
packet_id: newsroom_yym4_manual_import_check_packet_v1_2026_06_22
schema_version: newsroom_yym4_manual_import_check_packet.v1
review_status: ready_for_operator_manual_check
production_status: diagnostic_only
manual_check_status: not_run
diagnostic_only: true

## Source and Target

- source_tiny_csv_path: samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv
- source_tiny_proof_path: samples/_probe/newsroom_handoff/tiny_importable_proof_v1.json
- source_tiny_proof_id: newsroom_tiny_importable_proof_v1_2026_06_22
- source_tiny_importable_status: passed_with_warnings
- target filename: tiny_script_import_candidate_v1.csv
- target surface: speaker, text
- encoding: utf-8-sig (verified: true)
- has_header: false
- expected_rows: 4
- observed_rows_before_manual_check: 4

## Preconditions

- YMM4 is opened manually by the user/operator only; the agent does not launch or automate YMM4.
- Use no production project, no render, no TTS/audio, and no real media during this check.
- Do not commit any `.ymmp` produced by manual experimentation unless a later explicit slice requests it.
- Treat the tiny CSV as synthetic diagnostic-only data, not as production newsroom content.
- If the available YMM4 flow necessarily generates voice, audio, media, render output, or a production project, stop and record blocked_by_operator_uncertainty.

## Manual Procedure

1. Locate the committed target CSV: samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv.
2. Open YMM4 manually as the user/operator, not via this agent.
3. Use the repo-documented YMM4 script import / 台本読み込み function: ツール -> 台本読み込み. If the operator's YMM4 version differs, record operator_menu_unknown rather than inventing alternate menu names.
4. Select CSV import settings matching the repo contract when YMM4 exposes them: UTF-8 BOM / utf-8-sig, comma-delimited, headerless, two columns: speaker,text.
5. Import the CSV only far enough to observe the script rows or import preview; do not proceed into render, TTS/audio, real media, or production save flows.
6. Observe whether exactly 4 lines/rows appear.
7. If screenshot-only operator evidence is needed, record a placeholder path in the result template; do not save a production project.
8. Close without render and without committing any `.ymmp`.

## Expected Successful Observation

- imported_line_count: 4
- speaker_placeholder_behavior: synthetic_newsroom_placeholder appears as a speaker placeholder or is safely unmapped/manual-bindable without data loss
- text_behavior: all 4 target CSV texts appear in order
- timing_import_expected: false
- audio_media_render_expected: false

## Failure Categories

| category | when to use |
|---|---|
| encoding_error | CSV cannot be read as the expected UTF-8 BOM text. |
| header_or_column_mismatch | YMM4 treats the file as having the wrong header or column count. |
| speaker_binding_error | The synthetic speaker placeholder cannot appear, stay unmapped, or be manually bound safely. |
| text_import_error | One or more of the 4 diagnostic texts is missing or altered. |
| row_count_mismatch | YMM4 does not show exactly 4 lines/rows. |
| unsupported_csv_shape | YMM4 rejects the two-column headerless speaker,text CSV shape. |
| operator_menu_unknown | The operator cannot locate the YMM4 script import / 台本読み込み function. |
| unexpected_YMM4_behavior | YMM4 behavior crosses or threatens the diagnostic boundary. |

## Evidence Template

- screenshot_path_placeholder: operator_screenshot_path_placeholder
- observed_line_count: None
- observed_speaker_behavior: None
- observed_text_behavior: None
- error_message: None
- operator_notes_freeform: ""
- result: None
- allowed_results: pass, pass_with_warnings, fail, blocked_by_operator_uncertainty
- result_template_path: samples/_probe/newsroom_handoff/yym4_manual_import_result_template_v1.json

## Next Actions

| observed result | next action |
|---|---|
| pass | Create a result readback and consider a tiny YMM4 import-readiness proof. |
| pass_with_warnings | Classify warnings before changing the CSV or expanding the pipeline. |
| fail | Adjust CSV shape or encoding in a bounded follow-up slice. |
| blocked_by_operator_uncertainty | Improve manual instructions, not the pipeline. |

## Safety Boundary

- ymmp_created_by_agent: false
- YMM4_launched_by_agent: false
- render_created: false
- TTS_generated: false
- real_media_imported: false
- production_approval: false
- public_video_ready: false

## Review Card

Review Card: none. This packet only records the manual import-check contract and does not ask for repeated timing, caption, copy, blocker, neutral timeline, CSV, script, YMM4-adjacent, tiny proof, render, TTS, media, or production review.

## Boundary

This check packet is diagnostic-only. The agent did not launch YMM4, create `.ymmp`, create a carrier, render, generate TTS/audio, import real media, ingest a real newsroom packet, fetch external sources, or approve production/public video use. If YMM4 cannot show the four manual-check rows without crossing those boundaries, the operator should record `blocked_by_operator_uncertainty` instead of continuing.
