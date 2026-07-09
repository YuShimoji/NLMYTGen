# Episode 002 YMM4観測readback

状態: `operator_instruction_only`

実観測は未実行。YMM4 executable は検出されたが、このworkerからGUI import結果を安全に操作・視認する経路がないため、観測passは付けない。

YMM4 executable:
`C:\Users\PLANNER007\Downloads\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe`

開くもの:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/ymm4_import_ready_preview.html`

import候補CSV:
`production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`

blocker:
YMM4 executable was detected locally, but this worker has no safe manual/GUI visual readback channel for importing and inspecting the project.

## operatorが返す観測5点

1. CSV import後、cue順がS1 -> S2 -> S3、csv_row_1 -> csv_row_9として読めるか。
2. VoiceItemが9 cue分に見えるか、欠落・重複・順序入れ替わりがあるか。
3. subtitle/textがspeakerとcueに対応し、sample/diagnostic textであることが誤解なく見えるか。
4. timing orderは仮timingの流れを崩していないか。
5. visual/overlay/citation/thumbnail要素がplaceholder境界として読め、final素材やpublic-readyを示していないか。

Do not render/export. Do not save or write production `.ymmp`. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
