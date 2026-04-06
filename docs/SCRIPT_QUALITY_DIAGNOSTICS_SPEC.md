# SCRIPT QUALITY DIAGNOSTICS SPEC — B-18

NotebookLM 由来の台本（`.txt` / `.csv`）を `normalize()` した `StructuredScript` に対し、ゆっくり解説向けの手直し前に機械的に気づきやすいパターンを列挙する。

## 位置づけ

- **creative judgement の代替ではない**。最終判断は人間または GUI LLM（C-09）。
- 偽陽性を許容し、既定は **WARNING / INFO** が中心。**ERROR** は `--strict` 用の限定ケースに使う。
- 正本の境界: [INVARIANTS.md](INVARIANTS.md)（constrained rewrite 可、主台本ゼロ生成は不可）。

## Severity

| 値 | 意味 |
|----|------|
| `info` | ロールチェック省略など、コンテキスト説明 |
| `warning` | 見直し推奨（NLM マーカー、連続同一話者、ロール乖離の疑い） |
| `error` | `--strict` 時に exit 1 とする（例: 話者マップ未充足） |

## 診断コード（v1）

| code | severity | 条件（要約） |
|------|----------|----------------|
| `SPEAKER_MAP_UNMAPPED` | warning | `--speaker-map` に存在しない入力話者がある |
| `SPEAKER_MAP_STRICT` | error | `--strict` かつ `SPEAKER_MAP_UNMAPPED` がある |
| `ROLE_SKIPPED_NOT_TWO_SPEAKERS` | info | マップ後の話者種類が 2 以外 → れいむ/まりさ整合チェックをスキップ |
| `ROLE_SKIPPED_NO_MAP` | info | 話者マップなし → 期待名（れいむ/まりさ）との一致チェックはスキップ（ヒューリスティックのみ） |
| `EXPLAINER_ROLE_MISMATCH` | warning | 2 話者・マップあり、`analyze_speaker_roles` の host が `expected_explainer` と不一致 |
| `LISTENER_ROLE_MISMATCH` | warning | 同上で guest が `expected_listener` と不一致 |
| `LISTENER_LONG_AVG_DOMINANCE` | warning | guest の平均発話長が host の `listener_avg_ratio` 倍以上 |
| `NLM_STYLE_MARKER` | warning | 既知の NLM/番組調フレーズに一致（発話単位） |
| `LONG_RUN_SAME_SPEAKER` | warning | 同一話者の連続発話が `long_run_threshold` 以上 |

## パラメータ（CLI）

| フラグ | 既定 | 説明 |
|--------|------|------|
| `--expected-explainer` | `まりさ` | 解説寄り役として期待するマップ後の話者名 |
| `--expected-listener` | `れいむ` | 聞き手寄り役として期待するマップ後の話者名 |
| `--long-run-threshold` | `6` | 連続同一話者で警告する発話数 |
| `--listener-avg-ratio` | `1.25` | guest avg / host avg がこの倍率を超えたら `LISTENER_LONG_AVG_DOMINANCE` |

## CLI: `diagnose-script`

```
python -m src.cli.main diagnose-script <input> [--unlabeled]
  [--speaker-map K=V,...] [--speaker-map-file PATH]
  [--expected-explainer まりさ] [--expected-listener れいむ]
  [--long-run-threshold N] [--listener-avg-ratio R]
  [--format text|json] [--strict]
```

- 入力は `validate` / `inspect` と同様（`.txt` / `.csv`）。
- **text**: 人間可読な行（`[WARNING] code (utt N): message` / `HINT: ...`）。
- **json**: `{"diagnostics": [...], "meta": {...}}` 形式。各診断は `code`, `severity`, `utterance_index`, `message`, `hint`。
- **strict**: `error` Severity が 1 件でもあれば exit 1。それ以外は 0。

## NLM 様式マーカー

実装は [src/pipeline/script_diagnostics.py](../src/pipeline/script_diagnostics.py) 内定数。誤検知・取りこぼしが出たら **そのファイルでリストを調整**する（本書はコードを正とする）。

## 関連

- C-09: [S1-script-refinement-prompt.md](S1-script-refinement-prompt.md)
- WORKFLOW の話者例: [WORKFLOW.md](WORKFLOW.md)
