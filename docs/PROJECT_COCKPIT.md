# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-standard-gui-batch-observability-validated-v1
State-Revision: 2026-07-27.2
Updated: 2026-07-27 JST
Product-State: standard-production-gui-with-authority-bound-recoverable-batch-read-model
Product-Gate: owner-approved-real-change-set-through-gui
Recommended-Next: execute-one-owner-approved-change-set-through-gui-and-reconcile-effect
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-standard-gui-batch-observability-v1
Handoff-PR: none
Required-Base: 8896bbfa34bfb89febf6e7847738ac2527a4493a
Implementation-Checkpoint: resolved-by-current-branch-tip
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[STANDARD_GUI_BATCH_OBSERVABILITY_2026-07-27.md](verification/STANDARD_GUI_BATCH_OBSERVABILITY_2026-07-27.md)、
機械可読結果は
[STANDARD_GUI_BATCH_OBSERVABILITY_2026-07-27.json](verification/STANDARD_GUI_BATCH_OBSERVABILITY_2026-07-27.json)。

## いまの一文

standard Electron GUIのsecondary `バッチ実行`で、bounded four-package executorの
plan、no-op、authority、failure、effect-unknown、journal、safe resumeを
restart後も観測できる。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Default route | `自動動画生成` | 既存standard loopを維持 |
| Batch route | `バッチ実行` | secondary / serial / one active job |
| Queue | queue-v3 SHA exact | GUIからpackage追加なし |
| Change set | maximum 0 / entries 0 | real mutation authorityなし |
| Actual GUI execute | 4 `verified_noop` | dispatch / authority / write 0 |
| Package state | lifecycle / decision / execution表示 | exact status IDを保持 |
| Authority | exact one-shot preflight | plan/no-opでは消費しない |
| Failure | failed + `skipped_after_failure` | replacement authority待ち |
| Unknown effect | auto retry disabled | read-only reconciliation待ち |
| Journal | event 4 / prefix exact | explicit reopen、auto-resumeなし |
| Restart | `execute` read model復元 | prior no-op redispatch 0 |
| Tracked-only | actual plan/execute readback pass | private/untracked media 0 |
| Runtime | Electron 43 hidden pass | YMM4/render/playback 0 |
| External authority | human / rights / production / public false | technical stateと分離 |

## 次の入口

package ownerが指定したexact real change-setを一件だけGUIのplan-onlyへ読み込み、
queue、descriptor、edge、operation、plan identityを確認する。対応するone-shot
authorityを選択してexecuteし、journal、backend result、lifecycleをreadbackする。
次のgateはGUI polishではない。

## 公開・実行境界

今回のactual executeはzero-changeだけで、real mutating batchは未実施。
content/visual change、fifth topic、YMM4、render、playback、human acceptance、
rights、production、publication、upload、release、PR、merge、master mutation、
deployment、public exposureは未実施・未承認。
