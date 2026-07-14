# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-editorial-provenance-audited-visual-selection-ready-v1
State-Revision: 2026-07-14.2
Updated: 2026-07-14 JST
Product-State: new-banknote-script-lineage-audited-visual-direction-review-ready
Product-Gate: human-visual-direction-selection
Recommended-Next: select-new-banknote-visual-direction-with-lineage
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むtracked summaryです。短期capsuleは
[runtime-state.md](runtime-state.md)、履歴は[project-context.md](project-context.md)、
task経路は[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

承認済み9 cueの本文を変えず、claim/source由来、Workerの編集操作、判断権限、
現在のユーザー承認、prior user scriptの未証明範囲を9/9 cueで可視化しました。
次のgateはprovenanceを見ながら行うA/B/C visual-direction selectionです。

## 判断に使える現在地

| 対象 | 確定したこと | 判断に残る境界 |
| --- | --- | --- |
| cue lineage | 9/9、425文字を40の非重複segmentで被覆、15 adopted claims、20 factual units、raw fingerprintsと4 official sources | token-level authorshipは主張しない |
| editorial contribution | 19 single-source paraphrases、1 multi-source synthesis、9 bridges、9 voice units、38/38 realized | operation labelsはGit delta/receiptからのreview分類 |
| prior user script | raw Audio Overview transcript利用は証明、finished script候補はなし | repo外にしかなかったartifactの不使用は証明できない |
| approval | current execution contractで現在の9 cue継続を記録 | 独立した同時点receiptはなく、future silent editsも未許可 |
| content lock | script/CSV/trace/claim/YMM4/visualの24 identityが一致 | substantive deltaはlock無効化とsuccessor approvalが必要 |
| visual routes | A推奨、B/C比較を維持 | A/B/Cはいずれも未選択・未実装 |
| review surfaces | canonical/visualの4面からprovenanceへ到達 | metadata link以外のcontent/route deltaなし |
| local YMM4 evidence | tracked receipt/readback identityはlock済み | ignored project/resultは現checkoutに無くlocal再検証は未実施 |

Primary provenance surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/editorial_provenance/README_EDITORIAL_PROVENANCE.md`

Visual decision surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/visual_scene_decision/visual_direction_board.html`

## 次の入口

provenance READMEを確認してからHTML boardを開き、A / B / C、またはscene/cue ID付き
修正を返します。同時にS1/S2/S3の流れ、誤解を招く模式図、motionの抑制度だけを
判断します。選択後の別sliceでのみdiagnostic YMM4 visual projectを検討します。

## 公開・実行境界

No script rewrite, NotebookLM, web fetch, YMM4, Computer Use, route selection,
visual implementation, render, production, rights approval, upload, publication,
or master integration occurred in this slice.
