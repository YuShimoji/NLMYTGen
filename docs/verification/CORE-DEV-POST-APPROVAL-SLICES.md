# 承認後スライス — 実装ゲート手順（コア開発）

**原則**: [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) に **承認された項目だけ**をコードに反映する。ドラフトは [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)。

---

## 1. 現在の承認済みスライス

| ID / 名称 | 承認日 | 内容要約 | PR / コミット |
|-----------|--------|----------|----------------|
| **なし** | — | 2026-04-09 時点。ユーザー承認後に本表の行を追加する。 | — |

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

- 2026-04-09: 初版。承認済みスライスなしで開始。
