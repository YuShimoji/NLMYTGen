# B-11 Workflow proof（サンプル記録）

リポジトリ同梱の `samples/example_dialogue.txt` を用いた **記録例**。実制作では本ファイルをコピーして案件名に差し替え、YMM4 取込後の表を実測値で埋める。

## メタデータ

| 項目 | 値 |
|------|-----|
| 記録日 | 2026-04-06 |
| トランスクリプト識別子 | `samples/example_dialogue.txt` |
| 使用コマンド（取込前） | 下記と同一 |

---

## 1. 取込前（`build-csv` + `--stats`）

実行したコマンド:

```text
uv run python -m src.cli.main build-csv samples/example_dialogue.txt --max-lines 2 --chars-per-line 40 --stats --dry-run --format json
```

`--stats` 要約（標準出力の Stats ブロック）:

- Host1: 6 utterances, 172 chars (avg 28)
- Host2: 5 utterances, 155 chars (avg 31)
- Total: 11 utterances, 327 chars
- No overflow candidates (all within 2 lines at 40 chars/line)

`--format json` 最終行:

```json
{"input": "samples\\example_dialogue.txt", "success": true, "dry_run": true, "rows": 11, "speakers": {"Host1": 6, "Host2": 5}}
```

---

## 2. 取込後（YMM4 通し確認後）

> **注**: 以下の表はサンプル用プレースホルダ。実際の取込後に置き換える。

### 2.1 残修正の件数サマリ（4 区分）

| 区分 | 件数 | メモ |
|------|------|------|
| 辞書登録 | （未実施: サンプルのみ） | |
| 手動改行 | （未実施） | |
| 再分割したい長文 | （未実施） | |
| タイミングのみ | （未実施） | |

### 2.2 判断メモ

- 本ファイルは **テンプレ運用の実例** として、取込前ブロックのみ機械再現可能な値で固定した。
- 実案件ではここまでを 1 ファイルに揃えると B-11 の判断ゲートに使える。
