# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-three-run-operator-repeatability-validated-v1
State-Revision: 2026-07-26.1
Updated: 2026-07-26 JST
Product-State: two-topic-factory-with-clean-gui-zero-intervention-repeatability
Product-Gate: third-topic-variation-validation
Recommended-Next: run-third-real-topic-with-new-cue-scene-speaker-time-shape
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-three-run-operator-repeatability-v1
Handoff-PR: none
Required-Base: da88ad52d9157da9be3d40a56567d80a1b9f025b
Implementation-Checkpoint: 2d5c4f34c8b88070075a2678a08d9a72fafa9f31
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; ignored/private runs preserved

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[THREE_RUN_OPERATOR_REPEATABILITY_2026-07-26.md](verification/THREE_RUN_OPERATOR_REPEATABILITY_2026-07-26.md)、
機械可読集約は
[three_run_repeatability_receipt.json](../production_pilots/factory_canaries/real_estate_reins_transparency_001/three_run_repeatability_receipt.json)、
判断履歴は[project-context.md](project-context.md)。

## いまの一文

new-banknoteとREINSの2実トピックを一つのfactory contractで処理し、REINSは
clean Electron 43 GUIから3回連続zero-intervention render、identity一致、
completed-run no-op resumeまで実証した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Final series | `v3_01` / `02` / `03`、同一checkpoint | 旧run・failure保持 |
| GUI | doctor 4/4、protected 9/9、dry-run、実render pass | bypass/double false |
| Operation | manual / Computer Use / injection / SendKeys 0 | silent、playback 0 |
| Determinism | content/project/MP4/asset/cue semantic SHA一致 | raw project差はrun pathだけ |
| Cleanup | owned process residue各run 0 | pre-existing process不変 |
| Resume | GUI 1.4881秒、CLI `verified_noop` | 26 files SHA/size/mtime不変 |
| Drift | isolated render-setting driftを拒否 | real/private output不変 |
| Accepted cut | new-banknote 4 identity exact | human acceptance不変 |
| Prior REINS | source/project/MP4/GUI receipt exact | internal canary |

## 次の入口

第3実トピックを、7/9 cues、3/4 scenes、既存speaker分布、45/73秒と異なるshapeで
normal GUIへ通す。official sourceとclaim edgeを先に固定し、新しいrun identityで
doctor → dry-run → YMM4 render → receiptを完走する。既存2トピックとv3
repeatability identityを同時に再確認する。

## 公開・実行境界

現在の成果はtechnical internal-review evidenceである。creative acceptance、
rights、production、publication、upload、release、PR、merge、master mutation、
deployment、access changeは各ownerの明示判断を待つ。
