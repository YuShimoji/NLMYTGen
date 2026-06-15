# RSS Lane Exit Boundary

`NLMYTGen-rss-clean` は、RSS / OPML / Inoreader の入力取得を検証するための移行・互換レーンであり、NLMYTGen 本流の新しい長期プロダクトレーンではない。

現在の NLMYTGen 本流では、RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection は `newsroom-yt-pipeline` 側の upstream editorial responsibility として扱う。OPML import、source list readback、sanitized source smoke、RSS fetch、read-only Inoreader fetch は Newsroom 側へ移管済みの後継対象である。したがって、この worktree の次の判断は「拡張」ではなく、互換凍結または削除準備である。

## 許可される作業

- raw OPML / token / private feed URL を repo 外に置いた live smoke。
- sanitize 済み evidence の作成。
- `FeedSource` / `FeedEntry` / `rss-smoke` の互換性確認。
- Newsroom へ移管できる概念の抽出。
- 本流へ最小回収する場合の差分範囲整理。

## 避ける作業

- RSS / Inoreader を NLMYTGen 本流の active responsibility として拡張する。
- raw OPML、token、private feed URL、full article body を git に入れる。
- OAuth、refresh token storage、unread/read sync、subscription mutation、background polling、GUI sync をこの branch で増やす。
- NotebookLM packet selection、topic clustering、series planning を NLMYTGen 側へ戻す。
- YMM4 adapter、render、publishing と接続する。

## 出口候補

| 出口 | 意味 | 次に必要な判断 |
| --- | --- | --- |
| compatibility freeze | 既存 RSS helper を互換機能として残し、active 開発を止める | どの CLI / docs / tests を最小維持するか |
| migrate to Newsroom | OPML / Inoreader / smoke evidence の考え方を Newsroom upstream へ移す | 後継実装は `newsroom source import-opml`, `newsroom source smoke`, `newsroom fetch --source rss`, `newsroom fetch --source inoreader` |
| minimal recovery to mainline | 後方互換上必要な小差分だけ NLMYTGen 本流へ戻す | source ingest を active 化しない範囲 |
| archive | branch を参照用として閉じる | 最終 handoff と raw input 非保持の確認 |

## 認識合わせ

次にこの worktree を開くときは、NLMYTGen 本流の `docs/LANE_ALIGNMENT_PROMPTS.md` の `RSS / reader clean 移行レーン` を使い、最初に出口候補を選ぶための報告を返す。
