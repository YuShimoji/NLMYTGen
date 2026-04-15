# B-1 e2e_test 回帰 proof (2026-04-16)

**ブロック**: B-1 (実案件投入 sequential の 1 段目、assistant 単独)
**対象**: [samples/e2e_test/](../../samples/e2e_test/)
**目的**: e2e_test 既成 registry・IR が現行 `apply-production` で通るかを機械確認し、pipeline の健全性と drift を検出する。

## 結論: **observational close — pipeline は drift を正しく捕捉**

e2e_test の legacy ファイルは現行仕様と 2 箇所で drift しており、`apply-production` が両方を failure class として止めた。これは regression test の**正しい挙動**(pipeline が drift を前向きに検出している)。B-3 へ進行可。

---

## 入力

| ファイル | 内容 |
|---|---|
| ymmp | `samples/e2e_test/result.ymmp` (TachieItem 7 / VoiceItem 11 / ImageItem 1) |
| IR | `samples/e2e_test/ir.json` (11 utterance、2 speaker (marisa/reimu)、7 face label、row_range 未指定) |
| face_map | `samples/e2e_test/face_map.json` (7 label、非 character-scoped) |
| bg_map | `samples/e2e_test/bg_map.json` (studio_blue / dark_board) |

## 実行

```
uv run python -m src.cli.main apply-production \
  samples/e2e_test/result.ymmp samples/e2e_test/ir.json \
  --face-map samples/e2e_test/face_map.json \
  --bg-map samples/e2e_test/bg_map.json \
  --dry-run --format json
```

### Run 1 (原 IR) — exit 1
- **ERROR: PROMPT_FACE_DRIFT** — `neutral` label (IR で 2 回使用) が prompt contract の 6 ラベル (angry/sad/serious/smile/surprised/thinking) に無い
- Validation FAILED、patch 前に停止

### Run 2 (patched IR、neutral → serious に置換、probe のみ) — exit 1
- **FATAL: VOICE_NO_TACHIE_FACE** — VoiceItem index 1, 2, 9, 10 に TachieFaceParameter 無し
- result.ymmp は立ち絵表示チュートリアル型で、全 VoiceItem が TachieFaceParameter を持たない構造

### 観測値 (Run 2)
| 項目 | 値 |
|---|---|
| face_changes | 1 (4 件は VOICE_NO_TACHIE_FACE で skip、1 件のみ成功) |
| transition_changes | 11 |
| bg_added | 4 |
| bg_removed | 1 |
| fatal_warnings | 4 (VOICE_NO_TACHIE_FACE × 4) |

## 検出された failure class

1. **PROMPT_FACE_DRIFT** (ERROR)
   - e2e_test/ir.json が `neutral` を使用
   - prompt contract ([docs/S6-production-memo-prompt.md](../S6-production-memo-prompt.md)) は 6 label のみ
   - **原因**: e2e_test が古い設計で、prompt contract 確立前に `neutral` を採用していた
   - **補足**: WARNING `FACE_PROMPT_PALETTE_EXTRA: palette label 'neutral' is not listed in prompt contract` も同時発生

2. **VOICE_NO_TACHIE_FACE** (FATAL)
   - result.ymmp の VoiceItem 11 件中 4 件に TachieFaceParameter 無し
   - index 1 (Serif: 「魔理沙の立ち絵を表示します。」) はナレーター的 VoiceItem
   - **原因**: result.ymmp は YMM4 立ち絵表示のチュートリアル ymmp 的な構造で、全 VoiceItem が TachieItem に紐付いていない
   - **補足**: BG_SPAN_OVERLAP (utterance index=10 section=S3) も同時検出

## 判定

- **e2e_test は regression input として現状使用不可**
- pipeline は正しく drift を捕捉 → **pipeline 健全性: OK**
- e2e_test を復活させるなら:
  - ir.json の `neutral` → 現行 6 label のいずれかに置換
  - result.ymmp を全 VoiceItem が TachieFaceParameter を持つ ymmp に差し替え
  - もしくは e2e_test 自体を **archived 扱い**にし、回帰には production.ymmp + Part 1+2IR_row_range.json を正本とする(実質 B-3 が回帰を兼ねる)

## 推奨方針

**e2e_test を archived とする**。理由:
- production.ymmp + Part 1+2IR_row_range.json が既に完全な回帰実績 (B-3 で確認予定)
- 古い e2e_test を維持するコストが retry loop のリスクを生む
- 2 つの failure class は新規 drift ではなく既知の legacy 問題

## 成果物

- `samples/_probe/b1/dry_run.json` (Run 1 出力、PROMPT_FACE_DRIFT 検出)
- `samples/_probe/b1/dry_run_patched.json` (Run 2 出力、VOICE_NO_TACHIE_FACE 検出)
- `samples/_probe/b1/ir_patched.json` (probe のみの patched IR、原 e2e_test は未変更)
- `samples/_probe/b1/stderr.log` / `stderr_patched.log`

## 次アクション

**B-3 に進む**。B-3 は production.ymmp + Part 1+2IR_row_range.json + face_map.json で 2026-04-13 の CHABANGEKI proof の再現を確認する。e2e_test の archived 化判断は B-3 完了後に user に提案。

## 関連

- [FAILURE_DIAGNOSIS_MATRIX.md](FAILURE_DIAGNOSIS_MATRIX.md) — `PROMPT_FACE_DRIFT` / `VOICE_NO_TACHIE_FACE` / `BG_SPAN_OVERLAP` の診断
- [INVARIANTS.md](../INVARIANTS.md) — failure class で止める規律
