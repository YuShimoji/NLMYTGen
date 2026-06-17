# Lane Registry

NLMYTGen 周辺の複数レーンを、巨大化してから慌てて分離するのではなく、今の段階で責務境界ごとに管理するための台帳。

この文書は `docs/INVARIANTS.md`、`docs/REPO_LOCAL_RULES.md`、`docs/runtime-state.md` を置き換えない。通常再開の主軸は引き続き `runtime-state.md` が決める。この台帳は、別 repo / worktree / 開発スレッドが NLMYTGen との接続を忘れないための地図である。

## 管理原則

- repo 分離は規模ではなく責務で決める。上流編集、共通基盤、NLMYTGen 内 sidequest を同じ「別プロジェクト」として扱わない。
- NLMYTGen は NotebookLM / ScriptIR / VisualIR / YMM4 downstream adapter の中心であり、Newsroom や source ingest の所有者ではない。
- separate repo は NLMYTGen の実装へ依存しない。接続は portable artifact、schema、manifest、copy-in / read-only reference の判断で行う。
- in-repo sidequest は NLMYTGen の制作価値に戻る道を持つ。長期 worktree は merge / freeze / migrate / archive の出口を持つ。
- common foundation は NLMYTGen 固有語彙を吸い込まない。NLMYTGen は reference host / repo adapter であり、universal common core ではない。

## レーン台帳

| レーン | 管理単位 | 現在の場所 | 正本 / 読むもの | 起動条件 | NLMYTGen との接続 | 分離・終了条件 |
| --- | --- | --- | --- | --- | --- | --- |
| NLMYTGen 本流 | 中心 repo | `NLMYTGen` / `master` | `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, `docs/INVARIANTS.md`, `docs/TASK_DEVELOPMENT_CYCLE_SPEC.md` | 通常再開の既定。別レーンを明示されない限りここへ戻る | NotebookLM 由来テキスト、ScriptIR、VisualIR、YMM4 CSV、YMM4 adapter / proof ingest | 上流編集責務、source ingest、Newsroom 運営判断を取り込まない |
| 開発自動化の基盤 | common-core 候補 | 現在は `NLMYTGen/.agent/`, `docs/AGENT_ORCHESTRATION.md`, `docs/AGENT_OPERATOR_SURFACE.md`, `docs/verification/*REAL-RUNNER*` | `docs/AGENT_ORCHESTRATION.md`, `docs/AGENT_OPERATOR_SURFACE.md`, `docs/verification/REAL-RUNNER-BOUNDARY-DESIGN-2026-06-09.md`, `docs/verification/PRE-EXECUTION-DRY-RUN-FLOW-DESIGN-2026-06-10.md` | 開発自動化 / worker / gate / runner 基盤を明示されたとき | NLMYTGen は reference adapter。common core は prompt catalog, worker report schema, gate, preflight, notify stub の形だけを持つ | 2 つ目の repo adapter が必要になる、または real runner 実装に進む前に別 repo / package 化を検討する |
| newsroom-yt-pipeline | 独立 upstream repo | `newsroom-yt-pipeline` / `main` | `docs/PROJECT_SPEC.md`, `docs/NLMYTGEN_BOUNDARY.md`, `docs/HANDOFF.md`, `docs/RUNTIME_STATE.md` | Newsroom downstream intake / editorial pipeline / source ingest を明示されたとき | export bundle を NLMYTGen が copy-in または read-only reference で受ける。shared code / subprocess / local path dependency は持たない | 独立 repo 維持。NLMYTGen へ移すのは downstream adapter mapping と intake proof だけ |
| Baseball / sports_news | NLMYTGen 内 sidequest | `NLMYTGen/lanes/sports_news/`, `NLMYTGen/BaseballInfoGraphics/`, worktree `NLMYTGen-baseball-sidequest` | `docs/TASK_DEVELOPMENT_CYCLE_SPEC.md`, `docs/BASEBALL_NEWS_PIPELINE_SPEC.md`, `lanes/sports_news/README.md`, `BaseballInfoGraphics/README.md` | チャットで Baseball / sports_news sidequest と明示されたとき | screen plan first。BaseballInfoGraphics は design source であり、YMM4 へは PNG / animated asset / placement note として接続する | source ingest、league operations、publishing、独立データ運用が主責務になったら repo 分離を再検討する。それまでは NLMYTGen 内レーン |
| RSS / reader clean | 削除準備 / 互換凍結候補 | worktree `NLMYTGen-rss-clean`, branch `codex/rss-reader-sync-clean` | `docs/RSS_LANE_EXIT_BOUNDARY.md`, `docs/RSS_READER_SYNC_SPEC.md`, `docs/verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md`, 対象 worktree の `docs/runtime-state.md` | RSS legacy review / deletion prep / compatibility freeze を明示されたとき | raw OPML, token, private feed URL, full article body は入れない。OPML import / source list / sanitized smoke / RSS fetch / read-only Inoreader fetch は Newsroom 側へ移管済み | 現在の責務分類では source ingest は Newsroom 側。NLMYTGen 内では compatibility freeze か削除準備へ進む |

## separate repo の接続契約

NLMYTGen と別 repo の間では、次を各 repo 側の境界文書に置く。

| 項目 | 書く内容 |
| --- | --- |
| 位置 | upstream producer / downstream adapter / common foundation / sidequest のどれか |
| 渡せる artifact | export manifest, script CSV, ScriptIR, VisualIR, asset manifest, quote manifest, notes など |
| 持たない責務 | NLMYTGen 側の YMM4 geometry、render、publishing、source ingest など |
| 禁止依存 | subprocess, local absolute path dependency, shared code import, package dependency, hidden runtime DB coupling |
| NLMYTGen 側 gate | copy-in か read-only reference か、どの intake proof から始めるか |
| 終了条件 | merge / freeze / migrate / archive / separate repo 維持の判断 |

## レーン変更時の更新

- 本流 `next_action` が変わる場合は `docs/runtime-state.md` を更新する。
- 新しい separate repo が NLMYTGen と接続する場合は、相手 repo に `docs/NLMYTGEN_BOUNDARY.md` 相当を置く。
- 長期 worktree を作る場合は、この台帳に branch / purpose / exit condition を追加する。
- sidequest が NLMYTGen 本流へ戻る場合は、戻す artifact と lane 内に閉じる artifact を closeout で分ける。
- 各レーンへ認識合わせを投げるときは `docs/LANE_ALIGNMENT_PROMPTS.md` を使う。
