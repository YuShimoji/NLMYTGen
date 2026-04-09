# 次期実装プラン（ドラフト）— B-11 Gate 取り込み後・承認前

**ステータス**: ドラフト（**ユーザー承認までは実装しない**）。入力: [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) §3。受け入れ記録: [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)。

---

## 1. B-11 からの確定事項

| 項目 | 内容 |
|------|------|
| **Gate** | **B**（運用摩擦支配 → 運用側へ移行） |
| **根拠要約** | 4 区分は全編通しで 0 件。顕著な改行・辞書修正なし。overflow 機械候補は残存（監視対象）。 |
| **次投資先（オペレータ記述）** | 背景アニメを 1〜2 セクションで小規模適用し、route と見え方確認。F-01/F-02 は quarantined 維持。 |

---

## 2. コア開発での解釈（投資の割り当て）

Gate B の「運用導線・記録」に合わせ、**次の優先**を推奨する（実装は承認後）。

1. **P2 背景演出（ドキュメント＋registry 整備が中心）**  
   - 既存 CLI（`apply-production` / `patch-ymmp`、G-15〜G-17）は `done`。  
   - コアは **オペレータが [S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md) §2 の 5 条件を埋めたうえで**、実案件 IR の段階投入を支援する **verification 手順・サンプル JSON** の追補に留める。  
   - **新規 FEATURE ID を増やす必要が出た場合のみ** §3 の台帳案を発行し、承認後に実装。

2. **GUI / runbook**  
   - 既存タブ・[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) の改善は **文言・手順の明確化**に限定（新タブや F-01/F-02 相当は **quarantined のまま**。[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) F 節の再審査ゲート必須）。

3. **Gate A（改行）向けの L2 変更**  
   - 本 B-11 結果では **優先度低**。別案件で Gate A が出たら [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) に従い B-17 周辺の縦スライスを別ドラフト化する。

---

## 3. FEATURE_REGISTRY 変更案（承認待ち）

**現時点の提案: 台帳に新規行を追加しない**（ドキュメント・サンプルのみの想定）。

承認時にユーザーが「コード変更スライス」を明示した場合の **記入テンプレ**（採用した行だけ残す）:

| ID | 変更種別 | 提案ステータス | スコープ一行 | 境界（AUTOMATION_BOUNDARY） |
|----|----------|----------------|-------------|----------------------------|
| （例 B-xx または 新ID） | 追加 / 更新 | `proposed` → 承認後 `approved` | （例）build-csv の特定 overflow 緩和 | L2 のみ、画像・ymmp 生成なし |
| （未使用なら削除） | | | | |

---

## 4. 検証の出し方（承認後スライスごと）

- **最小**: `NLMYTGEN_PYTEST_FULL=1 uv run pytest` 緑。  
- **CLI 変更**: 既存 `tests/test_pipeline_smoke.py` パターンに **1 ケース**追加するか、該当モジュールの単体テスト。  
- **ドキュメントのみ**: verification に **手順と期待ログ 1 ブロック**。  
- **IR / ymmp**: [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) と矛盾しないこと。

---

## 5. 次のアクション

1. ユーザーが本ドラフトの §2〜§3 を **承認または差し替え**。  
2. 承認後、[CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) に **承認済みスライス**を記入し、PR を分割実装。  
3. P2 の YMM4 見え方・S6 §2 が揃うまで、**registry を広げるコード変更は起票しない**（チェックリスト OPEN 扱い）。

---

## 6. 変更履歴

- 2026-04-09: 初版。Gate B 確定版に基づくドラフト。
