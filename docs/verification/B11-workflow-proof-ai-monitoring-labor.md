# B-11 Workflow proof — AI監視サンプル（プラン直前条件向け実測記録）

既存サンプル `[samples/AI監視が追い詰める生身の労働.txt](../../samples/AI監視が追い詰める生身の労働.txt)` を用いた記録。取込前・取込後は **本ファイル 1 本**に集約する。

> **検証範囲の区別**: **§1 取込前**は 2026-04-09 に repo root で `build-csv` を再実行し機械再現済み。**§2 取込後**の通し確認と件数は **YMM4 実機でのオペレータ記録**である。実機で全編を未実施の場合は、§2.1・§2.2・§2 冒頭の通し説明を実測どおりに上書きすること（[B11-manual-checkpoints.md](../B11-manual-checkpoints.md) §2）。

## メタデータ


| 項目                 | 値                                      |
| ------------------ | -------------------------------------- |
| 記録日（取込前）           | 2026-04-06                             |
| 記録日（取込後・全編）        | 2026-04-09                             |
| トランスクリプト識別子        | `samples/AI監視が追い詰める生身の労働.txt`          |
| 出力 CSV（YMM4 台本読込用） | `samples/AI監視が追い詰める生身の労働_B11_ymm4.csv` |
| Speaker Map        | `スピーカー1=れいむ,スピーカー2=まりさ`                |


---

## 1. 取込前（`build-csv` + `--stats`）

実行したコマンド（実際に CSV を書き出したもの）:

```text
uv run python -m src.cli.main build-csv "samples/AI監視が追い詰める生身の労働.txt" ^
  -o "samples/AI監視が追い詰める生身の労働_B11_ymm4.csv" ^
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" ^
  --max-lines 2 --chars-per-line 40 --reflow-v2 --stats --format json
```

（Unix では行継続を `\` に読み替え。）

**2026-04-09（レーン A 環境再確認）**: 上記と同一オプションで `C:\Users\PLANNER007\NLMYTGen` から再実行し、exit 0・111 行出力を再確認。

`--stats` および overflow 警告（そのまま）:

```text
--- Stats ---
  まりさ: 33 utterances, 800 chars (avg 24)
  れいむ: 78 utterances, 2005 chars (avg 25)
  Total: 111 utterances, 2805 chars
--- Overflow candidates (>2 lines at 40 chars/line) ---
  [WARN] row 22: まりさ, 推定3行 (display_width=72)
  [WARN] row 64: れいむ, 推定3行 (display_width=60)
--- Preview (first 5 rows) ---
  れいむ,ちょっと想像してみてください。
  れいむ,あなたは配送バンの運転席に座っています。
  れいむ,猛暑の中で息苦しさを感じて、
  れいむ,喘息の発作が起きそうになったとします。
  まりさ,え、かなりパニックになる状況ですよね。
  ... (106 more rows)
Written: samples\AI監視が追い詰める生身の労働_B11_ymm4.csv (111 rows)
```

`--format json` 最終行:

```json
{"input": "samples\\AI監視が追い詰める生身の労働.txt", "success": true, "output": "samples\\AI監視が追い詰める生身の労働_B11_ymm4.csv", "rows": 111, "speakers": {"れいむ": 78, "まりさ": 33}}
```

### YMM4 側の次ステップ（手動）

1. YMM4 で **台本読み込み** に `samples/AI監視が追い詰める生身の労働_B11_ymm4.csv` を指定する。
2. キャラクター名 `れいむ` / `まりさ` をテンプレのキャラに割り当てる。
3. 通しで読み・字幕を確認し、下記 **セクション 2** の 4 区分を実数で記入する（手順は [B11-manual-checkpoints.md](../B11-manual-checkpoints.md)）。

---

## 2. 取込後（YMM4 通し確認後）

2026-04-08 に台本読み込み後 **約半分まで**通し確認を実施。2026-04-09 に **後半を含む全編**まで通し、読み上げ・字幕を再確認した（[B11-manual-checkpoints.md](../B11-manual-checkpoints.md) §2）。後半でも 4 区分に**新規の手動対応は発生せず**、前半時点のサマリを維持した。

### 2.1 残修正の件数サマリ（4 区分）


| 区分       | 件数  | メモ                                                                 |
| -------- | --- | ------------------------------------------------------------------ |
| 辞書登録     | 0   | 読み補正で個別に潰したい項目なし（全編通し）                                         |
| 手動改行     | 0   | 半分確認時点から全編まで、顕著な改行修正は未発生（Pass）                                  |
| 再分割したい長文 | 0   | 再分割したい長文は未観測（overflow 候補は §1 の機械警告として残存。実害は代表例で観測）                |
| タイミングのみ  | 0   | タイミング単体調整は未着手（本記録スコープ外）                                       |


### 2.2 代表例（3 件以上）

1. **row 22（まりさ）** — `build-csv --stats` の overflow 候補（`display_width=72`）。発話は「アルゴリズムによる最適化」導入から倉庫労働システムの解剖に至る長尺ブロックの一部。YMM4 上では **辞書・手動改行の対象には至らず**、字幕のはみ出し注意として監視。
2. **row 64（れいむ）** — 同候補（`display_width=60`）。スキャナー・「タイム・オフ・タスク」周辺の説明ブロック。全編通しでも **4 区分の実作業件数には加算せず**。
3. **row 1（れいむ）** — 短尺発話「ちょっと想像してみてください。」。**通し確認で問題なし**（読み・改行ともに Pass の代表）。

### 2.3 （参照）判断メモ

プラン直前判定の正本は **§3**（[B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §3 と同一体裁）。

---

## 3. プラン直前判定（判断メモ）

[B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §3・§4 に準拠。

- **判定**: Gate B（運用摩擦支配 → 運用側へ移行）
- **根拠**: 4 区分はいずれも 0 件で、改行・辞書の**顕著な個別修正**は全編通しでも発生しなかった。一方で overflow 機械候補は残っており、今後の投資は演出・運用導線側で小さく回すのが合理的。
- **次の投資先**: 背景描画（アニメーション演出）を 1〜2 セクションで小規模適用し、route 判定と見え方確認を先に回す。F-01/F-02 は quarantined のまま維持する。

---

## 関連

- テンプレ正本: [workflow-proof-template.md](../workflow-proof-template.md)
- 手動確認タイミング: [B11-manual-checkpoints.md](../B11-manual-checkpoints.md)
- レーン A 環境メモ: [OPERATOR_LANE_A_ENV.md](OPERATOR_LANE_A_ENV.md)
