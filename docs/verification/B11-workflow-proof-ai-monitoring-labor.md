# B-11 Workflow proof — AI監視サンプル（YMM4 取込前まで完了）

既存サンプル [`samples/AI監視が追い詰める生身の労働.txt`](../../samples/AI監視が追い詰める生身の労働.txt) を用いた記録。**セクション 2 は YMM4 取込・通し確認後に人手で埋める。**

## メタデータ

| 項目 | 値 |
|------|-----|
| 記録日（取込前） | 2026-04-06 |
| トランスクリプト識別子 | `samples/AI監視が追い詰める生身の労働.txt` |
| 出力 CSV（YMM4 台本読込用） | `samples/AI監視が追い詰める生身の労働_B11_ymm4.csv` |
| Speaker Map | `スピーカー1=れいむ,スピーカー2=まりさ` |

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

## 2. 取込後（YMM4 通し確認後 — 未記入）

> **以下は YMM4 確認後に編集すること。**

### 2.1 残修正の件数サマリ（4 区分）

| 区分 | 件数 | メモ |
|------|------|------|
| 辞書登録 | | |
| 手動改行 | | |
| 再分割したい長文 | | |
| タイミングのみ | | |

### 2.2 代表例（任意）

- （行番号 / 字幕内容）

### 2.3 判断メモ（次の投資先）

- 

---

## 関連

- テンプレ正本: [workflow-proof-template.md](../workflow-proof-template.md)
- 手動確認タイミング: [B11-manual-checkpoints.md](../B11-manual-checkpoints.md)
