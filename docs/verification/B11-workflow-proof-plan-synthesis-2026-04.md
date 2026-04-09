# B-11 workflow proof（開発プラン 2026-04 合成記録）

[workflow-proof-template.md](../workflow-proof-template.md) に沿った **F-01/F-02 再審査ゲート用の材料**として、repo 同梱サンプルで **取込前（L2）機械出力**までを記録する。YMM4 取込後の人手修正は **未実施**（次回オペレータが同テンプレで追記可能）。

## メタデータ

| 項目 | 値 |
| --- | --- |
| 記録日 | 2026-04-08 |
| トランスクリプト識別子 | `samples/example_dialogue.txt`（短い対話サンプル） |
| 使用コマンド（取込前） | 下記「1. 取込前」と同一 |

---

## 1. 取込前（`build-csv` + `--stats`）

実行したコマンド（コピペ）:

```text
uv run python -m src.cli.main build-csv samples/example_dialogue.txt --dry-run --max-lines 2 --chars-per-line 40 --stats --reflow-v2
```

CLI の `--stats` ブロックおよび overflow 警告の要約（そのまま貼付）:

```text
--- Stats ---
  Host1: 9 utterances, 172 chars (avg 19)
  Host2: 6 utterances, 155 chars (avg 25)
  Total: 15 utterances, 327 chars
--- No overflow candidates (all within 2 lines at 40 chars/line) ---
(dry-run: CSV not written)
```

---

## 2. 取込後（YMM4 通し確認後）

**未記入。** 実制作 1 本で YMM4 取込後に、テンプレート §2.1 の 4 区分を数えて追記する。

---

## 3. 判断メモ（次の投資先）

- 本ファイルは **開発プランの workflow-proof To-do 消化**用の下地。支配的 pain は **サンプルが短く overflow 0 件**のため、この時点では **F-01（分割プレビュー GUI）の必要性は観測されず**。
- 次の一手: **長尺トランスクリプト**（例: `samples/石油消失で書き換わる世界経済のOS.txt`）で同コマンドを再実行し、overflow / 手動改行の有無を B-11 表に記録すると、F-01/F-02 再審査ゲートの判断材料が揃う。

---

## 関連

- [OPERATOR_WORKFLOW.md](../OPERATOR_WORKFLOW.md)（B-11、F-01/F-02 再審査ゲート）
- [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)（motion G-17 / Phase2 の運用正本）
