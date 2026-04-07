# G-15 — 発話スパン Micro `bg`（Layer 0）

## 目的

`macro.sections[].default_bg` に加え、carry-forward 解決済みの Micro IR `bg` を発話タイムライン区間に合わせて Layer 0 の ImageItem に反映する。

## 優先順位

1. 発話に `bg` が解決されていれば、その発話の Frame スパンではそのラベルを使用する。
2. 発話がカバーしないセクション内ギャップ（先頭・末尾・発話間）は `default_bg` で埋める。
3. 隣接かつ同一ラベルの区間は 1 本の ImageItem にマージする。

## アンカー

- **row-range あり**: `_resolve_utterance_timing` と同じ VoiceItem 範囲で `[start, end)` を Frame 化する。
- **row-range なし**: 従来どおり index ベースの単一 VoiceItem スパン。

## Failure / warning クラス

| クラス | 意味 |
|--------|------|
| `BG_NO_TIMING_ANCHOR` | 発話にタイミングが取れずスキップ |
| `BG_SPAN_OVERLAP` | 区間が逆順・重複などでカーソルより前に戻る異常（警告） |
| （既存） | `bg` ラベルが `bg_map` に無いときは従来どおり warning |

## 互換

- `default_bg` のみ・Micro `bg` なしの IR は、従来と同様にセクション単位の 1 本に帰着する（同一 `default_bg` が連続すればマージ）。
