# NLMYTGen Project Cockpit

Project-State-ID: episode-002-verified-local-evidence-operator-batch-ready-v1
State-Revision: 2026-07-12.1
Updated: 2026-07-12 JST
Product-State: episode-002-verified-local-evidence-render-operator-batch-ready
Product-Gate: manual-yymm4-render-batch
Recommended-Next: run-one-yymm4-operator-batch
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むための追跡済みMarkdownです。
内部capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。これらは状態の保存・案内面であり、
開発セッションのPromptやWorker実行権限を定義しません。

## いまの一文

Episode 002は、実観測済みのローカル証拠だけを根拠にした9-cue台本、claim ledger、
canonical/derived CSV、VoiceItem不変のheadless project generator、内部非finalの
static contract、5アクションのone-shot YMM4 Operator Batchまで準備済みです。
次のgateはユーザーが一度だけbatchを実行し、local projectとMP4をcollectorで検証することです。

## 現在の状態

| 対象 | 現在地 | 次に進む条件 | まだ保証しないこと |
| --- | --- | --- | --- |
| source bundle | CSV/diagnostic/runtime/profileの6 tracked sourcesをhash/schema/statusで検証 | source hash drift時はbundleを再生成 | external editorial source、rights approval |
| script/claim | 9/9 cuesにauthorized source pointer、unsupported claim 0、S1/S2/S3=2/2/5 | 新claim追加時は同じprovenance gate | production/public-ready claim |
| CSV | canonical 9行をexplicit profileでspeaker列だけderived 9行へ射影 | operatorがderived CSVをclean YMM4 projectへ一度import | 全YMM4版でのuniversal mapping |
| historical base | 1 timeline / 9 VoiceItemsの構造は健全だが旧dry-run本文 | 新derived CSVから新baseを保存 | VoiceItem text/cacheのheadless置換 |
| project generator | new baseの9 VoiceItemsを不変保持し、3 ImageItems + 3 independent TextItemsを追加 | operator baseがnew CSVと完全一致 | actual YMM4 open/render済み |
| labels | 各sceneに`INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT` | manual reopenでparse/errorと表示異常がないことを確認 | final design、production `.ymmp` |
| operator batch | 5 manual actions、return最大3項目、preflight/syntax passed | userがone-shot batchを実行 | actual MP4、publication、upload |

## 次に使う入口

| 入口 | 解くbottleneck | 選ぶと可能になること |
| --- | --- | --- |
| **Run one operator batch** | headless準備は完了したがactual YMM4 project/render evidenceがない | exact local projectとMP4を一度生成し、`operator_result.json`で構造・hash・MP4 signatureを収集できる |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/operator_batch/README_OPERATOR_BATCH.md`

YMM4に未保存・無関係の作業、update要求、mapping dialog、character mismatch、parse errorが
ある場合はbatchを止めます。成功してもproduction/public/rights/uploadへ自動遷移しません。

## 証拠境界

- Source bundle / claim ledger / script / CSV:
  `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/`
- Headless validation:
  `verified_local_evidence_input_pilot/input_validation_readback.json`
- Static project contract:
  `verified_local_evidence_input_pilot/static_project_readback.json`
- Operator preflight:
  `verified_local_evidence_input_pilot/operator_batch/preflight_readback.json`
- Existing canonical CSV remains SHA-256
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`。
- Actual local `.ymmp`、MP4、actual readback、operator resultはignoredであり、現時点では未生成です。

## 公開境界

このページにはprivate URL、token、raw external source、権利未確認素材、user-home絶対pathを
載せません。actual render、production `.ymmp`、external editorial input、real-media replacement、
rights/legal approval、final thumbnail、upload/publication、default-branch integrationは未完了です。
