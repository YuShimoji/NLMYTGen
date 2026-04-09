# 承認後スライス — 実装ゲート手順（コア開発）

**原則**: [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) に **承認された項目だけ**をコードに反映する。ドラフトは [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)。

---

## 1. 現在の承認済みスライス


| ID / 名称 | 承認日 | 内容要約 | PR / コミット |
| ------- | --- | --- | --------- |
| **File6-2026-04-10-01（承認後スライス移行準備）** | 2026-04-10 | `CORE-DEV-LANE-PROMPT-QUICKREF.md` の File6 指示に基づき、承認記録の反映と `master` 起点トピックブランチでの実装準備を開始。承認ソース: 本チャット指示「File6 の承認後スライスを進めてください。承認記録を反映し、master起点トピックブランチで実装準備を開始してください。」。回帰: `NLMYTGEN_PYTEST_FULL=1 uv run pytest` = `301 passed`。判定: OPEN 継続。 | `topic/file6-post-approval-prep-2026-04-10` |


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