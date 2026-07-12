# Episode 002 Internal Review

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

既存のYMM4出力を再renderせず、project構造、original MP4のcontainer/codec、decode、軽量proxyをheadlessで検証した内部レビュー面です。成功はproduction、公開、権利承認、upload、default-branch統合を意味しません。

## まず見るもの

- 軽量review proxy（推奨）: `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/local_outputs/episode_002_verified_local_evidence_internal_review.proxy.mp4`
- immutable original render: `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/local_outputs/episode_002_verified_local_evidence_internal_review.mp4`
- local internal project: `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/local_outputs/episode_002_verified_local_evidence_internal_review.local.ymmp`
- human review questions: [operator_review_sheet.md](operator_review_sheet.md)

originalとproxyはignored local binaryでありcommitしません。originalは上書きされていません。proxyはoriginalより約1272.637倍小さく、size reductionは99.921423%です。

## Machine-verified

- container/brands: `mov,mp4,m4a,3gp,3g2,mj2` / `['isom', 'iso2', 'avc1', 'mp41']`
- video: `h264`, 1920x1080, 60.0 fps
- audio: `aac`
- duration: 59.383008 seconds
- streams: 2
- original SHA-256: `ACF2E8B284E7956529F8170B6BA5EC55CBC0A4B511DCF56E579087051DA00BAE`
- proxy SHA-256: `45BD0A060BAA45C1BB44068F4ADAE1A6B50DBBF86FABA70F3A1761809BE5A025`
- original/proxy decode smoke: passed

## Evidence grades

- **verified**: file identity、YMM4 project structure、ISO BMFF、ffprobe metadata、decode smoke。
- **observed**: operatorによるYMM4操作、YMM4 version、出力時に「MPEG」へ変更したという報告。
- **inferred**: originalが大きい主因はverifiedな高video bitrateであること。
- **unknown**: human playback quality、visual/editorial acceptance、encoded media内の9 cue意味一致。

## Evidence map

- [render_validation_readback.json](render_validation_readback.json): machine validation
- [render_receipt.json](render_receipt.json): adjudicated receipt
- [source_to_output_traceability.json](source_to_output_traceability.json): source → cue → CSV → VoiceItem → render boundary
- [operator_batch_correction_report.json](operator_batch_correction_report.json): future batch hardening
- [limitations.md](limitations.md): remaining debt and boundaries

次のproduct gateはfeature/default integration auditです。このREADMEはそのauditの固定内部証拠であり、統合そのものを実行済みとは主張しません。
