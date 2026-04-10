# B-11 Workflow proof — Amazon Panopticon サンプル（新台本・2026-04-10）

元台本 [`samples/The Amazon Panopticon Surveillance and the Modern Worker.txt`](../../samples/The%20Amazon%20Panopticon%20Surveillance%20and%20the%20Modern%20Worker.txt) と、レーン A 用に編集した refined 稿 [`samples/amazon_panopticon_lane_a_refined.txt`](../../samples/amazon_panopticon_lane_a_refined.txt) を用いた記録。取込前・取込後は **本ファイル 1 本**に集約する。

> **検証範囲の区別**
>
> - **§1 取込前**: 2026-04-10 に repo root で `diagnose-script` / `validate` / `build-csv --stats` を実行し機械再現済み。
> - **§2 取込後**: **YMM4 実機での全編通しは、本セッションの実行環境では未実施**（アプリ非搭載）。§2.1 の 4 区分は **プレースホルダ（暫定 0）** とし、オペレータが `samples/amazon_panopticon_B11_ymm4.csv` を YMM4 S-4 で読み込み、[B11-manual-checkpoints.md](../B11-manual-checkpoints.md) に沿って通し確認した **実測値で上書き**すること（[B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §5 の本番条件）。

## メタデータ

| 項目 | 値 |
| --- | --- |
| 記録日（取込前 CLI） | 2026-04-10 |
| 記録日（取込後 YMM4） | **未実施（オペレータ更新待ち）** |
| トランスクリプト識別子 | `samples/The Amazon Panopticon Surveillance and the Modern Worker.txt`（refined: `samples/amazon_panopticon_lane_a_refined.txt`） |
| 出力 CSV（YMM4 台本読込用） | `samples/amazon_panopticon_B11_ymm4.csv` |
| 話者 | **未ラベル**（`--unlabeled` → `Speaker_A` / `Speaker_B` 交互割当） |

### C-09（台本 refinement）について

GUI LLM は未使用。**C-09 相当**として、元台本の ASR 由来の誤変換・文法崩れを人手で修正した稿を `samples/amazon_panopticon_lane_a_refined.txt` に保存（87 発話・1 行 1 発話を維持）。診断 JSON の入力は既存 [`samples/p0_nextcycle_amazon_diag.json`](../../samples/p0_nextcycle_amazon_diag.json) を参照可能。

---

## 1. 取込前（`build-csv` + `--stats`）

実行したコマンド（CSV を実際に書き出したもの）:

```text
uv run python -m src.cli.main build-csv "samples/amazon_panopticon_lane_a_refined.txt" ^
  -o "samples/amazon_panopticon_B11_ymm4.csv" ^
  --unlabeled --max-lines 2 --chars-per-line 40 --reflow-v2 --stats --format json
```

`--stats` および overflow 警告（そのまま）:

```text
--- Stats ---
  Speaker_A: 122 utterances, 2691 chars (avg 22)
  Speaker_B: 122 utterances, 2894 chars (avg 23)
  Total: 244 utterances, 5585 chars
--- Overflow candidates (>2 lines at 40 chars/line) ---
  [WARN] row 39: Speaker_B, 推定3行 (display_width=79)
  [WARN] row 70: Speaker_B, 推定3行 (display_width=82)
  [WARN] row 85: Speaker_A, 推定3行 (display_width=72)
  [WARN] row 102: Speaker_A, 推定3行 (display_width=66)
  [WARN] row 104: Speaker_A, 推定3行 (display_width=76)
  [WARN] row 116: Speaker_A, 推定4行 (display_width=83)
  [WARN] row 158: Speaker_B, 推定3行 (display_width=79)
  [WARN] row 160: Speaker_A, 推定3行 (display_width=64)
  [WARN] row 161: Speaker_A, 推定3行 (display_width=72)
  [WARN] row 167: Speaker_B, 推定3行 (display_width=76)
  [WARN] row 169: Speaker_B, 推定3行 (display_width=60)
  [WARN] row 210: Speaker_B, 推定3行 (display_width=72)
  [WARN] row 235: Speaker_B, 推定3行 (display_width=81)
Written: samples\amazon_panopticon_B11_ymm4.csv (244 rows)
```

`--format json` 最終行:

```json
{"input": "samples\\amazon_panopticon_lane_a_refined.txt", "success": true, "output": "samples\\amazon_panopticon_B11_ymm4.csv", "rows": 244, "speakers": {"Speaker_A": 122, "Speaker_B": 122}}
```

**対比（同一台本・未 refined・2026-04-10 の CLI のみ run）**: [`P01-phase1-operator-e2e-proof.md`](P01-phase1-operator-e2e-proof.md) の `p0_nextcycle_amazon_2026-04-10_a` 行参照 — 232 rows、overflow 候補 18 行。refined 後は **244 rows / 14 件**（候補純減）。

**補助ログ（全文）**: [`samples/lane_a_amazon_2026-04-10_refined_build_utf8.txt`](../../samples/lane_a_amazon_2026-04-10_refined_build_utf8.txt)

**B-18（refined 稿）**: [`samples/lane_a_amazon_2026-04-10_refined_diag.json`](../../samples/lane_a_amazon_2026-04-10_refined_diag.json) — `ROLE_SKIPPED_NO_MAP`（info）のみ。

### YMM4 側の次ステップ（手動）

1. YMM4 で **台本読み込み** に `samples/amazon_panopticon_B11_ymm4.csv` を指定する。
2. `Speaker_A` / `Speaker_B` をテンプレのキャラに割り当てる（未ラベル CSV の既定手順）。
3. [B11-manual-checkpoints.md](../B11-manual-checkpoints.md) の順で通し、**§2.1 を実測で上書き**する。

---

## 2. 取込後（YMM4 通し確認後）

**現状**: 全編通し**未実施**。以下はプレースホルダであり、**実機確認後に必ず差し替える**こと。

### 2.1 残修正の件数サマリ（4 区分）

| 区分 | 件数（暫定） | メモ |
| --- | ---: | --- |
| 辞書登録 | 0 | YMM4 未実施のため暫定。実測後に更新。 |
| 手動改行 | 0 | 同上 |
| 再分割したい長文 | 0 | 同上（§1 の overflow 候補は**機械警告**として監視。実作業件数は実機でカウント） |
| タイミングのみ | 0 | 同上 |

### 2.2 代表例（3 件以上 — 取込前・overflow 候補ベース）

YMM4 上での手修正は未計測のため、**§1 の機械 overflow 候補**から代表を抜粋する。

1. **row 116（Speaker_A）** — `display_width=83`、**推定4行**。長尺の締め・問いかけブロックに近い表示負荷。
2. **row 39（Speaker_B）** — `display_width=79`、推定3行。中盤の説明ブロック。
3. **row 235（Speaker_B）** — `display_width=81`、推定3行。終盤のまとめに近いブロック。

### 2.3 （参照）判断メモ

プラン直前判定の正本は **§3**（[B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §3 と同一体裁）。

---

## 3. プラン直前判定（判断メモ）

[B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §3・§4 に準拠。

- **判定**: **保留**（§2 取込後が未実測のため Gate A/B/C の確定はしない）。取込前データからの **推定** は **Gate A 寄り**（overflow 候補 14 件・改行系リスクが目立つ）。
- **根拠**: refined により元の 18 件から 14 件へ候補が減少。いまだ `display_width` 最大 83 行（推定4行）が残存。
- **次投資先**:
  1. オペレータが本 CSV で YMM4 全編通し → §2.1 を実測で埋め、§3 を確定 Gate に更新する。
  2. 取込前観測のみを見る限り、L2 の reflow / C-09 ルールでの長尺分割を継続検証する価値あり（他台本の B-11 と併読）。

---

## 関連

- テンプレ正本: [workflow-proof-template.md](../workflow-proof-template.md)
- 手動確認タイミング: [B11-manual-checkpoints.md](../B11-manual-checkpoints.md)
- レーン A runbook: [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)
