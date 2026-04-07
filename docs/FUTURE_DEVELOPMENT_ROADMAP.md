# 今後の開発ロードマップ（repo 正本）

設計方針の詳細は [runtime-state.md](runtime-state.md) の開発プラン節、[USER_REQUEST_LEDGER.md](USER_REQUEST_LEDGER.md)、[AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md) を参照。このファイルは **G-15〜G-18 の承認ゲート**と **推奨検討順**を固定する。

**更新（2026-04）**: `feat/phase2-motion-segmentation` 上で **master とのマージ・コンフリクト解消済み**。P2A にあった「一括マージ回避」方針は、**分割マージ相当の作業が完了**した旨を [P2A](verification/P2A-phase2-motion-segmentation-branch-review.md) 冒頭注記に残している。以降の motion 系 CLI は [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md) を正とする。

---

## G-15〜G-18 の承認ルール

- **2026-04-07 承認済み**。[FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) では **G-15〜G-18 は `done`**（G-18 は [samples/AudioItem.ymmp](samples/AudioItem.ymmp) readback 後に実装完了）。
- **G-18** は [G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md) を正本とする（旧ゲート記録は [P2C](verification/P2C-se-audioitem-boundary.md)）。
- 各 ID は **verification 1 本**（仕様・failure class・readback 前提）を正本とする。

---

## 推奨検討順（痛点・ゲート優先）


| 順   | ID       | 推奨する理由                                        | ゲート / 保留条件                                                                                                                              |
| --- | -------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **G-15** | 資料パネル等で `macro.sections` 細分割が運用上辛いかが最初に判明しやすい | まず **セクション分割で背景を切る**運用を試し、それでも痛いと判断したら仕様（`default_bg` との優先順位）を書いてから承認を仰ぐ                                                                |
| 2   | **G-18** | SE はインパクトが大きいが **write JSON パス**が要る           | **実装済み**（2026-04-07）。[samples/AudioItem.ymmp](samples/AudioItem.ymmp) + [G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md)。YMM4 版差が出たら readback のみ再確認 |
| 3   | **G-16** | IR スキーマ拡張の影響が大きい                              | **単一 overlay + 合成 PNG**（[VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md)）で足りないことが運用上明文化されてから                                          |
| 4   | **G-17** | G-12 contract 済み。プロファイル限定で motion/transition/bg_anim を書き込み                    | 実装・台帳は [G17-motion-adapter-packet.md](verification/G17-motion-adapter-packet.md)。Phase2（`--tachie-motion-map`）との分岐はマトリクス参照 |


---

## 承認記録（ユーザー追記用）


| ID   | 承認日        | メモ  |
| ---- | ---------- | --- |
| G-15 | 2026/04/07 |     |
| G-16 | 2026/04/07 |     |
| G-17 | 2026/04/07 |     |
| G-18 | 2026/04/07 |     |


---

## 関連ドキュメント

- Phase 1 運用 E2E: [verification/P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md)、[OPERATOR_PARALLEL_WORK_RUNBOOK.md](OPERATOR_PARALLEL_WORK_RUNBOOK.md)
- motion ブランチ: [verification/P2A-phase2-motion-segmentation-branch-review.md](verification/P2A-phase2-motion-segmentation-branch-review.md)

## feat/phase2-motion-segmentation

**完了扱い（開発プラン 2026-04）**: ブランチ上で master を取り込み、G-17 / Phase2 / micro bg / G-14 キーフレームを統合済み。残作業は **master への PR マージ**と運用実証（workflow proof）。P2A 本文は歴史的判断として保持。