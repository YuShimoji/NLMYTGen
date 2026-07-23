# 監修AI向け・最新リモート同期、開発再開判断、長期目標案（2026-07-23 JST）

Scope: NLMYTGen

この文書は、公開リモートの最新後継開発線を受信端末へ取り込み、宣言済み依存、focused contract、
render driver、private artifactの可用性を再測定した時点証跡である。follow-up auditでは
`eb883979479fd9a0cdace1d82fdb1295e6c80950`を再監査anchorとしてfetchとFF-only pullを行い、
already up to dateを確認した。2026-07-23の送信端末と受信端末では
private artifactの可用性が異なるため、端末固有の観測を製品状態やGit可搬性へ読み替えない。製品状態と直近gateの
正本は[`runtime-state.md`](../runtime-state.md)、機能statusの正本は
[`FEATURE_REGISTRY.md`](../FEATURE_REGISTRY.md)とする。ここで提案する長期goalは監修判断の材料であり、
未承認feature、依存契約変更、rights、production、publication、PR merge、master integrationを
自動的に許可しない。

## 監修判断に必要な結論

受信worktree `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen` の
`codex/nlmytgen-regression-integrity-v1`は、`git fetch --prune origin`とFF-only pull後も
再監査anchor `eb88397`のままalready up to dateだった。この文書更新前のupstream差分は`0/0`、
`origin/master`より31 commit先行・遅れ0で、tracked worktreeはcleanである。送信端末で記録された
「review carrier不在」はその端末だけの観測であり、受信端末では次の3 artifactがexact pathに存在する。

- source `.local.ymmp`: SHA-256 `beee7eab...eaa54`
- generated project: SHA-256 `f0361f...19853`
- `internal_review.mp4`: 93,375,804 bytes、SHA-256 `f2444f...421f7`

3 hashはいずれもmanifest / tracked validated receiptと一致した。Python、Electron GUI、回帰支援、
.NET render driverの開発はこのworktreeで開始できる。`uv sync --extra dev --locked`、`npm ls --depth=0`、
focused 46 tests、state sync、対象module compile、.NET 10.0.204 Release build、silent `--dry-run`、
既存MP4のfresh full decodeがpassした。YMM4 4.54.0.1も正規discoveryで検出したため、現在の直近product
moveはcarrier復元ではなく、exact MP4を人間が通し視聴して内部review decisionを閉じることである。

## リモート同期と作業面

| 確認対象 | 実測 | 現在状態 | 監修上の意味 |
| --- | --- | --- | --- |
| remote fetch | `git fetch --prune origin` | 再監査時の新着なし | public remote refsをcurrentに更新 |
| current branch | FF-only pull | `eb88397`でalready up to date | Regression Integrityを含むcurrent handoff線を維持 |
| upstream parity | `HEAD...origin/codex/nlmytgen-regression-integrity-v1` | `0/0` | 受信時点でlocal/remoteのcommit差なし |
| default branchとの関係 | ancestry / rev-list | 文書更新前に31 ahead / 0 behind | master内容を欠かさずfeature成果を保持するが、未merge |
| worktree | status / diff / cached diff | tracked clean、upstream `0/0` | user成果物を退避・削除・一括stageしていない |
| publication state | runtime / PR readback | draft PR #2はreview-only | merge、release、公開承認を意味しない |

pre-existing untracked `.playwright-mcp/`、`artifacts/`、`phase-e-01-contact-acquired*.png`と、
ignoredのsource/output/media/browser evidenceは削除、移動、stageしていない。以後の受信端末での開発開始点は
`C:\Users\thank\Storage\Media Contents Projects\NLMYTGen`である。

## この端末で整えた開発基盤

| 基盤 | 実測・実施内容 | 判定 | 残る条件 |
| --- | --- | --- | --- |
| Python | Python 3.13.3、uv 0.10.7、pytest 8.4.2、`uv sync --extra dev --locked` | 開発可能 | entry point warningのため現行どおりmodule実行を使う |
| Python lock | ignored `uv.lock`を利用 | 同worktreeでは再現可能 | Gitだけの新規checkoutにはlockがなく、portable locked syncは未成立 |
| Electron GUI | Node 24.13.0、npm 11.6.2、Electron 35.7.5、`npm ls --depth=0` pass | 開発可能 | lockfileはignoredでlocal生成。clean checkoutの完全再現性はない |
| GUI security | `npm audit`でdirect Electronにhigh 1件 | 要計画修復 | 自動fixはElectron 43.2.0へのsemver-major。無監査の`--force`更新はしない |
| Media tools | ffmpeg / ffprobe 8.0.1 | **fresh full decode pass** | decodeは音声・tempo・creative acceptanceではない |
| Render driver | .NET SDK 10.0.204、Release build | **warning 0 / error 0** | `dotnet --info`のworkload installer例外は残る |
| YMM4 executable | `D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe`、4.54.0.1 | discovery可能 | 今回は再renderもGUI起動もしていない |
| Source YMM4 | manifest exact path/hash | **存在・hash一致** | private inputのためpublic Gitへ載せない |
| Generated project | receipt exact path/hash | **存在・hash一致** | current MP4とのbindingを維持 |
| Review MP4 | receipt exact path/hash、93,375,804 bytes | **存在・hash一致** | human reviewは未完了 |

GUIの`package-lock.json`とPythonの`uv.lock`はいずれもrepo policyでignoreされている。このworktreeでは依存を
解決済みなので即時開発を妨げないが、「Gitだけで別端末へ渡し、同じ依存集合を再現する」契約には不足する。
Electronのmajor upgradeはGUI runtime/API差分を伴いうるため、開発環境整備の名目で無断適用していない。

## 今回の検証結果

| 検証 | 結果 | 保証すること | 保証しないこと |
| --- | --- | --- | --- |
| episode video / media validation / silent runtime / project-state tests | **46 passed** | current manifest、synthetic pipeline、media判定、silent境界、state mirror | human quality |
| `scripts/check_project_state_sync.py` | **PASS** | runtime / cockpitのstate整合 | 過去reportの端末固有artifact可用性 |
| current CLI / pipeline / validation / state / integrity runner compile | **PASS** | 対象Python moduleの構文・import前段 | 外部tool操作 |
| render-driver Release build | **PASS: warning 0 / error 0** | .NET 10でcurrent UIA driverをcompile可能 | 実YMM4 UIとversion compatibility |
| silent `--dry-run` | **PASS** | source hash、18 protected inputs、9 cue、2/4/3 scenes、3/6 speakers、exact text order | render結果やhuman quality |
| source / generated / MP4 hash | **PASS** | manifest / receiptとcurrent local artifactのbyte identity | 別端末へのGit可搬性 |
| existing MP4 full decode | **PASS: exit 0** | current ffmpegで全stream decode可能 | 発音、tempo、字幕comfort、構図acceptance |
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
| One-command internal-review path | 過去same-machine evidenceで成立、receiptはtracked | source、YMM4 discovery、dry-run、driver buildまで再確認済み | approved repair以外では再render不要 |
| Internal-review carrier | receipt/hash/codec/frame inspectionの履歴あり | exact MP4が存在しfresh decode済み | human review surfaceとして利用可能 |
| Human creative/audio review | Product-Gateとして未完了 | **即時実行可能** | 通し視聴しcue別decision |
| Broad regression integrity | independent checkout green | focused開発 | 3実行形態のfixture/locator収束 |
| Dependency portability | local worktreeは準備済み | Python/GUI実装 | lock正本化方針とElectron upgrade検証 |
| Production asset / rights | proxyのみ、未承認 | ledger/設計作業 | asset identity、license、attribution、human visual判断 |
| Master / publication | 未承認 | release contractの設計 | creative、rights、merge、publicationの独立承認 |

North Star上は「source-backed contentからYMM4実MP4までの縦経路を1本で実証済み」で、この受信端末には
exact review carrierもある。次の価値は、新機能を増やすことより、まず人間判断まで1本を閉じること、その成功を
安全な回帰gate、依存可搬性、rights-cleared asset、別topic、GUI標準loopへ順序立てて一般化することにある。

## 先まで見通した目標設定案

以下は承認済みroadmapではない。各段階はexit signalが得られたときだけ次へ進み、互いのgateを代替しない。

| 段階 | 解くbottleneck | 完了条件 | 前提・現在状態 | 完了すると開く工程 |
| --- | --- | --- | --- | --- |
| **1. Human reviewを閉じる（直近推奨）** | machine pass後の発音・rhythm・cue切替・字幕comfort・構図が未判定 | exact MP4を通し視聴し、`accept / repair / reject`をcue IDと観測付きで返す | carrier/hash/full decodeは確認済み | stable internal cutまたはbounded repair scope |
| **2. Cue限定repairとacceptance freeze** | NG原因がcontent / timing / visual / toolのどこか曖昧 | 指摘cueだけを分類・修正し、content lockを守って再render、receipt/hash/frame reviewを更新。acceptなら再renderせずdecision固定 | goal 1のhuman signal | production asset/rights判断へ渡せるcut |
| **3. Regression Integrityを3実行形態で閉じる** | clean-roomだけgreenでsame-machine/worktreeがred | ignored media/profileをcopy対象外へし、private evidenceをauthorityから分離、locatorをrepo-relative化。disk spikeなし・Git差分不変で分類一致 | product artifactを変えない限定slice | 次実装のfalse red低減、CI gate設計 |
| **4. 依存再現性とGUI securityを閉じる** | ignored lockとElectron 35の既知脆弱性でclean machine再現と安全更新が未確定 | uv/npm lockの正本化方針を決定し、Electron supported majorへのupgradeをbranch内でAPI/UI smoke、package audit、rollback可能性付きで検証 | major updateの監修承認が必要 | 別端末のdeterministic setup、GUI保守基盤 |
| **5. Render/review portabilityを製品化** | private artifact/toolchain有無でhandoff判定が端末ごとに揺れる | tool version、YMM4/.NET discovery、artifact hash ingest、review-only transfer、fail-closed reasonを1 operator surfaceへ統合 | 今回の端末差とgoal 4の知見 | 別端末でreview/re-render可否を即判定 |
| **6. Technical milestoneをdefault branchへ統合** | feature branchだけがone-command能力を持つ | human decision、合意したregression gate、PR差分、privacy/path/state auditを満たし、監修承認後にnormal-history merge | 再監査anchorではmasterより31 commit先行、未merge | default branchから次sliceを開始 |
| **7. Proxyをrights-cleared production visualへ置換** | proxyは公開品質・rightsを満たさない | cue/sceneごとに`accepted / replace / cut / defer`を決め、source、permission、attribution、safe areaをledger化 | human aestheticとrights owner判断 | production master候補の制作 |
| **8. Production master candidateを閉じる** | internal-reviewと公開候補の品質差 | final audio、字幕、構図、motion、bitrate、decode、frame sample、source不変、rights ledgerとhuman acceptanceを満たす | goals 2・7 | packaging / release candidate判断 |
| **9. GUIで標準制作loopを完結** | current pathとreview decisionがCLI/docs中心 | ingest、dry-run、blocked reason、render progress、receipt、cue decisionがGUI primary surfaceで完結 | GUI security/portabilityを先に安定 | 人間をcreative判断へ寄せた日常運用 |
| **10. 3-topic vertical sliceでfactory性を証明** | 新紙幣1本だけではcase-specific成功を排除できない | 3 topicでsource→IR→visual decision→YMM4/internal reviewの同一contractを通し、topic固有差分をadapterへ隔離 | goals 5・9 | versioned factory contract |
| **11. 連続3本のoperator実績で量産性を測る** | smoke成功と実運用の時間・手戻りは別 | silent drift/private leak/fatal rerun各0、YMM4 open原則2回以内、例外修正量と所要時間を3本分receipt化 | goal 10 | 運用SLO、training、保守優先度 |
| **12. Publication governanceとfeedback loopを接続** | 技術完成・公開判断・学習が分断 | title/thumbnail promise、source attribution、rights、metadata、明示publication authorizationを束ね、取得権限内のfeedbackをversioned template/diagnosticへ戻す | master acceptance、公開/analytics権限が必要 | 継続改善する制作system |

goal 1で`accept`ならgoal 2の再renderを省き、Integrity / portability / rightsの独立sliceへ進める。
`repair`ならcue ID、観測、変更classを固定し、approved scriptの意味変更とvisual/timing修正を分離する。
`reject`なら局所micro-tuningを続けず、product direction checkへ戻る。受信端末にはexact carrierがあるため、
端末間転送や再renderをgoal 1の前提にしない。

## 監修AIが次に選べる入口

| 入口 | 先に減る摩擦 | 必要条件 | 選ぶと次に可能になること |
| --- | --- | --- | --- |
| **Advance — local MP4をhuman review（推奨）** | North Star最大の未判定 | 音声再生可能な環境でexact local MP4を通し視聴 | 発音、rhythm、cue切替、字幕comfort、proxy構図をdecision化 |
| **Audit — Regression Integrity修復** | linked/evidence-rich checkoutのfalse redとdisk spike | product artifactを変えないscope固定 | canonical gateを3実行形態で同じ分類へ収束 |
| **Excise — lock/Electron負債の限定slice** | clean checkoutの依存再現性とknown high advisory | major upgrade可否を監修判断 | deterministic setupとGUI security baseline |
| **Verify — draft PR #2とcurrent handoffの差分監査** | support branchの受理が未完了 | product gateとmerge判断を分離 | accept / revision / holdを明示しdefault integration条件を固定 |

推奨defaultはAdvanceである。carrier、hash、full decode、driver build、dry-runは成立しており、コード変更や
再renderなしでNorth Star最大の未判定へ直接届く。Auditはhuman review待ちと並行できるが、現canonical runnerを
修正前のevidence-rich checkoutで再実行しない。Exciseは依存契約とmajor runtimeに触れるため、別sliceとして
監修承認してから進める。

## 維持すべき停止条件

- source `.ymmp`、generated project、MP4、frames、browser profileをpublic Gitへ追加しない。
- source不在を空ファイル、異なるYMM4 project、旧hashの無断更新で埋めない。
- .NET 10 build passを実YMM4 render passやhuman acceptanceへ読み替えない。
- Electronのhigh advisoryを理由に`npm audit fix --force`でmajor upgradeを無監査適用しない。
- focused 46 passをsame-machine/worktree Regression Integrity greenへ読み替えない。
- human review前にproxyをfinal aesthetic、rights-cleared asset、production masterへ昇格しない。
- 監修承認なしにPR merge、master integration、external upload、publication、OAuth接続へ進まない。
- この長期goal案を承認済みfeature IDとして一括登録せず、選ばれた次sliceだけを狭い契約にする。
