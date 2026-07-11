# Episode 002 YMM4 CSV import gate readback

状態: `passed` / `actual_ymm4_gui_observation` / `ymm4_csv_import_gate.v1`

明示選択したcharacter profileから生成したderived CSVだけをYMM4 `4.53.0.9`へ読み込み、CSV gate checkpointを記録した。

import済みderived CSV:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/derived_yymm4_import.csv`

canonical source（不変）:
`production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`

## CSV gate 実観測結果5点

1. **passed** — scene order: S1 -> S2 -> S3; cue order: csv_row_1 -> csv_row_2 -> csv_row_3 -> csv_row_4 -> csv_row_5 -> csv_row_6 -> csv_row_7 -> csv_row_8 -> csv_row_9。
2. **passed** — VoiceItemは9件。missing=[]; duplicate=[]; reordered=False。
3. **passed** — mapping_dialog_present=False; automatic_binding=True; character_counts={'ゆっくり霊夢': 3, 'ゆっくり魔理沙': 6}; text/cue match=True。
4. **passed** — order_preserved=True; duration varianceはinformational。60fps・2790 frames・46.5秒。
5. **passed** — CSV expected=['VoiceItem', 'linked_subtitle']; diagnostic project fields (CSV-receipt scope only)=not_authorized/not_attempted; diagnostic item absence is CSV failure=False。

次gate: `supervisor_next_slice_decision`

Do not render/export or write a production `.ymmp`. Diagnostic-project authorization and evidence remain outside this CSV-gate receipt. Do not replace real input, approve rights/public/final thumbnail, or upload.
