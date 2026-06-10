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

===== SECTION 16: G-28 Map / Evidence Carrier 完了後の再開Prompt =====
用途: G-28 Reference-Driven Generic Screen Carrier が Lecture Diagram generic skeleton、2つの theme diagnostic variants、Map / Evidence Carrier diagnostic skeleton まで進んだ後、次の ChatGPT / Codex へ bounded context を渡すためのPrompt。G-28をproduction完了のように書かない。画像、URL、raw reference、source footage、RSS、NotebookLM、G-27復帰を混ぜない。

NLMYTGen の G-28 Reference-Driven Generic Screen Carrier を続けてください。

repo:
C:\Users\thank\Storage\Media Contents Projects\NLMYTGen

開始前:
1. git status --porcelain=v1 -uno
2. git fetch --all --prune
3. git pull --ff-only
4. git rev-list --left-right --count HEAD...origin/master
5. AGENTS.md -> docs/REPO_LOCAL_RULES.md -> docs/runtime-state.md を読む。

現状:
- G-28 Reference-Driven Generic Screen Carrier は diagnostic-only の refinement lane。
- Lecture Diagram Carrier generic skeleton は生成済みで readback-passed。
- Lecture Diagram theme variants は `real_estate_information_gap` と `game_mechanics_explanation` の2つだけ生成済みで、どちらも readback-passed。
- Map / Evidence Carrier は Lecture Diagram の追加 theme variant ではなく、別 archetype の diagnostic skeleton として生成済みで readback-passed。
- Map / Evidence output:
  - samples/_probe/g28/map_evidence_carrier_skeleton.json
  - samples/_probe/g28/map_evidence_carrier_skeleton_readback.json
  - samples/_probe/g28/map_evidence_carrier_skeleton.html
  - samples/_probe/g28/map_evidence_carrier_skeleton_report.md
- Map / Evidence spec:
  - docs/verification/G28-MAP-EVIDENCE-CARRIER-SPEC-2026-06-05.md
- artifact commit:
  - d1a421a docs: add G-28 map evidence carrier skeleton
- 最新remote handoff commit は `git log -1 --oneline` で確認する。

readback境界:
- diagnostic_only=true
- production_candidate=false
- frame=1920x1080 / 16:9
- composition_type=center-focal
- caption reserve clear
- annotation slots=3
- source note bounded
- host role non-focal
- dense_table=false
- indexed_whiteboard=false
- tiny_text=false
- external_image_count=0
- external_url_count=0
- token_like_pattern_count=0
- image_path=false
- image_url=false
- raw_reference=false

やらないこと:
- Lecture Diagram theme variant をこれ以上量産しない。
- G-28をproduction完了扱いしない。
- G-27 production carrier pathへ戻らない。
- 実地図画像、衛星画像、image path、URL、raw referenceをrepoに入れない。
- source footage / gameplay screenshot intakeへ進まない。
- .ymmp generation、render、production timing、creative final acceptance、実素材slot-fillをしない。
- RSS / OPML / Inoreader / NotebookLM source-pack workへ戻らない。

次にやるなら:
- G-28 archetype群の整理、frame contract比較、または human review packet の最小設計に限定する。
- 実装する場合は `docs/runtime-state.md` と `docs/project-context.md` に短く現在位置を残し、commit/push後に `HEAD...origin/master = 0 0` を確認する。

報告条件:
- ChatGPT監修へ貼れる単一コードブロックで返す。
- G-28をproduction完了のように書かない。
- 次に渡すPrompt欄を必ず含める。

===== SECTION 17: G-28 Game Mechanics Diagram Semantics Resume Prompt =====
Use when resuming G-28 after the game-mechanics human review returned `decision: revise` and the diagram semantics note was recorded. This prompt keeps G-28 diagnostic-only and does not reopen Source-Footage, G-27, RSS, NotebookLM, YMM4 generation, render, production timing, or creative final acceptance.

NLMYTGen の G-28 Reference-Driven Generic Screen Carrier を続けてください。

repo:
C:\Users\thank\Storage\Media Contents Projects\NLMYTGen

開始前:
1. git status --porcelain=v1 -uno
2. git fetch --all --prune
3. git pull --ff-only
4. git rev-list --left-right --count HEAD...origin/master
5. AGENTS.md -> docs/REPO_LOCAL_RULES.md -> docs/runtime-state.md を読む。

現状:
- latest remote handoff should be after the G-28 game-mechanics diagram semantics note; confirm current latest with `git log -1 --oneline`.
- `docs/verification/G28-CARRIER-ARCHETYPE-TOOLBOX-2026-06-05.md` で Lecture Diagram / Map Evidence / Source-Footage / Conversation Buffer の4 archetype を整理済み。
- `docs/verification/G28-SHOT-CARRIER-SELECTION-WORKSHEET-2026-06-05.md` で次の1 shot の carrier selection worksheet を作成済み。
- `docs/verification/G28-SHOT-CARRIER-SELECTION-GAME-MECHANICS-2026-06-05.md` で game mechanics shot は Lecture Diagram Carrier primary、Source-Footage Carrier future-only backup と判定済み。
- `docs/verification/G28-GAME-MECHANICS-HUMAN-REVIEW-PACKET-2026-06-05.md` で human design review packet 作成済み。
- human response は `decision=revise`, `carrier=Lecture Diagram Carrier`。
- `docs/verification/G28-GAME-MECHANICS-DIAGRAM-SEMANTICS-NOTE-2026-06-05.md` で diagram semantics note 記録済み。
- 対象 precedent は `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*`。
- chain direction は `入力操作 -> 内部ルール / 判定 -> 画面上の結果` のまま。
- middle node は抽象的な `内部ルール` 固定ではなく、first-review では `判定 / 当たり判定` を主軸にし、`無敵時間` / `硬直` は later substitution 候補として残す。
- callout は `判定 / 当たり判定` primary、`操作感` と `リスクとリターン` は supporting。
- host は non-focal のまま。medium caption 前提なので画面内 text は短く保つ。
- Lecture Diagram generic skeleton、`real_estate_information_gap`、`game_mechanics_explanation` は readback-passed。
- Map / Evidence Carrier skeleton も readback-passed。
- すべて `diagnostic_only=true` / `production_candidate=false`。
- Source-Footage Carrier と Conversation / Buffer Carrier は definition-only。generator / JSON / readback / HTML / report は未着手。
- G-28 を production 完了扱いしない。
- Source-Footage へ進んだ扱いにしない。

次の最小候補:
- diagram semantics note を使い、必要なら narrow semantics plan を作る。
- `判定 / 当たり判定` を主軸にする label / callout hierarchy を整理する。
- `accept` が後で返った場合だけ scoped YMM4-saved carrier review を検討可能。ただし `.ymmp` 生成、render、creative final acceptance ではない。
- Source-Footage が必要と判断された場合だけ、別 slice で design-only checklist を作る。footage / screenshot intake はしない。

禁止:
- 新しい theme variant / carrier skeleton / generator を追加しない。
- Source-Footage Carrier generator を作らない。
- gameplay screenshot intake / source footage intake をしない。
- image path、URL、raw reference を repo に入れない。
- `.ymmp` 生成、render、production timing、creative final acceptance に進まない。
- G-27 active blocker に戻らない。
- RSS / OPML / Inoreader / NotebookLM に戻らない。
- 既存 JSON / HTML / readback / report / generator を変更しない。
- AGENTS.md は変更しない。

検証:
- docs-only なら `git diff --check`、`git diff --cached --check`、staged forbidden scan。
- `src/` / `gui/` / Python package / tests を変更していなければ pytest は省略可。
- commit / push 後 `HEAD...origin/master` を `0 0` にする。

最終報告:
- G-28 を production 完了のように書かない。
- Source-Footage へ進んだように書かない。
- 変更内容、残る不確実性、次の取っ掛かりを自然文と必要な比較表で返す。
- 次に渡すPrompt欄を含める。

===== END =====
```

===== SECTION 19: Common Foundation Single Fake Execution Flow Resume Prompt =====
用途: common foundation single fake execution flow が commit / push / audit 済みになった後、次の ChatGPT / Codex へ bounded context を渡すためのPrompt。古い staged-diff / stage prompt に戻らず、real codex exec、subprocess runner、stdin piping、runtime worker loop、external notification service、ClipPipeGen、G-28 / NLMYTGen mainline work へ進めない。

```text
NLMYTGen common foundation single fake execution flow handoff 後の確認または次slice設計を続けてください。

repo:
C:\Users\thank\Storage\Media Contents Projects\NLMYTGen

開始前:
1. git status --porcelain=v1
2. git status --porcelain=v1 -uno
3. git fetch --prune origin
4. git pull --ff-only origin master
5. git rev-list --left-right --count "HEAD...@{u}"
6. git log --oneline -n 8
7. AGENTS.md -> docs/REPO_LOCAL_RULES.md -> docs/runtime-state.md を読む。

期待される最新remote:
- `e509863 feat: update orchestration scaffold`
- その後に this handoff seal commit がある場合は、それを最新HEADとして扱う。
- `HEAD...@{u}` は `0 0` にする。

完了済みaudit:
- `post_commit_audit_single_fake_execution_flow_001` passed.
- audited commit: `e509863 feat: update orchestration scaffold`.
- changed files in audited commit were only:
  - `docs/AGENT_ORCHESTRATION.md`
  - `scripts/agent_orchestrator.py`
  - `tests/test_agent_orchestration.py`
- stale prompts retired:
  - `stage_single_fake_execution_flow_001`
  - `single_fake_execution_flow_staged_diff_review_001`
  - any fake runner scaffold stage/commit prompt

現在のcommon foundation状態:
- Codex worker policy gate scaffold exists.
- Codex exec command preview plan exists.
- disabled execution preflight exists.
- inert NLMYTGen repo adapter exists.
- runtime artifact ignore policy exists.
- fake runner scaffold exists as tests-only helper in `scripts/agent_orchestrator.py`.
- single fake execution flow helper exists as test/helper-only.
- default CLI/runtime path does not expose the fake flow.
- there is no `--single-fake-flow` CLI flag.
- `.agent/state.json` remains runtime policy source.
- `.agent/repo_adapter.json` remains inert.
- `.agent/reports/.gitkeep` and `.agent/logs/.gitkeep` remain tracked.

Fake runner contract:
- `run_fake_runner(plan, scenario, state_path)` writes synthetic reports only to `ExecutionPlan.report_path`.
- supported scenarios:
  - `pass`
  - `needs_human`
  - `blocked`
  - `invalid_json`
  - `missing_report`
  - `nonzero_exit`
  - `timeout`
- valid synthetic reports go through `agent_gate.evaluate_report`.
- local notify stub is called only after `gate_result.needs_human=true`.
- pass writes no notify artifact.
- invalid JSON, missing report, nonzero exit, and timeout fail closed.
- `codex_execution_started=false`.
- `real_subprocess_started=false`.
- default orchestrator path still does not expose fake runner execution.

Verification baseline:
- `uv run pytest tests/test_agent_orchestration.py`
- `uv run pytest tests/test_guardrails.py`
- `uv run python -m py_compile scripts/agent_gate.py scripts/agent_notify_stub.py scripts/agent_orchestrator.py tests/test_agent_orchestration.py`
- `git diff --check`

禁止:
- real codex exec execution
- subprocess.run runner
- stdin piping to codex exec
- runtime worker loop
- external notification service
- secrets / API key handling
- publish / release
- rights_status changes
- production_candidate automation
- G-28 / NLMYTGen mainline work
- ClipPipeGen support
- `.ymmp` generation or render
- `.claude/worktrees/` or `samples/2026-05-16.ymmp` staging
- `git add -A`

known local residue:
- `.claude/worktrees/`
- `samples/2026-05-16.ymmp`
- These are unrelated and should remain untracked unless the user gives explicit scope.

次の最小候補:
- Do not proceed directly to real execution.
- If explicitly authorized, the next common foundation slice is design-only `real_runner_boundary_design_001`.
- That design must cover explicit opt-in execution policy, subprocess boundary, stdin piping boundary, timeout / cancellation, report path containment, gate authority, notify boundary, runtime artifact hygiene, and no external notification without separate authorization.
- If not explicitly authorized, stop after reporting the sealed state and do not reopen fake runner scaffold staging.

完了報告:
- branch / HEAD / origin同期 / dirty state を明記する。
- real codex exec を実行・有効化したように書かない。
- fake runner を runtime worker loop として扱わない。
- G-28 mainline と common foundation の作業台を混ぜない。
```

===== SECTION 18: G-28 Review Console Read-only Ingest Resume Prompt =====
用途: G-28 `real_estate_information_gap` YMM4 diagnostic probe が Review Console の read-only panel まで実装・push済みになった後、次の ChatGPT / Codex へ bounded context を渡すためのPrompt。production、render、rights、creative final acceptance、slot-fill、G-27 authority reuse、ClipPipeGen、RSS、NotebookLM、common foundation work へ進めない。

```text
NLMYTGen の G-28 `real_estate_information_gap` Review Console read-only ingest 後の確認作業を続けてください。

repo:
C:\Users\thank\Storage\Media Contents Projects\NLMYTGen

開始前:
1. git status --porcelain=v1
2. git status --porcelain=v1 -uno
3. git fetch --prune origin
4. git pull --ff-only origin master
5. git rev-list --left-right --count "HEAD...@{u}"
6. git log --oneline -n 5
7. AGENTS.md -> docs/REPO_LOCAL_RULES.md -> docs/runtime-state.md を読む。

期待される最新remote:
- `708b9e9 feat: add G-28 Review Console read-only panel`
- その後にこの handoff refresh commit がある場合は、それを最新HEADとして扱う。
- `HEAD...@{u}` は `0 0` にする。

現在の状態:
- G-28 `real_estate_information_gap` YMM4 diagnostic probe は作成済み。
- YMM4 GUI recheck は pass。
- Review Console ingest plan は作成済み。
- Review Console read-only ingest implementation は `708b9e9` で実装済み。
- `gui/index.html` に `#g28-review-console-ingest` が追加済み。
- `gui/renderer.js` は既存readback JSONを読み、artifact inventory / status badges / readback summary / human GUI summary / caveats / allowed diagnostic decisions を表示する。
- `gui/main.js` / `gui/preload.js` は repo-relative artifact existence check の `check-review-artifacts` を持つ。
- `gui/review_console_dom_smoke.js` は G-28 panel、badge、artifact paths、readback summary、human GUI summary、caveats、allowed diagnostic decision schema、production approval label 不在を検査する。

対象artifact:
- `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp`
- `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json`
- `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_report.md`
- `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md`
- `docs/verification/G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-PLAN-2026-06-07.md`

Review Consoleで確認する内容:
- `G-28 real_estate_information_gap YMM4 diagnostic probe` panel が読める。
- artifact inventory が5件表示される。
- `diagnostic_only=true`
- `production_candidate=false`
- `human_calibrated_override=true`
- `layout_metric_debt=true`
- `host_placeholder=true`
- `render=false`
- `rights_public_use=false`
- `classification=pass_callout_label_human_calibrated`
- `caption_reserve_clear=true`
- `focal_chain_count=3`
- `callout_count=3`
- `host_role=non_focal...`
- external image / URL / source footage / audio / TTS count が0
- `actual_x=313`
- human GUI summary が表示される。
- caveats に X=313 human override、title readback debt、host placeholder diagnostic-only、glyph optical center not directly measured が明示される。
- allowed diagnostic decisions は次の5件だけ:
  - `accept_as_diagnostic_review_surface`
  - `request_readback_fix`
  - `request_layout_system_redesign`
  - `defer_review_console_ingest`
  - `reject_probe_path`
- production approval系の decision label は表示しない:
  - `production_approve`
  - `creative_final_acceptance`
  - `render_approve`
  - `rights_approve`
  - `public_use_approve`

次の最小作業:
- screenshot / Electron smoke evidence / human GUI confirmation のどれかに限定する。
- まず可能なら `.\gui\node_modules\.bin\electron.cmd .\gui\review_console_dom_smoke.js` を実行する。
- 必要なら Review Console のスクリーンショット取得だけを行う。
- 人間確認へ渡す場合は「read-only diagnostic review surfaceとして読めるか」だけを聞く。

禁止:
- `.ymmp` regeneration
- builder/generator変更
- readback JSON変更
- probe report変更
- new variant generation
- production render / MP4
- production carrier approval
- creative final acceptance
- rights / public-use automation
- source footage / audio / TTS
- external image / URL / raw reference intake
- G-27復帰
- G-27 `review_decisions` authority の利用
- ClipPipeGen access
- RSS / OPML / Inoreader / NotebookLM work
- common foundation / Codex Worker Orchestration implementation
- known local residue のstage / commit

known local residue:
- この checkout では out-of-scope tracked residue が残っている可能性がある:
  - `docs/AGENT_ORCHESTRATION.md`
  - `scripts/agent_orchestrator.py`
  - `tests/test_agent_orchestration.py`
- known untracked:
  - `.claude/worktrees/`
  - `samples/2026-05-16.ymmp`
- これらはG-28 Review Console確認作業では編集・stage・commitしない。
- `git add -A` は使わない。

検証:
- DOM smokeを実行した場合は結果を報告する。
- docs-only / screenshot-only の場合は `git diff --check` と `git status --porcelain=v1` を確認する。
- commit/pushが必要な変更をした場合は対象ファイルだけ明示stageし、`git diff --cached --check`、staged scope check、forbidden scanを行う。
- push後 `HEAD...@{u}` を `0 0` にする。

完了報告:
- branch / HEAD / origin同期 / dirty state を明記する。
- G-28をproduction完了のように書かない。
- Review Console panel確認の結果、残るcaveat、次の人間確認項目を短く書く。
```

===== SECTION 20: G-28 Game Mechanics Inspector-first Accept Remote Handoff =====
Use this prompt when resuming the current G-28 game mechanics lane from another
terminal. Keep the scope to this repo and to diagnostic reviewability / scoped
YMM4-saved carrier review conditions only.

```text
NLMYTGen の G-28 game_mechanics_explanation inspector-first diagnostic review surface accept 後の作業を続けてください。

repo:
C:\Users\PLANNER007\NLMYTGen

開始前:
1. git status --porcelain=v1
2. git status --porcelain=v1 -uno
3. git fetch --all --prune
4. git pull --ff-only origin master
5. git rev-list --left-right --count HEAD...origin/master
6. git log -1 --oneline
7. AGENTS.md -> docs/REPO_LOCAL_RULES.md -> docs/runtime-state.md を読む。

期待する状態:
- latest remote commit は、この handoff commit 以降の `git log -1 --oneline` で確認する。
- `HEAD...origin/master` は `0 0` にする。
- tracked working tree は clean にする。
- active lane は G-28 game mechanics diagnostic reviewability / scoped YMM4-saved carrier review conditions。

現在の確定事項:
- Human review decision: accept.
- Carrier: Lecture Diagram Carrier.
- Accepted artifact precedent:
  - samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.html
  - samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_readback.json
  - samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_report.md
- Current accepted surface is inspector-first, not an in-frame overlay.
- HTML/readback contract:
  - review_surface=inspector_first
  - in_frame_review_overlay=false
  - review_overlay_default=false
  - clean_frame_available=true
  - semantic_labels_human_visible=true
  - review_label_layer_or_inspector_exists=true
  - production_text_budget_separate_from_review_labels=true
- Semantic labels are visible in the Review Inspector below the 16:9 frame:
  - 入力操作
  - 内部ルール
  - 画面上の結果
  - 操作感
  - 判定 / 当たり判定
  - リスクとリターン
- The default 16:9 frame remains clean. Review-only labels are separated from production-visible frame text.
- Boundary remains diagnostic_only=true / production_candidate=false.

Current owner docs:
- docs/verification/G28-GAME-MECHANICS-HUMAN-REVIEW-PACKET-2026-06-05.md
- docs/verification/G28-GAME-MECHANICS-YMM4-SAVED-CARRIER-REVIEW-CONDITIONS-2026-06-08.md
- docs/runtime-state.md
- docs/project-context.md
- docs/USER_COPYPASTE_BLOCKS.md SECTION 20

Next safe work:
- Collect human-supplied inputs for the scoped YMM4-saved carrier review conditions:
  - explicit human selection of that review mode
  - carrier path
  - preview screenshot
  - timeline screenshot
  - item/layer confirmation
  - bottom caption safe-area evidence
- Or stay with the accepted HTML/readback diagnostic precedent and only update handoff/decision docs if a new human decision is supplied.

Do not:
- Do not generate a new theme variant.
- Do not add a new carrier skeleton.
- Do not change generator/scripts unless the user explicitly asks for a narrow wording or readback/report correction.
- Do not generate Source-Footage Carrier work.
- Do not intake gameplay screenshots, source footage, image paths, URLs, or raw references.
- Do not generate `.ymmp`.
- Do not render.
- Do not perform production timing.
- Do not mark production_candidate.
- Do not approve production or creative final acceptance.
- Do not change rights_status.
- Do not return to the G-27 active blocker.
- Do not return to RSS / OPML / Inoreader / NotebookLM.
- Do not touch common foundation / `.agent` work.
- Do not touch ClipPipeGen.
- Do not modify AGENTS.md.

Verification for docs-only continuation:
- git status --porcelain=v1
- git status --porcelain=v1 -uno
- git diff --name-only
- git diff --check
- git diff --cached --check
- staged forbidden scan before commit
- pytest may be omitted if src / gui / Python package / tests are unchanged
- after commit and push, verify `git rev-list --left-right --count HEAD...origin/master` is `0 0`

Completion report:
- Summarize branch / HEAD / origin alignment.
- List changed files.
- State that inspector-first / clean-frame contract remains recorded.
- State diagnostic_only=true / production_candidate=false.
- State Source-Footage / .ymmp / render / production timing / creative final acceptance remained untouched.
- Provide the next prompt or next human input needed.
```

===== SECTION 24: Common Foundation Pre-execution Dry-run Preview MVP Handoff =====
Use this prompt when resuming after the preview-only pre-execution dry-run CLI
implementation. This is not permission to implement or run real execution.

BEGIN_COPY_BLOCK_FOR_AGENT

NLMYTGen common foundation has a preview-only pre-execution dry-run CLI. Review
or audit the preview surface, and preserve the execution boundary. Do not open a
real runner path from this prompt.

repo:
C:\Users\PLANNER007\NLMYTGen

Start by running:
git status --porcelain=v1
git status --porcelain=v1 -uno
git fetch --prune origin
git pull --ff-only
git branch --show-current
git rev-parse --short HEAD
git rev-list --left-right --count "HEAD...@{u}"
git diff --name-only
git diff --cached --name-only

Read in this order:
AGENTS.md
docs/REPO_LOCAL_RULES.md
docs/runtime-state.md
docs/project-context.md
docs/AGENT_ORCHESTRATION.md
docs/AGENT_OPERATOR_SURFACE.md
docs/verification/PRE-EXECUTION-DRY-RUN-FLOW-DESIGN-2026-06-10.md
docs/USER_COPYPASTE_BLOCKS.md SECTION 24

Expected state:
- branch: master
- upstream parity: 0 0
- tracked working tree: clean before new work
- latest remote should include `pre_execution_dry_run_preview_mvp_001` or a
  later approved handoff

Current decision:
- `scripts/agent_orchestrator.py --pre-execution-dry-run` exists.
- It builds the existing execution plan, runs `build_execution_preflight` in
  `dry_run_preview` mode, embeds `render_preflight_preview_card`, prints
  Markdown to stdout, and stops.
- The preview shows selected worker, prompt source, schema path, planned report
  path, working directory, timeout, shell-free argv preview, repo status
  summary, authority summary, preflight allowed/blocked state,
  `safe_to_start_real_runner`, reasons, inspected paths, preflight preview card,
  human next action, and explicit execution boundary.
- `--repo-status-clean` is an operator-provided clean assertion after external
  git checks. The CLI itself does not spawn Git.
- `--repo-status-json` can pass a repo-local status object for blocked/dirty
  preview review.
- `safe_to_start_real_runner=true` remains eligibility only, not execution
  permission.

Smoke command:
uv run python scripts/agent_orchestrator.py --worker audit --pre-execution-dry-run --timestamp handoff-smoke --repo-status-clean

Boundary:
- Do not implement real `codex exec`.
- Do not add `subprocess.run`.
- Do not add stdin piping.
- Do not add a runtime worker loop.
- Do not add an external notification service.
- Do not create `.agent/reports`, `.agent/logs`, or `.agent/needs_human.json`
  runtime artifacts from the preview path.
- Do not evaluate a worker report from a real run.
- Do not touch GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader,
  NotebookLM, `.ymmp`, render, rights, production, publishing, or release
  automation unless a new user request explicitly changes scope.

Allowed next common-foundation entry:
- human review of the preview Markdown surface
- audit of repo-status input handling
- docs/readback correction if the preview wording is unclear
- separate real-runner design only after explicit human authorization

Verification before any handoff commit:
- uv run pytest tests/test_agent_orchestration.py
- uv run pytest tests/test_guardrails.py
- uv run python -m py_compile scripts/agent_gate.py scripts/agent_notify_stub.py scripts/agent_orchestrator.py scripts/agent_operator_surface.py
- uv run python scripts/agent_orchestrator.py --worker audit --pre-execution-dry-run --timestamp handoff-smoke --repo-status-clean
- git diff --check
- git diff --cached --check
- staged forbidden scan:
  - no .agent runtime artifacts
  - no samples / .ymmp
  - no gui / src
  - no Newsroom / ClipPipeGen paths
  - no credentials / token-like strings

Completion report should state:
- branch, HEAD, and upstream parity
- changed files
- verification commands and outcomes
- whether runtime artifacts were generated
- whether real execution remains closed
- next safe entry point

END_COPY_BLOCK_FOR_AGENT

===== SECTION 23: Common Foundation Pre-execution Dry-run Flow Design Handoff =====
Use this prompt when resuming after the pre-execution dry-run flow design.
This is a restart / handoff prompt for design review or a future preview-only
implementation slice. It is not permission to implement or run real execution.

BEGIN_COPY_BLOCK_FOR_AGENT

NLMYTGen common foundation has a docs-only pre-execution dry-run flow design.
Review the design and preserve the execution boundary. Do not open a real
runner path from this prompt.

repo:
C:\Users\thank\Storage\Media Contents Projects\NLMYTGen

Start by running:
git status --porcelain=v1
git status --porcelain=v1 -uno
git fetch --prune origin
git pull --ff-only origin master
git branch --show-current
git rev-parse --short HEAD
git rev-list --left-right --count "HEAD...@{u}"
git diff --name-only
git diff --cached --name-only

Read in this order:
AGENTS.md
docs/REPO_LOCAL_RULES.md
docs/runtime-state.md
docs/project-context.md
docs/AGENT_ORCHESTRATION.md
docs/AGENT_OPERATOR_SURFACE.md
docs/verification/PRE-EXECUTION-DRY-RUN-FLOW-DESIGN-2026-06-10.md
docs/USER_COPYPASTE_BLOCKS.md SECTION 23

Expected state:
- branch: master
- upstream parity: 0 0
- tracked working tree: clean before new work
- known untracked residue may remain:
  - .claude/worktrees/
  - samples/2026-05-16.ymmp
- latest remote should include the docs-only dry-run flow design commit or a
  later approved handoff commit

Current decision:
- `pre_execution_dry_run_flow_design_001` is docs-only.
- The design explains how a human reviews a future execution attempt before
  anything real runs.
- The human-visible dry-run flow shows:
  - selected worker
  - prompt source
  - schema path
  - planned report path
  - working directory
  - timeout
  - shell-free command argv preview
  - `build_execution_preflight` result
  - raw preflight preview card
  - inspected files
  - stop reasons
  - human decision options
- `safe_to_start_real_runner=true` remains an eligibility signal only. It is
  not execution permission.

Boundary:
- Do not implement real `codex exec`.
- Do not add `subprocess.run`.
- Do not add stdin piping.
- Do not add a runtime worker loop.
- Do not add an external notification service.
- Do not create `.agent/reports`, `.agent/logs`, or `.agent/needs_human.json`
  runtime artifacts.
- Do not modify Python code or tests unless a later prompt explicitly opens a
  preview-only implementation slice.
- Do not touch GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader,
  NotebookLM, `.ymmp`, render, rights, production, publishing, or release
  automation unless a new user request explicitly changes scope.

Allowed next common-foundation entry, only with explicit user approval:
- human review of the dry-run flow design
- docs-only design correction if the preview flow is unclear
- preview-only implementation planning
- preview-only implementation that prints inputs, command argv, preflight
  result, and operator card, then stops

Still not allowed by this prompt:
- starting a real runner
- treating `safe_to_start_real_runner=true` as permission
- writing runtime reports/logs/needs-human artifacts
- sending external notification

Completion report should state:
- branch, HEAD, and upstream parity
- changed files, if any
- whether code/tests/runtime artifacts changed
- whether real execution remains closed
- verification commands and outcomes
- next safe entry point

END_COPY_BLOCK_FOR_AGENT

===== SECTION 22: Common Foundation Preflight Operator Surface Parked Handoff =====
Use this prompt when resuming the common foundation after the standalone
preflight preview card was human-reviewed as sufficient and the lane was parked.
This is a restart / handoff prompt, not permission to implement real execution.

BEGIN_COPY_BLOCK_FOR_AGENT

NLMYTGen common foundation is parked after human review of the standalone
preflight preview card. Preserve the parked state, confirm remote parity, and do
not open a real execution path.

repo:
C:\Users\PLANNER007\NLMYTGen

Start by running:
git status --porcelain=v1
git status --porcelain=v1 -uno
git fetch --prune origin
git pull --ff-only origin master
git branch --show-current
git rev-parse --short HEAD
git rev-list --left-right --count "HEAD...@{u}"

Read in this order:
AGENTS.md
docs/REPO_LOCAL_RULES.md
docs/runtime-state.md
docs/project-context.md
docs/AGENT_ORCHESTRATION.md
docs/AGENT_OPERATOR_SURFACE.md
docs/USER_COPYPASTE_BLOCKS.md SECTION 22

Expected state:
- branch: master
- upstream parity: 0 0
- working tree: clean before new work
- the parking decision after `f7d4733 docs: park preflight operator surface` is
  the current common-foundation state unless a newer remote commit says
  otherwise

Current decision:
- `cde00ca feat: add preflight preview card` implemented the standalone raw
  preflight preview card.
- Human review accepted the preflight preview card as sufficient for the
  current operator review surface.
- Operator Review Surface MVP now has two read-only faces:
  - an orchestration flow-result card
  - a standalone raw preflight preview card
- A human can inspect preflight status, `safe_to_start_real_runner`, reasons,
  inspected paths, authority summary, execution boundary, and human next action.
- The common foundation is parked at usable preflight / operator review-surface
  coverage.

Boundary:
- `safe_to_start_real_runner=true` is not execution permission.
- Any real runner still requires a separate, explicitly authorized runner slice.
- Do not implement real `codex exec`.
- Do not add `subprocess.run`.
- Do not add stdin piping.
- Do not add a runtime worker loop.
- Do not add an external notification service.
- Do not create `.agent/reports`, `.agent/logs`, or `.agent/needs_human.json`
  runtime artifacts.
- Do not touch `.ymmp`, render, production, rights, publishing, G-28, Newsroom,
  G-27, ClipPipeGen, RSS, OPML, Inoreader, or NotebookLM unless a new user
  request explicitly changes scope.

Allowed next common-foundation entry, only with explicit user approval:
- docs-only runner consumption design
- pre-execution dry-run flow design
- a narrow audit that verifies the parked review-surface contract without
  opening execution

If the user only asks to preserve context and sync remote:
- update only docs/runtime-state.md, docs/project-context.md, and, if useful,
  docs/USER_COPYPASTE_BLOCKS.md
- run `git diff --check`
- run `git diff --cached --check`
- run a staged forbidden scan before commit
- omit pytest for docs-only changes unless scripts/tests/src/gui changed
- stage explicit files only; do not use `git add -A`
- commit and push
- verify `git rev-list --left-right --count "HEAD...@{u}"` returns `0 0`

Completion report should state:
- branch, HEAD, and upstream parity
- changed files
- commands run and outcomes
- whether artifacts were generated
- that scripts/tests/.agent/gui/src/samples were untouched
- that real execution remains closed
- the next safe entry point

END_COPY_BLOCK_FOR_AGENT

===== SECTION 21: Newsroom Handoff Supervision Gate Request Authority =====
Use this prompt when resuming after the Newsroom handoff supervision gate. The
current decision is request_authority / no-op_wait. The Newsroom repo and export
paths were verified read-only on 2026-06-09, but do not implement until the
human explicitly chooses copy-in versus read-only reference and explicitly
authorizes pausing or superseding the G-28 game_mechanics lane.

For ChatGPT copy/paste reports, wrap the whole report in one outer Markdown
code fence. Keep `BEGIN_COPY_BLOCK_FOR_CHATGPT` and
`END_COPY_BLOCK_FOR_CHATGPT` inside that fence. Do not put any nested Markdown
code fences inside the copy block, including the next prompt section.

```text
NLMYTGen / Newsroom handoff は request_authority / no-op_wait として扱ってください。実装せず、まず cross-repo authority と export availability を確認するだけに限定してください。

repo:
C:\Users\thank\Storage\Media Contents Projects\NLMYTGen

開始時に必ず実行:
git status --porcelain=v1
git status --porcelain=v1 -uno
git fetch --prune origin
git pull --ff-only
git branch --show-current
git rev-parse --short HEAD
git rev-list --left-right --count "HEAD...@{u}"
git diff --name-only
git diff --cached --name-only

読む:
- AGENTS.md
- docs/REPO_LOCAL_RULES.md
- docs/runtime-state.md
- docs/project-context.md の Latest supervision gate
- docs/verification/NEWSROOM-HANDOFF-SUPERVISION-GATE-2026-06-09.md
- docs/USER_COPYPASTE_BLOCKS.md SECTION 21

現在の判定:
- NLMYTGen active lane は G-28 game_mechanics diagnostic reviewability / later scoped YMM4-saved carrier review conditions。
- active artifact は g28_lecture_diagram_carrier_game_mechanics_explanation_v1。
- Newsroom handoff は candidate downstream input であり、NLMYTGen authority ではない。
- Newsroom repo は read-only 確認済み: C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline
- Newsroom repo state は main / 1296b8e / HEAD...origin/main=0 0。
- Newsroom export folder は read-only 確認済み: C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853
- 確認済み handoff files:
  - export_manifest.json
  - script.csv
  - script_ir.json
  - visual_ir.json
  - visual_plan.md
  - source_list.md
  - quote_manifest.yml
  - asset_manifest.yml
  - ymm4_notes.md
- export_manifest は episode_756343df9853 / story_20260603_503c39418f15862d / script_d2a46430e084 / packet_20260603_2de578dcd4b0 / warnings=[] / deferred=[]。
- source_list は primary Microsoft Blog / critical NIST。
- ymm4_notes は speaker=ナレーター / warningsなし / human_required 0。
- ただし copy-vs-read-only decision と G-28 lane pause/supersede decision は未提供。

次に必要な human authority:
1. NLMYTGen側へコピーするか、read-only path参照にするかの人間判断
2. G-28 game_mechanics active lane を一時停止/上書きして Newsroom downstream intake に入るかの明示判断
3. downstream intake を開始する場合の最初の成果物範囲: docs-only intake plan / manifest mapping / adapter implementation のどれか

許可:
- 上記が揃った場合のみ、read-onlyで再確認・manifest整合・raw/private/copyright-unclear assetなしを確認する。
- read-only確認で十分なら docs/runtime-state.md / docs/project-context.md / docs/verification の狭い記録だけ検討する。

禁止:
- 実装
- export files の自動 copy-in
- Newsroom subprocess/path/pip dependency
- full .ymmp generation
- render / production / rights / creative approval
- Review Console implementation
- context visual plugin
- G-27 revival
- ClipPipeGen
- RSS / OPML / Inoreader / NotebookLM
- common foundation / real codex exec
- git add -A
- AGENTS.md への手順追記

完了報告:
- 全体を単一の外側 Markdown code block で囲む。
- ブロック内は BEGIN_COPY_BLOCK_FOR_CHATGPT で始め、END_COPY_BLOCK_FOR_CHATGPT で終える。
- next prompt 欄に内側の ```text や ``` を使わない。
- branch / HEAD / origin alignment / tracked dirty state を明記する。
- request_authority / no-op_wait のままなら、必要な human authority を明記して止める。
```
