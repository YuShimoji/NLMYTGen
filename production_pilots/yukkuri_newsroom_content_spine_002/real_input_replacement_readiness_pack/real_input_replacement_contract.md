# Episode 002 実入力置換前 operator contract

このcontractは、sample/diagnosticのEpisode 002を実入力へ置換する前に必要なローカル材料だけを定義する。ここでは置換を実行しない。YMM4 import、render/export、production `.ymmp` write、rights/public approval、YouTube uploadも実行しない。

参照元: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack`
cue map: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/edit_slice_to_ymm4_cue_map.json`

| 入力 | stable key | 必要な内容 | Episode 002 cue mapとの関係 |
| --- | --- | --- | --- |
| 元資料ファイル | `local_source_audio_video_or_document_path` | source audio/video/document path | source for S1-S3 narrative and citation placeholders |
| 文字起こし | `local_transcript_or_generation_receipt_path` | transcript path or transcript generation receipt | maps to csv_row_1 through csv_row_9 before replacement |
| 由来と権利メモ | `source_provenance_and_rights_note` | source provenance/rights note | keeps citation/thumbnail/public gates separated from replacement |
| 安定識別子 | `stable_file_identity` | file hash or stable identity expectation | prevents sample/real boundary drift during replacement |
| cue対応 | `episode_002_cue_map_alignment` | expected relation to Episode 002 cue map | 3 scenes / 9 cues must remain traceable |

## 5つの確認

1. source audio/video/document path と transcript path または transcript generation receipt path が、ローカルで開ける場所として示されている。
2. provenance/rights note はreview用メモであり、public-ready approvalやlegal acceptanceを主張していない。
3. hash、file size、modified time、export receiptなど、stable identityとして再確認できる情報がある。
4. Episode 002 cue map のS1-S3またはcsv_row_1-9へ、どの範囲が対応するかが書かれている。
5. live fetch、scraping、external media download、YMM4 import/render、`.ymmp` writeはこの段階で行っていない。

次に作るべきものは `validated_local_input_receipt_for_episode_002`。実ファイルが入るまでは real input replacement は未実行のままにする。
