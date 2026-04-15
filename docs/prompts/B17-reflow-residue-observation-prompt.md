# B-17 字幕改行 v2 残差観測 Prompt（委任正本）

**目的**: `reflow_subtitles_v2`（B-17 完了済）の残差ケースを観測記録する。**アルゴリズム変更は提案しない。観測のみ。**

**位置づけ**: 既存 [CORE-PARALLEL-HUB §5 Prompt-R](../verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md) の詳細版。[VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](../verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) §4 トラック B と連携。

---

## Actor / Owner

- actor: `assistant`（CLI 実行）または `user`（YMM4 実機目視確認）
- owner artifact: `docs/verification/P01-phase1-operator-e2e-proof.md` のメモ列 1 行追記
- 改変範囲: docs のみ。`src/` / `tests/` は触らない

---

## 入力

- 最新エピソードの build-csv 出力
  - `samples/<episode_id>_ymm4.csv`（build-csv 実行済 CSV）
  - `samples/<episode_id>_build.txt`（build-csv --stats ログ、`[WARN]` 行含む）

## 実行コマンド

v2 改行を有効化した build-csv は次のフラグで実行する（`src/cli/main.py` p_build 定義と一致）:

```
uv run python -m src.cli.main build-csv <input> \
  --reflow-v2 \
  --balance-lines \
  --max-lines 2 \
  --chars-per-line 40 \
  --stats \
  -o samples/<episode_id>_ymm4.csv
```

注:
- `--balance-lines` は v1 時代からのバランス再配分フラグで v2 と併用可。
- `--reflow-v2` は v2 アルゴリズム本体スイッチ。
- `--stats` で `[WARN]` 行（`display_width` 推定オーバー）を stdout に出す。

---

## 観測項目

build-csv 出力 CSV と、可能なら YMM4 実機での字幕表示を目視し、以下を数える:

1. 手動改行を入れた箇所の件数（`\n` が行途中に現れているもの）
2. 単語途中分断の件数（英単語・熟語が行境界で割れているもの）
3. 1 文字最終行の残存件数（2 行目末に 1 文字だけ残るケース）
4. 2 行字幕のバランス偏り（目視。1 行目 40 / 2 行目 2 のような強い偏り）

## P01 追記形式（メモ列）

既存の P01 表は 5 列 `| 日付 | 台本 | refined 使用 | 接続判定 | メモ |`。新規列は追加しない。メモ列に下記の 1 行要素として追記する:

```
reflow_residue: manual_break=<N>, word_split=<N>, single_char_tail=<N>, balance_skew=<N>; build=samples/<episode_id>_build.txt; csv=samples/<episode_id>_ymm4.csv
```

追記例（P01 表の 1 行全体）:

```
| 2026-04-20 (`reflow_residue_<episode_id>_2026-04-20_a`) | samples/<episode_id>_refined.txt | 任意 | reflow_residue（観測のみ） | reflow_residue: manual_break=0, word_split=1, single_char_tail=0, balance_skew=2; build=samples/<episode_id>_build.txt; csv=samples/<episode_id>_ymm4.csv |
```

---

## 制約（read-only observation）

- **アルゴリズム変更は提案しない。** 2 ケース以上の再現があれば別ブロックで起票検討（FEATURE_REGISTRY に proposed で追加）。
- docs 以外は変更しない。`src/` / `tests/` 変更は禁止。
- P01 表のスキーマ（列構成）は触らない。メモ列への 1 行追記のみ。
- `--reflow-v2` `--balance-lines` `--max-lines` `--chars-per-line` 以外のフラグ追加は本タスクの範囲外。

## 受理基準

- [ ] P01 表に 1 行追加されている
- [ ] メモ列に 4 観測項目の件数が記録されている
- [ ] `src/` / `tests/` の差分なし（git diff で確認）
- [ ] build / csv のパスがメモ列にリンクされている

## 参照

- [P01-phase1-operator-e2e-proof.md](../verification/P01-phase1-operator-e2e-proof.md) — 追記先
- [VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](../verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) §4 — トラック B（改行ギャップ記録）
- [CORE-PARALLEL-HUB §5 Prompt-R](../verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md)
- [src/cli/main.py](../../src/cli/main.py) `p_build` — build-csv argparse 実装
