# B-14 Implementation Verification

## Scope

- feature: `B-14 aggressive clause chunking`
- date: 2026-03-31
- status: implemented
- owner: `assistant`

## What Changed

- `split_long_utterances()` で、複数文発話の中にある単一長文も sentence ごとに先に再展開するよう変更
- 通常の clause-aware split 候補が尽きた残り長文に対し、引用句や機能語まで使った aggressive clause chunking fallback を追加
- 既存フラグは増やさず、`--balance-lines` の内部品質改善として適用

## Verification

| check | result |
|---|---|
| `uv run pytest` | 56 passed |
| targeted regression | 複数文発話の先頭長文再展開 + 引用句 split のテストを追加 |
| sample dry-run | `samples/AI監視が追い詰める生身の労働.txt` を `--max-lines 2 --chars-per-line 40 --balance-lines --stats --dry-run` で確認 |
| sample CSV write | `samples/AI監視が追い詰める生身の労働_balance_lines_ymm4.csv` を再生成 |

## Sample Observation

| item | result |
|---|---|
| input utterances | 57 |
| output rows after B-14 | 95 |
| overflow candidates | 3 |
| interpretation | 1 字幕に残っていた長い一文の多くが、複数字幕へ再編された |

### Remaining Overflow Candidates

- row 5: 推定 4 行 (`display_width=124`)
- row 42: 推定 3 行 (`display_width=104`)
- row 92: 推定 4 行 (`display_width=152`)

## Assessment

- B-14 は CLI 側では strong win。overflow candidates は大幅に減り、B-13 まで残っていた「長い一文が 1 字幕に残る」ケースをかなり崩せた
- 一方で、字幕行数は 57 → 95 まで増えているため、YMM4 上ではテンポが細かくなりすぎる新リスクがある
- 次に必要なのは、YMM4 取込後の fresh visual evidence で「再分割負荷がさらに減ったか」と「字幕が細かく切れすぎていないか」を同時に見ること

## Additional Operator Observation

- `、` 起点の分割強化により、長すぎる行はかなり減った
- 全字幕が 3 行以内に収まる水準まで改善した
- 残課題は bulk overflow ではなく、`ー`、カギ括弧 `「」`、`202/4` のような数値+記号折り返しなど、個別ケースの改行品質に移った
- ここから先は heuristic を増やすより、「改行すべき/すべきでない例」の corpus を集めて傾向化する方が自然

## Residual Risk

- post-import visual evidence はまだ未取得
- aggressive chunking により、意味まとまりよりテンポ分断が先に立つケースがあり得る
- 残り 3 件の overflow candidates は manual judgement が必要
