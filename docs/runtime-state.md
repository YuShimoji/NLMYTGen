# Runtime State — NLMYTGen

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

## Current Slice

- 既定`自動動画生成`を維持し、secondary route `バッチ実行`へbounded executorを
  接続した。
- Queue / Change Set → Execution Plan → Package States → Authority and Start →
  Journal / Recovery → Resultの一画面でoperator stateを表示する。
- queue-v3 + zero-change setのactual planとexecuteは4件`verified_noop`、
  mutating entry / authority consumption / backend dispatch / writeが0。
- package rowはlifecycle、technical decision、operation、authority、execution、
  reason、resume effectをexact status ID付きで表示する。
- plan-onlyとno-opはauthority不要。mutating executeはexact one-shot authority
  preflight成功までdisabled。failed resumeはreplacement authorityを要求する。
- `effect_unknown`はblockedで、自動retryとnormal resumeを許可しない。
- journalは明示的にopenし、application restart後も同じplanとevent prefixから
  `execute` read modelを復元する。auto-resumeはしない。
- standard loopとbatchは同じone-active-job boundaryを共有し、240行log、
  elapsed、project-owned process cancellationを維持する。

## Product Position

CLIだけにあったbounded serial executorがstandard production GUIでoperator
observableになった。現在のreal four-package queueは`変更はありません`として
安全に完了し、completed packageをbackendへdispatchしない。

operatorはno-op、authority wait、running、known failure、
`skipped_after_failure`、`effect_unknown`、safe resume位置をterminal JSONの
手動解釈なしで区別できる。GUIはpackage、operation、authority recordを生成せず、
executorのrepo-relative locator、exact identity、serial、append-only、
no-hidden-worker契約を維持する。

content、source、claims、canonical script、images、crops、subtitles、creative
review、rights reviewは別Web supervision threadが所有する。technical GUI stateは
human acceptance、rights、production、publication authorityを付与しない。

## Exact Next Action

owner-approved real change-setを一件だけGUIへ読み込み、plan-onlyでqueue、
change-set、descriptor、lifecycle edge、operation、plan identityを確認する。
対応するexact one-shot authorityを選択し、mutating execute後にjournal、
backend result、package lifecycleをreadbackしてeffectを照合する。

開始条件:

- package ownerがreal change-setとexpected effectを明示している
- queue / descriptor / content / render / output identityがplanとexact
- authorityは対象package / edge / operation / queue / change-setにone-shot束縛
- content、rights、production、publicationの各owner判断をtechnical authorityへ
  混ぜない
- failure時はserial stop、replacement authority、same journal prefixを維持
- `effect_unknown`時は自動retryせずread-only reconciliationへ移る

## Residual Work

### Owner-approved real change-set through GUI

- Purpose: validated GUI→executor pathで最初のreal package effectを一件に限定する。
- Effect: technical lifecycleをowner指定edgeへ進め、resultとjournalを照合できる。
- Requirements: exact change-set、one-shot authority、package owner承認、
  pre/post identity readback。
- State: GUI、plan、zero-change、authority/recovery read modelはvalidated。
  real mutating batchは未実施。
- Owner: package owner / supervising AI / technical executor operator。
- Next move: ownerが指定した一件をplan-onlyで確認し、authority発行後に実行する。

### Content, rights, and public gates

- Purpose:technical executionとeditorial/creative/legal/public判断を分離する。
- Effect: lifecycle stateから未承認の採用・公開判断が暗黙継承されない。
- Requirements: separate Web supervision result、human acceptance、rights、
  production/publication owner判断。
- State:今回のcontent/visual変更、human acceptance、rights/public actionは0。
- Owner: content supervisor / human reviewer / rights / production owners。
- Next move: technical changeがcontent/visual identityへ触れる場合だけ各ownerへ戻す。

## Evidence and Re-entry

- GUI module: `gui/batch_observability.js`
- Renderer: `gui/batch_renderer.js`
- Queue: `production_pilots/factory_queues/four_package_lifecycle_queue_v3.json`
- Change set:
  `production_pilots/factory_queues/four_package_zero_change_set_v1.json`
- Report:
  `docs/verification/STANDARD_GUI_BATCH_OBSERVABILITY_2026-07-27.md`
- Machine receipt:
  `docs/verification/STANDARD_GUI_BATCH_OBSERVABILITY_2026-07-27.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file。
Restore with `uv sync --extra dev --locked` and `cd gui; npm ci` if dependencies
are absent。Start with `npm start` → `バッチ実行` → plan-only。

## Active Boundaries

- 既存package descriptors、queue-v1/v2/v3、contracts、projects、MP4、receipts、
  media、locks、ignored failed runsはimmutable。
- real package mutation、YMM4、render driver、ffmpeg encode、media generation、
  playback、volume、private copyは今回0。
- fifth topic、content/visual revision、human acceptance、rights、production、
  publication、upload、release、PR、merge、master mutation、tag、deploymentは未実施。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
