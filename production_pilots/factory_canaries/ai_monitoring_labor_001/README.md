# AIによる職場モニタリング 第三トピック factory canary

このpackageは、固定題材「AIによる職場モニタリングと働く人への影響」を、
既存の標準Electron GUIと動画生成pipelineへ通す第三の実トピック技術検証である。

## 固定shape

- cues: 5
- scenes: 2
- speakers: れいむ 2 / まりさ 3
- target duration: 25–40秒
- profile: 1920x1080 / 60fps
- visuals: 公式一次資料から得た5点の異なるraster page

## Tracked authority

- `source_registry.json`: 公式一次資料3件と取得境界
- `claim_adjudication.json`: 発話事実の採否と根拠位置
- `source_support_edges.json`: cueからclaim/sourceへの結合
- `transformation_ledger.json`: 題材から短い日本語台本への変換記録
- `canonical_script.json` / `.txt`: canonical script
- `canonical_yymm4.csv`: canonical speaker label
- `derived_yymm4_import.csv`: 端末で観測済みのYMM4 character label
- `real_media_provenance.json`: 5点の公式raster素材の由来と権利境界
- `auto_video_pipeline/ai_monitoring_labor_episode_manifest.json`: 実行契約
- `technical_validation_receipt.json`: 技術検証結果
- `three_topic_variation_receipt.json`: 三題材間の限定的variation結果

## Ignored local evidence

- `source_cache/`: 取得した公式PDF、ページrender、抽出補助
- `source_extracts/`: bounded text extract
- `auto_video_runs/`: source project、素材実体、generated project、MP4、frame、GUI receipt

これらのlocal evidenceはGitへ追加しない。URLをファイル名にせず、固定の安全な
basenameだけを使う。

## Boundary

このcanaryは`internal_factory_canary_not_human_accepted`である。技術検証の成功は、
human creative acceptance、素材権利、production、publication、external upload、
release、PR、merge、master integrationを承認しない。
