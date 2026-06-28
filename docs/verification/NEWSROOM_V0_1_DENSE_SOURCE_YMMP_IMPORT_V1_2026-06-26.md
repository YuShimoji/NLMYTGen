# Newsroom v0.1 Dense Source YMM4 Import v1

package_id: newsroom_v0_1_dense_script_package_v1_2026_06_26
timing_plan_id: newsroom_v0_1_dense_caption_timing_plan_v1_2026_06_26
production_status: diagnostic_only
diagnostic_only: true

## CSV Pack

- output_csv_path: samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv
- encoding: UTF-8 BOM
- header: false
- columns: speaker, text
- row_count: 13
- yym4_import_mode: 蜿ｰ譛ｬ隱ｭ霎ｼ
- expected_character_binding: ゆっくり霊夢
- target_source_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp

## Dense Rows

| row | speaker | text |
|---:|---|---|
| 1 | ゆっくり霊夢 | This review-only sample proves a YMM4 video handoff can be assembled. |
| 2 | ゆっくり霊夢 | The goal is not public news; it is a controllable production path. |
| 3 | ゆっくり霊夢 | A tracked CSV becomes YMM4 dialogue with the same speaker binding. |
| 4 | ゆっくり霊夢 | The source project can be recreated without inventing hidden media. |
| 5 | ゆっくり霊夢 | That gives the next review a repeatable starting point. |
| 6 | ゆっくり霊夢 | Native Yukkuri audio stays in the YMM4 side of the workflow. |
| 7 | ゆっくり霊夢 | The timing patch holds the sample near sixty-eight seconds. |
| 8 | ゆっくり霊夢 | Four PNG cards appear as ImageItems on the timeline. |
| 9 | ゆっくり霊夢 | A prior local render confirms cards, voice, and timing can stay together. |
| 10 | ゆっくり霊夢 | This is still diagnostic: fake topic, fake claims, and no public approval. |
| 11 | ゆっくり霊夢 | Real sources, rights, and final narration are outside this proof. |
| 12 | ゆっくり霊夢 | Next, import this denser script and save a dense source project. |
| 13 | ゆっくり霊夢 | After that, a real packet or RSS dry run can be planned with clearer proof. |

## Timing Plan

- timing_status: planned_not_rendered
- total_duration_sec: 68
- uses_exact_yym4_voice_duration: false
- voice_audio_proof_for_dense_script: false

## User Steps

1. Open YMM4.
2. Import `samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv` via 蜿ｰ譛ｬ隱ｭ霎ｼ.
3. Use `ゆっくり霊夢` if speaker binding is requested.
4. Confirm thirteen dialogue rows appear.
5. Save as `_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp`.
6. Do not render in this import/save step.

Return only a freeform observation if something unexpected happens. A structured answer is not needed.

## Boundary Note

This import pack does not create `.ymmp` by itself, launch YMM4, render, generate audio/TTS, import real media, fetch real sources, or approve production/public use.
