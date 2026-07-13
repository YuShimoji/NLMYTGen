# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-yymm4-import-operator-batch-ready-v1
State-Revision: 2026-07-13.6
Updated: 2026-07-13 JST
Product-State: new-banknote-source-backed-script-yymm4-import-batch-ready
Product-Gate: manual-yymm4-import-observation
Recommended-Next: run-new-banknote-yymm4-import-operator-batch
External-State: public-repo-feature-branch

このページは public repository で現在地を読むための追跡済み Markdown です。
短期 capsule は [runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task 経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipeline は
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd) にあります。

## いまの一文

公式一次資料へtraceできる承認済み9 cueとCSV pairを変えずに、ユーザーが一度だけ
YMM4 importを行い、保存したlocal projectをheadless collectorで検証できる
Operator Batchをpreflight済みにしました。次のgateはmanual import observationであり、
production、render、rights、publicationの承認ではありません。

## レビュー判断に使える現在地

| 対象 | 現在状態 | 判断に残る境界 |
| --- | --- | --- |
| official sources | 13 captures、182/182 claims adjudicated、verified-primary 19 | S04 generation-time byte identityとexact S05 572KB identityはreview debt。採用claimの支持は維持 |
| approved script | 9 cues、scene 2/4/3、canonical speaker 3/6、unsupported spoken claim 0 | spoken cuesは今回変更していない。user creative acceptanceは未主張 |
| CSV | canonical / derived 9 rows、text/order同一、speaker列だけ3/6へ射影 | actual YMM4 mapping、sound、timing、subtitle appearanceは未観測 |
| supervisor gate | bounded YMM4 import-observation用batch準備をpass | production、render、rights、publication承認ではない |
| operator batch | 4 manual actions、return最大3、preflight / collect-onlyはlaunch 0 | normal modeだけが後でuser controlのYMM4を起動する |
| collector | fresh exact local project、9 VoiceItems、3/6、exact text/order、missing/duplicate 0を検証 | ImageItem、independent TextItem、render、MP4は不要 |
| runtime compatibility | installed 4.54.0.1、profile observation 4.53.0.9 | version差はwarning。mapping dialog / wrong characterはstop |
| privacy | tracked artifactはrepo-relative identityのみ | .local.ymmp、result、executable path/stateはignored local_outputsのみ |

Primary operator surface:
production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/operator_batch/README_OPERATOR_BATCH.md

## 次の入口

unrelated / unsaved YMM4 workを安全に閉じ、operator directoryで
run_new_banknote_yymm4_import_batch.ps1を一度だけ実行します。ユーザーだけが
新規空projectへのCSV import、exact local save、safe close、terminalへのCOLLECT入力を
行います。collector成功後にだけ、source-backed S1/S2/S3 visual/scene decisionへ進めます。

## 公開・実行境界

No NotebookLM access, source fetch, YMM4 launch, Computer Use, actual
new-banknote project, render, production, rights approval, upload, publication,
or master integration occurred in this slice.
