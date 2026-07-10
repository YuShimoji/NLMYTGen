# Episode 002 YMM4観測readback

状態: `partial` / `actual_ymm4_gui_observation`

YMM4 `4.53.0.9` で対象CSVを実際に読み込み、保存せずに終了した。観測結果はreceiptから再生成され、総合判定は`partial`。

YMM4 executable:
`D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe`

import済みCSV:
`production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`

## 実観測結果5点

1. **passed** — scene order: S1 -> S2 -> S3; cue order: csv_row_1 -> csv_row_2 -> csv_row_3 -> csv_row_4 -> csv_row_5 -> csv_row_6 -> csv_row_7 -> csv_row_8 -> csv_row_9。
2. **passed** — VoiceItemは9件。missing=[]; duplicate=[]; reordered=False。
3. **passed_with_manual_mapping** — linked subtitle textのspeaker/cue match=True; mapping: れいむ -> ゆっくり霊夢; まりさ -> ゆっくり魔理沙 (initial=ゆっくり霊夢)。
4. **passed_with_variance** — order_preserved=True; provisional_exact_durations_preserved=False; 60fps・2790 frames・46.5秒。sampled: csv_row_1=0/273 frames; csv_row_2=273/293 frames; csv_row_9=2317/473 frames。
5. **not_met** — VoiceItem/subtitle lane=True; ImageItem/TextItem placeholder scene laneはない; misleading_final_or_public_ready_claim=False。

次gate: `adapter_correction_after_observation`

Do not render/export. Do not save or write production `.ymmp`. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
