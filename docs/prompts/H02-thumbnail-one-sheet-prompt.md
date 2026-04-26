# H-02 / C-08 サムネ one-sheet 生成 Prompt（委任正本）

**目的**: H-01 Packaging brief + 台本の specificity 素材から、サムネイル 1 枚に載せるコピー / 表情 / 背景方向性をまとめた one-sheet を出力し、続く `score-thumbnail-s8` に流せる JSON payload まで揃える。

**位置づけ**: 既存 [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md) の拡張運用版。Specificity Ledger / Brief Compliance Check / Lane-E probe 連携が追加されている。

---

## Actor / Owner

- actor: `shared`（Custom GPT または別セッション LLM で生成 → user が YMM4 で作画）
- owner artifact: サムネ案 one-sheet（記録は `docs/verification/P03-thumbnail-one-sheet-proof.md` or 案件 verification に 1 ブロック）
- スコア記録: `score-thumbnail-s8` CLI の結果

---

## 入力

1. H-01 Packaging brief（上位制約）
2. 該当回の specificity 素材（`thumbnail_controls.preferred_specifics` の実値ソース）
3. 台本の `script_opening_commitment` 周辺テキスト

## 実行コマンド（採点時）

```
uv run python -m src.cli.main score-thumbnail-s8 \
  --scores '{"single_claim":2,"specificity":2,"title_alignment":2,"mobile_readability":2}' \
  --payload '{"run_id":"<run_id>","video_slug":"<video_slug>","output_file":"<thumb_path>"}' \
  --format json
```

- `--scores` 各 0..3（`docs/verification/LANE-E-S8-prep-2026-04-09.md` §入力契約）
- `total >= 80` かつ warning 0 件で `score-thumbnail-s8` は exit 0 を返す

---

## Prompt 本体（この枠内をそのままコピー）

```
あなたは NLMYTGen の Thumbnail Strategy v2 実行役 (H-02 / C-08) です。
仕様:
  - docs/THUMBNAIL_STRATEGY_SPEC.md v0.1
  - docs/THUMBNAIL_ONE_SHEET_WORKFLOW.md
  - docs/S8-thumbnail-copy-prompt.md
  - docs/verification/LANE-E-S8-prep-2026-04-09.md (Lane-E probe 入力契約)

入力:
  - Packaging brief (H-01 出力)
  - 該当回の specificity 素材 (preferred_specifics の実値ソース)

出力 (Markdown で以下を順に):
  1. キャッチコピー 5 案（各案に copy_family と strongest_evidence を付記）
  2. サブコピー 3 案
  3. 表情提案（れいむ / まりさ 各 1 つ以上、brief.rotation_axes.emotion_family に準拠）
  4. 背景方向性 1-2 案（brief.rotation_axes.layout_family / color_family に準拠）
  5. Specificity Ledger（5 案 × preferred_specifics の使用 / 未使用表）
  6. Brief Compliance Check（5 案 × promise 一致 Y/N + 理由）
  7. score-thumbnail-s8 payload (JSON)

制約:
  - brief.thumbnail_controls.preferred_specifics を 5 案中 3 案以上で使用する。
  - brief.thumbnail_controls.banned_copy_patterns を 1 件も使わない。
  - 固定テンプレ連打を避け、5 案で訴求軸を分散する
    （数値 / 比較 / 固有名詞 / 時系列 / 疑問 など）。
  - copy_family は 5 案間で少なくとも 3 家族以上カバーする。
  - 抽象煽り（「衝撃」「驚愕」「闇」「やばい」「○○の真実」等）を使わない。

Specificity Ledger フォーマット（Markdown 表）:
  | 案 | preferred_specifics 使用 | 未使用 | copy_family |
  |---|---|---|---|
  | 1 | 71.4%, タイム・オフ・タスク | 19億ドル | number_comparison |
  | 2 | ... | ... | ... |

Brief Compliance Check フォーマット（Markdown 表）:
  | 案 | promise 一致 | banned_copy_patterns 違反 | 理由 |
  |---|---|---|---|
  | 1 | Y | N | title_promise の 71.4% を直接載せている |
  | 2 | ... | ... | ... |

score-thumbnail-s8 payload (JSON 1 ブロック、docs/verification/LANE-E-S8-prep-2026-04-09.md
 §入力契約 に準拠):
  {
    "scores": {
      "single_claim":      <0-3>,
      "specificity":       <0-3>,
      "title_alignment":   <0-3>,
      "mobile_readability":<0-3>
    },
    "payload": {
      "run_id":     "<run_id>",
      "video_slug": "<video_slug>",
      "output_file":"<thumb_path>"
    }
  }
  各スコアは操作側が手動採点（0=不備, 3=強い）した暫定値を入れること。
  最終採点は operator が CLI 実行時に確定させる。

受理基準:
  - Specificity Ledger に 3 件以上のユニーク preferred_specific が登場
  - Brief Compliance Check で全案とも promise 一致 Y / banned_copy_patterns 違反 N
  - copy_family カバー 3 家族以上
  - score-thumbnail-s8 payload が `--scores` / `--payload` の双方に使える JSON として
    そのままコピペできる
```

---

## operator セルフチェック（出力受領後）

- [ ] 5 案すべてに copy_family と strongest_evidence が付いている
- [ ] Specificity Ledger に 3 件以上のユニーク preferred_specific
- [ ] Brief Compliance Check 全案 Y / violation N
- [ ] payload JSON をそのまま `score-thumbnail-s8 --scores ... --payload ...` に流せる
- [ ] YMM4 で作画後、`score-thumbnail-s8` 実行 → `docs/verification/P03-thumbnail-one-sheet-proof.md` に run_id / 出力パス / 判定を 1 ブロック追記

## 参照

- [THUMBNAIL_STRATEGY_SPEC.md](../THUMBNAIL_STRATEGY_SPEC.md)
- [THUMBNAIL_ONE_SHEET_WORKFLOW.md](../THUMBNAIL_ONE_SHEET_WORKFLOW.md)
- [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md) — ベース Prompt
- [verification/LANE-E-S8-prep-2026-04-09.md](../verification/LANE-E-S8-prep-2026-04-09.md) — Lane-E probe 契約・実行例
- [verification/P03-thumbnail-one-sheet-proof.md](../verification/P03-thumbnail-one-sheet-proof.md) — 運用記録先
- [runtime-state.md](../runtime-state.md) — 現在の主軸とメンテ層の優先順位
