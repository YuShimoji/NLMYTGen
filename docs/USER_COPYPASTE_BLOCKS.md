# User Copypaste Blocks

This file stores reusable user-facing copy/paste blocks that were repeatedly
being reconstructed across ChatGPT / Codex sessions.

It is not a restart manual, not an active workflow source, and not an
instruction to execute the blocks below. Use the blocks only when the user
explicitly needs a reusable prompt, command, stop message, or report template.

```text
NLMYTGen ユーザー用コピペ資産集
目的: ChatGPT / Codex 間で毎回組み立てていた長文回答・Prompt・PowerShell・停止テンプレート・報告テンプレートを、必要な時に該当ブロックだけコピーして使える形にまとめる。
注意: これは「次のAgentへの再開マニュアル」ではなく、ユーザーが保存して使うPromptライブラリ。実装、commit、push、NotebookLM投入、YMM4作業、G-27作業はこの文書だけでは行わない。

===== SECTION 1: repo同期・現在地確認 PowerShell =====
用途: NLMYTGen の実在repoを確認し、tracked dirty が無い場合だけ master を origin/master に揃え、runtime-state / RSS summary / local-only artifact の有無を見るための確認コマンド。

$repoCandidates = @(
  'C:\Users\PLANNER007\NLMYTGen',
  'C:\Users\thank\Storage\Media Contents Projects\NLMYTGen'
)

$repo = $repoCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $repo) {
  Write-Host 'NLMYTGen repo が見つかりません。候補pathを確認してください。'
  exit 1
}

Set-Location -LiteralPath $repo
Write-Host "repo: $repo"

Write-Host '--- tracked dirty check before sync ---'
$trackedDirty = git status --porcelain=v1 -uno
if ($trackedDirty) {
  Write-Host 'tracked working tree に差分があります。ここで停止してください。'
  git status --short
  exit 1
}

Write-Host '--- sync master ---'
git status --short --branch
git fetch --all --prune
git checkout master

$trackedDirtyAfterCheckout = git status --porcelain=v1 -uno
if ($trackedDirtyAfterCheckout) {
  Write-Host 'checkout 後に tracked 差分があります。pullせず停止してください。'
  git status --short
  exit 1
}

git pull --ff-only origin master

Write-Host '--- branch / HEAD ---'
git status --short --branch
git log -1 --oneline
git rev-list --left-right --count HEAD...origin/master

Write-Host '--- runtime-state top ---'
Get-Content -LiteralPath 'docs/runtime-state.md' -Encoding UTF8 -TotalCount 60

Write-Host '--- RSS sanitized summary if present ---'
if (Test-Path -LiteralPath 'docs/verification/RSS-PICKUP-FIRST-BRIEF-SUMMARY-2026-06-01.md') {
  Get-Content -LiteralPath 'docs/verification/RSS-PICKUP-FIRST-BRIEF-SUMMARY-2026-06-01.md' -Encoding UTF8
} else {
  Write-Host 'missing docs/verification/RSS-PICKUP-FIRST-BRIEF-SUMMARY-2026-06-01.md'
}

Write-Host '--- local-only artifact presence only; contents are not printed ---'
@(
  '_tmp/rss_topic_cluster_briefs_current.md',
  '_tmp/rss_topic_cluster_briefs_current.json',
  '_tmp/rss_topic_candidates_current.md',
  '_tmp/rss_topic_candidates_current.json',
  '_local/rss/feeds.opml.xml'
) | ForEach-Object {
  if (Test-Path -LiteralPath $_) { "present`t$_" } else { "missing`t$_" }
}

Write-Host '確認のみ完了。実装、commit、push、NotebookLM投入、YMM4作業、G-27作業、RSS source pack再生成には進まない。'

===== SECTION 2: tracked dirty がある場合の停止報告テンプレート =====
用途: repo同期前またはcheckout後に tracked dirty が見つかった時、作業を進めずに返す短い報告。

tracked working tree に差分があるため、ここで停止しました。

現在の状態:
- repo: <repo path>
- branch / HEAD: <git status と git log -1 の結果>
- tracked dirty: あり
- untracked / ignored local artifact: <分かる範囲で記載>
- 実行したこと: repo存在確認と git status まで
- 実行していないこと: fetch後のpull、実装、commit、push、NotebookLM投入、YMM4作業、G-27作業、RSS source pack再生成

次に必要なこと:
- この tracked 差分がユーザー作業か、前回Agent作業かを確認する。
- 差分を維持したまま進めるか、別作業として保存するかを決める。
- 内容不明のまま reset / checkout / 上書きはしない。

===== SECTION 3: _tmp がある場合のRSS source pack継続Prompt =====
用途: _tmp/rss_topic_cluster_briefs_current.md / .json が手元にある時だけ、生成済みclusterを安全に読み、ユーザーが1〜3clusterを選べる候補整理を頼むPrompt。NLMYTGenではRSS線は旧水路なので、必要に応じてnewsroom-yt-pipelineへ寄せる判断も含める。

NLMYTGen の RSS source pack 継続準備をしてください。これは実装作業ではなく、local-only artifact からユーザーが選べる候補を整理するための確認です。

前提:
- _tmp/rss_topic_cluster_briefs_current.md と _tmp/rss_topic_cluster_briefs_current.json が存在する場合だけ使う。
- _tmp の中身は記事タイトルやsource-selection詳細を含みうるため、repoへcommitしない。
- 記事タイトル一覧、記事URL、feed URL、raw OPML、token、article bodyを出力しない。
- 候補は記事タイトルではなく、生成済み動画テーマ名で扱う。
- failed feed cleanupをblockerにしない。
- NotebookLM実投入はしない。
- G-27、YMM4、Baseball、Thumbnail、GUI作業へ進まない。
- 最終的にユーザーが1〜3clusterを選べるようにする。

境界注記:
RSS / OPML / topic clustering / NotebookLM source-pack selection は、NLMYTGenでは旧水路です。今後のactive workとして続ける場合は newsroom-yt-pipeline 側へ寄せる可能性があります。NLMYTGenは downstream adapter として、packet / transcript / ScriptIR / VisualIR / export bundle を受けて YMM4 CSV / adapter / review / proof ingest に落とすrepoとして扱います。

やってほしい出力:
- branch / HEAD / working tree / local-only artifact有無の確認
- 記事タイトルやURLを出さない generated theme title ベースの候補一覧
- 各候補の論点構成の違い
- ユーザーが選べる1〜3clusterの短い選択肢
- 次にsource pack化する場合の注意点
- 次作業は実行しないという明記

共通禁止:
failed feed cleanup を blocker にしない。Inoreader 完全同期を目標にしない。failed feed ゼロを目標にしない。Inoreader API を使わない。NotebookLM API 連携を始めない。実際に NotebookLM へ投入しない。台本生成を勝手に始めない。YMM4 patch、動画生成、YouTube投稿、DB sync、background polling に進まない。G-27、Baseball、Thumbnail、GUI gap audit を混ぜない。PR を作成しない。_local/rss/feeds.opml.xml、_tmp/rss_topic_*、記事URL、記事タイトル一覧、feed URL、raw OPML、token を commit しない。.claude/worktrees/ や samples/2026-05-16.ymmp を巻き込まない。

===== SECTION 4: _tmp がないが OPML がある場合のRecover Prompt =====
用途: _tmp/rss_topic_* が無いが _local/rss/feeds.opml.xml がある時だけ、local-only recoveryとして候補再生成を頼むPrompt。今すぐOPMLを要求するためではなく、存在している場合の復旧用。

NLMYTGen の RSS local-only artifact を recovery してください。これは _local/rss/feeds.opml.xml が存在する場合だけ行う復旧作業です。OPMLが無い場合は安全停止してください。

前提:
- _tmp/rss_topic_candidates_current.* または _tmp/rss_topic_cluster_briefs_current.* が無い。
- _local/rss/feeds.opml.xml が存在する場合だけ進める。
- OPMLや_tmpはcommitしない。
- RSS / OPML / topic clustering / NotebookLM source-pack selection は NLMYTGenでは旧水路であり、今後は newsroom-yt-pipeline 側へ寄せる可能性がある。
- NLMYTGenは downstream adapter として、packet / transcript / ScriptIR / VisualIR / export bundle を受けて YMM4 CSV / adapter / review / proof ingest に落とすrepoである。

やること:
- fetch-topics は可能なら --limit 7000 を使う。
- CLI が --limit を受け付けない場合は既存 intake boundary を壊さず、現行オプションで最大限広く再生成する。
- _tmp/rss_topic_candidates_current.md / .json を作る。
- そこから _tmp/rss_topic_cluster_briefs_current.md / .json を作る。
- URLや記事タイトルを含む成果物は _tmp のみに置く。
- repoにはURLなしsanitized summaryだけを残す。
- NotebookLM実投入はしない。

共通禁止:
failed feed cleanup を blocker にしない。Inoreader 完全同期を目標にしない。failed feed ゼロを目標にしない。Inoreader API を使わない。NotebookLM API 連携を始めない。実際に NotebookLM へ投入しない。台本生成を勝手に始めない。YMM4 patch、動画生成、YouTube投稿、DB sync、background polling に進まない。G-27、Baseball、Thumbnail、GUI gap audit を混ぜない。PR を作成しない。_local/rss/feeds.opml.xml、_tmp/rss_topic_*、記事URL、記事タイトル一覧、feed URL、raw OPML、token を commit しない。.claude/worktrees/ や samples/2026-05-16.ymmp を巻き込まない。

===== SECTION 5: _tmp も OPML もない場合の安全停止テンプレート =====
用途: RSS source pack材料が一切無い時に、仮データで進めず止めるための文面。

安全停止します。RSS source pack 作成に必要な入力artifactがありません。

見つからなかったもの:
- _tmp/rss_topic_cluster_briefs_current.*
- _tmp/rss_topic_candidates_current.*
- _local/rss/feeds.opml.xml

この状態では source pack は作成しません。仮データで捏造しません。NotebookLM投入、台本生成、YMM4、G-27には進みません。repoには何もcommitしません。

次に必要なのはどちらかです。
- _local/rss/feeds.opml.xml を配置する。
- 前端末の _tmp/rss_topic_*_current.md / .json を戻す。

ただし、RSS / OPML / topic clustering / NotebookLM source-pack selection はNLMYTGenでは旧水路です。今後のactive workとして続けるなら newsroom-yt-pipeline 側へ寄せる判断を優先します。NLMYTGenで進める場合は、newsroom由来の packet / transcript / ScriptIR / VisualIR / export bundle を受け取る下流作業として再開します。

===== SECTION 6: ゲーム業界source pack作成Prompt =====
用途: generated theme title「ゲーム業界はなぜ遊びづらくなったのか」を、NotebookLM投入候補source packへ絞るためのPrompt。投入自体はしない。

テーマ:
ゲーム業界はなぜ遊びづらくなったのか

目的:
NotebookLM投入候補source packをlocal-onlyで作る。NotebookLM投入は実行しない。

working angle:
ゲームそのものの品質低下だけではなく、開発費高騰、ライブサービス化、プラットフォーム依存、収益化圧力、開発者労働環境、メディア言説の変化が、プレイヤーにとっての「遊びづらさ」を構造的に作っている、という観点でまとめる。

viewer hook:
最近のゲームはなぜ疲れるのか。
なぜ買い切りなのに未完成に見えるのか。
なぜ大型タイトルほど安全運転になるのか。

やること:
- _tmp/rss_topic_cluster_briefs_current.md / .json が存在する場合だけ使う。
- 代表ソースは8〜15件へ絞る。
- source packは _tmp/rss_notebooklm_source_pack_game_industry_current.md / .json に置く。
- 記事URLや記事タイトルを含む詳細は _tmp のみに置く。
- repoに残すなら docs/verification/RSS-GAME-INDUSTRY-SOURCE-PACK-SUMMARY-YYYY-MM-DD.md のようなURLなしsummaryだけにする。
- generated theme title は記事タイトルではなく、生成された動画テーマ名にする。
- source role として core evidence / contrast / background / case example / trend signal を付ける。
- 開発側、ビジネス側、プレイヤー側、市場構造側が混ざるようにする。
- 最終報告では、記事タイトルやURLなしで、どの論点をNotebookLMに読ませる構成になったか説明する。

境界注記:
RSS / OPML / topic clustering / NotebookLM source-pack selection は、NLMYTGenでは旧水路です。今後のactive workとして続ける場合は newsroom-yt-pipeline 側へ寄せる可能性があります。NLMYTGenは downstream adapter として、packet / transcript / ScriptIR / VisualIR / export bundle を受けて YMM4 CSV / adapter / review / proof ingest に落とすrepoです。

共通禁止:
failed feed cleanup を blocker にしない。Inoreader 完全同期を目標にしない。failed feed ゼロを目標にしない。Inoreader API を使わない。NotebookLM API 連携を始めない。実際に NotebookLM へ投入しない。台本生成を勝手に始めない。YMM4 patch、動画生成、YouTube投稿、DB sync、background polling に進まない。G-27、Baseball、Thumbnail、GUI gap audit を混ぜない。PR を作成しない。_local/rss/feeds.opml.xml、_tmp/rss_topic_*、記事URL、記事タイトル一覧、feed URL、raw OPML、token を commit しない。.claude/worktrees/ や samples/2026-05-16.ymmp を巻き込まない。

===== SECTION 7: NotebookLM投入前チェックリスト =====
用途: ユーザーがNotebookLMへ手動投入する直前に見るチェック項目。

NotebookLM投入前チェック:
- source pack は8〜15件に絞れている。
- 同一媒体に偏りすぎていない。
- 開発側、ビジネス側、プレイヤー側、市場構造側が混ざっている。
- core evidence / contrast / background / case example / trend signal の役割が付いている。
- 記事URLや記事タイトルを含む詳細はlocal-onlyである。
- repoにはURLや記事タイトル一覧をcommitしていない。
- raw OPML、feed URL、token、article bodyをrepoに入れていない。
- NotebookLMへ入れるか、別clusterへ切り替えるかをユーザーが判断する。
- NotebookLM API連携ではなく、ユーザーの手動投入として扱う。
- 投入後すぐにYMM4 patch、動画生成、YouTube投稿へ進まない。
- NLMYTGenへ戻す場合は、transcript / script / packet / ScriptIR / VisualIR / export bundle として戻す。

ユーザー短文:
NotebookLMへ投入します。テーマは「ゲーム業界はなぜ遊びづらくなったのか」です。source pack は8〜15件で、媒体と観点の偏りを確認済みです。投入後は transcript / script / packet として戻します。

===== SECTION 8: NotebookLM出力をNLMYTGenへ戻すPrompt =====
用途: NotebookLMで得た台本・要約・transcriptを、NLMYTGenの下流変換へ渡すPrompt。RSS選定には戻らない。

NotebookLM出力をNLMYTGenへ戻します。NLMYTGenは downstream adapter として扱ってください。

入力:
- NotebookLM由来の transcript / script / packet
- 必要に応じて、URLなしのsource pack要約
- ユーザーが選んだgenerated theme title

やること:
- NotebookLM由来の transcript / script / packet を読む。
- RSS source selectionには戻らない。
- CSV生成、話者map、ScriptIR/VisualIR、YMM4 adapter、review、proof ingest の範囲で進める。
- raw article URLやsource packの詳細をrepoに残さない。
- YMM4 renderやcreative acceptanceへ勝手に進まない。
- G-27と混ぜない。
- まず不足artifact、変換方針、次の安全な作業単位を出す。

境界:
NLMYTGenは、packet / transcript / ScriptIR / VisualIR / export bundle を受けて YMM4 CSV / adapter / review / proof ingest に落とすrepoです。RSS / OPML / topic clustering / NotebookLM source-pack selection は今後 newsroom-yt-pipeline 側へ寄せる可能性があります。

共通禁止:
failed feed cleanup を blocker にしない。Inoreader 完全同期を目標にしない。failed feed ゼロを目標にしない。Inoreader API を使わない。NotebookLM API 連携を始めない。実際に NotebookLM へ投入しない。台本生成を勝手に始めない。YMM4 patch、動画生成、YouTube投稿、DB sync、background polling に進まない。G-27、Baseball、Thumbnail、GUI gap audit を混ぜない。PR を作成しない。_local/rss/feeds.opml.xml、_tmp/rss_topic_*、記事URL、記事タイトル一覧、feed URL、raw OPML、token を commit しない。.claude/worktrees/ や samples/2026-05-16.ymmp を巻き込まない。

===== SECTION 9: NLMYTGen責務境界をnewsroom-yt-pipelineへ戻すPrompt =====
用途: NLMYTGen側のruntime-stateや境界docで、RSS線をactive next actionから外すためのPrompt。既存RSS codeは削除しない。

NLMYTGenの責務境界を整理してください。RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection を active next action から外し、newsroom-yt-pipeline 側へ寄せる方向で、必要最小限のdocs更新だけを行います。

要件:
- RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection は newsroom-yt-pipeline 側へ寄せる上流編集責務。
- NLMYTGen は newsroom-produced packet / transcript / ScriptIR / VisualIR / export bundle を受ける downstream adapter。
- NLMYTGen の active next action から RSS source-pack再実行を外す。
- 既存RSS codeは削除しない。active lane から retired / migrated / reference-only に落とすだけ。
- AGENTS.md は膨らませない。
- runtime-state / project-context / 境界docを最小限更新する。
- commitする場合はdocs-only。
- OPMLや_tmpを復元しない。
- RSS source packを再生成しない。
- 差分限定の漏洩確認を行う。

共通禁止:
failed feed cleanup を blocker にしない。Inoreader 完全同期を目標にしない。failed feed ゼロを目標にしない。Inoreader API を使わない。NotebookLM API 連携を始めない。実際に NotebookLM へ投入しない。台本生成を勝手に始めない。YMM4 patch、動画生成、YouTube投稿、DB sync、background polling に進まない。G-27、Baseball、Thumbnail、GUI gap audit を混ぜない。PR を作成しない。_local/rss/feeds.opml.xml、_tmp/rss_topic_*、記事URL、記事タイトル一覧、feed URL、raw OPML、token を commit しない。.claude/worktrees/ や samples/2026-05-16.ymmp を巻き込まない。

===== SECTION 10: G-27 carrier判断Prompt =====
用途: RSSとは別に、G-27本流のcarrier判断へ戻る時のPrompt。

G-27 carrier判断へ戻ります。RSS / OPML / NotebookLM source-pack selection とは混ぜないでください。

前提:
- G-27 は human-authored G27_PublicVsBrokerDB carrier 待ち。
- diagnostic proof / GUI proof は production carrier readiness ではない。
- samples/2026-05-16.ymmp は3 itemだけの不完全 .ymmp であり carrier ではない。
- 進めるには carrier .ymmp、preview screenshot、timeline screenshot、G27PBD_PublicPanel / G27PBD_PublicCard1 / G27PBD_BrokerPanel / G27PBD_Lock の property screenshot、light/dark stage、caption safe area メモが必要。
- diagnostic carrier を production proxy に昇格する場合は、明示的な判断と readback / 境界記録が必要。
- render / creative acceptance / production timing には進まない。

やること:
- docs/runtime-state.md と docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md を確認する。
- carrier .ymmp と必要スクリーンショット類が揃っているか見る。
- 不足している場合は不足分だけを返して停止する。
- 揃っている場合も、まずreadback / 境界記録 / anchored slot contract準備までに留める。
- RSS、Baseball、Thumbnail、GUI gap auditを混ぜない。

共通禁止:
failed feed cleanup を blocker にしない。Inoreader 完全同期を目標にしない。failed feed ゼロを目標にしない。Inoreader API を使わない。NotebookLM API 連携を始めない。実際に NotebookLM へ投入しない。台本生成を勝手に始めない。YMM4 patch、動画生成、YouTube投稿、DB sync、background polling に進まない。G-27以外のBaseball、Thumbnail、GUI gap auditを混ぜない。PR を作成しない。_local/rss/feeds.opml.xml、_tmp/rss_topic_*、記事URL、記事タイトル一覧、feed URL、raw OPML、token を commit しない。.claude/worktrees/ や samples/2026-05-16.ymmp を巻き込まない。

===== SECTION 11: 漏洩確認コマンド =====
用途: commit対象や今回差分だけに、URL・token・raw OPMLなどが入っていないか確認するPowerShell。既存docs全体を雑にgrepしない。

Write-Host '--- staged diff: docs/runtime-state.md docs/verification/ ---'
git diff --cached -U0 -- docs/runtime-state.md docs/verification/

Write-Host '--- unstaged diff: docs/runtime-state.md docs/verification/ ---'
git diff -U0 -- docs/runtime-state.md docs/verification/

$patterns = @(
  [string]::Concat('http', '://'),
  [string]::Concat('https', '://'),
  [string]::Concat('Bear', 'er'),
  [string]::Concat('access', '_token'),
  [string]::Concat('refresh', '_token'),
  [string]::Concat('<', 'outline'),
  [string]::Concat('rss', '.xml'),
  [string]::Concat('feed', '.xml'),
  'article body',
  'raw OPML'
)

Write-Host '--- staged leak scan ---'
$cached = git diff --cached -U0 -- docs/runtime-state.md docs/verification/
foreach ($pattern in $patterns) {
  $cached | Select-String -Pattern $pattern -SimpleMatch | ForEach-Object {
    Write-Host "LEAK-CANDIDATE staged pattern=$pattern line=$($_.Line)"
  }
}

Write-Host '--- unstaged leak scan ---'
$unstaged = git diff -U0 -- docs/runtime-state.md docs/verification/
foreach ($pattern in $patterns) {
  $unstaged | Select-String -Pattern $pattern -SimpleMatch | ForEach-Object {
    Write-Host "LEAK-CANDIDATE unstaged pattern=$pattern line=$($_.Line)"
  }
}

Write-Host '実URL、記事URL、feed URL、private URL、token、raw OPML、article body が含まれる場合は commit しない。'
Write-Host '記事タイトル一覧が含まれる場合も commit しない。URLなしsanitized summaryだけを残す。'

===== SECTION 12: Agent完了報告テンプレート =====
用途: Agent作業後に、ファイルを開かなくても意味が伝わるように返す報告テンプレート。薄い固定ラベルではなく、本文として使う。

NLMYTGenは branch=<branch> / HEAD=<short hash> で確認しました。working tree は <clean / tracked dirtyあり / untrackedのみあり> です。local-only artifact は _tmp/rss_topic_cluster_briefs_current.* が <あり / なし>、_tmp/rss_topic_candidates_current.* が <あり / なし>、_local/rss/feeds.opml.xml が <あり / なし> でした。commit は <作成していない / 作成した: hash> です。

今回作ったものは <_tmp/...> と <docs/...> です。_tmp は source-selection 詳細を含みうるためrepoには入れていません。docsに残した場合はURLなしのsanitized summaryだけです。

漏洩確認は既存docs全体ではなく、今回の差分またはcommit対象だけを見ました。repoにURL、記事タイトル一覧、feed URL、raw OPML、token、article bodyを入れていないことを確認しました。候補が出た場合はcommitしていません。

候補は記事タイトルやURLではなく、生成された動画テーマ名で扱っています。次にユーザーが選べる入口は、<ゲーム業界source pack化 / 別cluster確認 / newsroom-yt-pipelineへ境界移管 / G-27 carrier判断> です。

この報告では次作業は実行していません。NotebookLM投入、台本生成、YMM4、G-27、動画生成、YouTube投稿には進んでいません。

===== SECTION 13: ユーザーが短く返すための選択肢テンプレート =====
用途: ユーザーが長文を書かず、短い返答だけで方向を指定するためのテンプレート。

ゲーム業界source packへ進めます。
テーマは「ゲーム業界はなぜ遊びづらくなったのか」です。
NotebookLM投入はまだしません。
記事タイトルやURLは出さず、8〜15件の投入候補構成だけ作ってください。

別clusterへ切り替えます。
候補テーマ名は「<ここにgenerated theme title>」です。
NotebookLM投入はまだしません。
記事タイトルやURLは出さず、source pack化できるかだけ見てください。

RSS線はNLMYTGenから外します。
RSS / OPML / topic clustering / NotebookLM source-pack selection は newsroom-yt-pipeline 側へ寄せる前提で、NLMYTGenの責務境界だけ整理してください。
既存RSS codeは削除しないでください。

NotebookLM出力をNLMYTGenへ戻します。
入力は <transcript / script / packet / ScriptIR / VisualIR / export bundle> です。
RSS source selectionには戻らず、YMM4 CSV / adapter / review / proof ingest の下流変換として扱ってください。

G-27へ戻ります。
RSSとは混ぜず、G27_PublicVsBrokerDB carrier判断だけ扱ってください。
carrier .ymmp と必要スクリーンショット類が揃っているか確認し、不足があれば不足分だけ返してください。
render / creative acceptance / production timing には進まないでください。

安全停止してください。
_tmp、OPML、NotebookLM出力、G-27 carrier のどれも揃っていません。
仮データで進めず、repoを変更せず、次に必要な入力だけ短く返してください。

===== SECTION 14: ChatGPT貼付用 Codex作業報告コードブロック =====
用途: Codex の最終報告を ChatGPT 側へそのまま貼り、監修できるようにするための単一コードブロック形式。毎回の確認・停止・作業完了で、通常文の短い要約の後にこの形を使う。ブロック内に記事URL、feed URL、raw OPML、token、article body、private data は入れない。

BEGIN_COPY_BLOCK_FOR_CHATGPT

# NLMYTGen 作業報告

## authority / lane
- repo:
- branch / HEAD:
- origin同期:
- tracked working tree:
- known untracked:
- active lane:
- owner:
- authority docs read:

## 実施したこと
-
-
-

## 変更ファイル
- なし / あり
- 変更した場合:
  - path:
  - 目的:
  - commit:

## 検証
- command:
  result:
- command:
  result:
- full pytest:
  実行 / 省略
  理由:

## 境界維持
- RSS / OPML / Inoreader / topic clustering:
  実行していない / 実行した場合は理由
- NotebookLM API / 実投入:
  実行していない
- G-27 carrierなしslot-fill/render/creative:
  実行していない
- raw OPML / URL / token / article body:
  commitしていない
- known untracked:
  触っていない

## 欠けているartifact
- newsroom bundle:
- G-27 carrier:
- review_decisions.json:
- その他:

## 判断
- 現在できること:
- まだできないこと:
- blocker:
- 非blocker:

## 次に返すもの / 次の入力
- 人間が返すもの:
- newsroom側から返すもの:
- G-27側で返すもの:
- Agentが次にできること:

## 注意
- 次に進んでよい作業:
- 進んではいけない作業:

END_COPY_BLOCK_FOR_CHATGPT

===== SECTION 15: G-28 parked / input-wait ChatGPT貼付用コードブロック =====
用途: G-28 Reference-Driven Generic Screen Carrier を「参照画像待ち」として安全に駐車し、別作業へ移れる状態を ChatGPT 監修へそのまま貼るための単一コードブロック形式。G-28 を実装完了のように書かない。raw OPML、URL、token、article body、private data、reference image URL は入れない。

BEGIN_COPY_BLOCK_FOR_CHATGPT

# NLMYTGen G-28 区切り報告

## authority / lane
- repo:
- branch / HEAD:
- origin同期:
- tracked working tree:
- known untracked:
- active lane:
- parked lane:
- owner:
- authority docs read:

## 実施したこと
-
-
-

## 変更ファイル
- なし / あり
- 変更した場合:
  - path:
  - 目的:
  - commit:

## G-28 parking
- status: parked / input-wait
- parked reason: 参照画像と per-image memo が未受領
- next input: 人間が用意する参照画像 3-7 枚 + 各画像の参考対象メモ
- return condition: 画像を素材ではなく principle source として読み、reference style brief / SCS mapping / generic carrier archetype を作れる状態
- not doing now: `.ymmp` ゼロ生成、YMM4 carrier authoring、adapter patch、render、production timing、creative final acceptance

## G-27 の扱い
- active blocker に戻したか:
- retained evidence:
- diagnostic carrier production 昇格:
- review_decisions.json の扱い:

## 人間側作業
- 必要な操作: 参照画像を 3-7 枚選ぶ
- 必要な入力: 各画像に「何を参考にしたいか」の短いメモを付ける
- 画像の扱い: 素材ではなく、構図・余白・密度・色階層・視線誘導・UI感の参照標本として扱う
- OK条件:
- NG時に返す情報:

## 参照画像メモの推奨テンプレート
G-28 参照画像入力

画像1:
- 参考対象:
- 使いたい理由:
- 避けたい要素:

画像2:
- 参考対象:
- 使いたい理由:
- 避けたい要素:

画像3:
- 参考対象:
- 使いたい理由:
- 避けたい要素:

全体方針:
- light / dark の希望:
- 情報密度:
- YouTube解説感:
- DB / dashboard 感:
- lock / gated information 感:
- 最初に試したい題材:
  - 不動産DX
  - newsroom explainer
  - AI monitoring
  - baseball / sports news
  - その他

## 別作業へ移る条件
- 進めてよいこと:
- 混ぜてはいけないこと:
- 次にユーザーから受け取るもの:

## 検証
- command:
  result:
- command:
  result:
- full pytest:
  実行 / 省略
  理由:

## 境界維持
- RSS / OPML / Inoreader / topic clustering:
  実行していない / 実行した場合は理由
- NotebookLM API / 実投入:
  実行していない
- G-27 diagnostic carrier production 昇格:
  実行していない
- G-28 image / URL / raw reference commit:
  実行していない
- YMM4 .ymmp ゼロ生成 / render / production timing / creative final acceptance:
  実行していない
- known untracked:
  触っていない

## そもそも論チェック
- 長期 blocker 化の有無:
- human work transfer の有無:
- docs-only drift の危険:
- case-specific / generic capability の分離:
- evidence / authority の分離:

## 次に返すもの / 次の入力
- 人間が返すもの:
- Agentが次にできること:
- 進んではいけない作業:

END_COPY_BLOCK_FOR_CHATGPT

===== END =====
```
