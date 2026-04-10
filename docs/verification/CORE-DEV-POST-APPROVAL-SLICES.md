# 承認後スライス — 実装ゲート手順（コア開発）

**原則**: [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) に **承認された項目だけ**をコードに反映する。ドラフトは [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)。

---

## 1. 現在の承認済みスライス


| ID / 名称 | 承認日 | 内容要約 | PR / コミット |
|-----------|--------|----------|----------------|
| CORE-RETURN-DOCSYNC | 2026-04-09 | コア復帰準備スライス。P2/S6 再判定（見え方一行 + §2の5条件）反映、フル回帰結果反映、`runtime-state` の next_action を実装着手可能状態へ更新。 | local docs sync（このブロック） |
| T1-P2-DOCSAMPLE | 2026-04-11 | [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) §2.1: P2 段階投入向け **verification 手順 1 本 + 期待ログ**、および **IR/設定サンプル JSON**（[PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) と矛盾なし）。FEATURE_REGISTRY 新規行なし。正本: [T1-P2-DOCSAMPLE-p2-staged-rollout-mechanical-proof.md](T1-P2-DOCSAMPLE-p2-staged-rollout-mechanical-proof.md)。 | `8c12391`（`docs: T1-P2-DOCSAMPLE 機械検証パック（P2 overlay/se/bg_anim）`） |
| T1-RUNBOOK-GUI | 2026-04-11 | 同ドラフト §2.2: [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) と GUI 導線（[gui-llm-setup-guide.md](../gui-llm-setup-guide.md) 等）の **文言・手順の明確化**のみ。新タブ・F-01/F-02 復活は禁止。 | `72f9ff2`（`docs: T1-RUNBOOK-GUI（runbook↔gui 用語・導線の明確化）`） |
| **File6-2026-04-10-01（承認後スライス移行準備）** | 2026-04-10 | `CORE-DEV-LANE-PROMPT-QUICKREF.md` の File6 指示に基づき、承認記録の反映と `master` 起点トピックブランチでの実装準備を開始。承認ソース: 本チャット指示「File6 の承認後スライスを進めてください。承認記録を反映し、master起点トピックブランチで実装準備を開始してください。」。`origin/master` 同期後のフル回帰は `313 passed`（2026-04-11、`runtime-state.md` 参照）。 | `topic/file6-post-approval-prep-2026-04-10` |

---

## 2. 承認からマージまでのチェックリスト（1 スライスごと）

1. [ ] [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) の該当スライスにユーザーが **明示承認**（チャットまたは issue へのリンクを §1 表に貼る）。
2. [ ] [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) を更新（`proposed` → `approved` → 実装後 `done` の遷移を守る）。
3. [ ] 実装ブランチは `**master` 起点のトピックブランチ**を使用。
4. [ ] 実装は **縦スライス 1 本**（一括マージしない。[P2A-phase2-motion-segmentation-branch-review.md](P2A-phase2-motion-segmentation-branch-review.md) の精神）。
5. [ ] `NLMYTGEN_PYTEST_FULL=1 uv run pytest` が緑（フル回帰必須）。
6. [ ] [runtime-state.md](../runtime-state.md) の「最終検証」日付・必要なら `last_change_relation` を更新。
7. [ ] Gate 別の参照:
  - **Gate A**: B-17 周辺・再現コーパス・テストを同じ PR に。
  - **Gate B**: まず runbook / GUI 文言。コードが要る場合のみ台帳に ID。
  - **Gate C**: 運用文書優先。コードは診断・validate の **バグ修正**に限定。

---

## 3. 承認なしでやってよいこと（再掲）

- 回帰テストの実行・既存テストの修正。  
- オペレータ入力のマージレビュー（[CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)）。  
- 本ファイル §1 表の **承認行の追記**（メタのみ）。

---

## 4. 変更履歴

- 2026-04-10: **T1-RUNBOOK-GUI 完了**。[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) に用語正本・T1-P2 導線・汎用 `cd` 例を追加。[gui-llm-setup-guide.md](../gui-llm-setup-guide.md) にトラック A との対応と Electron 節の runbook 参照を追記。コード・新タブなし。`NLMYTGEN_PYTEST_FULL=1 uv run pytest` 緑。
- 2026-04-10: **T1-P2-DOCSAMPLE 完了**。[T1-P2-DOCSAMPLE-p2-staged-rollout-mechanical-proof.md](T1-P2-DOCSAMPLE-p2-staged-rollout-mechanical-proof.md) を正本化し、[PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) §6 に導線を追加。`NLMYTGEN_PYTEST_FULL=1 uv run pytest` 緑。§2 のうち FEATURE 更新は該当なし（ドキュメントのみ）。`runtime-state` の最終検証日付は T1 完了後の T3 または本スライス後の handoff で更新する。
- 2026-04-11: T0 承認に基づき `T1-P2-DOCSAMPLE` / `T1-RUNBOOK-GUI` を起票（フェーズ T1 用）。
- 2026-04-09: `CORE-RETURN-DOCSYNC` を追加（コア復帰判定の承認後スライスとして起票）。
- 2026-04-10: File6 承認記録（移行準備）を §1 に追加。`topic/file6-post-approval-prep-2026-04-10` を起票。
- 2026-04-10: §2 に `master` 起点トピックブランチとフル回帰必須を明記。
- 2026-04-09: 初版。承認済みスライスなしで開始。

---

## 5. File6-2026-04-10-01 進捗メモ

- [x] ユーザー明示承認を §1 に反映（本チャット指示）
- [x] `master` 起点トピックブランチを作成（`topic/file6-post-approval-prep-2026-04-10`）
- [x] 判定入力（P2/S6 2行）を正本間で整合
- [x] 条件4/5 の先行入力証跡を記録（`P2-CONDITION45-PRECHECK-TEMPLATE.md`）
- [x] FEATURE_REGISTRY の実装前提を確認（現時点の `approved` は H-01。未承認拡張は起票しない）
- [x] `NLMYTGEN_PYTEST_FULL=1 uv run pytest` 実行結果を反映（2026-04-10、`301 passed`）
- [x] 実装着手判定を最終確定（`OPEN 継続`。`YMM4見え方=NG` / `S6§2(5条件)=未充足` のため READY 条件未達）