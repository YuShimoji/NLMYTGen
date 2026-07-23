# 監修AI向け・最新リモート同期、開発再開性、長期目標案（2026-07-22 JST）

Scope: NLMYTGen

この文書は、2026-07-22 21:54 JSTから公開リモートを再取得し、repoが指定する
最新の後継開発線をローカルへ同期した結果、実際に整えた開発環境、再検証した契約、
evidence-rich checkoutとclean-roomの差をまとめた時点証跡です。製品の現在位置と直近gateの正本は
[`runtime-state.md`](../runtime-state.md)、機能statusの正本は
[`FEATURE_REGISTRY.md`](../FEATURE_REGISTRY.md)です。本書の長期目標は監修用の提案であり、
未承認feature、rights、production、publication、PR、master integrationを自動的に許可しません。

## 監修判断に必要な結論

開始branch `codex/nlmytgen-end-to-end-auto-video-v1`はfetch後に2 commit遅れていたため、
`7eaaef1`から`9ed7cdf`へfast-forward-onlyで同期しました。同じfetchで、そこから4 commit
直線的に進み、repo-local runtimeが取得先に指定する
`origin/codex/nlmytgen-regression-integrity-v1`を確認したため、local tracking branchへ
非破壊で切り替えました。同期baselineは`6f12bbc45f380b766ba74f54ec70b5c8dd1a9239`、
upstream差分`0/0`、`origin/master`より27 commit先行・遅れ0です。draft PR #2は
`codex/nlmytgen-end-to-end-auto-video-v1`向けのreview-onlyで、mergeやproduct gate前進ではありません。

Python/Electronの通常開発とcurrent video sliceの診断・再render準備は開始できます。
`uv sync --extra dev --locked`、`npm ls --depth=0`、focused 46 tests、state sync、compile、
.NET 10 driver build、silent `--dry-run`、既存MP4のfresh full decodeがpassしました。
Python 3.13.3、uv 0.10.7、pytest 8.4.2、Node 24.13.0、npm 11.6.2、Electron 35.7.5、
.NET SDK 10.0.204、ffmpeg/ffprobe 8.0.1をreadbackしています。

manifest exact pathのsource YMM4、generated project、human review対象の`internal_review.mp4`は
この端末のignored領域に実在し、SHA-256はmanifest/receiptと一致します。YMM4 executableも
探索可能です。今回は音声再生と再renderを行わず、existing validated mediaを保全しました。
したがって最短のproduct moveは、ローカルMP4を人間が通し視聴して`accept / repair / reject`を
cue IDと観測付きで返すことです。

一方、後継branchのRegression Integrityは**独立clean-roomではgreenだが、全再開形態でgreenでは
ありません**。このevidence-rich checkoutではprivate evidence混入と巨大temp copyにより
`135 passed / 11 failed / 16 errors / 4 skipped`、tracked-only linked worktreeでは
`156 passed / 1 failed / 9 skipped`でした。いずれもGit status/diff/cached diffは不変です。
このため、focused product developmentは再開可能ですが、canonical回帰runnerをsame-machineまたは
Codex worktreeでrelease gateとして使う前に追加修復が必要です。

## リモート同期と履歴の位置

| 確認対象 | 今回のreadback | 現在状態 | 監修上の意味 |
| --- | --- | --- | --- |
| 旧handoff線 | `fetch --prune`、incoming確認、FF-only pull | `7eaaef1`から`9ed7cdf`へ2 commit取得 | 監修roadmapとsync報告を欠落なく回収 |
| 最新handoff線 | ancestry、runtime取得先、4 commit差を確認してtracking switch | baseline `6f12bbc`、upstream `0/0` | Regression Integrity支援とdraft PR handoffを含む先端から再開 |
| default branch | ancestryと`HEAD...origin/master`を確認 | masterはancestor、ahead 27 / behind 0 | default内容を欠かさずfeature成果を保持 |
| worktree | 同期前後、検証後に確認 | tracked/cached clean、pre-existing untracked保持 | user証拠を退避・上書き・追跡化していない |
| current authority | `runtime-state`と`project-context`先頭handoffを再読 | `human-internal-review` gateを維持 | sync/reportだけで製品gateを進めていない |

開始時点から`.playwright-mcp/`、`artifacts/supervision/AGENT_REPORT_H2_SOURCE_V1.md`、
`phase-e-01-contact-acquired*.png`がpre-existing untrackedでした。ignoredのsource/output/media/
browser evidenceも保持しています。fetch/pull、dependency sync、tests、dry-run、build診断、
full decodeはそれらを削除・移動・追跡化していません。今回の文書更新だけを意図したtracked差分とします。

## この端末で整えた開発基盤

| 基盤 | 実測値・実施内容 | 判定 | 残る条件または注意 |
| --- | --- | --- | --- |
| Python | Python 3.13.3、uv 0.10.7、pytest 8.4.2、locked sync完了 | 開発可能 | entry point warningがあるため現行READMEどおり`uv run python -m src.cli.main`を使う |
| Electron GUI | Node 24.13.0、npm 11.6.2、Electron 35.7.5、`npm ls --depth=0` pass | 開発可能 | 今回はhealthy treeのため`npm ci`を重複実行していない |
| Browser | Chrome 150.0.7871.129、Edge 150.0.4078.83 | SVG materialization用候補あり | 実行時はsilent policyとisolated profileを維持 |
| Media tools | ffmpeg / ffprobe 8.0.1 | validation可能 | existing MP4の全stream decodeをfresh実行しexit 0 |
| Render driver | .NET SDK 10.0.204、target `net10.0-windows` | **build pass** | Release build warning 0 / error 0 |
| .NET CLI健全性 | SDK/runtime列挙とbuildは可能、`dotnet --info` workload情報だけinstaller例外 | **部分的要修復** | render driverは利用可能。workload操作前にCLI installer診断が必要 |
| YMM4 executable | pipeline discoveryが`YukkuriMovieMaker.exe`を解決 | **再render候補あり** | 今回はlaunchしていない。再renderはapproved repair時だけ |
| Source YMM4 | manifest exact pathに存在 | **hash一致** | SHA-256 `beee7eab...eaa54`、dry-run preflight pass |
| Review MP4 | expected ignored pathに存在 | **human review可能** | SHA-256 `f2444f...421f7`、93,375,804 bytes。音声再生はhuman判断待ち |

Python projectは`requires-python >=3.11`を満たします。`uv sync`のentry-point warningは
`[project.scripts]`がある一方でbuild-system / `tool.uv.package`が未定義なためですが、current CLIは
module実行で動作し、今回のfocused testsでも問題を起こしていません。ここを直すことは開発再開の
前提ではなく、packagingを正式に配布対象へ昇格するときの保守候補です。

## 今回実行した検証

| 検証 | 結果 | 保証すること | 保証しないこと |
| --- | --- | --- | --- |
| `test_episode_video_pipeline`、media validation、silent runtime、project-state sync | **46 passed** | manifest/preflight、synthetic pipeline、media判定、silent境界、状態同期のcurrent contract | human acceptance |
| `scripts/check_project_state_sync.py` | **PASS** | runtime / cockpit /関連state mirrorが同じProject-State-IDを参照 | 過去verification文書の全記述がcurrentであること |
| current CLI / pipeline / state / regression runnerの`py_compile` | **PASS** | 対象Python modulesがcompile可能 | GUIと外部toolの操作品質 |
| render driver Release build | **PASS: warning 0 / error 0** | current .NET 10でdriverをcompile可能 | 実YMM4 GUI renderの再実行 |
| pipeline `--dry-run` | **PASS** | source hash、18 protected inputs、9 cue、2/4/3 scenes、3/6 speakers、silent policy | render結果やhuman quality |
| existing MP4 hash + full decode | **PASS** | expected binaryがreceipt hashと一致し、current ffmpegで全stream decode可能 | 音声、テンポ、字幕comfort、構図のcreative acceptance |
| independent clean-room regression（remote evidence） | **157 pass / 9 skip / 0 fail / 0 error** | tracked-only独立checkoutでcanonical 16 modulesがgreen | same-machine evidence-rich checkout、linked worktree |
| evidence-rich current checkout | **135 pass / 11 fail / 16 error / 4 skip** | Git差分保護はpass | private evidence分類とcopy fixtureの安全性。release gateには不可 |
| tracked-only linked worktree | **156 pass / 1 fail / 9 skip** | product testsはほぼportable | absolute-path `git check-ignore`のworktree互換性 |

same-machine runnerの11 failuresは、ignored/privateなHTMLやNotebookLM識別情報が存在すると
authoritative package validatorが`no_private_or_notebook_identifiers`でfailする同一contract群です。
16 errorsはfixtureがpilot全体を`tmp_path`へcopyし、ignoredの複数MP4とChrome profile/cacheまで
複製してC driveを一時的に枯渇させた`WinError 112`です。runner終了後と一時worktree回収後、
空き容量は38.62 GBへ戻りました。Git status、worktree diff、cached diffはrun前後不変でした。

linked worktreeの1 failureは
`test_local_research_media_are_ignored_and_absent_from_tracked_proof`です。テストはnested tracked
`.gitignore`で正しくignoreされるpathを、`git check-ignore`へlinked-worktree内のabsolute pathとして渡し、
return code 1になりました。main checkoutのrepo-relative pathでは同じruleがreturn code 0です。
したがって監修上は、**focused current contractと独立checkout clean-roomはgreenだが、same-machine
evidence-rich実行とCodex linked worktreeはcanonical回帰gateとして未完成**です。repo-local ruleどおり
full suiteを通常gateへ昇格せず、次のIntegrity修復を限定sliceとして扱います。

## tracked authorityとprivate evidenceの境界

| artifact | Gitで取得できるもの | この端末の状態 | 次工程での扱い |
| --- | --- | --- | --- |
| episode manifest | 9 cue、scene/speaker mapping、18 protected hashes、tool/output contract | 存在 | input authorityとして利用可能 |
| pipeline / CLI / UIA driver | source、tests、operator README | 存在 | code変更・focused検証を開始可能 |
| validated receipt | project/media hash、73.583008秒、H.264/AAC、full decode、9 cue frame inspection | 存在 | tracked success authorityとして利用 |
| source `.local.ymmp` | public Gitへ載せない | exact path/hashで存在 | dry-runとapproved repair時の再render入力。無断変更しない |
| generated `.local.ymmp` | public Gitへ載せない | SHA-256 `f0361f...9853`で存在 | current MP4 bindingを維持 |
| `internal_review.mp4` / frames | public Gitへ載せない | SHA-256 `f2444f...21f7`で存在 | human reviewのprimary surface。再生成不要 |

source project、generated project、MP4はいずれもrepoのignore ruleで保護されています。
今回それらをGitへ追加、外部upload、再render、音声再生、空ファイルで代替する操作はしていません。
MP4はexpected ignored pathでSHA-256
`f2444f9657a569e9a374582765c41a28e414040a018f029b0180f256657421f7`と照合済みです。

## 製品の現在地と残る判断

| 能力・gate | 現在状態 | 根拠 | 次に必要なもの |
| --- | --- | --- | --- |
| Source / claim / approved script | 完了・hash lock維持 | 18 protected inputs、9 cue text/order、2/4/3 scenes、3/6 speakers | content変更時だけsuccessor approval |
| Reference-grounded proxy visual | 実装済み・内部レビュー用 | reference reconstruction、cue-bound SVG、tracked readback | final aesthetic、production asset、rights判断 |
| One-command internal-review video | same-machine evidenceで成立 | source/project/media hash、46 tests、driver build、dry-run、full decode | approved repair以外では再render不要 |
| Human audio/creative review | **未完了・即時実行可能** | exact MP4がlocalに存在 | reviewerが通し視聴しcue別decisionを返す |
| Broad regression integrity | **独立checkout green・実行形態互換は未完了** | remote 157/9/0、same-machine 135/11/16、linked worktree 156/1/0 | private evidenceとlinked-worktree対応 |
| Production asset / rights | **未承認** | proxy geometryのみ | asset identity、license/permission、attribution、replacement decision |
| Production master / publication | **未承認** | current outputはinternal review only | creative、rights、packaging、publicationの独立gate |

North Starに対する推定現在地は、「source-backed contentからYMM4実MP4までの縦経路を1本で
実証し、この端末でreview carrierも到達済みだが、human acceptance、rights-cleared asset、全checkout形態での
回帰再現、GUI標準運用、複数topic反復は未完了」です。ここからは機能数を増やすより、
**1本を人間判断まで閉じること**と、**その成功を別端末・別topicでも再現できるfactory contractへ
昇格すること**が価値になります。

## 先まで見通した目標設定案

次の表は承認済みroadmapではなく、監修AIがsliceを選ぶための提案です。各goalは前段の成功を
暗黙に仮定せず、exit signalが得られた時だけ次へ進みます。Integrity作業はhuman review待ちと
並行できますが、reviewやrightsを代替しません。

| 段階 | 解くbottleneck | 完了条件 | 前提・現在状態 | 完了すると開く工程 |
| --- | --- | --- | --- | --- |
| **1. Human reviewを閉じる（直近推奨）** | machine pass後のcreative/audio判断が未完了 | local exact MP4を通し視聴し、`accept / repair / reject`をcue ID・観測付きで返す | carrier/hash/full decodeは確認済み。音声再生だけhuman許可待ち | repair scope確定またはinternal creative acceptance |
| **2. Cue限定repairとacceptance freeze** | human NGがコード・content・assetのどこに属するか曖昧 | 指摘cueだけを分類・修正し、content lockを守って再render、receipt/hash/frame reviewを更新。acceptなら変更なしでdecisionを固定 | goal 1のhuman signalが必要。repairが無ければskip | production asset/rights判断へ進めるstable internal cut |
| **3. Regression Integrityを全実行形態で閉じる** | independent checkoutだけgreenで、same-machineとlinked worktreeがred | copy fixtureからignored media/profileを除外し、private evidenceをauthority入力から分離、`git check-ignore`をrepo-relative化。独立checkout・evidence-rich checkout・linked worktreeで同じ分類、disk spikeなし、Git diff不変 | focused 46はgreen。draft PR #2はreview-onlyで未受理 | 次の実装をfalse red/容量枯渇なしで評価、CI gate設計 |
| **4. Render/review portabilityを製品化** | toolchainとprivate mediaの有無でhandoff判定が揺れる | tool versions/preflightを機械可読化し、YMM4/.NET discovery、private artifact hash ingest、review-only transfer、fail-closed診断を1つのoperator surfaceへ統合 | この端末はrender-ready。raw mediaはpublic Gitへ置かない | 別端末でもreview/re-render可否を即判定 |
| **5. Technical milestoneをdefault branchへ統合** | feature branchだけがone-command能力を持つ | goal 1のdecision、goal 3の合意したgate、draft PR監査、commit/path/privacy audit、state一意化を満たし、監修承認後にnormal-history merge | 現在はmasterより27 commit先行、draft PR #2、merge未承認 | 次の開発者がdefault branchから再開可能 |
| **6. Proxyをrights-cleared production visualへ置換** | machine-pass proxyが公開品質・rightsを満たさない | 各cue/sceneを`accepted asset / replace / cut / defer`へ分類し、source/permission/attributionをledger化、誤解リスクとsubtitle safe areaを再review | visual aesthetic・asset・rights判断は未完了 | production master candidateの制作 |
| **7. Production master candidateを閉じる** | internal-review品質と公開候補品質の差 | final audio/pronunciation、字幕、構図、motion、bitrate、full decode、frame sampling、source不変、rights ledgerを満たすmaster候補とhuman creative acceptance | goals 2・6が必要。internal banner/proxyの扱いを明示 | packaging / release candidate判断 |
| **8. GUIで標準制作loopを完結** | current one-command pathとreview decisionがCLI/docs中心 | ingest、dry-run、blocked reason、render progress、receipt、cue review decisionがGUI primary surfaceで完結し、CLIは診断/automation経路に限定 | production contractはGUIをprimaryと規定、current episode pathは未統合 | 人間をcreative判断へ寄せた日常運用 |
| **9. 3-topic vertical sliceでfactory性を証明** | 新紙幣1本だけではcase-specific成功の可能性が残る | Real Estate DX、AI monitoring、Baseball等の少なくとも3 topicで、source→IR→visual decision→YMM4/internal reviewの同一contractを通し、topic固有差分をregistry/adapterへ隔離 | Baseballはsidequestのため、本流acceptanceを置換しない | reusable factoryとしてのversioned release |
| **10. 連続3本のoperator実績で量産性を測る** | smoke成功と実運用の時間・手戻りは別 | 3本連続でsilent content drift 0、private leak 0、fatal rerun 0、YMM4を開く回数は原則2回以内、例外修正量と所要時間をreceipt化 | goals 4・8・9が必要 | 運用SLO、training、保守優先度の決定 |
| **11. Packaging / publication governanceを接続** | 技術完成と公開判断が分離されたまま | title/thumbnail promise、source attribution、rights、description/metadata、final checklist、明示publication authorizationを1つのrelease decisionへ束ねる | YouTube uploadやOAuthは現時点でhold/未承認 | human ownerが安全に公開可否を決定 |
| **12. 公開後feedbackを次episodeへ戻す** | 動画完成が学習せず、同じmanual painを繰り返す | retention/feedbackを取得権限内で集約し、content変更とvisual改善を分離、template/diagnosticへversionedに反映し、過去approvalをsilentに書き換えない | publication後かつanalytics accessの明示許可が必要 | 継続的に改善する制作system |

この目標列の重要な分岐は、goal 1で`accept`か`repair`かが決まる点です。`accept`ならgoal 2の
再renderを省き、Integrity / portability / default integrationとasset-rightsを並行できます。
`repair`なら、指摘をcue IDで限定し、approved scriptの意味変更が必要か、visual/timingだけかを
先に分類します。`reject`なら局所repairを続けず、product direction checkへ戻します。

長期のfactory性は、単に3 topicでコマンドがexit 0になることではありません。少なくとも次を
横断指標にする提案です。

- approved contentのsilent drift、private path leak、未分類rights itemを各0件にする。
- local-only artifactが無いclean checkoutでも、code/contract開発と失敗理由の判定までは行える。
- 人間の入力を、visual方向、発音・rhythm、asset/rights、最終公開という高位判断へ寄せる。
- 同じfailure classでの無根拠な再試行をせず、receiptからownerと次artifactを一意に決める。
- YMM4はbasic design discoveryに使わず、template登録と全素材後のcreative acceptanceに限定する。

## 監修AIが次に選べる入口

| 入口 | 先に減る摩擦 | 必要条件 | 選ぶと次に可能になること |
| --- | --- | --- | --- |
| **Advance — local MP4をhuman review（推奨）** | North Star最大の未判定 | 音声再生可能な環境でexact local MP4を通し視聴 | 発音、rhythm、cue切替、字幕comfort、proxy構図を`accept / repair / reject`へdecision化 |
| **Verify — draft PR #2を監修差分監査** | Regression Integrity修正自体の受理が未完了 | product gateと切り離してreview | 既存支援差分を受理・修正要求・保留に分類 |
| **Audit — same-machine/worktree Integrity修復** | private evidence混入、disk spike、linked-worktree 1 failure | current product/artifactを変えないscope固定 | canonical gateを3実行形態で同じ分類へ収束 |
| **Repair — cue限定再render** | human reviewで具体的NGが出た場合 | cue ID、観測、変更class、content lock維持 | build済みdriverとdry-run済みsourceからbounded再生成 |

推奨defaultはAdvanceです。carrier、hash、full decode、driver build、dry-runは成立しており、
新しいtoolchain作業なしにhuman gateへ直接届きます。Auditはhuman review待ちと並行可能ですが、
same-machineで現runnerを再実行すると再び大容量temp copyを起こすため、先にfixture設計を修正します。
Repairはhumanからcue-specific指示が出るまで開始しません。

## 維持すべき停止条件

- current buildがpassしているため、render driverの`net10.0-windows` targetを理由なく下げない。
- source `.ymmp`、generated project、MP4、framesをpublic Gitへ追加しない。
- fresh full decodeをhuman視聴・音声・画面品質acceptanceへ読み替えない。
- human review前にproxy visualをfinal aesthetic、production asset、rights approvedへ昇格させない。
- independent clean-room greenをsame-machine/worktree greenへ読み替えず、今回の11 failures、16 errors、
  1 worktree failureをcurrent pipeline defectへ一括分類もしない。
- evidence-rich checkoutで現canonical runnerを再実行し、ignored media/profileをtempへ再複製しない。
- user/supervisor判断なしにPR、master integration、publication、外部upload、OAuth接続へ進まない。
- long-range goalを承認済みfeature IDとして`FEATURE_REGISTRY`へ追加せず、実際に選ばれたsliceだけを
  狭い契約として起票する。
