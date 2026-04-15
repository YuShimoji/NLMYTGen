# H-01 Packaging Brief 生成 Prompt（委任正本）

**目的**: NotebookLM 台本ドラフト + トピック概要から、C-07 / C-08 / E-02 / H-03 / H-04 が参照する Packaging Orchestrator brief を 1 本生成する。

**位置づけ**: これは**別セッションの LLM / Custom GPT / user の GUI 作業**に渡すための Prompt 正本。既存 [CORE-PARALLEL-HUB §5 Prompt-D](../verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md#prompt-dh-01-brief-運用) の詳細版に当たる。

---

## Actor / Owner

- actor: `shared`（Custom GPT 固定 運用を推奨。別セッション assistant でも可）
- owner artifact: `docs/PACKAGING_ORCHESTRATOR_SPEC.md` 準拠の brief ファイル（Markdown または JSON）
- 入力の正本: NLM 生成直後の台本ドラフト + トピック概要
- 出力の保存先: 案件ごとに brief ファイル 1 本（例: `samples/<video_id>_brief.md`）

---

## 入力

1. 台本ドラフト（NLM 生成直後でよい。refined 前でも可）
2. トピック概要 1〜3 行
3. 想定視聴者の入口 1 行

## 実行コマンド（任意）

空の brief skeleton は CLI で出力できる。`uv run python -m src.cli.main emit-packaging-brief-template --format markdown -o samples/<video_id>_brief.md`（`--format json` で JSON skeleton）

---

## Prompt 本体（この枠内をそのままコピー）

```
あなたは NLMYTGen プロジェクトの Packaging Orchestrator です。
仕様は docs/PACKAGING_ORCHESTRATOR_SPEC.md v0.1 に準拠してください。

入力: 台本ドラフト（NLM 生成直後でも可）+ トピック概要
出力: docs/PACKAGING_ORCHESTRATOR_SPEC.md §4 に定義された brief
(Markdown または JSON。少なくとも以下を必須で含む)

必須フィールド:
- brief_version: "0.1"
- video_id
- topic_label
- target_viewer
- audience_hook
- title_promise
- thumbnail_promise
- novelty_basis (list)
- required_evidence (list[EvidenceItem])
- forbidden_overclaim (list)
- thumbnail_controls (object with: prefer_specificity, preferred_specifics,
                       banned_copy_patterns, rotation_axes)
- script_opening_commitment
- alignment_check (list)

制約:
- 具体性優先: 数値・年数・人数・割合・金額・固有名詞を
  thumbnail_controls.preferred_specifics に必ず 3 件以上。
- 抽象煽り（「驚愕」「衝撃」「闇」「やばい」「○○の真実」等）は
  thumbnail_controls.banned_copy_patterns に必ず列挙する。
- title_promise / thumbnail_promise / 台本 opening が同じ promise を共有しているかを
  alignment_check の yes/no 項目に明示。
- alignment_check の各項目は後続 consumer（C-07/C-08/H-03/H-04）が yes/no で
  評価できる文に整える。
- brief のみを出力。タイトル最終案・サムネコピー最終案・台本本文は出さない。

受理基準（docs/PACKAGING_ORCHESTRATOR_SPEC.md §8 に準拠）:
- title_promise が 1 文で、forbidden_overclaim を踏み越えない。
- thumbnail_controls.preferred_specifics が 3 件以上。
- thumbnail_controls.banned_copy_patterns が列挙されている。
- alignment_check に script 側の根拠（opening または body 前半で回収されるか）を
  yes/no で確認できる項目が含まれる。
- required_evidence の各 item に kind / value / why_it_matters / must_surface_in /
  status (strong|weak|missing) が揃う。
```

---

## 受理基準（operator 側セルフチェック）

- [ ] brief ファイルが Markdown または JSON で 1 本保存されている
- [ ] `preferred_specifics` に具体 3 件以上
- [ ] `banned_copy_patterns` 列挙あり
- [ ] `alignment_check` が yes/no で評価可能な形
- [ ] `required_evidence` の各 item が full field 揃い

## 参照

- [PACKAGING_ORCHESTRATOR_SPEC.md](../PACKAGING_ORCHESTRATOR_SPEC.md) — 仕様本体（§4 データモデル / §5 Markdown format / §8 受入基準）
- [CORE-PARALLEL-HUB §5 Prompt-D](../verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md)
- [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md) — C-08 側で brief を参照する側のプロンプト
