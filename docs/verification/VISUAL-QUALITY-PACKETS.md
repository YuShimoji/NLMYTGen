# 画面演出クオリティ運用パケット（bg_anim / overlay）

目的: コア本開発レーンで、演出ごとの達成を機械的に判定する。
対象は `bg_anim`（A1-A4）と `overlay`（B1-B4）に限定する。

---

## 1. 共通運用

- 判定は **スコア + チェックリスト**の両方で行う。
- スコアは 0-3（0=不可, 1=弱い, 2=実用, 3=強い）。
- **PASS 条件**:
  - タスク対象カテゴリが `>=2`
  - かつ必須チェック項目が全て `yes`
- **NEEDS_FIX 条件**:
  - 上記のいずれかを満たさない

提出フォーマット（JSON 例）:

```json
{
  "run_id": "bg_a1_2026-04-09_x",
  "task_id": "A1",
  "scores": {
    "target_quality": 2,
    "readability": 2,
    "timing_fit": 2,
    "stability": 3
  },
  "checklist": {
    "route_consistent": true,
    "no_abrupt_jump": true,
    "no_layer_conflict": true
  },
  "result": "pass",
  "notes": "..."
}
```

---

## 2. bg_anim パケット（A1-A4）

### A1 切替品質

- 目的: セクション開始/終了の違和感を除去
- 必須チェック:
  - `route_consistent`
  - `no_abrupt_jump`
  - `section_boundary_intent_match`

### A2 速度品質

- 目的: 速すぎ・遅すぎ・停滞を回避
- 必須チェック:
  - `speed_is_readable`
  - `no_excess_stillness`
  - `pace_matches_script`

### A3 意図一致

- 目的: 台本の感情/論点に背景演出が一致
- 必須チェック:
  - `tone_match`
  - `topic_match`
  - `no_contradicting_visual`

### A4 失敗クラス監視

- 目的: `BG_ANIM_*` / `TRANSITION_*` を見逃さない
- 必須チェック:
  - `no_bg_anim_failure_class`
  - `no_transition_failure_class`
  - `dry_run_exit_zero`

---

## 3. overlay パケット（B1-B4）

### B1 可読性

- 目的: 小画面で読める情報量と配置
- 必須チェック:
  - `text_legible_mobile`
  - `font_contrast_ok`
  - `no_text_overflow`

### B2 情報密度

- 目的: 情報過多/不足を回避
- 必須チェック:
  - `one_overlay_one_claim`
  - `not_overloaded`
  - `has_concrete_anchor`

### B3 タイミング一致

- 目的: 発話論点と表示タイミングの同期
- 必須チェック:
  - `appears_on_topic`
  - `disappears_without_lag`
  - `no_topic_drift`

### B4 レイヤ競合

- 目的: 立ち絵・背景との重なり不具合を除去
- 必須チェック:
  - `no_character_occlusion`
  - `no_key_info_occlusion`
  - `safe_area_respected`

---

## 4. 並行実行 Prompt（即実行）

以下の箇条書きは **evergreen の依頼テンプレ**である。個々のパケットが PASS したか・コアが採用したかは、[CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)（ファイル2）や本リポジトリに残した JSON 証跡・`runtime-state.md` で判断する。テンプレは完了しても削除しない。

- Prompt-Bg-A1:
  - 「ファイル6のレーンCを進めてください。bg_animのA1（切替品質）だけ実施し、`VISUAL-QUALITY-PACKETS` のJSON形式で提出してください。」
- Prompt-Bg-A2:
  - 「ファイル6のレーンCを進めてください。bg_animのA2（速度品質）だけ実施し、PASS/NEEDS_FIXを提出してください。」
- Prompt-Bg-A3:
  - 「ファイル6のレーンCを進めてください。bg_animのA3（意図一致）だけ実施し、論点一致の証跡を提出してください。」
- Prompt-Bg-A4:
  - 「ファイル6のレーンCを進めてください。bg_animのA4（失敗クラス監視）だけ実施し、`BG_ANIM_*`/`TRANSITION_*` の発生有無を提出してください。」
- Prompt-Ov-B1:
  - 「ファイル6のレーンCを進めてください。overlayのB1（可読性）だけ実施し、小画面可読判定を提出してください。」
- Prompt-Ov-B2:
  - 「ファイル6のレーンCを進めてください。overlayのB2（情報密度）だけ実施し、過不足判定を提出してください。」
- Prompt-Ov-B3:
  - 「ファイル6のレーンCを進めてください。overlayのB3（タイミング一致）だけ実施し、同期証跡を提出してください。」
- Prompt-Ov-B4:
  - 「ファイル6のレーンCを進めてください。overlayのB4（レイヤ競合）だけ実施し、遮蔽/重なりの有無を提出してください。」

---

## 5. コア受け入れ

コアは [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) に従い、
各パケットを個別判定して **PASS のみ** [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) に反映する。