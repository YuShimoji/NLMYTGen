# RSS Pickup-First Brief Summary — 2026-06-01

RSS cleanup や Inoreader 完全同期を blocker にせず、取得済み RSS 候補から動画テーマ候補 brief を作った。

詳細 brief は local-only の `_tmp/rss_topic_cluster_briefs_current.md` と `_tmp/rss_topic_cluster_briefs_current.json` にある。これらは source selection 用の作業 artifact であり、記事タイトルやリンクを含むため commit 対象外。

## 今回の pickup 面

| 観測項目 | 件数 |
| --- | ---: |
| sources | 147 |
| fetched sources | 121 |
| error sources | 26 |
| candidate entries | 6470 |
| category-bearing entries | 5410 |
| represented categories | 7 |
| generated clusters | 9 |

failed feed は skip 済みの既知ノイズとして扱い、topic selection の blocker にはしていない。cleanup は任意であり、動画テーマ選択の前提ではない。

## 生成した動画テーマ候補

| 優先 | 生成テーマ名 | cluster label | topic-match count | broad category mix | NotebookLM投入適性 |
| ---: | --- | --- | ---: | --- | --- |
| 1 | AIの燃料を誰が握るのか | AI計算資源・半導体 | 529 | The Economist / エンターテイメント / uncategorized / World News | 高 |
| 2 | 関税が世界を小さくする日 | 米中・関税・経済ブロック化 | 1397 | The Economist / 国際主要 / uncategorized / World News | 高 |
| 3 | 終わらない戦争が日常を変える | 戦争・安全保障・地政学リスク | 1164 | The Economist / World News / uncategorized / 国際主要 | 高 |
| 4 | ゲーム業界はなぜ遊びづらくなったのか | ゲーム産業・プラットフォーム再編 | 1489 | ゲーム系 / uncategorized / フリーゲームまとめ / エンターテイメント | 中〜高 |
| 5 | あなたの情報はどこで漏れているのか | サイバー攻撃・個人情報・脆弱性 | 110 | エンターテイメント / uncategorized / World News / The Economist | 中〜高 |
| 6 | SFが先に描いた現実ニュース | 映画・配信・SF的想像力 | 643 | エンターテイメント / ゲーム系 / World News / uncategorized | 中 |
| 7 | 投票箱の外で社会は割れている | 選挙・社会分断・制度不信 | 435 | The Economist / 国際主要 / World News / uncategorized | 中 |
| 8 | 科学ニュースが静かに警告していること | 科学・気候・健康リスク | 253 | エンターテイメント / World News / uncategorized / ゲーム系 | 中 |
| 9 | 日本のニュースは生活費にどう返ってくるのか | 日本国内・市場・生活実感 | 295 | 国内主要 / The Economist / 国際主要 / ゲーム系 | 低〜中 |

優先投入候補は 5 本。高適性は「AIの燃料を誰が握るのか」「関税が世界を小さくする日」「終わらない戦争が日常を変える」の 3 本で、中〜高はゲーム産業とサイバーの 2 本。

## 次の動き

次は 1〜3 cluster を選び、local-only brief から代表ソースを 8〜15 件程度へ絞って NotebookLM input 候補にする。実際の NotebookLM 投入、台本生成、YMM4、動画生成にはまだ進んでいない。

repo に残したのは sanitized summary のみ。記事タイトル一覧、実リンク、feed リンク、購読一覧の生データ、token、本文詳細は commit しない。
