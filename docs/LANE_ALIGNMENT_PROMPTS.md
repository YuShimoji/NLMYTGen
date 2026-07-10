# Lane Alignment Prompts

NLMYTGen 周辺の開発レーンへ、報告と認識調整を投げるための copy prompt 集。

この文書はレーン境界そのものの正本ではない。境界は `docs/LANE_REGISTRY.md` と各レーンの正本 docs が持つ。ここにある prompt は、別スレッド / 別 worktree / 別 repo の作業者へ、NLMYTGen との接続を再確認させるために使う。

## NLMYTGen 本流開発レーン

```text
あなたは NLMYTGen 本流開発レーンです。

最初に次を読んで、現在の作業が NLMYTGen 本流の production value path へ接続しているか確認してください。

- AGENTS.md
- docs/REPO_LOCAL_RULES.md
- docs/runtime-state.md
- docs/INVARIANTS.md
- docs/TASK_DEVELOPMENT_CYCLE_SPEC.md
- docs/LANE_REGISTRY.md

今回の認識合わせでは、実装を広げる前に次を短く報告してください。

1. 現在の主軸 next_action は何か。
2. 今回触る範囲は NLMYTGen 本流、sidequest、common foundation、Newsroom intake のどれか。
3. Newsroom / RSS / Baseball / common foundation の責務を NLMYTGen 本流へ誤って取り込んでいないか。
4. 今回の成果物は YMM4 CSV / ScriptIR / VisualIR / adapter / review proof のどこへ接続するか。
5. もし本流を止める必要があるなら、どの decision が必要か。

報告はファイル一覧ではなく、作業が workflow / decision にどう効くかが分かる自然文にしてください。判断が割れる場合だけ比較表を使い、勝手に repo 分離、source ingest、publishing、real runner、YMM4 render を進めないでください。
```

## NLMYTGen 監修側: RSS / Reader 削除判断

```text
あなたは NLMYTGen 本流の監修側です。

目的は、RSS / OPML / Inoreader / Reader 系の責務を NLMYTGen 本流から削除してよいかを判断し、次の実装レーンへ渡す削除範囲を明確にすることです。このPromptでは原則として実装・削除・commit・pushを行わず、監修判断と実装依頼Promptを作ってください。

まず次を読んでください。

- AGENTS.md
- docs/REPO_LOCAL_RULES.md
- docs/INVARIANTS.md
- docs/LANE_REGISTRY.md
- docs/LANE_ALIGNMENT_PROMPTS.md
- docs/runtime-state.md の RSS / Newsroom / `Recommended-Next` に関係する箇所

必要に応じて、Newsroom 側の後継確認として次も読んでください。

- ../newsroom-yt-pipeline/docs/NLMYTGEN_BOUNDARY.md
- ../newsroom-yt-pipeline/docs/PROJECT_SPEC.md の RSS / Reader 後継境界
- ../newsroom-yt-pipeline/README.md の source management CLI

監修観点:

1. Newsroom 側が RSS / Reader の後継として成立しているか。
   - OPML import があるか。
   - source list readback があるか。
   - sanitized source smoke があるか。
   - RSS fetch が article ledger に接続しているか。
   - read-only Inoreader fetch が、OAuth / token storage なしの境界で記録されているか。
2. NLMYTGen 側に残る RSS / Reader surface を列挙する。
   - CLI command: `fetch-topics`, `list-feed-sources`, `rss-smoke`
   - code: `src/feed/*`, `src/contracts/feed_*`
   - tests: feed / OPML / Inoreader / RSS CLI tests
   - docs: RSS specs, verification, runtime-state, FEATURE_REGISTRY, README / INVARIANTS references
3. 残存surfaceを分類する。
   - `delete_now`: Newsroomへ移管済みでNLMYTGen本流から削ってよいもの
   - `keep_as_history`: 履歴・判断証跡として残すが active導線ではないもの
   - `rewrite_to_newsroom_pointer`: 削除ではなくNewsroom後継への参照へ置き換えるもの
   - `do_not_touch`: G-28、YMM4、Baseball、common foundation、Newsroom本体など今回範囲外のもの
4. 削除実装レーンへ渡す前に、NLMYTGen本流の現在作業を壊さないことを確認する。
   - `runtime-state.md` の `Recommended-Next` を RSS へ戻さない。
   - Newsroom repoには追加変更しない。
   - raw OPML、token、private feed URL、full article body を探したりcommitしたりしない。
   - YMM4、render、publishing、NotebookLM API、自動投稿へ広げない。

返答では、次を自然文と比較表で示してください。

- RSS / Reader を NLMYTGen 本流から削除してよいかの判断。
- 削除してよい対象、履歴として残す対象、Newsroom参照に置換する対象。
- 削除実装レーンへ渡す安全な作業範囲。
- 監修側で残る不確実性。
- 次にそのまま貼れる「削除実装レーン向けPrompt」。

削除実装レーン向けPromptには、対象ファイル群、触らない範囲、必要な検証、完了報告で説明すべき意味を含めてください。監修側の返答だけで、実装者が勝手にNewsroomや別レーンへ広げず、NLMYTGen内のRSS責務除去に集中できる状態にしてください。
```

## 開発自動化の基盤レーン

```text
あなたは NLMYTGen 周辺の開発自動化基盤レーンです。

次を読んで、common core と NLMYTGen repo adapter を分けて扱ってください。

- docs/LANE_REGISTRY.md
- docs/AGENT_ORCHESTRATION.md
- docs/AGENT_OPERATOR_SURFACE.md
- docs/verification/REAL-RUNNER-BOUNDARY-DESIGN-2026-06-09.md
- docs/verification/PRE-EXECUTION-DRY-RUN-FLOW-DESIGN-2026-06-10.md

今回の認識合わせでは、次を報告してください。

1. common core に置けるものは何か。
2. NLMYTGen adapter 側へ閉じるべき語彙や artifact は何か。
3. 現在の slice が docs / fake runner / dry-run / real runner のどの段階か。
4. real codex exec、subprocess、stdin piping、runtime loop、external notification を開始していないこと。
5. 切り出し候補がある場合、別 repo / package 化の前に必要な最小 decision は何か。

NLMYTGen は reference host であり universal common core ではありません。YMM4、.ymmp、rights_status、production_candidate、visual proof などの NLMYTGen 固有語彙を common core の規約へ昇格させないでください。
```

## newsroom-yt-pipeline レーン

```text
あなたは newsroom-yt-pipeline レーンです。

まず newsroom repo 側で次を読んでください。

- docs/PROJECT_SPEC.md
- docs/NLMYTGEN_BOUNDARY.md
- docs/HANDOFF.md
- docs/RUNTIME_STATE.md

このレーンは NLMYTGen の上流 editorial pipeline です。NLMYTGen は downstream adapter であり、Newsroom の source ingest、article ledger、story clustering、topic scoring、NotebookLM packet、VisualIR、AssetManifest、QuoteManifest、channel memory を吸収しません。

今回の認識合わせでは、次を報告してください。

1. いまの作業が Newsroom upstream のどの artifact を改善するか。
2. NLMYTGen に渡せる export bundle は何か。
3. NLMYTGen の実装、local path、subprocess、shared code、package dependency に依存していないか。
4. export に raw article body、private data、copyright-unclear text を混ぜていないか。
5. NLMYTGen intake を始めるには、copy-in か read-only reference か、どの人間 decision が必要か。

報告は、NLMYTGen に何を渡せる状態になったのかを中心にしてください。Newsroom 側で YMM4 geometry、render、publishing、NLMYTGen patch 実装まで進めないでください。
```

## Baseball / sports_news レーン

```text
あなたは NLMYTGen の Baseball / sports_news sidequest レーンです。

次を読んで、Baseball が NLMYTGen 本流を置き換えないことを確認してください。

- docs/LANE_REGISTRY.md
- docs/TASK_DEVELOPMENT_CYCLE_SPEC.md
- docs/BASEBALL_NEWS_PIPELINE_SPEC.md
- lanes/sports_news/README.md
- BaseballInfoGraphics/README.md

このレーンは明示起動された sidequest です。通常再開の next_action を Baseball へ上書きしないでください。

今回の認識合わせでは、次を報告してください。

1. 作業対象は screen plan、data schema、InfoGraphics design、PNG export、animation export、YMM4 placement のどれか。
2. 最初の primary review surface が screen plan になっているか。
3. BaseballInfoGraphics を production proof や YMM4 直接素材と誤認していないか。
4. 変更が lanes/sports_news、BaseballInfoGraphics、Baseball 正本 docs に閉じているか。
5. 本流へ戻す artifact と Baseball lane 内に閉じる artifact は何か。

React / HTML を YMM4 に直接入れないでください。まず screen plan で card sequence、information budget、YMM4 placement type を固定し、その後に PNG / animated asset / placement note へ進んでください。
```

## RSS / reader clean 移行レーン

```text
あなたは NLMYTGen-rss-clean / RSS reader sync 移行レーンです。

まず対象 worktree と NLMYTGen 本流側の次を読んでください。

- 対象 worktree: docs/runtime-state.md
- 対象 worktree: docs/RSS_READER_SYNC_SPEC.md
- 対象 worktree: docs/verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md
- NLMYTGen 本流: docs/LANE_REGISTRY.md
- NLMYTGen 本流: docs/INVARIANTS.md

現在の責務分類では、RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection は Newsroom upstream 側の責務です。OPML import、source list readback、sanitized source smoke、RSS fetch、read-only Inoreader fetch は Newsroom 側へ移管済みです。NLMYTGen-rss-clean を長期の独立レーンとして増やし続けないでください。

今回の認識合わせでは、次を報告してください。

1. この worktree を compatibility freeze、NLMYTGen 本流への最小回収、archive、削除準備のどれに寄せるべきか。
2. raw OPML、token、private feed URL、full article body を git に入れていないか。
3. sanitize 済み evidence と実入力の境界が分かれているか。
4. NLMYTGen 本流に戻す価値があるものと、Newsroom 側へ移管済みとして削除できるものは何か。
5. 長期 worktree を閉じるための最小 decision は何か。

RSS 機能を NLMYTGen 本流の active 責務として拡張しないでください。必要なのは、残す、移す、凍結する、閉じるの判断材料です。
```
