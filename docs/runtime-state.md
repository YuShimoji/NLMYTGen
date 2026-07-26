# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-bounded-factory-queue-executor-validated-v1
State-Revision: 2026-07-27.1
Updated: 2026-07-27 JST
Product-State: four-package-authority-bound-change-only-executor-with-noop-elision-and-resumable-journal
Product-Gate: standard-gui-queue-batch-observability
Recommended-Next: connect-bounded-executor-to-standard-production-loop-gui-with-recoverable-batch-state
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-bounded-factory-queue-executor-v1
Handoff-PR: none
Required-Base: 995728f8e04c25b702d628a95e73e2801964f964
Implementation-Checkpoint: 995728f8e04c25b702d628a95e73e2801964f964
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- `execute-factory-queue`はversioned change-setをplan-only既定で読み、
  queue orderに沿ってbounded serial executionを行う。
- change-setはqueue、descriptor、content、render settings、completed output、
  target、lifecycle edge、operation、authority IDをexactに束縛する。
- mutating effect直前にqueueと全identityを再読込・再hashし、drift時は
  authorityを消費せず停止する。
- one-shot authorityはbackend invocation直前にlocal control recordを原子的に
  consumedへ更新する。plan-onlyとcompleted/no-op validationは消費しない。
- journalはpackageごとのplanned / validated / started / succeeded / failed /
  effect_unknown / skipped historyをappend-onlyで保持する。
- known non-effect failureは後続を停止する。resumeはprior successをskipし、
  failed entryへreplacement authorityを要求する。effect_unknownは自動再試行しない。
- queue-v3のzero-change executeは4件`verified_noop`、mutating entry、
  authority consumption、backend dispatch、product/private writeがすべて0。
- tracked-onlyは4件`recorded_complete_no_live_file`。private欠落から
  source generationやrenderを予定しない。

## Product Position

4 package queueはtechnical decisionからbounded executionまで接続された。
completed packageとreceipt-only packageはadvancement backendへ渡らず、
明示されたchange-set内のmutating entryだけがexact one-shot authorityで進める。

executorは直列、有限、append-only、resumableである。worker pool、daemon、
database、background scheduler、arbitrary command、external/public actionを
実行契約に含めない。

実mutating multi-package executionは未実施。contentとvisual workは別の
Web supervision threadが所有し、technical queue stateからhuman acceptance、
rights、production、publication authorityは継承しない。

## Exact Next Action

bounded executorをstandard production loop GUIへ接続し、recoverable batch
stateを観測可能にする。

開始条件:

- GUIはplan identity、queue/change-set identity、package stateを表示する
- no-op / not-selected / authority-wait / running / failed / effect-unknown /
  resumable位置をjournalから表示する
- GUIから任意packageやoperationを追加しない
- execute前にexact authority fileとchange-setを再確認する
- restart後も同じjournal prefixを保持し、prior successを再実行しない
- render、playback、public actionは別authority gateに残す

## Residual Work

### GUI batch observability

- Purpose: operatorがserial batchの現在位置と安全なresume地点を一画面で把握する。
- Effect: terminal JSONを手で解釈せず、no-op、authority待ち、failureを区別できる。
- Requirements: journal read-only ingest、exact plan display、recoverable state、
  execute confirmation、no hidden worker。
- State: executorとjournal contractはvalidated。GUI接続は未実装。
- Owner: standard production GUI maintainer / supervising AI。
- Next move: synthetic journalとreal zero-change receiptをGUI read modelへ接続する。

### Real change-set and external gates

- Purpose:将来のowner-approved package changeをtechnical batchへ安全に渡す。
- Effect: exact一件または有限batchをchange-onlyで進められる。
- Requirements: real package用change-set、one-shot authority、content/rights/
  production owner判断、effect後readback。
- State: synthetic mutationだけを実行。real mutating batchは未実施。
- Owner: package owner / human reviewer / rights / production owners。
- Next move: owner-approved changeが発生した時点でexact identityへauthorityを発行する。

## Evidence and Re-entry

- Queue: `production_pilots/factory_queues/four_package_lifecycle_queue_v3.json`
- Change set:
  `production_pilots/factory_queues/four_package_zero_change_set_v1.json`
- Executor: `src/pipeline/factory_queue_executor.py`
- Report:
  `docs/verification/BOUNDED_FACTORY_QUEUE_EXECUTOR_VALIDATION_2026-07-27.md`
- Machine receipt:
  `docs/verification/BOUNDED_FACTORY_QUEUE_EXECUTOR_VALIDATION_2026-07-27.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file。
Restore with `uv sync --extra dev --locked`。Use `execute-factory-queue` without
`--execute` for the first read-only plan。

## Active Boundaries

- 既存package descriptors、queue-v1/v2/v3、contracts、projects、MP4、receipts、
  media、locks、ignored failed runsはimmutable。
- current zero-change executionはreal mutation authorityを付与しない。
- YMM4、Electron、render driver、ffmpeg encode、playback、volume、product write、
  private copyは今回0。
- human acceptance、rights、production、publication、upload、release、fifth topic、
  PR、merge、master mutation、tag、deploymentは未実施。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
