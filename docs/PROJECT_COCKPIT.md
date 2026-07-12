# NLMYTGen Project Cockpit

Project-State-ID: episode-002-verified-local-evidence-internal-render-validated-v1
State-Revision: 2026-07-12.2
Updated: 2026-07-12 JST
Product-State: episode-002-verified-local-evidence-internal-render-validated
Product-Gate: milestone-integration-audit
Recommended-Next: audit-feature-branch-integration-after-render-milestone
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むための追跡済みMarkdownです。
内部capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

Episode 002のverified-local-evidence pilotは、実際のlocal YMM4 projectと
約59.38秒のMP4について、hash整合、project構造、ISO-BMFF、H.264/AAC stream、
全編video/audio decodeを確認し、内部レビュー用proxyとtracked review packageまで
整備済みです。次はfeature branchをmergeせずに行うmilestone integration auditです。

## 現在の状態

| 対象 | 現在地 | 次に進む条件 | まだ保証しないこと |
| --- | --- | --- | --- |
| source/script | 9/9 cuesがauthorized pointersへ接続、S1/S2/S3=2/2/5 | source/hash drift時は再検証 | external editorial/rights approval |
| local project | 3563 frames、9 VoiceItems、3 ImageItems、3 TextItems、speaker 3/6をparse | 別環境利用時はprofile/path portabilityを再確認 | production `.ymmp` |
| original MP4 | 1920x1080/60 fps、H.264/AAC、59.383008秒、全編decode passed | humanが5問review sheetで内容を判断 | visual/editorial acceptance |
| review proxy | 1280x720/60 fps、H.264/AAC、全編decode passed、originalは不変 | review後もmaster扱いしない | production master |
| operator batch | success resultをbyte-for-byte保持し、UTF-8/collect-only/misnamed JSONをhardening | 将来のbatchは同collector contractを使う | 全YMM4版でのportable execution |
| review package | receipt、traceability、correction report、review sheet、limitationsがprimary | bounded integration audit | merge/publication/upload |

## 次に使う入口

| 入口 | 解くbottleneck | 成果 |
| --- | --- | --- |
| **Milestone integration audit** | feature branchの証拠・privacy・authority・target riskを未監査 | merge/rebaseを行わずintegration recommendationを返す |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/README_INTERNAL_REVIEW.md`

## 証拠境界

- Machine evidence:
  `verified_local_evidence_input_pilot/render_validation_readback.json`
- Receipt/traceability:
  `verified_local_evidence_input_pilot/render_receipt.json`、
  `verified_local_evidence_input_pilot/source_to_output_traceability.json`
- Human review:
  `verified_local_evidence_input_pilot/operator_review_sheet.md`
- Original MP4、proxy、local `.ymmp`、operator resultはignored。tracked receiptには
  repo-relative label、hash、size、検証結果だけを残します。

## 公開境界

このページにはprivate URL、token、raw external source、user-home絶対pathを載せません。
valid renderはproduction/public/rights/creative acceptanceを意味しません。external editorial input、
real-media replacement、final thumbnail、upload/publication、default-branch integrationは未完了です。
