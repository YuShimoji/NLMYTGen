# Bounded Factory Queue Executor Validation — 2026-07-27

## Outcome

queueが返すtechnical decisionを手動で単体advancementへ翻訳していた状態から、
versioned change-set、exact one-shot authority、deterministic serial executor、
append-only journal、resume contractを持つchange-only batchへ進めた。

sourceは`995728f8e04c25b702d628a95e73e2801964f964`、成果branchは
`codex/nlmytgen-bounded-factory-queue-executor-v1`。

## Contracts and public command

- change-set: `nlmytgen.factory_queue.change_set.v1`
- authority set: `nlmytgen.factory_queue.execution_authority_set.v1`
- authority record: `nlmytgen.factory_queue.execution_authority.v1`
- journal: `nlmytgen.factory_queue.execution_journal.v1`

公開入口:

```powershell
uv run python -m src.cli.main execute-factory-queue `
  --queue production_pilots/factory_queues/four_package_lifecycle_queue_v3.json `
  --change-set production_pilots/factory_queues/four_package_zero_change_set_v1.json `
  --execute --format json
```

既定はplan-only。正常なplanまたは完了batchはexit 0、contract、authority、
resume、execution failureはexit 1。mutating entryはqueue orderで一件ずつ処理し、
各backend effect直前にqueue、descriptor、content、render settings、output、
lifecycle、authorityを再読込・再hashする。

## Current four-package execution

`four_package_zero_change_set_v1.json`はqueue-v3 SHA
`214d5e99...927`へexactに束縛され、maximum mutation 0、entry 0。

execute modeを2回実行し、結果はbyte-equivalentだった。

- queue evaluation: `cc8a5ca4...b9c`
- plan identity: `0d07e9bb...1fa`
- execution receipt: `56f26d1b...217`
- packages validated: 4
- `verified_noop`: 4
- authority consumption / backend dispatch: 0 / 0
- source generation / render / product write / private copy: 0
- YMM4 / Electron / render driver / ffmpeg / playback / volume: 0

execute modeのzero-changeはerrorではなく、実際に4 packageを再検証した
zero-mutation successである。completed packageはadvancement backendへ渡らない。

## Authority and journal behavior

plan-onlyとno-op validationはauthorityを消費しない。mutating entryはpackage、
descriptor SHA、queue/change-set SHA、content/render/output identity、lifecycle edge、
operation、authority IDをexactに束縛する。

authorityはbackend呼出し直前にlocal authority recordを原子的に`consumed`へ
更新し、成功後に`started` eventを記録する。同じauthority fileをjournalなしで
再投入しても再利用できない。
既知のnon-effect failureは`failed`を追記し、後続を
`skipped_after_failure`にする。resumeは同じplanとevent prefixを保持し、
成功済みentryを再dispatchしない。failed entryは元authorityを置換する新しい
exact authorityで成功した場合だけ後続へ進む。`effect_unknown`はread-only
reconciliationがない限り自動再試行しない。

## Synthetic and tracked-only evidence

isolated synthetic fixtureで、authorized entry一件のdispatch 1、no-op dispatch 0、
failure後の後続dispatch 0、resume時のprior success skip、replacement authority、
append-only event prefixを確認した。実package、project、MP4、queueは変更していない。

短いtracked-only worktreeではprivate directoryとMP4が0のまま、4件すべて
`recorded_complete_no_live_file`、mutating entry / dispatch / private copy 0。
receipt SHAは`8f9621a7...e38f`。temporary worktreeは回収済み。

## Validation and preservation

executor focused 35件、queue / Contract v2.0 / v2.1 / source promotion /
render promotionを含むfocused 153件が合格した。modified Python compile、
JSON parse、state sync、diff checksをcloseout gateとする。canonical Regression
Integrityはoutcome commit後に一度だけ実行する。

開始時に16 factory package descriptors、queue-v1/v2/v3、102 project/MP4の
集合identityを固定した。executorのwrite scopeにはこれらを含めていない。

## Boundary and next stage

実mutating multi-package batchは実施していない。content、script、source、
visual、crop、subtitle、human acceptance、rights、production、publication、
upload、release、fifth topic、PR、merge、master、deploymentも範囲外である。

次の技術stageは、このbounded executorをstandard production GUIへ接続し、
plan identity、package state、authority待ち、failure、resume可能位置を
recoverable batch stateとして観測可能にすること。GUI接続も同じserial /
change-only / no-rerender contractを維持する。
