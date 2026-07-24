# 監修AI向け・最新リモート同期、開発再開判断、長期目標案（2026-07-24 JST・複数端末）

Scope: NLMYTGen

この文書は、公開リモートのaccepted-cut / regression-integrity線を複数端末で再取得した結果を、
端末固有の開発可用性と製品checkpointに分離して記録する。最上段のThank端末refreshが今回の
最新handoffであり、後続のPLANNER007節は先行受信端末の履歴として読む。製品状態と直近gateの正本は
[`runtime-state.md`](../runtime-state.md)、非交渉境界は
[`INVARIANTS.md`](../INVARIANTS.md)、三モード回帰の機械可読結果は
[`REGRESSION_INTEGRITY_2026-07-24.json`](REGRESSION_INTEGRITY_2026-07-24.json)である。

ここで示す遠方目標は監修判断用の提案であり、依存契約変更、Electron major更新、rights、
production、publication、PR、merge、master integrationを一括承認するものではない。選択された
次sliceだけを狭い契約にし、accepted cutのclosed creative dimensionsを別目的の変更で開き直さない。

## Thank端末の最新refresh

### 今回の到達点

`C:\Users\thank\Storage\Media Contents Projects\NLMYTGen`で
`git fetch --prune origin`を実行したところ、current handoff branchのremoteがlocal
`e574614`より3 commit進んだ`739c5a4`であることを確認した。差分はruntime、cockpit、
project context、本監修roadmapの更新だけで、`git pull --ff-only`により競合なしで取り込んだ。
merge、rebase、history rewrite、master更新、PR作成は行っていない。取込直後はupstream
`0/0`、`origin/master`より40 ahead / 0 behindで、masterはcurrent branchの祖先だった。

同期前から存在した`.playwright-mcp/`、`artifacts/`、
`phase-e-01-contact-acquired*.png`はuntrackedのまま保全した。`.venv/`、
`gui/node_modules/`、private media、YMM4 project、run archiveもignored local stateとして
保持し、stage、削除、public Gitへの追加を行っていない。この報告のcommit / push後にも
upstream `0/0`とtracked cleanをhandoff条件とする。

現在の判定は「code development readyかつprivate-artifact preflight ready」である。
accepted carrierとYMM4 runtimeはローカルに存在するが、accepted cutはrerender不要であり、
今回のreadiness確認ではwindow、playback、render、remux、fresh full decodeを実行していない。
技術的にファイルが存在すること、実機renderを今回再実行したこと、人間が再視聴したことを
同じpassとして扱わない。

### この端末で整えた開発基盤

| 基盤 | 今回の実測 | 判定 | 残るportable条件 |
| --- | --- | --- | --- |
| Python | Python 3.13.3、uv 0.10.7、`uv sync --extra dev --locked` | package audit完了、module/script開発可能 | `uv.lock`はignored local |
| Electron GUI | Node 24.13.0、npm 11.6.2、`npm ci`、`npm ls --depth=0` | Electron 35.7.5 exact、tracked JS 12件syntax pass | `gui/package-lock.json`はignored local |
| GUI security | live `npm audit --json` | direct high 1件、17 advisory経路 | offered fixは43.2.0 semver-major、互換検証が必要 |
| Python quality | compile、project-state sync、runner focused contracts | compile pass、state sync pass、6 tests pass | full suiteは通常gateにしない |
| Canonical regression | 16 modules / 170 tests | 166 pass / 4 declared-locator skip / failure 0 / error 0 | 4 skipはNotebookLM private locator不在 |
| Workspace integrity | status / diff / cached diff前後比較 | 全面不変、temporary workspace回収 | unrelated untracked evidenceの内容は保証しない |
| .NET render driver | SDK 10.0.204、Release build | warning 0 / error 0 | actual YMM4 UI automationは今回未実行 |
| Media tools | ffmpeg / ffprobe 8.0.1 | command readback済み | accepted MP4のfresh decodeは今回未実行 |
| YMM4 | bounded candidate pathの4.54.0.1 | executable identityをreadback | window、project open、render compatibilityは今回未実行 |

`uv.lock`のSHA-256は
`40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0`、
`gui/package-lock.json`は
`81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73`で、
先行Dependency Lock Authority attempt 1が保全した値から変わっていない。今回のlocked
sync / installはlocal readinessを証明するが、clean Git checkoutからlockを得られることは
証明しない。

### Private evidenceと実素材preflight

| 対象 | live availability | identity判定 | 今回実行していないこと |
| --- | --- | --- | --- |
| real-media assets | 9/9 present | provenance記載SHA-256 9/9一致 | rights clearance、production採用 |
| source project | present、1,337,084 bytes | SHA-256 `beee7eab...aa54`一致 | source変更、YMM4 open |
| generated project | present、1,521,444 bytes | SHA-256 `244c05ae...12611`一致 | regeneration |
| accepted MP4 | present、93,375,529 bytes | SHA-256 `423553e0...ca476`一致 | playback、fresh decode、再受理 |
| YMM4 executable | 4.54.0.1 present | expected observed versionと一致 | render、UI automation |

`NLMYTGEN_AUDIO_POLICY=silent`でreal-media manifestのread-only `--dry-run`を実行し、
18 protected inputs、9 cues、S1/S2/S3=`2/4/3`、speaker=`3/6`、4415 frames、
1920×1080/60fps、9/9 cue provenanceがpassした。statusは`dry_run`、render requestedは
falseで、media materialization以降は計画表示だけである。この結果は、同じsourceとassetから
pipelineを再開できるpreflight evidenceであり、accepted MP4の再生成や人間再確認ではない。

### 現在の残作業と所有境界

| 残作業 | 目的と効果 | 必要条件 | 現在状態 | owner / 次のmove |
| --- | --- | --- | --- | --- |
| Dependency Lock Authority | clean checkoutの依存集合を決定可能にし、Electron検証とCIの基準を作る | `.gitignore`とlock更新契約を狭く変更 | local locksは健全、tracking未実施 | assistant実装。handoff push後のfresh remote tipから再開 |
| Electron major compatibility | support外35系とhigh advisoryを解消し、保守可能なGUI runtimeへ移す | lock authority、major変更の監修承認、rollback基準 | 43.2.0 fix candidateのみ確認 | 監修AIがgo / revise / hold、assistantがisolated検証 |
| Private artifact portability | review-only端末とrender-capable端末を誤判定しない | private storage / transfer owner、hash contract | Thank端末は揃うがPLANNER007端末は欠落 | storage owner決定後、assistantがingest/doctorを実装 |
| Default integration | feature branchに滞留するcheckpointを通常入口へ戻す | PR差分監査と明示merge承認 | masterより40 commit先行、未merge | merge ownerが条件決定、assistantは監査まで |
| Rights clearance | human-accepted visual intentを公開可能asset identityへ変換 | cue別license / permission / attribution判断 | 9 asset全てproduction false | rights owner判断、assistantがledger整備 |
| Production / publication | exact production masterとrelease packetを閉じる | rights、production QA、publication authorization | internal stable cutのみ | production / publication ownerの独立gate |

最短の次moveはDependency Lock Authorityである。attempt 1の`0b29c5a`を再利用せず、
このhandoffをpushした後のcurrent remote tipをfresh exact baseとして取得する。
`uv.lock`と`gui/package-lock.json`をmanifestおよびElectron 35.7.5を変えずにportable
authorityへ昇格し、fresh checkoutのlocked installとdrift checkをexit signalにする。
Electron 43.2.0互換性は別commit / successor missionとし、accepted media、script、timing、
visual decisionを変更しない。

## PLANNER007先行受信時の監修判断（履歴）

初回受信時には、旧branch
`codex/nlmytgen-end-to-end-auto-video-v1`のtip `9ed7cdf`を直線的に進めた正式な後継
`origin/codex/nlmytgen-accepted-cut-regression-integrity-v1`へtracking移行した。今回の再開では
そのlocal branch上で`git fetch --prune origin`と`git pull --ff-only`を再実行し、検証base
`0b29c5a9adc91b8c002967b19ca052f30d1a7a90`がremote tipと一致していることを確認した。
取得直後のupstream差分は`0/0`、`origin/master`より38 commit先行・遅れ0で、masterはcurrent
branchの祖先である。競合解消、merge、rebase、history rewriteは発生していない。

製品checkpointは、実素材版のexact MP4を`stable_internal_cut`として人間受理し、
canonical Regression Integrityを三実行形態でfailure 0 / error 0へ閉じた状態である。
speech、wording/order、cue timing、subtitle timing、subtitle line breaks、real-media visual
treatmentはclosedで、再renderは不要である。rights、production、publication、upload、release、
PR、merge、master integrationは依然falseである。

この受信端末ではPython、Electron GUI、回帰runner、.NET render driverのコード開発と機械検証を
開始できる。locked Python sync、locked npm install、Electron dependency readback、.NET Release build、
state sync、Python/JavaScript構文検査、canonical 170-test selectionが成立した。一方、受理済みMP4、
generated project、source `.local.ymmp`、real-media 9 assets、YMM4 executableはこの端末にない。
したがって、製品受理を取り消す理由はないが、この端末単独ではreal-media dry-run、再render、
accepted MP4の再生確認は行えない。

## 取り込んだ後継差分

| 後継slice | 主な変更 | 現在の効力 | 再び開かない境界 |
| --- | --- | --- | --- |
| Regression Integrity基盤 | canonical 16 modules、clean-room runner、Git三面不変検査、private locator skip契約 | temporary workspaceへignored media/profileを再帰複製せず、端末差をfailと混同しない | テスト拡張をproduction valueの代替にしない |
| Real-media visual replacement | 9 cueをtracked manifest/provenanceとlocal real-media locatorへ結合し、実素材review MP4を検証 | 旧proxy cutのvisual rejectionを後継artifactで解消 | rights-cleared / production-readyとは扱わない |
| Accepted-cut freeze | exact MP4 SHA-256 `423553e0...ca476`とgenerated project SHA-256 `244c05ae...12611`へhuman decisionを結合 | `stable_internal_cut`、rerender不要 | speech、cue/subtitle timing、line breaks、visual treatmentを無関係なlaneで変更しない |
| Regression causal repair | Git-object subtree materialization、repo-relative ignore probe、local evidenceのread-only分離 | clean-room / evidence-rich / linked worktreeでfailure 0 / error 0 | historical receiptをlive artifact availabilityへ読み替えない |
| Handoff更新 | runtime、project context、cockpit、machine-readable receiptをcurrent tipへ同期 | 別端末はcurrent branchから再開できる | public Gitへprivate mediaやabsolute local pathを載せない |

旧branchから検証baseまでの差分は15 commit、36 tracked files、3,671 insertions / 381 deletionsである。
中心は`src/pipeline/episode_video.py`のreal-media path、回帰fixture/runner、受理receipt、
manifest/provenance、状態文書であり、branch履歴はmergeなしの直線系列である。

## PLANNER007先行受信時のリモート同期とGit作業面（履歴）

| 確認対象 | 実測 | 判定 | 監修上の意味 |
| --- | --- | --- | --- |
| remote refresh | `git fetch --prune origin` | pruneを含め正常終了、current upstreamに新しいcommitなし | stale remote-tracking refで判断していない |
| local branch | current canonical tracking branchで`git pull --ff-only` | already up to date | 競合、rebase、history rewriteなし |
| upstream parity | 取得・検証開始時の`HEAD...@{u}` | `0/0` | 検証base `0b29c5a`はremote tipと一致 |
| default branchとの関係 | `origin/master...HEAD`、ancestry | 38 ahead / 0 behind、masterは祖先 | default branch内容を欠かさず後継成果を保持するが、未merge |
| worktree保護 | canonical runner前後のstatus / diff / cached diff | byte-exact不変 | testsやsetupがtracked product artifactを汚していない |
| ignored setup | `.venv/`、`uv.lock`、`gui/node_modules/`、`gui/package-lock.json` | local development用に保持 | Gitだけの再現authorityではない |

この報告をcommit / pushした後も、current branchのupstream差分`0/0`とtracked cleanをhandoff条件とする。

## PLANNER007端末で整えた開発基盤（履歴）

| 基盤 | 実測・実施内容 | この端末の判定 | 可搬性または残存条件 |
| --- | --- | --- | --- |
| Python | Python 3.11.0、uv 0.10.0、`uv sync --extra dev --locked` | 開発可能 | entry point warningがあるため現状はmodule/script実行を使う |
| Python lock | ignored `uv.lock`、pytest 8.4.2を解決 | locked sync成功 | clean Git checkoutだけではlockが得られない |
| Electron GUI | Node 22.19.0、npm 10.9.3、`npm ci`、`npm ls --depth=0` | Electron 35.7.5をexact install | ignored `gui/package-lock.json`に依存し、Git可搬ではない |
| GUI security | latest registryに対する`npm audit --json` | Electron 1 packageをhighとして集約、17 advisory entry | fix候補はElectron 43.2.0へのbreaking major。無監査適用しない |
| GUI source | tracked JavaScript 12 filesへ`node --check` | 全件pass | UI interaction / screenshot smokeは未実行 |
| .NET render driver | SDK 10.0.302、Release build | warning 0 / error 0 | YMM4 executable不在のため実UI互換は未検証 |
| Media tools | ffmpeg / ffprobe 8.1.1 | command利用可能 | accepted MP4不在のためfresh full decodeは未実行 |
| YMM4 | bounded local rootsとPATHを確認 | executable未検出 | real render / discovery / version readback不可 |
| Source project | manifest exact locator / SHA-256 authorityはtracked | local fileなし | public Gitへ追加せず、必要時のみexact fileを復元 |
| Real-media assets | manifestの9 cue locators | 9/9 local fileなし | rights/permission確認済みtransfer経路が必要 |
| Generated project / accepted MP4 | receipt exact locator / hashはtracked | どちらもlocal fileなし | product acceptanceはtracked decisionに残るが、この端末で再観測不可 |

`npm audit fix --force`、package manifestの変更、lockfileのtracked authority化は行っていない。
前者はbreaking major、後二者は依存契約変更に当たるため、次sliceの監修判断を経て実装する。
Electron公式は最新3 stable majorだけをsupport対象とし、現在のstableは41 / 42 / 43、
registry latestは43.2.0である。したがって35.7.5は「advisoryを個別回避すれば保守継続できる
supported baseline」ではなく、互換性を測りながらsupported majorへ移す対象である。
根拠は[Electron release policy](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)と
[Electron 43 release](https://www.electronjs.org/blog/electron-43-0)を参照する。

## PLANNER007端末のローカル検証（履歴）

| 検証 | 結果 | 保証すること | 保証しないこと |
| --- | --- | --- | --- |
| canonical Regression Integrity | **165 passed / 5 skipped / 0 failed / 0 errors**、72.82秒 | current terminalのtracked + available local evidenceで16 modulesがgreen | 欠けたprivate artifactの内容 |
| skip contract | historical YMM4 3、reference layout review surface 1、trace capture 1 | 5件すべて`requires_local_evidence`として分類済み | private artifactをGitで持つべきこと |
| workspace integrity | status / diff / cached diff不変、temp除去 | runnerがworktreeを汚さない | unrelated ignored outputのbyte identity |
| runner focused contracts | **6 passed** | JUnit、skip分類、Git三面、cleanup契約 | product quality |
| project state sync | **PASS** | runtime / cockpitのstate mirror | 過去reportの端末固有可用性 |
| Python compile | `src`とcanonical runner | **PASS** | 外部tool runtime |
| GUI dependency/syntax | npm exact tree、Electron version、JS 12 files | **PASS** | 実window操作とvisual correctness |
| render driver build | .NET 10 Release | **warning 0 / error 0** | 実YMM4 render |
| Git drift | fetch/pull後、setup/test後に確認 | tracked cleanを維持 | ignored lockのremote portability |

tracked machine resultの正本に記録された三モード値はclean-room `161/9`、
evidence-rich same-machine `166/4`、tracked-only linked worktree `161/9`である。今回の`165/5`は
別端末のlive locator可用性差であり、total 170、failure/error 0、valid skip contract、
workspace integrity passは一致する。端末差を製品regressionや受理取消しへ読み替えない。

## PLANNER007 snapshot時点の製品現在地（履歴）

| 能力・gate | 製品checkpoint | この端末で今できること | 次に必要な判断 |
| --- | --- | --- | --- |
| Source / script lock | 18 protected inputs、9 cue、2/4/3 scene、3/6 speaker | contract / adapter開発と回帰 | contentを変える場合だけ別approval |
| One-command internal-review path | same-machine実MP4まで成立済み | synthetic pathとcodeを検証 | render portabilityは別goal |
| Stable internal cut | exact real-media cutをhuman accepted | receipt / manifest / hash authorityを利用 | rerenderせず次gateへ進む |
| Regression integrity | 三モードgreen、Git非破壊 | canonical runnerで端末固有165/5 green | CI / lock strategyへ接続 |
| Dependency portability | local locksでこの端末は開発可能 | Python / GUI実装 | lockをtracked authorityにする方針 |
| GUI security | Electron 35.7.5が動作基準 | source検査とlocal launch準備 | supported majorの互換検証 |
| Rights / production | internal review only | provenance設計、ledger準備 | asset owner / permission / attribution |
| Default integration | 検証base時点でfeature branchが38 commit先行 | PR差分監査 | mergeを別途明示承認 |

North Star上、source-backed contentからYMM4実MP4へ至る縦経路、real-media visual acceptance、
evidence-safe regression gateまでは閉じた。次の価値は同じcutを再生成することではなく、依存とGUIを
別端末で再現できる開発基盤にし、その後にreview portability、default integration、rights-cleared
production、GUI標準loop、複数topic factoryへ順序立てて一般化することである。

## 先まで見通した段階目標

以下は到達順の提案であり、各段階のexit signalを得たときだけ次へ進む。後段目標の存在は、
前段の依存変更・rights・publication approvalを代替しない。

| 段階 | 解くbottleneck | 完了条件 | 現在の前提 | 完了すると開く工程 |
| --- | --- | --- | --- | --- |
| **0. Accepted cut / Regression checkpoint** | creative判断と回帰信頼性 | exact cut human acceptance、三モードfailure/error 0 | **完了済み** | 開発基盤とproduction準備をcreative再審なしで進められる |
| **1. Dependency authorityを固定** | ignored lockでclean checkoutが再現不能 | `uv.lock`と`gui/package-lock.json`のowner、tracking、更新手順、drift checkを決め、fresh checkoutでlocked install成功 | local locksとcurrent manifestsあり | 別端末のdeterministic setup |
| **2. Electron 43.2.0候補へ安全移行** | Electron 35がsupport外かつhigh advisory | isolated branchで43.2.0を固定し、startup、IPC、file dialog、Python bridge、capture scripts、audio-safety、rollbackを検証しaudit結果を更新。重大非互換時だけ41/42の最新minorを比較 | 段階1のlock authority、major変更承認 | GUI security baselineと保守可能なruntime |
| **3. Development bootstrapを一コマンド化** | Python / npm / .NET / ffmpeg / YMM4可否の判定が手作業 | non-destructive doctorがversion、lock、tool discovery、private locator availability、blocked reasonを機械可読receiptへ出す | 段階1–2のversion authority | 端末差を数分で分類し、誤ったrender開始を防止 |
| **4. Review / render portabilityを分離実装** | accepted decisionとlocal media availabilityが端末ごとに混同される | review-only artifact ingestとrender-capable source ingestを別contractにし、hash照合、private storage、fail-closed理由をGUIへ表示 | 段階3、private transfer方針 | 別端末でreviewだけ／rerenderまでの可否を即決 |
| **5. Current checkpointをdefault branchへ統合** | 後継成果がfeature branchに滞留 | accepted cut、regression、dependency/security方針、privacy/path audit、PR reviewを満たし、normal-history mergeを明示承認 | 段階1–4のどこまでmerge条件にするか監修決定 | default branchから後続topic / production laneを開始 |
| **6. Rights-cleared visual setを確定** | human-accepted real mediaがinternal-review rightsに留まる | cueごとにkeep / replace / crop / omit、source、license、permission、attribution、territory、expiry、safe-areaをledger化 | accepted visual intentを変更しない | production master候補で使えるasset identity |
| **7. Production master candidateを閉じる** | internal cutと公開候補の品質・権利差 | rights-cleared asset、final audio/subtitle/motion、codec/bitrate/full decode、frame review、human acceptanceをexact hashへ結合 | 段階6、production authorization | packaging / release candidate判断 |
| **8. GUI標準制作loopを完結** | current operator pathがCLI/docs中心 | ingest、doctor、dry-run、blocked reason、render progress、receipt、cue decision、acceptance freezeをGUI primary surfaceで完結 | 段階2–4 | 人間をcreative / rights判断へ集中させる日常運用 |
| **9. 3-topic vertical sliceでfactory性を証明** | 新紙幣1本だけではcase-specific成功を排除できない | 3 topicでsource packet→IR→template/asset resolution→YMM4/internal reviewを同じcontractで通し、差分をadapter/registryへ隔離 | 段階5・8 | versioned production factory contract |
| **10. 連続3本のoperator実績を閉じる** | smoke成功と継続運用の再現性が別 | silent drift、private leak、fatal rerun各0、YMM4 open原則2回以内、例外classと修正量を3本分receipt化 | 段階9 | 運用SLO、training、保守優先度 |
| **11. Publication governanceを接続** | 技術完成と公開判断が分離 | title/thumbnail promise、source attribution、rights、metadata、publication authorization、rollbackをrelease packetへ束ねる | 段階7・10、公開owner承認 | 制御された公開判断 |
| **12. Feedbackをversioned改善へ戻す** | 公開後学習が場当たり化 | 権限内analytics / review feedbackをtopic、script、visual、template、operator failureへ分類し、採用変更だけをversioned registry / diagnosticへ反映 | 段階11とanalytics権限 | 継続改善する制作system |

直近は段階1と2を同じ「dependency-portability / GUI-security lane」で設計してよいが、commitは
「lock authority」と「Electron major compatibility」を分離するとrollbackとレビューが明確になる。
accepted cutのmedia、script、timing、visual decisionはこのlaneで変更しない。

## 監修AIが次に選べる入口

| 入口 | 先に減る摩擦 | 必要条件 | 選ぶと次に可能になること |
| --- | --- | --- | --- |
| **Advance — lock authorityを固定（推奨）** | clean checkoutで依存集合を再現できない | `.gitignore`と依存更新契約を変更する承認 | Electron upgradeとCIを同じlock基準で検証 |
| **Audit — Electron 43系互換性の実験計画** | high advisoryの解消方法が未確定 | production codeを変えない検証branchとrollback基準 | major upgradeのgo / revise / hold判断 |
| **Verify — private artifact portability設計** | この端末でrender/review不可、receiptとlive availabilityが分離 | private storage / transfer ownerの決定 | review-only ingestとrender-capable ingestの実装契約 |
| **Explore — default integration / rights gate分解** | feature成果と公開準備が同じ大きな判断に見える | merge ownerとrights ownerを分離 | 技術checkpointのmerge条件とproduction asset計画を独立決定 |

推奨defaultはAdvanceである。コード開発はすでに可能で、最大の横断摩擦は、別checkoutへ依存集合を
再現できないことにある。lock authorityを先に固定すれば、Electron major検証、bootstrap、CI、
default integrationの全てが同じ基準を使える。YMM4やprivate mediaの復元は、直近dependency laneの
前提ではなく、render/review portabilityを実装・検証するときに必要な別入口である。

## 維持すべき停止条件

- accepted cutのspeech、wording/order、cue/subtitle timing、line breaks、visual treatmentを、
  dependency / GUI security laneで変更しない。
- source `.ymmp`、generated project、MP4、frames、real-media binary、browser profileをpublic Gitへ追加しない。
- private artifact不在を空file、異なるproject、旧hashの無断更新で埋めない。
- tracked acceptance receiptを、この端末にlive MP4があるという証明へ読み替えない。
- .NET build passやffmpeg availabilityを、YMM4 discovery、real render、human playbackのpassへ読み替えない。
- `npm audit fix --force`でElectron majorを無監査適用しない。
- ignored lockをそのままportable reproducibilityと呼ばない。
- canonical `165/5`を、欠けた5 private locatorsの内容検証済みとは扱わない。
- rights-cleared、production-ready、publication-approvedをtechnical checkpointから推論しない。
- PR、merge、master integration、external upload、publicationは明示された別判断なしに実行しない。
