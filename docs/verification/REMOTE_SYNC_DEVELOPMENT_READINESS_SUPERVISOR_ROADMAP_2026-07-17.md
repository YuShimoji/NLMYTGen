# 監修AI向け・リモート同期、開発再開性、長期目標の現状報告（2026-07-17 JST）

この文書は、リモート上の最新再開ハンドオフをローカルへ取り込み、NLMYTGenを
次の実装へ進められる状態か確認した時点証跡です。現在位置とnext actionの正本は
[`runtime-state.md`](../runtime-state.md)です。本書は同端末のignored証跡を公開物へ
昇格させず、visual、render、production、rights、publicationを承認しません。

## 監修判断に必要な結論

`git fetch --prune origin`後、開始時の
`codex/new-banknote-authoritative-source-script-v1`がupstreamと`0/0`でcleanであることを
確認しました。そのうえで、repoの2026-07-17再開ハンドオフが取得先として明示する
`origin/codex/new-banknote-content-lineage-yymm4-batch-v1`をlocal tracking branchとして
checkoutし、fast-forward限定pullを実施しました。取得時HEADは
`2dbc5d7ec0ae027caa2dad1a270eb5dc5af75849`、upstream parityは`0/0`、
`origin/master`に対して7 commit先行・遅れ0です。

ただし、日付が新しいbranchを既存の進行branchへ自動統合してはいません。現在branchと
`origin/codex/new-banknote-authoritative-source-script-v1`はapproval baseline
`b05eb3867caabda496fb9a0070d230a4e81aea01`から分岐し、現在branchだけに3 commit、
後者だけに13 commitがあります。後者には既存YMM4 import観測、editorial provenance、
A/B/C visual directionがあり、現在branchには新しいT00-T07 content lineageと
no-silent-change lockを含むOperator Batchがあります。current-state文書が競合するため、
merge / rebase / cherry-pickを機械的に行わず、両branchを保持しました。

開発環境はPython 3.13.3 / uv 0.10.7、Node.js 24.13.0、Electron 35.7.5をreadback済みです。
`uv sync --extra dev`は7 package resolved / 6 auditedで完了し、tracked worktreeへ依存関係
差分を残していません。したがって、次のPython/GUI実装を追加install待ちなしで開始できます。

## 取り込み・整備・検証の結果

| 確認対象 | 実施内容 | 結果 | 監修上の意味 |
| --- | --- | --- | --- |
| リモート同期 | fetch/prune、指定branchのtracking checkout、FF-only pull | HEAD `2dbc5d7`、upstream `0/0` | 2026-07-17 handoffと同じtracked stateを取得 |
| master関係 | `HEAD...origin/master` | ahead 7 / behind 0 | default branchの内容を欠かさずfeature成果を保持 |
| branch分岐 | visual/provenance branchとmerge-base・固有commitを比較 | merge-base `b05eb386`、3対13で分岐 | supervisor判断なしの自動統合を避けた |
| Python環境 | `uv sync --extra dev`、Python/uv readback | Python 3.13.3、uv 0.10.7 | focused実装・検証を再開可能 |
| GUI環境 | Node/npm依存readback | Node 24.13.0、Electron 35.7.5 | GUI sliceもdependency recovery不要 |
| lineage / batch | focused pytest 25件 | 25 passed | approval lock、deterministic artifacts、collector契約を維持 |
| 上流回帰 | authoritative script / source reconciliation 17件 | 14 passed / 3 skipped | 現行9 cueとsource freezeの通常回帰は維持 |
| Python syntax | modified modulesを`py_compile` | passed | import可能 |
| lineage validate | current packageをbyte exact / privacy boundaryで検査 | passed、7/7 artifact一致 | approved content変更なし |
| Operator runtime preflight | current batchをheadless検査 | passed、manual 5 / return 3、YMM4 launch 0 | batchコード自体は実行前状態として健全 |
| PowerShell preflight | `-PreflightOnly`を実行 | 既存operator-owned evidence 3件で意図どおり停止 | 再実行・上書きは安全でなく、既存証跡の照合が先 |

full `uv run pytest`は実行していません。repo-local ruleがgenerated artifact/path driftと
tracked-fixture side effectを既知のIntegrity課題としており、通常closeout gateではありません。
今回の変更対象に直結するfocused tests、validator、headless preflightを判断根拠にしました。

## リモート正本と同端末事実の差分

リモートhandoffはactual YMM4 importを未実施としていましたが、このcheckoutのignored
`local_outputs/`には2026-07-14のoperator-owned project、result、batch stateが残っています。
3件は追跡対象外のまま保持し、削除・移動・上書きしていません。

既存`operator_result.json`のsanitized readbackは`status=success`で、VoiceItem 9、
れいむ3 / まりさ6、exact text/order、missing 0、duplicate 0、60 fps、4415 frames、
73.583333秒を記録します。project SHA-256は
`beee7eab59196453c8d36b8889343cc82e876ea69e2bb00f5576bf17987eaa54`でresult内identityと
current local bytesが一致し、mapping/error/update/character mismatchなしのoperator確認も
記録されています。YMM4は4.54.0.1、profileは4.53.0.9で、既存receiptのpolicy上はwarningです。
render、production、rights、publicationの証拠または承認ではありません。

この結果は現在branchのapproved 9 cueと同じtext/orderを示しますが、current lineage packageを
追加した後のcollectorが作ったreceiptではなく、pronunciation/clipping noteも記録されていません。
したがって「manual importをもう一度実行する」も「current lineage gateを完全通過した」も不適切です。
安全な次のmoveは、既存3件を変えずにcurrent approval/lineage lockと再照合し、sanitized successor
receiptを作ることです。

## 製品の現在地

| 能力・gate | 現在状態 | 完了度の見方 | 次に必要な証拠 |
| --- | --- | --- | --- |
| Source / claim adjudication | 182 claims adjudicated、15 adopted、4 official sources | 完了 | content変更時だけsuccessor evidence |
| Approved 9-cue script | 2/4/3 scenes、れいむ3 / まりさ6、8 hashes lock | 完了 | silent changeを拒否し続ける |
| Content lineage | T00-T07、20 factual units、21 edges | 完了 | deterministic validation維持 |
| YMM4 CSV import | same-machine resultでは成功 | 観測済みだがcurrent lineage receipt未統合 | non-overwriting current-code revalidation |
| Pronunciation / clipping | 既存resultにnoteなし | 未判定 | cue ID付きhuman observation。必要時だけ再観測判断 |
| Visual direction | 別branchにA/B/C案とRoute A推奨あり | 分岐成果。current successorへ未統合 | branch integration audit後のhuman selection |
| Visual implementation / render | 未承認・未実施 | 未着手 | selected route、GUI review、adapter gate |
| Production / public release | 未承認・未実施 | 範囲外 | creative、rights、publicationの独立承認 |

North Starに対する現在地は「source-backed contentとYMM4台本読込は接続済み、visual production
chainはまだ人間判断とbranch統合前」です。preflightやdocsの追加だけをproduction valueと扱わず、
次は既存観測の再利用、一本化されたsuccessor state、GUI-visible visual decisionへ進めます。

## 先を見据えた目標設定案

### G0 — 既存YMM4観測の非破壊再受入（推奨する直近slice）

- **目的**: 同端末の成功resultを再実行せず、current approval/lineage lockへ接続する。
- **効果**: manual import gateの重複を消し、次のvisual判断へ進める。
- **要件**: 既存3件を上書きしないread-only revalidator、current hash lock、9/3/6/text/order/
  timingのreadback、YMM4 version warning、sanitized successor receipt。
- **現在状態**: raw evidenceあり、旧result成功、current headless preflight成功。current-code receiptだけ未作成。
- **owner / next**: assistant-owned実装。pronunciation noteを回収できない場合はunknownを保持し、再度YMM4を
  開くかは別のhuman decisionにする。

### G1 — 分岐した新紙幣レーンのsuccessor統合監査

- **目的**: current lineage/approval lockと、別branchのimport intake・editorial provenance・A/B/C案を
  一つのsuccessor stateへ統合する。
- **効果**: 「日付が新しいbranch」と「製品gateが先のbranch」のねじれを解消する。
- **要件**: 3対13 commitのartifact classification、overlap matrix、content hash不変確認、current-state
  docsの一意化、tracked/ignored境界、normal merge/cherry-pick方針の監修判断。
- **現在状態**: merge-baseと分岐量を確認済み。自動統合は未実施。
- **owner / next**: assistantがintegration audit packetを作り、監修AIが採用順とsuccessor branchを承認。

### G2 — provenance付きvisual directionの人間選択

- **目的**: A/B/C、S1/S2/S3 flow、misleading diagram risk、motion restraintを決定する。
- **効果**: visual実装の曖昧さを減らし、Shot Layout / Motion Beatへ進める。
- **要件**: G1で統合されたreview surface、9-cue lock維持、選択またはcue/scene ID付きrevision。
- **現在状態**: 候補は別branchにあるが、current successorでは未採用。
- **owner / next**: human visual reviewer。assistantは比較と誤解リスクを整理する。

### G3 — GUI-visible Shot Layout / Motion Beat契約

- **目的**: 選択routeをscript beat、visual direction、shot layout、motion beatへ機械可読に接続する。
- **効果**: YMM4をbasic design discoveryに使わず、GUI timelineで判断できる。
- **要件**: subtitle safe area、label budget、reading order、motion primitives、anti-pattern、decision schema。
- **現在状態**: production contractとmulti-topic smoke基盤はあるが、新紙幣successorへの適用は未実施。
- **owner / next**: assistant-owned実装、humanはGUI review decisionだけを返す。

### G4 — Asset / proxy gap解消とtemplate registry接続

- **目的**: 各sceneをaccepted proxy、real asset、needs revision、cut、deferへ分類する。
- **効果**: rights不明素材や抽象図の誤解をYMM4 adapter前に止める。
- **要件**: scene decision packet、gap report、asset identity/rights context、repo-tracked template source。
- **現在状態**: 新紙幣について未作成。
- **owner / next**: assistantが分類とregistry候補、人間が素材・rights・creative tradeoffを決定。

### G5 — 限定的YMM4 adapter出力とdiagnostic project

- **目的**: 既存import済みVoiceItemsを保持し、provenなregistry解決と限定patchだけを適用する。
- **効果**: Python接着層の成果を実YMM4 timeline writeとして確認する。
- **要件**: G2-G4承認、no zero-generation、dry-run/readback、changed item inventory、rollback可能なlocal copy。
- **現在状態**: 未承認。現在のoperator projectはVoiceItem-only internal observation。
- **owner / next**: assistantがadapter/readback、人間が一度だけYMM4 creative確認。renderはまだ別gate。

### G6 — 内部render、編集受入、rights gate

- **目的**: 音声、字幕、構図、motion、clipping、全尺整合を内部動画で判断する。
- **効果**: artifact-level proofを実視聴品質へ接続する。
- **要件**: selected visual、resolved gaps、pronunciation decision、internal/non-final表示、media identity、rights ledger。
- **現在状態**: 新紙幣successorでは未実施。
- **owner / next**: YMM4/operatorとhuman creative reviewer。public uploadは許可しない。

### G7 — Episode 002統合監査とdefault branch採用

- **目的**: provenanceを壊さず、完成したsuccessor milestoneをdefault branchへ統合する。
- **効果**: 別端末・次案件が単一のcurrent stateから再開できる。
- **要件**: commit/path classification、tests/readback、ignored evidence boundary、normal history、明示的統合承認。
- **現在状態**: current feature branchはmasterより7 commit先行。新紙幣分岐統合は未実施。
- **owner / next**: assistantがaudit、監修AIがintegration decision。統合はproduction/public承認を意味しない。

### G8 — topic横断factory化とGUI完結

- **目的**: content lineage、approval lock、operator/result ingest、visual reviewを他topicへ再利用する。
- **効果**: 一回限りの新紙幣proofを制作factoryへ変える。
- **要件**: 少なくとも3 topicのsmoke、GUI episode ingest、failure-class統一、template rotation、
  production IR / registry / adapter capabilityの一致。
- **現在状態**: reusable contractとsmoke fixtureはあるが、end-to-end GUI production loopは未完成。
- **owner / next**: assistantがvertical slice、人間はbrief/creative/rightsの高位判断だけを担当。

### G9 — production / publication governance

- **目的**: internal artifactを公開可能なvideo、thumbnail、metadata、uploadへ進める最終境界を作る。
- **効果**: 技術的成功とcreative・rights・publication承認を混同しない。
- **要件**: final creative acceptance、rights status、source attribution、thumbnail/title promise、release checklist、
  明示的publication authorization。
- **現在状態**: 範囲外・未承認。
- **owner / next**: human production owner。assistantは証跡と候補を準備するが勝手に公開しない。

## 監修AIへの推奨判断

直近はG0を既定にしてください。既存YMM4証跡があるためmanual batchの再実行は価値がなく、
上書きリスクがあります。G0でcurrent lineage compatibilityを非破壊に固定した後、G1のbranch
統合監査で一本のsuccessor stateを作り、G2の人間visual selectionへ渡すのが最短です。

停止条件は、approved content hash drift、既存operator evidenceへの上書き要求、分岐成果の
意味的競合、mapping/character mismatch、raw/private evidenceの追跡化、visual未選択のままの
adapter/render、rights/publicationの暗黙承認です。これら以外のmechanical closureはassistant-ownedです。
