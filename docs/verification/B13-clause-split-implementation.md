# B-13 Implementation Verification

## Scope

- feature: `B-13 節分割 + widow/orphan guard`
- date: 2026-03-31
- status: implemented
- owner: `assistant`

## What Changed

- `split_long_utterances()` に、文末がない長文向けの clause-aware split fallback を追加
- `、` / `,` / `，` / `;` / `:` と、`しかし` / `ですが` / `なので` / `一方で` / `ということ` などを節分割候補に使用
- `balance_subtitle_lines()` 側では、極端に短い2行目を作る改行候補を棄却するよう変更
- 既存フラグは増やさず、`--balance-lines` の内部品質改善として適用

## Verification

| check | result |
|---|---|
| `uv run pytest` | 54 passed |
| targeted tests | clause split 2件 + widow guard 1件を追加 |
| sample dry-run | `--max-lines 2 --chars-per-line 40 --balance-lines --stats --dry-run` で確認 |
| sample CSV write | `samples/AI監視が追い詰める生身の労働_balance_lines_ymm4.csv` を再生成 |

## Sample Observation

| item | result |
|---|---|
| input utterances | 57 |
| output rows after B-13 | 62 |
| interpretation | 長い一文の一部が clause-aware split で複数行へ再編された |

## Post-import Visual Evidence

| check | result |
|---|---|
| manual line breaks | 5 |
| re-split long lines | 10 |
| awkward word wraps | 5 |
| timing-only issues | 0 |
| overall | improved, but still too many residual fixes |

### Notes

- 手動改行は `10 -> 5`、再分割したい長文は `15 -> 10` まで減った
- 不自然な単語分割は `5` のままで、大きな改善は見られない
- 最初の数発話以外は見た目の変化が小さい
- 例: `私たちが普段「アルゴリズムによる最適化」と聞くと、効率的でクリーンな魔法を想像しがちですが、もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。`
  は依然として 1 つの字幕として残った

### Assessment

- B-13 は partial win。手動改行と再分割負荷は減ったが、「まだ多い」という operator judgement は変わらない
- 主 pain は、長い一文が 1 字幕に残るケースと、不自然な単語折り返しが残るケース
- 次候補は、`--max-lines` 超過の単一長文をより積極的に複数字幕へ落とす aggressive clause chunking

## Residual Risk

- YMM4 取込後の fresh visual evidence はまだ未取得
- 接続句ルールは最小限なので、句読点も接続句も少ない長文や、1 字幕に残る説明文にはまだ弱い
- テンプレート差込みの見た目最適化は引き続き manual judgement が必要
