# 監修AI向け・最新リモート同期と開発再開性の現状報告（2026-07-21 JST）

Scope: NLMYTGen

この文書は、2026-07-21 11:31 JST時点で公開リモートを再取得し、現在の開発先端を
ローカルへ同期した結果と、この端末で実際に再開できる工程を分けて記録する時点証跡です。
製品の現在位置と次のgateの正本は[`runtime-state.md`](../runtime-state.md)です。本書は
ignoredのYMM4 projectやMP4をGitへ昇格させず、human creative acceptance、rights、
production、publication、master integrationを承認しません。

## 監修判断に必要な結論

開始時のbranch
`codex/new-banknote-content-lineage-yymm4-batch-v1`は、fetch後にupstreamから3 commit
遅れていたため、`--ff-only`で`220a9b554f267a5367c9589eb09f35fc9058d4a0`まで取り込みました。
その後、同commitをancestorとして11 commit直線的に進んだ
`origin/codex/nlmytgen-end-to-end-auto-video-v1`をリモート全体の後継開発線として確認し、
local tracking branchへ非破壊で切り替えました。現在HEADは
`7eaaef1b384c4b412001dfb312a977ac96052f71`、upstream差分は`0/0`、
`origin/master`に対して21 commit先行・遅れ0です。

Python/Electronの通常開発は開始できます。Python 3.11.0はproject要件`>=3.11`を満たし、
`uv sync --extra dev`と`npm ci`は完了しました。現在sliceに直結する46 tests、project-state
sync、Python compileもpassしています。

ただし、この端末だけで実YMM4 renderを再現できる状態には達していません。render driverは
`net10.0-windows`を要求しますが、local SDKは9.0.304だけで、buildは`NETSDK1045`で停止します。
さらに、manifestがhash固定するsource YMM4 projectと、remote handoffが人間確認対象にする
`internal_review.mp4`はpublic Gitに含めないsame-machine artifactであり、この端末にはありません。
非書き込み`--dry-run`は意図どおり`source_ymmp_missing`でfail closedしました。

したがって監修上の現在地は、**コード開発環境は再開可能、既存の内部レビュー成果はremote
evidenceで検証済み、この端末での動画レビューまたは再renderは外部依存とlocal artifact待ち**です。
.NET 10 SDK導入はdependency追加なので、明示判断なしに実行していません。

## 何を取り込み、何を変えなかったか

| 対象 | 今回の実施 | 現在状態 | workflowへの効果 |
| --- | --- | --- | --- |
| 旧作業branch | fetch/prune後にFF-only pull | `220a9b5`、remote parity `0/0` | 2026-07-18のsync/readiness handoffを欠落なく回収 |
| 後継開発線 | 祖先関係と11 commitの直線系譜を確認してtracking checkout | `7eaaef1`、remote parity `0/0` | 旧G0前ではなく、one-command internal-review video実装済みの先端から再開可能 |
| default branch関係 | `HEAD...origin/master`をreadback | ahead 21 / behind 0 | master内容を欠かさずfeature成果を保持 |
| Python依存 | `uv sync --extra dev` | 7 packages resolved / 6 audited | Python CLI・testsを追加install待ちなしで実行可能 |
| GUI依存 | `npm ci --no-audit --no-fund` | Electron 35.7.5を含む70 packages導入 | Electron開発を再開可能 |
| 承認済みcontent | 読取とtestsだけ。生成・修正なし | 9 cue、2/4/3 scenes、3/6 speakers、approval/lineage lock維持 | silent content driftを起こしていない |
| local operator/media evidence | 存在確認だけ。生成・移動・削除・追跡化なし | source `.ymmp`とreview MP4はこの端末に不存在 | private/ignored境界を維持 |

`npm ci`ではtransitive dependency `boolean@3.2.0`のdeprecated warningが出ましたが、installは
成功し、直ちに起動を止めるerrorではありません。承認済み台本、source/claim、visual authority、
YMM4 project、render media、rights/publication状態は変更していません。

## この端末で成立している開発基盤

| 基盤 | Readback | 判定 | 残る条件 |
| --- | --- | --- | --- |
| Python / uv | Python 3.11.0、uv 0.10.0 | 利用可能 | project script entry pointはpackage未定義warningのため`uv run python -m src.cli.main`を使う |
| Node / npm / Electron | Node 22.19.0、npm 10.9.3、Electron 35.7.5 | 利用可能 | deprecated transitive dependencyは将来の保守対象 |
| Browser | Chrome 150.0.7871.129、Edge 150.0.4078.83をstandard install pathで確認 | 利用可能 | render時もsilent policyとisolated profileを維持 |
| Media tooling | ffmpeg / ffprobe 8.1.1 | 利用可能 | 実MP4が無いためこの端末では再validation未実施 |
| Render driver | .NET SDK 9.0.304、target `net10.0-windows` | **block** | .NET 10 SDK追加の明示承認が必要 |
| Source YMM4 project | manifest pathに不存在、pilot配下にも`.ymmp`候補なし | **block** | exact pathとSHA-256 `beee7eab...aa54`を満たすprivate artifactが必要 |
| Internal-review MP4 | expected ignored run pathに不存在 | **block for human review** | source端末の検証済みMP4をprivate transferするか、前2条件を満たして再生成 |

YMM4自体の互換性は、source projectが無いため今回のdry-runで到達確認していません。remoteの
sanitized receiptはYMM4 4.54.0.1、1920x1080/60 fps、4415 frames、73.583008秒、
H.264/AAC、full-file decode passを記録しますが、これはこの端末での再実行結果ではありません。

## 検証結果とテスト健全性

現在sliceのportable contractを優先し、次の検証を通しました。

| 検証 | 結果 | 解釈 |
| --- | --- | --- |
| `test_episode_video_pipeline` + media validation + silent runtime + project-state sync | 46 passed | one-command pipelineのsynthetic contract、media判定、無音実行境界、状態正本同期は健全 |
| `scripts/check_project_state_sync.py` | passed | runtime / cockpit / pipeline / registryのProject-State-IDは同期 |
| `py_compile` | passed | current CLIとepisode video moduleはimport可能 |
| .NET render driver build | failed: `NETSDK1045` | code defectの判定前にSDK major versionが不足 |
| pipeline `--dry-run` | failed closed: `source_ymmp_missing` | renderやYMM4 launchへ進まず、missing private inputを正しく拒否 |
| tracked diff / whitespace | clean | test副作用で一度削られたREADME 8行はHEAD内容へ復元済み |

current/new-banknote周辺を広めに選んだ131 testsでは98 passed / 33 failedでした。full
`uv run pytest`は、repo-local ruleが既知のgenerated-artifact/path driftとtracked-fixture side
effectを通常gateから外しているため実行していません。33 failuresは一つの原因ではなく、次の
3 classに分かれます。

1. Gitへ載せないsource bodies、local YMM4 evidence、reference capturesを「この端末にも存在する」
   前提でassertするためのfailure。
2. Route A / reference proofなど過去slice固有の`Project-State-ID`を、後継stateでもcurrentと
   期待するhistorical-state failure。
3. generatorと後続補正文書のdrift、およびsuccessor integration blob期待値のstaleness。
   実際に旧generatorがreference READMEのsilent-policy追記8行を削るside effectを起こしたため、
   変更を残さず復元した。

このため「current pipelineのfocused checksがgreen」と「repository横断の回帰基盤がgreen」は
同義ではありません。通常開発は進められますが、広い回帰をrelease gateとして信用する前に、
端末依存fixtureとhistorical-state assertionsを現行contractから分離するIntegrity sliceが必要です。

## 製品の現在地

| 能力・gate | 状態 | 今回確認できた範囲 | 次に必要なもの |
| --- | --- | --- | --- |
| Remote source / lineage / approved script | 実装済み・lock済み | 最新直線系譜を取得、content変更なし | future content revision時だけsuccessor approval |
| Existing YMM4 evidence revalidation | 実装済み | tracked receiptと後継履歴を取得 | local raw evidenceはprivateのまま保持 |
| Visual design / reference reconstruction | 実装済み、proxy authority | tracked proofとmappingを取得 | final aesthetic / asset / rights判断 |
| One-command internal-review video | 実装済み、remote evidenceで検証済み | current contract tests 46 pass | この端末では.NET 10とsource projectが不足 |
| Human internal review | 未完了 | 対象MP4がこの端末に無い | validated MP4のprivate transferまたは承認済み再生成 |
| Broad regression integrity | 進行中の負債 | 131中98 pass / 33 failを分類 | local-only fixtureとhistorical stateの分離 |
| Production / rights / publication | 未承認 | 今回は実施なし | 独立したcreative、asset、rights、publication approval |

North Starに対しては、source-backed contentから実MP4までの縦経路そのものはremote evidence上で
成立しています。現在の摩擦はfeature不足ではなく、**レビュー媒体のportability、render toolchainの
SDK差、横断testsの端末依存**です。ここで新しいvisual機能を増やすより、既存MP4を人間判断へ渡すか、
再現に必要なprivate inputと.NET 10を明示的に整える方が下流を早く開きます。

## 次に選べる具体的な入口

| 入口 | 解くbottleneck | 必要条件 | 選ぶと次に可能になること |
| --- | --- | --- | --- |
| **Advance — 検証済みMP4をprivate transferしてレビュー（推奨）** | human review対象がこの端末に無い | source端末の`internal_review.mp4`をexpected ignored pathへ置き、SHA-256 `f2444f...21f7`を照合 | 発音・rhythm・cue切替・字幕comfort・proxy構図を`accept / repair / reject`へ進められる。再render不要 |
| Enable — .NET 10とsource projectを用意して再現 | render driver buildとdry-runが止まる | .NET 10 SDK追加の明示承認、manifest exact path/hashのsource `.ymmp`、compatible YMM4 | dry-run → bounded silent render → media validationをこの端末で再実行できる |
| Audit — regression portabilityを修復 | 広いtestsの端末依存とhistorical-state drift | current sliceを変えないIntegrity作業としてscope固定 | checkout直後でも意味のある回帰gateを作れ、次の実装でfalse redとtracked side effectを減らせる |
| Verify — source端末で人間レビューだけ実行 | media移送とtoolchain追加を避けたい | validated MP4が残る元端末へreviewerがアクセス | 最短でhuman decisionを返し、この端末はrepair指示が出るまでcode-only readyを維持できる |

推奨defaultはAdvanceです。remote receiptが既存MP4をすでにhash固定・full decode検証しており、
レビューのためだけに.NET SDKとprivate sourceを再構成するよりblast radiusが小さいためです。
MP4を移送できない場合にだけEnableへ進みます。assistantは依存追加の承認後に.NET 10導入とbuild/
dry-run再検証を担当できます。source `.ymmp`または既存MP4のprivate供給と、最終creative判断は
human ownerが必要です。Auditは外部artifact待ちと並行可能ですが、human reviewを直接代替しません。

## 次にしてはいけないこと

- `.NET 10`不足を隠すためrender driverのtargetを`net9.0-windows`へ勝手に下げない。
- source `.ymmp`やMP4をpublic Gitへ追加しない。
- missing local mediaをremote validated receiptと混同して「この端末で再生確認済み」と報告しない。
- 33 historical/local-fixture failuresをcurrent pipeline defectへ一括分類しない一方、既知負債として
  無視してrepository-wide greenとも主張しない。
- proxy visualのmachine passをfinal aesthetic、asset rights、production、publication approvalへ
  昇格させない。
