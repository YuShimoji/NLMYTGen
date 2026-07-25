# 3回連続 Operator Repeatability / Resume Recovery — 監修AI向け現状報告

日付: 2026-07-26 JST
対象branch: `codex/nlmytgen-three-run-operator-repeatability-v1`
source base: `da88ad52d9157da9be3d40a56567d80a1b9f025b`
decisive implementation checkpoint:
`2d5c4f34c8b88070075a2678a08d9a72fafa9f31`
Project-State-ID: `nlmytgen-three-run-operator-repeatability-validated-v1`

## 結論

REINS factory canaryを、同一のclean implementation commitから通常のElectron 43
標準制作GUI経路で3回連続実行した。3回ともdeep runtime doctor 4/4 ready、
protected inputs 9/9 exact、write-free dry-run、実YMM4 render、MP4 validation、
GUI result readbackを無介入で完走した。

3つのrunでcontent identity、正規化YMM4 project identity、最終MP4、real-media
manifestのsemantic identity、cue readbackのsemantic identityが一致した。
生project SHAの差は各run-idを含むrun-local path 8か所だけであり、run-id置換後の
全文SHAは3本とも
`d7aeee07b07f06b797b618c9b2b0e18981533f58ef7963cf51cd788f3dad10cf`
で一致した。

final run 03に対する実GUI resumeは1.4881秒で完了した。CLIの同一実装経路でも
`verified_noop`、`validation_only=true`、`outputs_rewritten=false`、
`yymm4_launched=false`を観測した。run 03配下26ファイルのSHA、size、mtimeは
resume前後で完全一致した。安全な一時fixtureではrender settingの意味的変更を
`resume_artifact_drift`として拒否した。

これにより、named blocker
`OPERATOR_REPEATABILITY_AND_RESUME_IDENTITY_UNPROVEN`は技術的にcloseした。
現在のProduct-Gateは`third-topic-variation-validation`であり、次の既定作業は
異なるcue / scene / speaker / time shapeを持つ第3実トピックのfactory proofである。

REINSは`internal_factory_canary_not_human_accepted`のまま保持する。human creative
acceptance、rights、production、publication、external upload、release、PR、
merge、master integrationは独立gateである。

## Git、開始点、保全

- source remote
  `origin/codex/nlmytgen-second-real-topic-factory-v1`は開始時にexact
  `da88ad52d9157da9be3d40a56567d80a1b9f025b`だった。
- attempt 1のdirty implementation 13 tracked filesと1 untracked smoke wrapperを
  ownership分類した。全tracked差分はMission implementationまたはMission testで、
  unrelated / unknown tracked overlapは0件だった。
- ignored backupを`_tmp/operator-repeatability-attempt2-backup-2026-07-26/`へ
  作成した。tracked patch SHA-256は
  `38a9c703...5956c7`、smoke wrapper copy SHA-256は
  `c70669d9...86c2`。
- attempt 1のtemporary proof checkoutをread-only比較し、現在のdirty
  implementationと対象file treeが一致することを確認した。proof commitをreset、
  cherry-pick、worktree置換には使用していない。
- `.playwright-mcp/`、`artifacts/`、
  `phase-e-01-contact-acquired*.png`、既存のprivate/ignored media、全run archiveを
  保持した。
- `repeatability_01`、`repeatability_02`、途中のGUI probe、v2 failure receipt、
  run logは削除・上書き・renameしていない。
- `uv.lock`、`gui/package-lock.json`、accepted new-banknote、prior REINS artifactは
  変更していない。

## 失敗の因果診断

### attempt 1 run 02

run 02の最終完了stageは`YMM4 project generation/readback passed`だった。旧GUI observer
は固定1200秒、Python pipelineは1260秒、.NET stageは1200秒を個別に持っていた。
外側observerが先に失敗表示へ到達し、内側stageとowned descendant cleanupが完了する前に
観測が切れた。20分という経過時間そのものではなく、timeout authorityの分散が原因だった。

対策としてmanifestの`render_settings.timeout_seconds`をauthorityに固定し、次を導出する
一つのcontractへ統合した。

| deadline | 秒 | 意味 |
| --- | ---: | --- |
| render | 1200 | YMM4 automationの実作業 |
| cleanup grace | 60 | owned treeの停止と残留検査 |
| pipeline | 1260 | render + cleanup |
| observer grace | 30 | receipt読戻し |
| GUI observer | 1290 | pipeline + observer grace |

PythonはWindows Job Objectへrender driverとYMM4 descendantを割り当てる。timeout時は
stageを固定し、新規作業を止め、owned treeだけを終了し、bounded cleanup後に残留を検査し、
sanitized `pipeline_failure_receipt.json`を残してnonzeroで終了する。

synthetic containment testではproject-owned child / grandchild treeを短いtimeoutで停止し、
residue 0とunrelated process不変を確認した。

### v2 run 01と、ユーザーが観測した保存ダイアログ停止

最初の修正版checkpoint
`547ae7f8a94a47a69960e5a6251e19e2e7a3157c`からv2 seriesを開始した。
ユーザーから「ファイル名にアドレス値を入力しようとして止まっている」と観測報告があり、
UIA / Win32 process stateをread-onlyで調査した。

ファイル名fieldには期待したabsolute output pathが完全に入っており、native Save buttonも
enabledだった。driver telemetryは`confirm_save`から`wait_render_file`へ進んでいた。
Save dialogには`保存したゲーム`というTreeItemと`保存(S)`というButtonが同時に存在し、
旧`FindNamedAction`のdescendant name部分一致がTreeItemを先に選択していた。このため
driverは保存操作を完了したと誤認し、存在しないrender fileを待っていた。

修正は保存dialogのowning layerへ限定した。

- filename edit: AutomationId `1001` + ControlType `Edit`
- Save action: AutomationId `1` + ControlType `Button`

v2 run 01は診断証跡として保持した。failure receiptは
`failed_stage=yymm4_render`、`driver_stage=wait_render_file`、
`job_object_assigned=true`、`cleanup_verified=true`、`residual_count=0`を持つ。
この修正後のdecisive checkpoint
`2d5c4f34c8b88070075a2678a08d9a72fafa9f31`から、namespaceをv3へ進めて完全な3回seriesを
再開始した。

## 実装内容

### Identityとrun safety

- run IDの文字集合、長さ、path traversalをfail-closedで検査する。
- content identityとrun identityを分離する。
- projectのrun-local `project.FilePath` / `ImageItem.FilePath`を宣言的に正規化し、
  item content、timing、effects、asset、structureはidentityへ残す。
- real-media manifestとcue readbackにsemantic identityを追加する。
- existing runの無断上書きを拒否する。

### Resume

- completed runは全canonical artifactとcontent identityを検証してno-opで返す。
- no-opはreceiptやmtimeを更新せず、YMM4を起動しない。
- incomplete runは完了済みstageを検証し、必要なstageから再開できる。
- completed artifact破損、content identity差、render setting差をfail-closedで拒否する。

### Timeout、failure receipt、GUI

- manifest-derived timeout contractをPython、GUI observerへ伝播する。
- .NET driverは各UIA stageをstructured stderr telemetryとしてstreamする。
- Job Object cleanup結果をfailure receiptへ保存する。
- absolute local pathとcommand lineはfailure receiptでsanitizeする。
- Electron rendererのreal probeはcontract由来の1290秒を待ち、固定外側timeoutを持たない。
- 通常GUI readiness gate、tracked-clean gate、silent policyは維持する。

## 最終3回series

共通条件:

- checkpoint:
  `2d5c4f34c8b88070075a2678a08d9a72fafa9f31`
- Electron: 43.2.0
- YMM4: 4.54.0.1
- doctor: code / review / render / regenerate = ready
- protected inputs: 9/9 exact
- dry-run: passed
- `readiness_bypass=false`
- `render_test_double=false`
- tracked worktree clean at dispatch
- manual intervention / Computer Use / SendKeys / keyboard-mouse injection = 0
- playback / system-volume operation = 0
- console / preload / security / load / renderer errors = 0
- post-run Electron / Python / YMM4 / Win32Service / driver / ffmpeg residue = 0

| run | pipeline | GUI | raw project SHA | total | GUI total |
| --- | --- | --- | --- | ---: | ---: |
| `v3_01` | pass | pass | `ac50673d...afdfcc` | 226.260147秒 | 239.1471秒 |
| `v3_02` | pass | pass | `fab4d0ef...aa6b7` | 137.568453秒 | 145.1584秒 |
| `v3_03` | pass | pass | `f4df9497...598eed` | 163.916620秒 | 170.6850秒 |

### 共通semantic identity

| identity | SHA-256 / value |
| --- | --- |
| content | `15375b3a9265269776e0c35e5f3104025fa5857155f4888ab75e9e43b3d45c06` |
| normalized project structure | `6211ca91e0db06d54ef15d1f40cc53a18722aafd457385c253483d2a790dd3cf` |
| final MP4 | `4c99feed4e487743e5243074c3eca6aad51a7b16392f7f405ce158f038cb5c75` |
| YMM4 render intermediate | `6790e3f29279e64dd266f776956d278d5d65b8f090eb923252bc73767fe7ccf6` |
| asset manifest semantic | `c5165a0f615189a1a870a667a768560fc691d6a740ef0e87744f4f522386a8f9` |
| cue readback semantic | `bb5fa4b7c5c408965b92794ee88e80fdc43fb85dfab1926c2f6290eccd92a196` |

共通shapeはVoiceItem 7、ImageItem 7、7 cues、4 scenes、Reimu 4 / Marisa 3、
2725 frames、60 fps。text order、subtitle fragment、source identityも一致した。
MP4は57,508,191 bytes、H.264/AAC、1920x1080、60 fps、45.416016秒で、
ISO-BMFF、ffprobe、full-file decodeを各runでpassした。

### stage timing

| stage | min | median | max |
| --- | ---: | ---: | ---: |
| preflight | 0.052061 | 0.065295 | 0.132827 |
| content identity | 0.021038 | 0.021861 | 0.032740 |
| media materialization | 1.159186 | 1.172306 | 2.043761 |
| YMM4 project | 0.209933 | 0.233171 | 0.289505 |
| cue readback | 0.018197 | 0.019497 | 0.029146 |
| YMM4 render | 127.642074 | 153.711543 | 212.934911 |
| cleanup | 0.011336 | 0.013341 | 0.014905 |
| normalization | 0.538451 | 0.705392 | 0.719824 |
| media validation | 7.302050 | 7.474887 | 9.178687 |
| receipt generation | 0.000606 | 0.000639 | 0.000827 |
| total | 137.568453 | 163.916620 | 226.260147 |

最大差はYMM4 render時間にあり、artifact identity、cleanup、GUI outcomeへ影響していない。

## Completed-run live resume

run 03の成功後、26ファイルのrelative path、SHA-256、size、mtimeを記録した。
同じrun IDを新しいappend-only GUI probe IDから通常Electron標準制作画面へ渡した。
GUIはdoctor、dry-run、既存output検出、`--resume` dispatchを通り、render jobを
1.4881秒で完了した。

同じ実装のCLI readback:

- `status=passed`
- `resume=true`
- `resume_observation.status=verified_noop`
- `validation_only=true`
- `outputs_rewritten=false`
- `artifact_identities_exact=true`
- `yymm4_launched=false`
- elapsed 1.067912秒

resume前後の26ファイルでSHA、size、mtime mismatchは0件だった。YMM4 / render driverを
含むowned processはresume前後とも0件。append-only observationはaggregate receiptに
保存し、canonical run receiptとoutput timestampは更新していない。

## Semantic drift / corrupt outputのfail-closed

isolated temporary manifestとrun directoryを使い、completed runの
`render_settings.video_bitrate_kbps`を1段階変更した。resumeは
`resume_artifact_drift`で拒否された。fixtureは実/private outputを参照せず、
REINSおよびnew-banknoteのcanonical artifactは変更していない。

focused suiteにはcorrupt completed MP4とincomplete render stage resumeも含む。
completed outputの破損は拒否し、incomplete stageは検証済みartifactを維持して必要stageだけを
再開する。

## Identity保護

作業後にprivate/local実体をread-onlyで再hashした。

### accepted new-banknote

- source project:
  `beee7eab59196453c8d36b8889343cc82e876ea69e2bb00f5576bf17987eaa54`
- generated project:
  `244c05ae6fe6179e9dace4b569cd5f3f9f496cfe70d46ac16ac459e787712611`
- accepted MP4:
  `423553e0aff40619ffb0fd88bcc80344417788aa6128f0a8778aefbdd19ca476`
- human acceptance receipt:
  `cd0b4f02fb54cb0b0dbf8625a5baed6db3952b0a7342257c5456d1426e23f4b8`

### prior REINS

- source project:
  `ed2773ce87a41936dd82d16d666d253f8bdba8763fc11bfa829d4818cb1b3ec9`
- prior generated project:
  `ea4bc001068cf0f398d428072b2b94a6b3b1f4beed5ba0efb2b04f0d040e4da8`
- prior MP4:
  `4c99feed4e487743e5243074c3eca6aad51a7b16392f7f405ce158f038cb5c75`
- prior GUI receipt:
  `da9b0b0341c2cbed2865f8944cb564f4f44bf2c138f4e14d67e07a24f21fdee7`

全identityはauthority receiptと一致した。v3 MP4がprior REINS MP4と同一であることも
再現性の一部として確認した。

## 検証構成

outcome commit前のgate:

- repeatability / resume / corrupt-output、standard GUI、runtime doctor、
  Electron 43、dependency lock、state syncを含むfocused Python 65件: pass
- standard production-loop JavaScript 7件: pass
- actual Electron 43.2.0 compatibility smoke: pass
- modified Python compile / JavaScript syntax: pass
- .NET Release build: warning 0 / error 0
- aggregate JSONのlive receipt突合: mismatch 0
- JSON / Markdown structure / state sync / local-path leak検査: pass
- `git diff --check`、worktree / cached-diff scope検査: pass

`gui/package.json`にはcheckpointでtracked smoke commandが1件追加された。依存versionと
`gui/package-lock.json`は不変であり、dependency testのmanifest hash authorityだけを
新しいmanifest bytesへ同期した。lock SHAは`uv.lock`
`40e64f79...435d0`、`gui/package-lock.json`
`095706ab...f047`のまま。

outcome commit後にcanonical Regression Integrityを一度だけ実行する。正本runnerの
failure / error 0、declared-locator skip contract、Git三面不変を最終監修handoffで報告する。

## 現在の状態遷移

- Project-State-ID:
  `nlmytgen-three-run-operator-repeatability-validated-v1`
- Product-State:
  `two-topic-factory-with-clean-gui-zero-intervention-repeatability`
- Product-Gate:
  `third-topic-variation-validation`
- Recommended-Next:
  `run-third-real-topic-with-new-cue-scene-speaker-time-shape`
- Development-Audio-Policy:
  `silent_by_default`

## 残作業

### 第3実トピック variation validation

- 目的: 2トピックと同一shapeに依存するhard-codeを検出する。
- 効果: factory contractが異なる入力形状を処理する証拠を3本へ拡張する。
- 要件: 7/9 cues、3/4 scenes、4/3・3/6 speaker、45/73秒とは異なるshape、
  official source、new run identity、private media非追跡。
- 状態: 未着手。現Product-Gate。
- owner: 次の実装AI。source/rights判断は人間owner。
- next move: topic選定後、source registryからGUI receiptまでを一つのvertical
  factory sliceとして通す。

### Human creative review

- 目的: REINSの字幕、keyword emphasis、source crop、情報密度を人が採否判断する。
- 効果: technical canaryをcreative candidateへ昇格できるか確定する。
- 要件: exact MP4 SHA固定、通し視聴、cue ID付きaccept / repair / reject。
- 状態: 未実施。technical evidenceのみ。
- owner: human editorial reviewer。
- next move: rights-cleared candidateを用意する判断と合わせてreview scopeを決める。

### Rights-cleared asset replacement

- 目的: official page captureの内部技術利用と公開利用を分離する。
- 効果: production/publication可能なasset registryを作る。
- 要件: 許諾済み、自作、または契約で利用可能な素材。置換後は新SHAと新review identity。
- 状態: rights approved 0件。
- owner: rights / production owner。
- next move: cue単位のreplacement briefとlicense evidenceを準備する。

### Cross-terminal real render portability

- 目的: private source locator、YMM4、driver、GPU encoderを別端末で同じdoctor契約へ載せる。
- 効果: Thank端末固有の成功からoperator環境contractへ進める。
- 要件: private artifact ingest、hash exact、Electron 43、YMM4 4.54.0.1、
  no-playback silent policy。
- 状態: code pathはportable。live private artifact availabilityは端末依存。
- owner: operator environment owner。
- next move: declared locatorだけを投入した新端末でdoctor → dry-run →一回のinternal runを行う。

## 条件付き長期目標

### Goal 1 — 第3形状のfactory proof

現在のProduct-Gateを閉じる。新しいshapeを通し、既存2トピックとv3 repeatability
identityの不変を同時検査する。

### Goal 2 — Factory Contract v2

3本の実例からcommon schemaとtopic extensionを分離する。source registry、claim edge、
canonical script、media provenance、YMM4 project、GUI receipt、resume identityを
versioned contractにする。

### Goal 3 — Operator procedure v1

run plan、ID予約、collision、resume、fresh successor、failed attempt archive、timeout、
owned process cleanup、aggregate receiptを一つのdelete-free procedureにする。

### Goal 4 — Bounded queue

one-active-job、silent policy、resource limit、cancel、restartを保ち、複数episodeを
bounded queueで生成する。episode failureを次jobへ伝播させない。

### Goal 5 — Cross-topic quality corpus

3本以上のcue-level accept / repair / rejectを集積し、字幕可読性、source crop、
情報密度、emphasis、scene variationをmachine checkとhuman judgementへ分離する。

### Goal 6 — Rights-cleared production candidates

technical canaryと別identityで、許諾済み/自作素材、production registry、human
creative acceptanceを揃える。素材変更ごとにartifact SHAとreview identityを更新する。

### Goal 7 — Performance envelope

render min / median / max、GPU/CPU/memory、queue wait、resume率、timeout率を
private内容なしで計測する。SLOは3トピック以上の実測後に設定する。

### Goal 8 — Compatibility matrix

Electron、Node、Python、YMM4、ffmpeg、GPU driverの更新をcompatibility branchで評価し、
accepted artifactの再生成を要求しないrollback contractを維持する。

### Goal 9 — Security and dependency maintenance

lock update、audit remediation、framework upgradeを専用sliceに分け、factory identityと
runtime regressionをそれぞれ検査する。

### Goal 10 — Editorial provenance automation

claim/source edge、transformation ledger、subtitle fragment、visual sourceをcue単位で
追跡し、unsupported factual unitをpreflightで拒否する。

### Goal 11 — Human review workspace

exact artifact SHA、cue frame、source edge、machine warningを一画面にまとめ、
accept / repair / rejectをimmutable receiptとして返す。

### Goal 12 — Production readiness gate

code、dependency、security、content、rights、creative acceptance、operator runbook、
rollbackを独立checkとして束ねる。各checkのownerとexpiryを明示する。

### Goal 13 — Controlled publication integration

publication authorityが明示されたsliceで、credential、metadata、dry-run、private preview、
upload receipt、rollbackを実装する。現branchはpublication authorityを持たない。

### Goal 14 — Operational observability

topic数、run成功率、manual intervention、render時間、resume率、drift率、human repair率を
個人情報とprivate sourceを含めず集計し、異常をtopic / cue / runへ遡れるようにする。

### Goal 15 — Release candidate governance

factory contract、rights-cleared asset、human acceptance、security、compatibility、
bounded operationが揃った時点でrelease candidateを作る。PR、merge、master、
release、deploymentはそれぞれowner承認後に個別実行する。

## 監修判断

`three-run-operator-repeatability-and-resume-recovery-v1`は、final post-commit
Regression Integrityとremote parityがgreenならclose可能である。製品開発の次gateは
`third-topic-variation-validation`。creative、rights、production、publicationは
現在も明示的な人間判断を要する。
