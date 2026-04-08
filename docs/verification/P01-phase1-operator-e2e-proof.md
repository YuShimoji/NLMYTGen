# P-01 — Phase 1 運用 E2E 手順（オペレータ向け）

Phase 1（B-18 + C-09）を **1 本の台本**で通すための再現手順。GUI LLM 上の実編集は人間作業のため、ここでは **CLI まで機械再現可能な部分**を正本とする。

## 前提

- リポジトリ root で [uv](https://github.com/astral-sh/uv) が使えること。
- 台本が `normalize` で読める `.txt` または `.csv` であること。

## 手順

### 1. 機械診断（B-18）

```bash
uv run python -m src.cli.main diagnose-script "samples/AI監視が追い詰める生身の労働.txt" ^
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" ^
  --format json > _tmp_script_diag.json
```

（PowerShell 以外では `^` を `\` に読み替える。）

- **text** 表示にする場合は `--format text`（省略可）。
- GUI の場合: 「品質診断」タブ → B-18 台本診断 → 台本選択 → Speaker Map 入力 → Diagnose Script。

### 2. GUI LLM（C-09）

1. [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md) の **LLM への指示**を Custom GPT / Claude Project 等の Instructions に含める。
2. 同ファイルの **入力テンプレート**に、`_tmp_script_diag.json` の内容と **元台本全文**を貼る。
3. 出力の **修正済み台本全文**だけを `refined.txt` 等に保存する（話者ラベル形式を維持）。

### 3. パース確認と CSV（build-csv）

```bash
uv run python -m src.cli.main validate refined.txt
uv run python -m src.cli.main build-csv refined.txt -o _tmp_out.csv ^
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" ^
  --max-lines 2 --chars-per-line 40 --reflow-v2 --dry-run
```

（`refined.txt` が元と同じラベルなら `--speaker-map` は実ラベルに合わせる。）

### 4. 効果の記録（任意）

- 修正前後の **手動編集時間**（分）と、**IR 生成時の曖昧さ**（主観メモ）を 1 行でも残す。
- 追記先の例: 本ファイル末尾「記録」、または `project-context.md` の DECISION LOG。

## repo-local 機械確認（2026-04-06 時点）

以下は **C-09 を除く**自動ステップのスモークとして実行済み（開発時）:

- `diagnose-script` on `samples/AI監視が追い詰める生身の労働.txt` → JSON 正常終了（exit 0）。診断内容は [B18-script-diagnostics-ai-monitoring-sample.md](B18-script-diagnostics-ai-monitoring-sample.md) と同型。
- `build-csv` on 上記サンプル（未 refinement）→ 既存パイプラインどおり CSV 生成可能（E2E の「refined 稿」は人間または LLM 出力待ち）。

### ロードマップ実装スライス（2026-04-06）

将来開発プラン（repo: [FUTURE_DEVELOPMENT_ROADMAP.md](../FUTURE_DEVELOPMENT_ROADMAP.md)）に沿い、同サンプルで **CLI 部分を再実行**（exit 0）:

- `diagnose-script` … `--format json`
- `validate` … `OK: 28 utterances parsed`（既知 WARN: row 10 長文）
- `build-csv` … `--dry-run`、111 行相当プレビュー

**C-09（GUI LLM refinement）は未実施**のため、本スライスは「機械パス」の記録に留まる。人間＋ LLM で refined 稿まで進めたら、上表に別行で追記する。

## 記録

| 日付 | 台本 | refined 使用 | 手動時間(前/後) | メモ |
|------|------|--------------|-----------------|------|
| 2026-04-06 | samples/AI監視が追い詰める生身の労働.txt | 未（C-09 未実施） | 未計測 | ロードマップ手順: CLI のみ再スモーク exit 0。refined 稿での E2E は運用者待ち |
| 2026-04-08 | samples/AI監視が追い詰める生身の労働.txt | 未（C-09 未実施） | 未計測 | B-11 途中確認（約半分）: 改行 Pass / 辞書 0。次着手は P2 背景アニメ演出の小規模適用（1〜2セクション）で route と見え方を確認。 |
