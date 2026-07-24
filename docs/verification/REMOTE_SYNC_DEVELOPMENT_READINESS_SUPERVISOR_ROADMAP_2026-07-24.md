# 監修AI向け・最新リモート同期、開発再開判断、長期目標案（2026-07-24 JST）

Scope: NLMYTGen

この文書は、`C:\Users\PLANNER007\NLMYTGen` で公開リモートを再取得し、旧handoff線から
現在の正本であるaccepted-cut / regression-integrity線へ移行した後の、端末固有の開発可用性と
製品checkpointを分離して記録する。製品状態と直近gateの正本は
[`runtime-state.md`](../runtime-state.md)、非交渉境界は
[`INVARIANTS.md`](../INVARIANTS.md)、三モード回帰の機械可読結果は
[`REGRESSION_INTEGRITY_2026-07-24.json`](REGRESSION_INTEGRITY_2026-07-24.json)である。

ここで示す遠方目標は監修判断用の提案であり、依存契約変更、Electron major更新、rights、
production、publication、PR、merge、master integrationを一括承認するものではない。選択された
次sliceだけを狭い契約にし、accepted cutのclosed creative dimensionsを別目的の変更で開き直さない。

## 監修判断に必要な結論

作業開始時のローカルbranch
`codex/nlmytgen-end-to-end-auto-video-v1`はtracking先と`0/0`だったが、fetch後に、そのtip
`9ed7cdf`を直線的に14 commit進めた正式な後継
`origin/codex/nlmytgen-accepted-cut-regression-integrity-v1`が存在すると判明した。
後継にはreal-media版、human acceptance、三モード回帰修復が含まれ、旧branchへ逆流mergeする必要が
ないため、同名のlocal tracking branchを作成してFF系列のtip `e574614`へ移行した。取得直後の
upstream差分は`0/0`、`origin/master`より37 commit先行・遅れ0で、masterはcurrent branchの祖先である。

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

旧branchからcurrent tipまでの差分は35 tracked files、約3,470 insertions / 381 deletionsである。
中心は`src/pipeline/episode_video.py`のreal-media path、回帰fixture/runner、受理receipt、
manifest/provenance、状態文書であり、branch履歴はmergeなしの直線系列である。

## リモート同期とGit作業面

| 確認対象 | 実測 | 判定 | 監修上の意味 |
| --- | --- | --- | --- |
| remote refresh | `git fetch --prune origin` | 新branch 2本と既存回帰branch更新を取得 | stale remote-tracking refで判断していない |
| local branch | current canonical branchをtracking作成、`git pull --ff-only` | already up to date | 競合、rebase、history rewriteなし |
| upstream parity | 取得・検証開始時の`HEAD...@{u}` | `0/0` | 受信したtracked成果はremote tipと一致 |
| default branchとの関係 | `HEAD...origin/master`、ancestry | 37 ahead / 0 behind、masterは祖先 | default branch内容を欠かさず後継成果を保持するが、未merge |
| worktree保護 | canonical runner前後のstatus / diff / cached diff | byte-exact不変 | testsやsetupがtracked product artifactを汚していない |
| ignored setup | `.venv/`、`uv.lock`、`gui/node_modules/`、`gui/package-lock.json` | local development用に保持 | Gitだけの再現authorityではない |

この報告をcommit / pushした後も、current branchのupstream差分`0/0`とtracked cleanをhandoff条件とする。

## この端末で整えた開発基盤

| 基盤 | 実測・実施内容 | この端末の判定 | 可搬性または残存条件 |
| --- | --- | --- | --- |
| Python | Python 3.11.0、uv 0.10.0、`uv sync --extra dev --locked` | 開発可能 | entry point warningがあるため現状はmodule/script実行を使う |
| Python lock | ignored `uv.lock`、pytest 8.4.2を解決 | locked sync成功 | clean Git checkoutだけではlockが得られない |
| Electron GUI | Node 22.19.0、npm 10.9.3、`npm ci`、`npm ls --depth=0` | Electron 35.7.5をexact install | ignored `gui/package-lock.json`に依存し、Git可搬ではない |
| GUI security | `npm audit` | high severity 1件 | fixはElectron 43.2.0へのbreaking major。無監査適用しない |
| GUI source | tracked JavaScript 12 filesへ`node --check` | 全件pass | UI interaction / screenshot smokeは未実行 |
| .NET render driver | SDK 10.0.302、Release build | warning 0 / error 0 | YMM4 executable不在のため実UI互換は未検証 |
| Media tools | ffmpeg / ffprobe 8.1.1 | command利用可能 | accepted MP4不在のためfresh full decodeは未実行 |
| YMM4 | bounded local rootsとPATHを確認 | executable未検出 | real render / discovery / version readback不可 |
| Source project | manifest exact locator / SHA-256 authorityはtracked | local fileなし | public Gitへ追加せず、必要時のみexact fileを復元 |
| Real-media assets | manifestの9 cue locators | 9/9 local fileなし | rights/permission確認済みtransfer経路が必要 |
| Generated project / accepted MP4 | receipt exact locator / hashはtracked | どちらもlocal fileなし | product acceptanceはtracked decisionに残るが、この端末で再観測不可 |

`npm audit fix --force`、package manifestの変更、lockfileのtracked authority化は行っていない。
前者はbreaking major、後二者は依存契約変更に当たるため、次sliceの監修判断を経て実装する。

## 今回のローカル検証

| 検証 | 結果 | 保証すること | 保証しないこと |
| --- | --- | --- | --- |
| canonical Regression Integrity | **165 passed / 5 skipped / 0 failed / 0 errors** | current terminalのtracked + available local evidenceで16 modulesがgreen | 欠けたprivate artifactの内容 |
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

## 製品の現在地

| 能力・gate | 製品checkpoint | この端末で今できること | 次に必要な判断 |
| --- | --- | --- | --- |
| Source / script lock | 18 protected inputs、9 cue、2/4/3 scene、3/6 speaker | contract / adapter開発と回帰 | contentを変える場合だけ別approval |
| One-command internal-review path | same-machine実MP4まで成立済み | synthetic pathとcodeを検証 | render portabilityは別goal |
| Stable internal cut | exact real-media cutをhuman accepted | receipt / manifest / hash authorityを利用 | rerenderせず次gateへ進む |
| Regression integrity | 三モードgreen、Git非破壊 | canonical runnerで端末固有165/5 green | CI / lock strategyへ接続 |
| Dependency portability | local locksでこの端末は開発可能 | Python / GUI実装 | lockをtracked authorityにする方針 |
| GUI security | Electron 35.7.5が動作基準 | source検査とlocal launch準備 | supported majorの互換検証 |
| Rights / production | internal review only | provenance設計、ledger準備 | asset owner / permission / attribution |
| Default integration | 取得時点でfeature branchが37 commit先行 | PR差分監査 | mergeを別途明示承認 |

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
| **2. Electron supported majorへ安全移行** | Electron 35にhigh advisory | isolated branchでtarget majorを固定し、startup、IPC、file dialog、Python bridge、capture scripts、audio-safety、rollbackを検証しaudit結果を更新 | 段階1のlock authority、major変更承認 | GUI security baselineと保守可能なruntime |
| **3. Development bootstrapを一コマンド化** | Python / npm / .NET / ffmpeg / YMM4可否の判定が手作業 | non-destructive doctorがversion、lock、tool discovery、private locator availability、blocked reasonを機械可読receiptへ出す | 段階1–2のversion authority | 端末差を数分で分類し、誤ったrender開始を防止 |
| **4. Review / render portabilityを分離実装** | accepted decisionとlocal media availabilityが端末ごとに混同される | review-only artifact ingestとrender-capable source ingestを別contractにし、hash照合、private storage、fail-closed理由をGUIへ表示 | 段階3、private transfer方針 | 別端末でreviewだけ／rerenderまでの可否を即決 |
| **5. Current checkpointをdefault branchへ統合** | 37 commitの価値がfeature branchに滞留 | accepted cut、regression、dependency/security方針、privacy/path audit、PR reviewを満たし、normal-history mergeを明示承認 | 段階1–4のどこまでmerge条件にするか監修決定 | default branchから後続topic / production laneを開始 |
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
