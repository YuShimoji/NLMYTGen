# B-16 Workflow Proof Log

- date: 2026-03-31
- transcript / source: `AI監視が追い詰める生身の労働.txt`
- packet markdown: `AI監視が追い詰める生身の労働_diagram_packet.md`
- packet json: `AI監視が追い詰める生身の労働_diagram_packet.json`
- packet command: `python -m src.cli.main build-diagram-packet samples/AI監視が追い詰める生身の労働.txt`

## Packet Quality

| 項目 | 記録 |
|---|---|
| utterance count | 28 |
| section seed count | 3 |
| figure-worthy sections looked plausible? | yes。S1/S2/S3 の 3 図に絞られ、diagram-first な区間選定として自然 |
| missing context | S4/S5 は図より背景演出寄りと判断されたようで、現時点では大きな欠落には見えない |

## Diagram Brief Result

| 項目 | 記録 |
|---|---|
| summary quality | high。個人の身体→倉庫→都市・制度のスケール拡張で 3 図へ整理できている |
| diagram brief usefulness | high。各図の goal が明確で、図の役割がすぐ掴める |
| must_include usefulness | high。図に入れる要素が具体的で、白紙時間を減らせそう |
| label_suggestions usefulness | medium-high。たたき台として十分使える |
| avoid_misread usefulness | high。矮小化しやすい誤読ポイントを先回りできている |

## Time Comparison

| 項目 | 分 | メモ |
|---|---:|---|
| before: manual diagram planning estimate | 15 | どの区間を図にするか、各図に何を入れるかを決める想定時間 |
| after: diagram brief assisted planning | 3 | diagram brief を見ながら同じ判断が終わるまでの概算 |
| delta | 12 | diagram planning の白紙時間を大きく短縮 |

## Assessment

| 項目 | 記録 |
|---|---|
| useful enough to keep using? | yes 寄り。diagram planning の初動支援として価値あり |
| next improvement inside repo | B-15 cue memo との差分をさらに明確にする。diagram 対象 section を少し絞る余地はある |
| should remain text-only? | yes |
| should stay separate from B-15? | yes。背景演出メモと図作成メモは役割が異なる |

## Rerun Result

| 項目 | 記録 |
|---|---|
| response file | `AI監視が追い詰める生身の労働_diagram_brief_rerun_received.md` |
| selected diagrams | 3 |
| selected sections | `S1-S2`, `S3`, `S3` |
| excluded sections | 導入の雰囲気説明だけで足りる区間、終盤の抽象締め |
| better | 背景で足りる区間を図対象から外し、因果・比較・層構造がある箇所だけに絞れた |
| unchanged | goal / avoid_misread / operator_todos の有用性は高いまま |
| worse | `source_section` が section seed 粒度より粗く、`S3` 内に複数図が入るため局所参照の粒度はまだ荒い |

## Notes

- diagram brief そのものはこのファイルに貼るか、別ファイルへの参照を書く
- 実レスポンス保存先: `AI監視が追い詰める生身の労働_diagram_brief_received.md`
- rerun 実レスポンス保存先: `AI監視が追い詰める生身の労働_diagram_brief_rerun_received.md`
- 画像生成や図版ファイル生成は行わない
- 1 回の proof が終わったら、次に repo 内で直す点を 1 件だけ残す
