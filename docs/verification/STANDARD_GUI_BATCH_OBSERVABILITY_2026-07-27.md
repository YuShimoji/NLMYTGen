# Standard GUI Batch Observability Validation — 2026-07-27

## Outcome

bounded queueをterminal JSONで解釈していた状態から、既存Electron標準GUIの
secondary route `バッチ実行`でplan、package state、authority、journal、
recovery、resultを一続きに読める状態へ進めた。既定routeは
`自動動画生成`のまま変更していない。

sourceは`8896bbfa34bfb89febf6e7847738ac2527a4493a`、成果branchは
`codex/nlmytgen-standard-gui-batch-observability-v1`。outcome commitは
current branch tipから解決する。

GUIは次で起動する。

```powershell
cd gui
npm start
```

起動後、headerの`バッチ実行`を選ぶ。画面はQueue / Change Set、
Execution Plan、Package States、Authority and Start、Journal / Recovery、
Resultの縦順で、queue identity、change-set identity、plan状態、変更対象数、
primary actionを最初のviewportに置く。

## Actual queue and zero-change execution

実bridgeは公開CLI `execute-factory-queue`を任意shell入力なしで呼ぶ。
plan-onlyは`--execute`を付けず、executeはGUIで確定したselection tokenから
repo-relative locatorだけを組み立てる。

- queue: `four_package_lifecycle_queue_v3.json`
- queue SHA: `214d5e99...927`
- change-set: `four_package_zero_change_set_v1.json`
- change-set SHA: `0d846817...724`
- queue evaluation: `cc8a5ca4...b9c`
- plan identity: `0d07e9bb...1fa`
- plan receipt: `50d4737b...c8c`
- zero-change execution receipt: `56f26d1b...217`
- GUI execution-result identity: `cf7d21bc...5bf`

actual hidden Electron pathでplan-onlyと許可されたzero-change executeを行った。
結果は`変更はありません`、4 package validation、4 `verified_noop`、
mutating entry 0。authority consumption、backend dispatch、source generation、
render、YMM4、ffmpeg、playback、system volume、private copy、product write、
public actionはすべて0だった。

GUIの行表示は次のとおり。

| Package | Lifecycle | Decision / Execution | Authority | Resume |
| --- | --- | --- | --- | --- |
| `new_banknote_security_notebooklm_001` | `human_accepted` | `verified_noop` | `not_required` | 再実行しない |
| `real_estate_reins_transparency_001` | `rendered` | `verified_noop` | `not_required` | 再実行しない |
| `ai_monitoring_labor_001` | `rendered` | `verified_noop` | `not_required` | 再実行しない |
| `food_expiry_labels_001` | `rendered` | `verified_noop` | `not_required` | 再実行しない |

## Authority, failure, and recovery

read modelは`not_required`、`required`、`absent`、`invalid`、`available`、
`consumed`、`replacement_required`、`reconciliation_required`を区別する。
mutating executeはqueue path/SHA、change-set ID/SHA、package ID/path/SHA、
lifecycle edge、operation、one-shot count、constraints、authority statusが
exactなときだけ有効になる。failed resumeでは使用済みIDと異なるexact
replacement authorityを要求する。executorもeffect直前に同じ契約を再確認する。

plan-onlyとno-opはauthorityを選ばず、消費もしない。authorityとresume journalは
executor contractに合わせrepo-relative locatorだけをCLIへ渡す。GUIはauthority
recordを生成・編集せず、standing authorityをsettingsへ保存しない。

synthetic isolated read modelでauthority wait、running、succeeded、failed、
`skipped_after_failure`、`effect_unknown`、safe resumeを表示した。
`effect_unknown`はblockedとなり通常resumeを無効化する。journalのplan/order/
descriptor mismatchは拒否し、long package IDと長い日本語errorは省略と折返しで
viewport内へ収める。synthetic stateは実packageを変更していない。

actual execute journalはidentity `da8b8a54...9cbc`、event 4、prefix
`e1dc3a2b...7b5d`。明示的に「直近の Journal を開く」を選ぶまでauto-resume
しない。runtime stateを消去してrendererを再loadし、planを再確認してから
local journalを再読込した結果、read modelは`execute`へ戻り、同じprefixを
保持した。completed/no-op entryのredispatchは0。

## Runtime and tracked-only evidence

Electron 43.2.0 / Chrome 150.0.7871.129 / Node 24.18.0の実main、
production preload、renderer、Python bridgeをhidden/offscreen・silentで実行した。
1280×720と1920×1080の両方でfirst viewport contract、logical keyboard order、
11px table text、横overflowなしを確認した。console、security、load、preload、
renderer crash、unhandled errorは0。window表示、focus takeover、audio/video
playbackは発生していない。完了後のproject-owned process residueは0。

- 1280×720 screenshot SHA: `db3dc574...ce3`
- 1920×1080 screenshot SHA: `c61356ce...51f`

短いdetached tracked-only worktreeを通常checkoutとして作り、独立`.venv`で
actual planとzero-change executeを再実行した。untracked/private project/mediaは
0で、GUI read modelは4 package、4 `verified_noop`、mutation 0、
`変更はありません`を返した。一時worktreeは回収済み。

## Validation and preservation

batch/standard JavaScript 22件、GUI/IPC/Electron/Factory executor/queue/
Contract v2.0/v2.1/source promotion/render promotion Python 173件、
batch hidden Electron、Electron 43 compatibilityが合格した。
標準production hidden smokeはpre-commitのtracked diffをruntime doctorが
正しく検出して3 profileを閉じたため、clean outcome commit後に再実行する。
canonical Regression Integrityもoutcome commit後に一度だけ実行する。

開始時に固定した16 factory descriptors、queue-v1/v2/v3、102 project/MP4の
集合identityは維持した。`uv.lock`と`gui/package-lock.json`もbyte exact。
protected untracked/ignored/private evidence、既存worktree、既存user processは
stage、削除、上書きしていない。

## Claim boundary and next gate

今回の実executeはzero-changeだけであり、real mutating batchを実行していない。
content、script、source、image、crop、subtitle、visual、fifth topic、human
acceptance、rights、production、publication、upload、release、PR、merge、
master mutation、deploymentも行っていない。

次の技術gateはGUI polishではない。package ownerが作成したexact real change-setと
対応するone-shot authorityを受け、GUI planでidentityとeffectを確認し、一件の
owner-approved changeを実行後readbackで照合する。その時点でもcontent/visualと
human・rights・production・public authorityは別ownerのgateに残る。
