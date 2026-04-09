# 次期実装プラン（ドラフト）— B-11 Gate 取り込み後・承認前

**ステータス**: ドラフト（**ユーザー承認までは実装しない**）。入力: [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) §3。受け入れ記録: [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)。

---

## 1. B-11 からの確定事項


| 項目                | 内容                                                               |
| ----------------- | ---------------------------------------------------------------- |
| **Gate**          | **B**（運用摩擦支配 → 運用側へ移行）                                           |
| **根拠要約**          | 4 区分は全編通しで 0 件。顕著な改行・辞書修正なし。overflow 機械候補は残存（監視対象）。              |
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


| ID               | 変更種別    | 提案ステータス                     | スコープ一行                       | 境界（AUTOMATION_BOUNDARY） |
| ---------------- | ------- | --------------------------- | ---------------------------- | ----------------------- |
| （例 B-xx または 新ID） | 追加 / 更新 | `proposed` → 承認後 `approved` | （例）build-csv の特定 overflow 緩和 | L2 のみ、画像・ymmp 生成なし      |
| （未使用なら削除）        |         |                             |                              |                         |


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
4. P0 は [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) の `p0_nextcycle_amazon_2026-04-10_a` を基準に継続し、YMM4 読込結果はオペレータ追記を待って判定を確定する。

### 5.3 起票ゲート（OPEN / READY）

- **OPEN の間**: コードスライスは起票しない（ドキュメント・ログ整備のみ許可）。
- **READY 到達時のみ**: [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) に承認済みスライスを起票し、トピックブランチで実装へ進む。
- 判定根拠は [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) の P2/S6 行を単一正本とする。

### 5.1 OPEN / READY 判定（分岐C）

- 判定入力は [P2-READY-INPUT-TEMPLATE.md](P2-READY-INPUT-TEMPLATE.md) の 2 行を使用。
- YMM4 実測後の更新手順は [P2-READY-INPUT-TEMPLATE.md](P2-READY-INPUT-TEMPLATE.md) §4.1 を使用（1 行更新で再判定）。
- **READY** に昇格する条件:
  - `YMM4見え方 = OK`
  - `S6§2(5条件) = 充足`
- 条件を満たさない場合は **OPEN 継続**（コード変更なし）。

### 5.2 先行実行パケット（YMM4 未確認でも進める）

目的: P2 判定を止めず、`READY` 手前までを先に完了する。

1. **条件4ログ収集（機械判定）**
  - 候補コマンド（いずれか）:
    - `uv run python -m src.cli.main apply-production samples/production.ymmp samples/p2_overlay_se_ir.json --palette samples/palette.ymmp --csv samples/reflow.csv --dry-run`
    - `uv run python -m src.cli.main measure-timeline-routes samples/production.ymmp --expect --profile production_ai_monitoring_lane`
  - 期待: exit 0 と、failure class が出た場合の内容が記録されていること。
  - 実績（2026-04-10）: `measure-timeline-routes ... --expect samples/timeline_route_contract.json --profile production_ai_monitoring_lane` を実行し exit `0`。記録先: [P2-CONDITION45-PRECHECK-TEMPLATE.md](P2-CONDITION45-PRECHECK-TEMPLATE.md)。
2. **条件5接続点の記録**
  - `docs/OPERATOR_WORKFLOW.md` と `docs/S6-background-animation-next-step-plan-prep.md` を参照し、接続点を 1 行で記入。
  - 記入例: `接続点: CSV 生成後の production.ymmp に apply-production を適用し、YMM4 で見え方確認へ接続`
3. **P2/S6 観測 2 行の暫定入力**
  - [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) に暫定 2 行を先行記入。
  - YMM4 実測が可能になった時点で 1 行目のみ差し替え、再判定する。

このパケットは承認不要の文書・ログ整備に限定し、コードスライス起票はしない。

---

## 6. 変更履歴

- 2026-04-10: §5.2 条件4ログの最新実績（exit 0）を追記。
- 2026-04-10: §5.1 追加。分岐Cの OPEN/READY 判定条件を明文化。
- 2026-04-10: P0 次サイクル実行（Amazon・CLI）を次アクションへ反映。P2 は OPEN 条件維持。
- 2026-04-09: 初版。Gate B 確定版に基づくドラフト。