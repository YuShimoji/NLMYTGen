# 監修AI向け・最新リモート同期、開発再開性、長期目標案（2026-07-22 JST）

Scope: NLMYTGen

この文書は、2026-07-22 13:25 JST時点で公開リモートを再取得し、repoが指定する
後継開発線をローカルへ同期した結果、実際に整えた開発環境、再検証した契約、実動画工程に
残る外部条件をまとめた時点証跡です。製品の現在位置と直近gateの正本は
[`runtime-state.md`](../runtime-state.md)、機能statusの正本は
[`FEATURE_REGISTRY.md`](../FEATURE_REGISTRY.md)です。本書の長期目標は監修用の提案であり、
未承認feature、rights、production、publication、PR、master integrationを自動的に許可しません。

## 監修判断に必要な結論

repo-local handoffが取得先に指定する
`origin/codex/nlmytgen-end-to-end-auto-video-v1`をfetch/prune後に確認し、
fast-forward-only pullを実施しました。同期対象HEADとupstreamはともに
`47d301b09503c82c169567e0a56e346b530006be`で差分`0/0`、pull結果は
`Already up to date`でした。取得時点でこのbranchはcommitter dateが最も新しいremote branchで、
`origin/master`をancestorとして22 commit先行・遅れ0です。本報告の追加commitは同期baselineを
書き換えず、handoff commitはpush後の同branch tipから解決します。

Python/Electronの通常開発は開始できます。`uv sync --extra dev --locked`と
`npm ci --no-audit --no-fund`を完了し、Python 3.11.0、pytest 8.4.2、Node 22.19.0、
Electron 35.7.5をreadbackしました。ロックファイルやtracked sourceへの差分はありません。
current one-command video sliceに直結する46 tests、project-state sync、current CLI/pipelineの
Python compileはpassしています。

ただし、この端末だけで実YMM4 renderまたはhuman reviewを完結できる状態ではありません。
render driverは`net10.0-windows`を要求しますが、local SDKは9.0.304だけで、buildは
`NETSDK1045`で停止します。manifestがhash固定するsource YMM4 projectと、human review対象の
`internal_review.mp4`もこの端末にはありません。非書き込み`--dry-run`は期待どおり
`source_ymmp_missing`でfail closedし、YMM4起動・render・output writeへ進みませんでした。

したがって現在地は、**portableなコード開発とfocused検証は再開可能、one-command内部レビュー
動画の成立はtracked receiptで確認可能、実視聴と再renderはprivate artifactおよびtoolchain待ち**です。
最短のproduct moveは新機能追加ではなく、検証済みMP4をprivateに渡してhuman reviewを閉じるか、
MP4が残るsource端末でreviewすることです。.NET 10導入はdependency追加に当たるため、明示判断なしに
実行していません。

## リモート同期と履歴の位置

| 確認対象 | 今回のreadback | 現在状態 | 監修上の意味 |
| --- | --- | --- | --- |
| 指定開発線 | `fetch --prune`、incoming/outgoing確認、FF-only pull | baseline `47d301b`、upstream `0/0` | 取り残した同branch commitやlocal-only commitなし |
| remote全体 | committer date順にbranch tipを確認 | current branchが最新remote tip | 日付だけで別branchへ乗り換える必要なし |
| default branch | ancestryと`HEAD...origin/master`を確認 | masterはancestor、ahead 22 / behind 0 | default内容を欠かさずfeature成果を保持 |
| worktree | 同期前後、依存同期後、診断後に確認 | tracked / untrackedともclean | user作業を退避・上書きしていない |
| current authority | `runtime-state`と`project-context`先頭handoffを再読 | `human-internal-review` gateを維持 | sync/reportだけで製品gateを進めていない |

開始時点から作業ツリーは空で、既存のuntracked residueもこのcheckoutにはありませんでした。
fetch/pull、dependency sync、tests、dry-run、build診断のいずれもtracked差分を生んでいません。

## この端末で整えた開発基盤

| 基盤 | 実測値・実施内容 | 判定 | 残る条件または注意 |
| --- | --- | --- | --- |
| Python | Python 3.11.0、uv 0.10.0、pytest 8.4.2、locked sync完了 | 開発可能 | project entry pointはpackage設定warningがあるため、現行READMEどおり`uv run python -m src.cli.main`を使う |
| Electron GUI | Node 22.19.0、npm 10.9.3、Electron 35.7.5、70 packagesをlockから再導入 | 開発可能 | transitive `boolean@3.2.0`のdeprecated warningは将来の保守対象 |
| Browser | Chrome 150.0.7871.129、Edge 150.0.4078.83 | SVG materialization用候補あり | 実行時はsilent policyとisolated profileを維持 |
| Media tools | ffmpeg / ffprobe 8.1.1 | validation実行環境あり | local MP4がないため今回のfull decode再実行対象なし |
| Render driver | .NET SDK 9.0.304、target `net10.0-windows` | **build block** | .NET 10 SDKが必要。target downgradeは契約変更なので行わない |
| .NET CLI健全性 | SDK/runtime列挙は可能だが`dotnet --info`のworkload情報取得でinstaller例外 | **要再確認** | .NET 10導入時にCLI healthも再readbackし、例外が残るならSDK/workload修復を別診断 |
| YMM4 executable | common install locationsに実行ファイルなし | **未確認 / block候補** | source不足でpipelineのYMM4探索段階へ未到達。不存在と断定せず、再render選択時にexact discoveryを行う |
| Source YMM4 | manifest exact pathに不存在、pilot配下の`.ymmp`候補0 | **dry-run block** | exact SHA-256 `beee7eab59196453c8d36b8889343cc82e876ea69e2bb00f5576bf17987eaa54`のprivate artifactが必要 |
| Review MP4 | expected ignored pathに不存在、pilot配下の`.mp4`候補0 | **human review block** | validated MP4のprivate transfer、またはsource端末でのreviewが必要 |

Python projectは`requires-python >=3.11`を満たします。`uv sync`のentry-point warningは
`[project.scripts]`がある一方でbuild-system / `tool.uv.package`が未定義なためですが、current CLIは
module実行で動作し、今回のfocused testsでも問題を起こしていません。ここを直すことは開発再開の
前提ではなく、packagingを正式に配布対象へ昇格するときの保守候補です。

## 今回実行した検証

| 検証 | 結果 | 保証すること | 保証しないこと |
| --- | --- | --- | --- |
| `test_episode_video_pipeline`、media validation、silent runtime、project-state sync | **46 passed / 4.36 sec** | manifest/preflight、synthetic pipeline、media判定、silent境界、状態同期のcurrent contract | 実YMM4、local MP4の画質・音質、human acceptance |
| `scripts/check_project_state_sync.py` | **PASS** | runtime / cockpit /関連state mirrorが同じProject-State-IDを参照 | 過去verification文書の全記述がcurrentであること |
| current CLI / episode pipeline / state checkerの`py_compile` | **PASS** | 対象Python modulesがcompile可能 | subprocess、外部tool、GUIの実動作 |
| render driver build | **FAIL: NETSDK1045** | source code判定前にSDK major不足で止まることを再現 | .NET 10環境でdriverが失敗すること |
| pipeline `--dry-run` | **FAIL CLOSED: `source_ymmp_missing`** | missing private inputをoutput write前に拒否 | source供給後のYMM4 discovery、version compatibility、render成功 |
| dependency sync後のGit readback | **clean** | lock定義の再導入でtracked driftなし | remote CIやclean-room別端末の再現性 |

最初のcompile診断では、実装pathを`src/pipelines/episode_video.py`と誤指定したため
path not foundになりました。current実装は`src/pipeline/episode_video.py`です。sourceを検索して
current importと一致する3 moduleへ修正後、compileはpassしました。これはruntime code defectではなく、
時点報告に残った検証コマンドのpath driftです。今後のreportでは実装pathを固定文字列で再利用せず、
current importまたは`rg`で解決します。

full `uv run pytest`は実行していません。repo-local ruleが、generated artifact/path driftと
tracked-fixture side effectを修復する明示的Integrity sliceまでfull suiteを通常closeout gateから
外しています。直前の2026-07-21 reportは広めの131 testsで98 passed / 33 failedを記録し、
local-only fixture、historical Project-State-ID、generator/補正文書driftへ分類しています。
今回のremote差分はそのreport 1 commitだけで実装変更を含まないため、side effectを再発させて
同じ広域runを繰り返していません。したがって監修上は、**focused current contractはgreenだが、
repository-wide regression gateはgreenと主張できない**状態を維持します。

## tracked authorityとprivate evidenceの境界

| artifact | Gitで取得できるもの | この端末の状態 | 次工程での扱い |
| --- | --- | --- | --- |
| episode manifest | 9 cue、scene/speaker mapping、18 protected hashes、tool/output contract | 存在 | input authorityとして利用可能 |
| pipeline / CLI / UIA driver | source、tests、operator README | 存在 | code変更・focused検証を開始可能 |
| validated receipt | project/media hash、73.583008秒、H.264/AAC、full decode、9 cue frame inspection | 存在 | source端末の成功証跡として利用。local再実行と混同しない |
| source `.local.ymmp` | public Gitへ載せない | 不存在 | exact path/hashのprivate供給が必要 |
| generated `.local.ymmp` | public Gitへ載せない | 不存在 | 再renderまたはprivate transferなしには復元不可 |
| `internal_review.mp4` / frames | public Gitへ載せない | 不存在 | human reviewのprimary surfaceを別経路で用意する |

source project、generated project、MP4はいずれもrepoのignore ruleで保護されています。
今回それらをGitへ追加、外部upload、探索目的のpublic access、空ファイルで代替する操作はしていません。
tracked receiptのMP4 SHA-256は
`f2444f9657a569e9a374582765c41a28e414040a018f029b0180f256657421f7`です。private transferを
選ぶ場合はexpected ignored pathへ置いた後、このhashを照合してからreview対象にします。

## 製品の現在地と残る判断

| 能力・gate | 現在状態 | 根拠 | 次に必要なもの |
| --- | --- | --- | --- |
| Source / claim / approved script | 完了・hash lock維持 | 18 protected inputs、9 cue text/order、2/4/3 scenes、3/6 speakers | content変更時だけsuccessor approval |
| Reference-grounded proxy visual | 実装済み・内部レビュー用 | reference reconstruction、cue-bound SVG、tracked readback | final aesthetic、production asset、rights判断 |
| One-command internal-review video | remote evidence上で成立 | validated receipt、46 current contract tests | local再現にはprivate sourceとrender toolchain |
| Human audio/creative review | **未完了** | runtimeの`human-internal-review` gate | validated MP4をreviewerへ届け、cue別decisionを返す |
| Broad regression integrity | **未完了** | 直前広域runに33 known failures | clean checkoutでも意味のあるfixture/state分離 |
| Production asset / rights | **未承認** | proxy geometryのみ | asset identity、license/permission、attribution、replacement decision |
| Production master / publication | **未承認** | current outputはinternal review only | creative、rights、packaging、publicationの独立gate |

North Starに対する推定現在地は、「source-backed contentからYMM4実MP4までの縦経路を1本で
実証したが、review mediaの可搬性、human acceptance、rights-cleared asset、clean-room再現、GUI標準運用、
複数topic反復は未完了」です。ここからは機能数を増やすより、**1本を人間判断まで閉じること**と、
**その成功を別端末・別topicでも再現できるfactory contractへ昇格すること**が価値になります。

## 先まで見通した目標設定案

次の表は承認済みroadmapではなく、監修AIがsliceを選ぶための提案です。各goalは前段の成功を
暗黙に仮定せず、exit signalが得られた時だけ次へ進みます。Integrity作業はhuman review待ちと
並行できますが、reviewやrightsを代替しません。

| 段階 | 解くbottleneck | 完了条件 | 前提・現在状態 | 完了すると開く工程 |
| --- | --- | --- | --- | --- |
| **1. Human review carrierを到達させる（直近推奨）** | review MP4がこの端末にない | hash一致したMP4をprivate transferして再生、またはsource端末でreviewし、`accept / repair / reject`をcue ID・観測付きで返す | tracked receiptはpassed、media binaryだけlocal欠落 | repair scope確定またはinternal creative acceptance |
| **2. Cue限定repairとacceptance freeze** | human NGがコード・content・assetのどこに属するか曖昧 | 指摘cueだけを分類・修正し、content lockを守って再render、receipt/hash/frame reviewを更新。acceptなら変更なしでdecisionを固定 | goal 1のhuman signalが必要。repairが無ければskip | production asset/rights判断へ進めるstable internal cut |
| **3. Regression Integrityをclean-room化** | 広域testsの33 false/stale failuresとtracked side effect | local-only fixtureをskip/explicit profile化、historical stateをcurrent assertionから分離、generatorをnon-mutatingにし、clean checkoutの定義済みsuiteがside effectなしでgreen | current focused 46はgreen。human review待ちと並行可能 | 次の実装をfalse redなしで評価、CI gate設計 |
| **4. Render/review portabilityを製品化** | source端末に依存し、別端末handoffがmedia missingになる | tool versions/preflightを機械可読化し、.NET 10/YMM4 discovery、private artifact hash ingest、review-only transfer手順、fail-closed診断を1つのoperator surfaceへ統合 | .NET 10追加は明示承認が必要。public Gitへraw mediaを置かない | 再renderまたはreviewを別端末で再現可能 |
| **5. Technical milestoneをdefault branchへ統合** | feature branchだけがone-command能力を持つ | goal 1のdecision、goal 3の合意したgate、commit/path/privacy audit、state一意化を満たし、監修承認後にnormal-history PR/merge | 現在はmasterより22 commit先行、PR/master未承認 | 次の開発者がdefault branchから再開可能 |
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
| **Advance — validated MP4をprivate transferしてreview（推奨）** | この端末にprimary review surfaceがない | expected ignored pathへMP4を置きSHA-256 `f2444f...21f7`を照合 | 発音、rhythm、cue切替、字幕comfort、proxy構図を最短でdecision化 |
| **Verify — source端末でhuman review** | media移送とtoolchain追加を避ける | validated MP4が残る端末へreviewerがアクセス | 同じ`accept / repair / reject`を返し、この端末はcode-readyのまま維持 |
| **Audit — Regression Integrity slice** | 広域testsのfalse redとside effect | current product stateを変えないscope固定 | clean-room CI、default integration、次実装の信頼性を高める |
| **Enable — この端末で再render可能にする** | .NET/source/YMM4の再現block | .NET 10追加の明示承認、exact source `.ymmp`、compatible YMM4 | build → dry-run → bounded silent render → media validationを再実行 |

推奨defaultはAdvanceです。reviewのためだけにtoolchainを再構築すると、.NET導入、CLI health、
YMM4 discovery、private source供給という複数の新しいfailure pointが増えます。既存MP4はtracked receiptで
hashとfull decodeが固定されているため、private transferまたはsource端末reviewの方がhuman gateへ
直接届きます。Auditはその待ち時間に並行でき、EnableはMP4を取得できないか、承認済みrepairを
この端末で回す必要が生じた場合に選びます。

## 維持すべき停止条件

- .NET 10不足を隠すため、render driverを`net9.0-windows`へ下げない。
- source `.ymmp`、generated project、MP4、framesをpublic Gitへ追加しない。
- tracked receiptを「この端末で再生・再decode済み」の証拠に読み替えない。
- human review前にproxy visualをfinal aesthetic、production asset、rights approvedへ昇格させない。
- broad testのknown failuresをcurrent pipeline defectへ一括分類しない一方、repository-wide greenとも
  報告しない。
- user/supervisor判断なしにPR、master integration、publication、外部upload、OAuth接続へ進まない。
- long-range goalを承認済みfeature IDとして`FEATURE_REGISTRY`へ追加せず、実際に選ばれたsliceだけを
  狭い契約として起票する。
