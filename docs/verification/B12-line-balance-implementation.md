# B-12 Implementation Verification

## Scope

- feature: `B-12 行バランス重視の字幕分割`
- date: 2026-03-31
- status: implemented
- owner: `assistant`

## What Changed

- `build-csv` に `--balance-lines` を追加
- `--max-lines` 使用時に、2行字幕向けの自然改行を opt-in で挿入
- 読点・句点・カギカッコ付近を候補にしつつ、2行の表示幅バランスを崩しにくい位置を優先
- 既存テキストは削らず、改行位置のみを調整

## Verification

| check | result |
|---|---|
| `uv run pytest` | 51 passed |
| CLI help | `uv run python -m src.cli.main build-csv --help` で `--balance-lines` 表示 |
| sample dry-run | `samples/AI監視が追い詰める生身の労働.txt` を `--max-lines 2 --chars-per-line 40 --balance-lines --stats --dry-run` で確認 |
| CSV newline contract | embedded newline を含む1行CSVの保持テストを追加 |

## Sample Observation

- preview 上で、2行字幕向けの明示改行が追加されることを確認
- 例:
  - `ちょっと想像してみてください。\nあなたは配送バンの運転席に座っています。`
  - `猛暑の中で息苦しさを感じて、\n喘息の発作が起きそうになったとします。`

## Post-import Visual Evidence

| check | result |
|---|---|
| manual line breaks | 10 |
| re-split long lines | 15 |
| awkward word wraps | 5 |
| timing-only issues | 0 |
| overall | partial win |

### Notes

- `。` 位置での改行は一定数効いた
- 一文が `、` などで長くつながる発話は依然としてはみ出しやすい
- カギカッコ、カタカナ語、3字以上の漢字連なりでの折り返しは残る
- 1文字だけの最終行が増えた。例: `す。` のような widow/orphan が発生

### Assessment

- B-12 は純粋な手動改行の負荷を減らしたが、長文再分割の負荷はまだ高い
- 次の主 pain は「句読点が少ない長文の節分割」と「1文字行の回避」
- 次候補は clause-aware split と widow/orphan guard を組み合わせた L2 改善

## Residual Risk

- YMM4 テンプレート差込みの見た目最適化は未検証
- overflow warning 自体は全件解消ではなく、長文が残るケースは引き続き manual judgement が必要
- post-import visual evidence を更新して、bulk rework がどこまで減ったかを再確認する必要がある
