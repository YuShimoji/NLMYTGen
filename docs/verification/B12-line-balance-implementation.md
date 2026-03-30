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

## Residual Risk

- YMM4 テンプレート差込みの見た目最適化は未検証
- overflow warning 自体は全件解消ではなく、長文が残るケースは引き続き manual judgement が必要
- post-import visual evidence を更新して、bulk rework がどこまで減ったかを再確認する必要がある
