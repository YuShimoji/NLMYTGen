# B-15 Workflow Proof Log

- date: 2026-03-31
- transcript / source: `AI監視が追い詰める生身の労働.txt`
- packet markdown: `AI監視が追い詰める生身の労働_cue_packet.md`
- packet json: `AI監視が追い詰める生身の労働_cue_packet.json`
- packet command: `python -m src.cli.main build-cue-packet samples/AI監視が追い詰める生身の労働.txt`

## Packet Quality

| 項目 | 記録 |
|---|---|
| utterance count | 28 |
| section seed count | 3 |
| role analysis looked correct? | 概ね Yes。host/guest の機能差は実感と合う |
| missing context | 特に大きな欠落は見えないが、実編集上は素材候補を絞り込む補助がさらにあるとよい |

## Cue Memo Result

| 項目 | 記録 |
|---|---|
| summary quality | 高い。論理勾配と視覚弧が短くまとまっている |
| section cues quality | 高い。packet の 3 seed から 5 section へ自然に再構成できている |
| background cue usefulness | 高い。ただし候補が多いので実運用では主背景1つ＋補助素材1つ程度まで圧縮したい |
| emotion / BGM / transition usefulness | 中。方向づけとして有用だが、SE は現状ほぼ不要 |
| operator_todos usefulness | 高い。proof で見るべき観点がそのまま残っている |

## Time Comparison

| 項目 | 分 | メモ |
|---|---:|---|
| before: manual prep estimate | 30-60 | 構成・粒度・方向性をゼロから決める想定時間 |
| after: cue memo assisted prep | 5 | cue memo を見ながら方針メモ化した時間 |
| delta | 25-55 | 初回観測として大きい短縮 |

## Assessment

| 項目 | 記録 |
|---|---|
| useful enough to keep using? | Yes。全体構成、粒度、具体例、方向性の叩き台として明確に有効 |
| next improvement inside repo | SE を必須項目のように見せないことと、背景候補を主背景＋補助素材へ圧縮しやすい contract に寄せること |
| should remain text-only? | Yes |
| should SDK integration wait? | Yes。まずは contract 改善を優先 |

## Notes

- cue memo そのものはこのファイルに貼るか、別ファイルへの参照を書く
- YMM4 / `.ymmp` direct edit は行わない
- 1 回の proof が終わったら、次に repo 内で直す点を 1 件だけ残す
- cue memo 参照: `AI監視が追い詰める生身の労働_cue_memo_received.md`
- 役に立った: 全体構成、粒度、具体的ケース、方向性
- ノイズ: SE 関連は現状ほぼ不要。AI 生成前提なら目安になるが、後で埋もれやすい
- 注意: 実際の制作時間は素材選定で大きく変わる。動画素材でつなぐ場合は 3 時間級になることもある
- 注意: 特に図の作成、いらすとや等のフリー素材探索、動画素材の尺つなぎが強い bottleneck
- cue memo は「演出方針決め」を大きく軽くしたが、素材取得そのものの重さは別問題として残る
- rerun cue memo 参照: `AI監視が追い詰める生身の労働_cue_memo_rerun_received.md`
- rerun 所感: section は 4 区分に収まり、背景は primary/supporting に揃った。前回より扱いやすい
- rerun 所感: sound cue は空欄または一点指定に減り、optional 化の意図は概ね反映された
