# 承認後スライス — 実装ゲート手順（コア開発）

**原則**: [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) に **承認された項目だけ**をコードに反映する。ドラフトは [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)。

---

## 1. 現在の承認済みスライス

| ID / 名称 | 承認日 | 内容要約 | PR / コミット |
|-----------|--------|----------|----------------|
| CORE-RETURN-DOCSYNC | 2026-04-09 | コア復帰準備スライス。P2/S6 再判定（見え方一行 + §2の5条件）反映、フル回帰結果反映、`runtime-state` の next_action を実装着手可能状態へ更新。 | local docs sync（このブロック） |
| T1-P2-DOCSAMPLE | 2026-04-11 | [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) §2.1: P2 段階投入向け **verification 手順 1 本 + 期待ログ**、および **IR/設定サンプル JSON**（[PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) と矛盾なし）。FEATURE_REGISTRY 新規行なし。 | `927588e`: [T1-P2-staged-bg-anim-verification.md](T1-P2-staged-bg-anim-verification.md) + [p2_staged_bg_anim_verification.bundle.json](../../samples/p2_staged_bg_anim_verification.bundle.json) |
| T1-RUNBOOK-GUI | 2026-04-11 | 同ドラフト §2.2: [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) と GUI 導線（[gui-llm-setup-guide.md](../gui-llm-setup-guide.md) 等）の **文言・手順の明確化**のみ。新タブ・F-01/F-02 復活は禁止。 | runbook トラック C 補足・最短チェックリスト、`gui-llm-setup-guide` CLI ゲート節、`LANE-B-gui-llm-sync-checklist` B-3 注記 |

---

## 2. 承認からマージまでのチェックリスト（1 スライスごと）

1. [ ] [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) の該当スライスにユーザーが **明示承認**（チャットまたは issue へのリンクを §1 表に貼る）。
2. [ ] [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) を更新（`proposed` → `approved` → 実装後 `done` の遷移を守る）。
3. [ ] 実装は **縦スライス 1 本**（一括マージしない。[P2A-phase2-motion-segmentation-branch-review.md](P2A-phase2-motion-segmentation-branch-review.md) の精神）。
4. [ ] `NLMYTGEN_PYTEST_FULL=1 uv run pytest` が緑。
5. [ ] [runtime-state.md](../runtime-state.md) の「最終検証」日付・必要なら `last_change_relation` を更新。
6. [ ] Gate 別の参照:
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

- 2026-04-11: T0 承認に基づき `T1-P2-DOCSAMPLE` / `T1-RUNBOOK-GUI` を起票（フェーズ T1 用）。
- 2026-04-09: `CORE-RETURN-DOCSYNC` を追加（コア復帰判定の承認後スライスとして起票）。
- 2026-04-09: 初版。承認済みスライスなしで開始。
