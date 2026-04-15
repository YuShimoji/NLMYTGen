# B-18 台本品質機械診断 Prompt（委任正本）

**目的**: 新規 NLM 台本に対して `diagnose-script` を実行し、診断コード別の warning/error 件数を P01 に記録する。**Block-A 通過済みの継続観測** として運用する。

**位置づけ**: 既存 [CORE-PARALLEL-HUB §5 Prompt-A](../verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md) の機械診断部分を詳細化した運用正本。[SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md](../SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md) と `diagnose-script` CLI に直結する。

---

## Actor / Owner

- actor: `assistant`（CLI 実行）
- owner artifact: `docs/verification/P01-phase1-operator-e2e-proof.md` のメモ列 1 行追記
- 改変範囲: 診断 JSON ファイル 1 件（`samples/<episode_id>_diag.json`）+ P01 の 1 行

**台本本文の書き換えはしない。** 診断のみ。修正が必要な場合は C-09 constrained rewrite（user 作業）にエスカレーションして停止する。

---

## 入力

1. 新規台本ファイル（`.txt` または `.csv`、通常は `samples/<episode_id>.txt`）
2. 期待話者ラベル（既定は `--expected-explainer まりさ` / `--expected-listener れいむ`）

## 実行コマンド

`src/cli/main.py` p_diag_script の argparse 実装と一致:

```
uv run python -m src.cli.main diagnose-script <path> \
  --format json \
  --expected-explainer まりさ \
  --expected-listener れいむ \
  > samples/<episode_id>_diag.json
```

追加オプション（必要時のみ）:
- `--long-run-threshold N`（既定 6。同一話者連続発話の上限）
- `--listener-avg-ratio R`（既定 1.25。guest/host 平均長の倍率閾値）
- `--speaker-map-file <path>`（2 話者以上のマッピング明示時）
- `--unlabeled`（マップ未指定で走らせる場合）

**`--strict` は付けない。** 件数のみ記録する（`--strict` はコア本開発の gate 用）。

---

## 抽出値

JSON 形式は `{"diagnostics": [...], "meta": {...}}`。各診断は `code` / `severity` / `utterance_index` / `message` / `hint` を持つ（`SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md` §CLI）。

観測対象の診断コード（v1、warning レベル）:

| code | 意味（要約） |
|---|---|
| `EXPLAINER_ROLE_MISMATCH` | host 役が expected_explainer と不一致 |
| `LISTENER_ROLE_MISMATCH` | guest 役が expected_listener と不一致 |
| `LISTENER_LONG_AVG_DOMINANCE` | guest 平均発話長が host の listener_avg_ratio 倍以上 |
| `NLM_STYLE_MARKER` | NLM/番組調フレーズに一致 |
| `LONG_RUN_SAME_SPEAKER` | 同一話者の連続発話が long_run_threshold 以上 |

`ERROR` severity は `--strict` 用であり本観測の対象外。

## P01 追記形式（メモ列）

既存 P01 表（5 列）のメモ列に次の 1 行情報を追記する。新規列は追加しない。

```
diagnose-script: warnings=<N>, errors=<N>, codes=[<list of triggered codes>]; diag=samples/<episode_id>_diag.json
```

追記例（P01 表の 1 行全体）:

```
| 2026-04-20 (`script_diag_<episode_id>_2026-04-20_a`) | samples/<episode_id>.txt | 未（診断のみ） | script_diagnostics（観測のみ） | diagnose-script: warnings=2, errors=0, codes=[EXPLAINER_ROLE_MISMATCH, LISTENER_LONG_AVG_DOMINANCE]; diag=samples/<episode_id>_diag.json |
```

warning 0 件の場合:

```
| 2026-04-20 (...) | samples/<episode_id>.txt | 未 | script_diagnostics（観測のみ） | diagnose-script: warnings=0, errors=0, codes=[]; diag=samples/<episode_id>_diag.json |
```

---

## 制約

- **台本本文の書き換え禁止**。warning が検出された場合は user に C-09 constrained rewrite を案内して停止する。
- **新しい diagnostic rule を提案しない**（仕様は `SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md` v1 で固定）。
- `--strict` を付けない（score 記録のみ）。
- `src/` / `tests/` 変更禁止。
- P01 表のスキーマ変更禁止。メモ列への 1 行追記のみ。

## 受理基準

- [ ] 診断 JSON ファイルが保存されている（`samples/<episode_id>_diag.json`）
- [ ] P01 表に 1 行追加されている
- [ ] メモ列に `warnings`, `errors`, `codes`, `diag=...` が揃っている
- [ ] 台本原文に手を入れていない（git diff で `samples/<episode_id>.txt` 無変更を確認）
- [ ] `src/` / `tests/` の差分なし

## 参照

- [SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md](../SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md) — 診断コード v1 / severity / CLI 仕様
- [P01-phase1-operator-e2e-proof.md](../verification/P01-phase1-operator-e2e-proof.md) — 追記先（メモ列に `diagnose-script=...` 実績あり）
- [CORE-PARALLEL-HUB §5 Prompt-A](../verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md)
- [src/cli/main.py](../../src/cli/main.py) `p_diag_script` — argparse 実装
