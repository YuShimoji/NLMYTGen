# P2A — `origin/feat/phase2-motion-segmentation` ブランチレビュー

> **履歴注記（2026-04-以降）**: 以下の「一括マージしない」は **当時のリスク判断**である。のち **`feat/phase2-motion-segmentation` に `origin/master` をマージ**し、G-17 の `--motion-map`（`video_effect` 辞書）と Phase2 の **`--tachie-motion-map`**（配列台帳）を **CLI・実装で分離**した。現行の運用・正本は [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) と [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) の G-17 行を参照。

## 概要

- **ベース差分**: `master..origin/feat/phase2-motion-segmentation` は **1 コミット**（`bcfb1f0`）だが、`master` 対比で **約 38 ファイル / +3487 行** の大きな差分。
- **主な内容**（`git diff --stat` より）:
  - `src/pipeline/ymmp_patch.py` 大幅拡張（motion / transition 等のパッチ設計）
  - `tests/test_ymmp_motion_patch.py`, `test_ymmp_transition_patch.py`, `test_ymmp_bg_anim_patch.py` 追加
  - `docs/verification/G16-motion-patch-design.md`, `G15-transition-patch-design.md`, `G17-template-ir-patch-design.md` 等
  - B-11 系 workflow proof 文書・サンプル CSV、GUI（renderer/style/index）の大規模変更
  - `packaging_brief_template.py`、IR capability matrix、FEATURE_REGISTRY 変更
  - `samples/v4_re.ymmp` 等

## マージ判断（推奨）

| 観点 | 評価 |
|------|------|
| **現行 master との整合** | 現行 master には B-18/C-09 等が先行マージ済み。**そのまま fast-forward マージはコンフリクト大量・レビュー不能リスクが高い**。 |
| **FEATURE_REGISTRY** | ブランチ側で G 系・B 系の記述が動いている。取り込む場合は **台帳を正として差分を再整理**し、`proposed`→承認の流れを崩さないこと。 |
| **価値** | motion/transition/bg_anim の **設計ドキュメント + テスト**は Phase 2 の方向性と一致。コードは **小さなパケットに分割して cherry-pick / 再実装**する方が安全。 |

**結論（本レビュー）**: **現時点では master へ一括マージしない。** 必要な機能は

1. 設計 md（G15/G16/G17）を参照しつつ、
2. 現行 `ymmp_patch.py` / `validate-ir` / `FEATURE_REGISTRY` に合わせて **別スライスで再適用**する。

次のアクション例: G-16 の一部のみを新規 FEATURE ID で `approved` → テスト付きで段階マージ。

## 参照コマンド

```bash
git fetch origin
git log master..origin/feat/phase2-motion-segmentation --oneline
git diff master...origin/feat/phase2-motion-segmentation --stat
```
