# Episode 002 YMM4観測readback

状態: `operator_instruction_only`

実観測は未実行。YMM4 executable は検出されたが、このworkerからGUI import結果を安全に操作・視認する経路がないため、観測passは付けない。

YMM4 executable:
`D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe`

開くもの:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/ymm4_import_ready_preview.html`

importするderived CSV:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/derived_yymm4_import.csv`

canonical source（上書き禁止）:
`production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`

selected character profile:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_character_alias_profiles/ymm4_4_53_0_9_yukkuri_characters_v1.json`

blocker:
YMM4 restored an existing unsaved untitled project containing the prior nine-item, 2790-frame observation state. Starting a clean derived-CSV import would require discarding that existing unsaved state, which this slice does not authorize.

## operatorが返す観測5点

1. CSV import後、cue順がS1 -> S2 -> S3、csv_row_1 -> csv_row_9として読めるか。
2. VoiceItemが9 cue分に見えるか、欠落・重複・順序入れ替わりがあるか。
3. mapping dialogが出ず、れいむ行=ゆっくり霊夢、まりさ行=ゆっくり魔理沙として自動bindingされるか。linked subtitle textがspeaker/cueに一致するか。
4. timing orderは仮timingの流れを崩していないか。duration再計算はinformationalとして記録する。
5. CSV責務がVoiceItem + linked subtitleに限定され、ImageItem/独立TextItemのdiagnostic projectがnot_authorized/not_attemptedのままか。

Do not render/export. Do not save or write production `.ymmp`. Do not start the diagnostic project. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
