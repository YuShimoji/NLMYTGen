# 監修AI向け・最新リモート同期、開発再開判断、長期目標案（2026-07-23 JST）

Scope: NLMYTGen

この文書は、公開リモートの最新後継開発線を現在端末へ取り込み、宣言済み依存、focused contract、
render driver、private artifactの可用性をこの端末で再測定した時点証跡である。製品状態と直近gateの
正本は[`runtime-state.md`](../runtime-state.md)、機能statusの正本は
[`FEATURE_REGISTRY.md`](../FEATURE_REGISTRY.md)とする。ここで提案する長期goalは監修判断の材料であり、
未承認feature、依存契約変更、rights、production、publication、PR merge、master integrationを
自動的に許可しない。

## 監修判断に必要な結論

開始worktree `C:\Users\PLANNER007\NLMYTGen` の
`codex/nlmytgen-end-to-end-auto-video-v1`はremoteと`0/0`だった。同じfetchで、直系後継
`origin/codex/nlmytgen-regression-integrity-v1`に新着2 commitを確認した。このbranchは別のlinked
worktree `C:\Users\PLANNER007\NLMYTGen-regression-integrity-v1`ですでにcheckout済みだったため、
重複branchを作らず、その既存worktreeを`6f12bbc`から`2f55849`へfast-forward-onlyで同期した。
同期直後のupstream差分は`0/0`、`origin/master`より29 commit先行・遅れ0、tracked worktreeはcleanである。

Python、Electron GUI、回帰支援、.NET render-driverの開発はこのworktreeで開始できる。
`uv sync --extra dev --locked`、Electron 35.7.5導入、focused 46 tests、state sync、対象module compile、
.NET 10.0.302によるRelease buildが完了した。元の.NET 9.0.304ではtarget `net10.0-windows`をbuildできなかった
ため、repoの既存要求に合わせMicrosoft .NET SDK 10.0.302を追加し、targetを下げていない。

ただし、この端末の全4 worktreeにはmanifest指定のsource `.local.ymmp`、generated project、
`internal_review.mp4`が存在しない。silent `--dry-run`はtrackedな18 inputを読む前段ではなく、private
source locatorで`source_ymmp_missing`としてfail-closeした。したがって「one-command経路が過去の
same-machine evidenceで成立済み」という製品状態は維持できる一方、この端末ではhuman reviewと再renderを
今すぐ実行できない。直近の実行可能なproduct moveは、既存MP4をexact hashで安全に再配置するか、
manifest hashに一致するsource projectを再配置してtoolchain preflightから再開することになる。

## リモート同期と作業面

| 確認対象 | 実測 | 現在状態 | 監修上の意味 |
| --- | --- | --- | --- |
| remote fetch | `git fetch --prune origin` | 後継branchに2 commitの新着を取得 | cross-device handoffと最新roadmapを回収 |
| 開始branch | `HEAD...@{u}` | `9ed7cdf`、`0/0` | 旧handoff線は改変せず保持 |
| 後継branch | FF-only pull | `6f12bbc` → `2f55849` | Regression Integrityを含むcurrent handoff線へ同期 |
| default branchとの関係 | ancestry / rev-list | 29 ahead / 0 behind | master内容を欠かさずfeature成果を保持するが、未merge |
| worktree | status / diff / cached diff | tracked clean、upstream `0/0` | user成果物を退避・削除・一括stageしていない |
| publication state | runtime / PR readback | draft PR #2はreview-only | merge、release、公開承認を意味しない |

対象branchがすでにlinked worktreeに割り当てられていたため、開始worktreeでの`git switch`はGitが安全に拒否した。
その拒否を回避するためのbranch複製やworktree削除は行わず、既存の正規worktreeを更新した。以後の開発開始点は
`C:\Users\PLANNER007\NLMYTGen-regression-integrity-v1`である。

## この端末で整えた開発基盤

| 基盤 | 実測・実施内容 | 判定 | 残る条件 |
| --- | --- | --- | --- |
| Python | Python 3.11.0、uv 0.10.0、pytest 8.4.2、`uv sync --extra dev --locked` | 開発可能 | entry point warningのため現行どおりmodule実行を使う |
| Python lock | ignored `uv.lock`を利用 | 同worktreeでは再現可能 | Gitだけの新規checkoutにはlockがなく、portable locked syncは未成立 |
| Electron GUI | Node 22.19.0、npm 10.9.3、Electron 35.7.5、`npm ls --depth=0` pass | 開発可能 | lockfileはignoredでlocal生成。clean checkoutの完全再現性はない |
| GUI security | `npm audit`でdirect Electronにhigh 1件 | 要計画修復 | 自動fixはElectron 43.2.0へのsemver-major。無監査の`--force`更新はしない |
| Media tools | ffmpeg / ffprobe 8.1.1 | media診断可能 | review MP4自体がないためfresh decodeは未実行 |
| Render driver | .NET SDK 10.0.302を追加、Release build | **warning 0 / error 0** | workload検証warningは残るがcurrent driver buildは成立 |
| YMM4 executable | 正式discoveryが`yymm4_executable_missing` | render実行は未準備 | source復元と併せ、`NLMYTGEN_YMM4_EXE`または標準pathへ正規installが必要 |
| Source YMM4 | 全4 worktreeでmanifest locatorを照合 | **不在** | SHA-256 `beee7eab...eaa54`のexact sourceが必要 |
| Review MP4 | 全4 worktreeでexpected locatorを照合 | **不在** | SHA-256 `f2444f...421f7`の既存carrier移送、または承認済み再renderが必要 |

GUIの`package-lock.json`とPythonの`uv.lock`はいずれもrepo policyでignoreされている。このworktreeでは依存を
解決済みなので即時開発を妨げないが、「Gitだけで別端末へ渡し、同じ依存集合を再現する」契約には不足する。
Electronのmajor upgradeはGUI runtime/API差分を伴いうるため、開発環境整備の名目で無断適用していない。

## 今回の検証結果

| 検証 | 結果 | 保証すること | 保証しないこと |
| --- | --- | --- | --- |
| episode video / media validation / silent runtime / project-state tests | **46 passed** | current manifest、synthetic pipeline、media判定、silent境界、state mirror | private sourceと実YMM4 render、human quality |
| `scripts/check_project_state_sync.py` | **PASS** | runtime / cockpitのstate整合 | 過去reportの端末固有artifact可用性 |
| current CLI / pipeline / validation / state / integrity runner compile | **PASS** | 対象Python moduleの構文・import前段 | 外部tool操作 |
| render-driver Release build | **PASS: warning 0 / error 0** | .NET 10でcurrent UIA driverをcompile可能 | 実YMM4 UIとversion compatibility |
| silent `--dry-run` | **expected block: `source_ymmp_missing`** | private input不在をfail-close | protected 18 input、cue、scene、speakerの実source preflight |
| Git drift | status、diff-check、upstream差分を確認 | tracked product artifactに意図しない差分なし | ignored依存・build outputのbyte portability |
| canonical Regression Integrity | **今回再実行せず** | 既知の危険なtemp copyを避けた | same-machine / linked-worktree green |

canonical runnerは、独立clean-roomでは`157 passed / 9 skipped / 0 failed / 0 errors`だが、
evidence-rich checkoutではprivate evidence混入と巨大temp copyで`135 passed / 11 failed / 16 errors /
4 skipped`、tracked-only linked worktreeではabsolute-path `git check-ignore`のため
`156 passed / 1 failed / 9 skipped`という既知状態である。repo-local runtimeの指示どおり、fixture修正前に
このlinked worktreeで再実行してdisk spikeを再発させていない。46件のfocused passを、この未完了gateの
代替greenとは扱わない。

## 製品の現在地と現在端末の差

| 能力・gate | 製品としての状態 | 現在端末で可能なこと | 次に必要なもの |
| --- | --- | --- | --- |
| Source / claim / script | 18 protected input、9 cue、2/4/3 scene、3/6 speakerをtracked lock | code・contract変更とfocused検証 | content変更時だけ別approval |
| One-command internal-review path | 過去same-machine evidenceで成立、receiptはtracked | pipeline/driverの開発とsynthetic検証 | private source + YMM4 discoveryで実行可能性を再確認 |
| Internal-review carrier | receipt/hash/codec/frame inspectionの履歴あり | tracked receiptの監査 | exact MP4または正規再生成input |
| Human creative/audio review | Product-Gateとして未完了 | carrier不在のため実行不可 | MP4復元後に通し視聴しcue別decision |
| Broad regression integrity | independent checkout green | focused開発 | 3実行形態のfixture/locator収束 |
| Dependency portability | local worktreeは準備済み | Python/GUI実装 | lock正本化方針とElectron upgrade検証 |
| Production asset / rights | proxyのみ、未承認 | ledger/設計作業 | asset identity、license、attribution、human visual判断 |
| Master / publication | 未承認 | release contractの設計 | creative、rights、merge、publicationの独立承認 |

North Star上は「source-backed contentからYMM4実MP4までの縦経路を1本で実証済み」だが、この端末では
private carrierが切れている。次の価値は、新機能を増やすことより、まず可搬性境界を守ってreview carrierを
復元し、人間判断まで1本を閉じること、その成功をclean checkout・別topic・GUI標準loopへ一般化することにある。

## 先まで見通した目標設定案

以下は承認済みroadmapではない。各段階はexit signalが得られたときだけ次へ進み、互いのgateを代替しない。

| 段階 | 解くbottleneck | 完了条件 | 前提・現在状態 | 完了すると開く工程 |
| --- | --- | --- | --- | --- |
| **1. Review carrierを復元（直近推奨）** | current端末にMP4/sourceがなくhuman gateへ届かない | 第一選択は既存MP4をexpected pathへ置きSHA-256 `f2444f...421f7`を照合。無ければsourceをexact path/hashで復元しsilent dry-runをpass | code/driverはready。private binaryはpublic Gitへ置かない | human review、または承認済み再render |
| **2. Human reviewを閉じる** | machine pass後の発音・rhythm・cue切替・字幕comfort・構図が未判定 | exact MP4を通し視聴し、`accept / repair / reject`をcue IDと観測付きで返す | goal 1が必要 | stable internal cutまたはbounded repair scope |
| **3. Cue限定repairとacceptance freeze** | NG原因がcontent / timing / visual / toolのどこか曖昧 | 指摘cueだけを分類・修正し、content lockを守って再render、receipt/hash/frame reviewを更新。acceptなら再renderせずdecision固定 | goal 2のhuman signal | production asset/rights判断へ渡せるcut |
| **4. Regression Integrityを3実行形態で閉じる** | clean-roomだけgreenでsame-machine/worktreeがred | ignored media/profileをcopy対象外へし、private evidenceをauthorityから分離、locatorをrepo-relative化。disk spikeなし・Git差分不変で分類一致 | product artifactを変えない限定slice | 次実装のfalse red低減、CI gate設計 |
| **5. 依存再現性とGUI securityを閉じる** | ignored lockとElectron 35の既知脆弱性でclean machine再現と安全更新が未確定 | uv/npm lockの正本化方針を決定し、Electron supported majorへのupgradeをbranch内でAPI/UI smoke、package audit、rollback可能性付きで検証 | major updateの監修承認が必要 | 別端末のdeterministic setup、GUI保守基盤 |
| **6. Render/review portabilityを製品化** | private artifact/toolchain有無でhandoff判定が揺れる | tool version、YMM4/.NET discovery、artifact hash ingest、review-only transfer、fail-closed reasonを1 operator surfaceへ統合 | goals 1・5の知見 | 別端末でreview/re-render可否を即判定 |
| **7. Technical milestoneをdefault branchへ統合** | feature branchだけがone-command能力を持つ | human decision、合意したregression gate、PR差分、privacy/path/state auditを満たし、監修承認後にnormal-history merge | 現在はmasterより29 commit先行、未merge | default branchから次sliceを開始 |
| **8. Proxyをrights-cleared production visualへ置換** | proxyは公開品質・rightsを満たさない | cue/sceneごとに`accepted / replace / cut / defer`を決め、source、permission、attribution、safe areaをledger化 | human aestheticとrights owner判断 | production master候補の制作 |
| **9. Production master candidateを閉じる** | internal-reviewと公開候補の品質差 | final audio、字幕、構図、motion、bitrate、decode、frame sample、source不変、rights ledgerとhuman acceptanceを満たす | goals 3・8 | packaging / release candidate判断 |
| **10. GUIで標準制作loopを完結** | current pathとreview decisionがCLI/docs中心 | ingest、dry-run、blocked reason、render progress、receipt、cue decisionがGUI primary surfaceで完結 | GUI security/portabilityを先に安定 | 人間をcreative判断へ寄せた日常運用 |
| **11. 3-topic vertical sliceと連続3本でfactory性を証明** | 新紙幣1本のcase-specific成功を排除できない | 3 topicで同一contractを通し、その後3本連続でsilent drift/private leak/fatal rerun各0、YMM4 open原則2回以内をreceipt化 | goals 6・10 | versioned factory、運用SLO、training |
| **12. Publication governanceとfeedback loopを接続** | 技術完成・公開判断・学習が分断 | title/thumbnail promise、source attribution、rights、metadata、明示publication authorizationを束ね、取得権限内のfeedbackをversioned template/diagnosticへ戻す | master acceptance、公開/analytics権限が必要 | 継続改善する制作system |

goal 1の最短経路は、以前の端末にvalidated MP4が残っていれば再renderせずcarrierだけを安全に移すことだ。
MP4が失われていれば、source `.local.ymmp`をmanifest exact hashで復元し、YMM4 executable discovery、
silent dry-run、承認済みrender、media validation、frame inspectionの順に進む。sourceも失われている場合は、
YMM4台本読込から同一9 VoiceItem source projectを再取得し、旧hashと異なる新authorityを無断で作らない。

## 監修AIが次に選べる入口

| 入口 | 先に減る摩擦 | 必要条件 | 選ぶと次に可能になること |
| --- | --- | --- | --- |
| **Advance — review carrier復元（推奨）** | human gateへ届かない最大の遮断 | 既存MP4、またはexact source projectの所在確認 | hash照合後のhuman review、またはbounded再render |
| **Audit — Regression Integrity修復** | linked/evidence-rich checkoutのfalse redとdisk spike | product artifactを変えないscope固定 | canonical gateを3実行形態で同じ分類へ収束 |
| **Excise — lock/Electron負債の限定slice** | clean checkoutの依存再現性とknown high advisory | major upgrade可否を監修判断 | deterministic setupとGUI security baseline |
| **Verify — draft PR #2とcurrent handoffの差分監査** | support branchの受理が未完了 | product gateとmerge判断を分離 | accept / revision / holdを明示しdefault integration条件を固定 |

推奨defaultはAdvanceである。validated carrierが別端末に残っていれば、コード変更や再renderなしでNorth Star最大の
未判定へ直接届く。所在確認ができない間はAuditを並行できるが、現canonical runnerを修正前のlinked worktreeで
再実行しない。Exciseは依存契約とmajor runtimeに触れるため、別sliceとして承認してから進める。

## 維持すべき停止条件

- source `.ymmp`、generated project、MP4、frames、browser profileをpublic Gitへ追加しない。
- source不在を空ファイル、異なるYMM4 project、旧hashの無断更新で埋めない。
- .NET 10 build passを実YMM4 render passやhuman acceptanceへ読み替えない。
- Electronのhigh advisoryを理由に`npm audit fix --force`でmajor upgradeを無監査適用しない。
- focused 46 passをsame-machine/worktree Regression Integrity greenへ読み替えない。
- human review前にproxyをfinal aesthetic、rights-cleared asset、production masterへ昇格しない。
- 監修承認なしにPR merge、master integration、external upload、publication、OAuth接続へ進まない。
- この長期goal案を承認済みfeature IDとして一括登録せず、選ばれた次sliceだけを狭い契約にする。
