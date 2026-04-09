# Packaging Orchestrator Brief

> H-01 用の空テンプレ。仕様は [docs/PACKAGING_ORCHESTRATOR_SPEC.md](../docs/PACKAGING_ORCHESTRATOR_SPEC.md)。動画ごとに複製し `video_id` をファイル名に含めてよい。

- brief_version: "0.1"
- video_id: (例: topic_slug_2026-04-09)
- topic_label:
- target_viewer:
- audience_hook:
- title_promise:
- thumbnail_promise:

## novelty_basis

- （この動画が「見慣れた話」ではなくなる根拠を列挙）

## required_evidence

- kind: number | named_entity | anecdote | case | study | freshness
  value:
  why_it_matters:
  must_surface_in:
    - thumbnail | opening | body | metadata
  status: confirmed | weak | missing

## missing_or_weak_evidence

- （任意。弱い根拠があれば列挙）

## forbidden_overclaim

- （タイトル・サムネ・台本が言ってはいけない盛り方）

## thumbnail_controls

- prefer_specificity: true
- preferred_specifics:
  - （サムネに載せやすい具体項目）
- banned_copy_patterns:
  - （抽象煽りの禁止パターン）
- rotation_axes:
  - layout_family:
  - emotion_family:
  - color_family:
  - copy_family:

## script_opening_commitment

- （導入で早めに回収すべき根拠や約束）

## must_payoff_by_section

- （任意。section ごとの回収約束）

## alignment_check

- （後続 consumer が yes/no で見る整合チェック項目）

## consumer_hints

- for_c07:
- for_c08:
- for_e02:
- for_h04:
- for_h03:
