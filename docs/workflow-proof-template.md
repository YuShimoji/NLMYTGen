# Workflow proof 記録テンプレート（B-11）

[OPERATOR_WORKFLOW.md](OPERATOR_WORKFLOW.md) の **B-11** に従い、**1 本のトランスクリプト**について「取込前の機械出力」と「YMM4 取込後の人手修正」を**同一ファイル**に残すための正本です。

**手動確認が必要なタイミング**は [B11-manual-checkpoints.md](B11-manual-checkpoints.md) を参照。

## 使い方

1. このファイルを `docs/verification/` にコピーし、ファイル名を `B11-workflow-proof-<案件名または日付>.md` にする。
2. 下記プレースホルダを埋める。
3. `build-csv` は `**--max-lines 2 --chars-per-line 40 --stats`** を含める（Reflow v2 等、実運用と同じオプションにそろえる）。

---

## メタデータ


| 項目          | 値                  |
| ----------- | ------------------ |
| 記録日         | YYYY-MM-DD         |
| トランスクリプト識別子 | （ファイル名・回など）        |
| 使用コマンド（取込前） | （下記「取込前」に貼ったものと同一） |


---

## 1. 取込前（`build-csv` + `--stats`）

実行したコマンド（コピペ）:

```text
python -m src.cli.main build-csv <INPUT> -o <OUTPUT.csv> --max-lines 2 --chars-per-line 40 --stats [--reflow-v2 等]
```

CLI の `--stats` ブロックおよび overflow 警告の要約（そのまま貼付）:

```text
（ここに貼付）
```

`--format json` で得た最終行 JSON があれば（任意）:

```json
{}
```

---

## 2. 取込後（YMM4 通し確認後）

### 2.1 残修正の件数サマリ（4 区分）

[OPERATOR_WORKFLOW](OPERATOR_WORKFLOW.md) で定義された区分ごとに件数を記載する。


| 区分       | 件数  | メモ  |
| -------- | --- | --- |
| 辞書登録     |     |     |
| 手動改行     |     |     |
| 再分割したい長文 |     |     |
| タイミングのみ  |     |     |


### 2.2 代表例（任意・箇条書き）

- （字幕行 / CSV 行番号が分かれば併記）
- …

---

## 3. 判断メモ（次の投資先）

- 残修正が「例外」に寄ったか / 支配的な pain が何か（1〜3 行）
- 次に触るレイヤー（L2 改行ルール / GUI パケット / IR 等）の仮説

---

## 関連

- `build-cue-packet` / `build-diagram-packet` の `**--bundle-dir**` 利用時は、同梱される `*_workflow_proof.md` と本テンプレを役割分担する（パケット側は外部 LLM 貼付用、本テンプレは **B-11 通し記録** 用）。

