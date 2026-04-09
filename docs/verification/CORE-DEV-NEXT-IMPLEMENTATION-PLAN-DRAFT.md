# 次期実装プラン（ドラフト）— B-11 Gate 取り込み後・承認前

**ステータス**: ドラフト（**ユーザー承認までは実装しない**）。入力: [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) §3。受け入れ記録: [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)。
**反映ルール**: 本書に反映してよいのは **PASS 判定入力のみ**（NEEDS_FIX は差し戻し後に再審査）。

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
   - [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) の 2026-04-09 再判定で、P2/S6 は「見え方一行（NG）+ §2 の5条件」を満たして PASS 化済み。  
   - コアは実案件 IR の段階投入を支援する **verification 手順・サンプル JSON** の追補を先行し、実装拡張が必要な場合のみ §3 の台帳案を発行する。

2. **GUI / runbook**  
   - 既存タブ・[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) の改善は **文言・手順の明確化**に限定（新タブや F-01/F-02 相当は **quarantined のまま**。[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) F 節の再審査ゲート必須）。

3. **Gate A（改行）向けの L2 変更**  
   - 本 B-11 結果では **優先度低**。別案件で Gate A が出たら [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) に従い B-17 周辺の縦スライスを別ドラフト化する。

---

## 3. FEATURE_REGISTRY 変更案（承認待ち）

**現時点の提案: 台帳に新規行を追加しない**（ドキュメント・サンプルのみの想定）。
**境界ルール**: 未承認 FEATURE の実装は禁止。必要時は台帳に `proposed` 行だけ作成し、承認後に `approved` へ昇格してから実装に進む。

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

0. コア本開発の進め方・並行の組み合わせは [CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md) を参照。即実行 Prompt は [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md) §3.0。
1. ユーザーが本ドラフトの §2〜§3 を **承認または差し替え**。  
2. 承認後、[CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) に **承認済みスライス**を記入し、PR を分割実装。  
3. 実装提案は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) へ 1 スライスずつ起票し、承認済み範囲でのみ着手する。  
4. P0 は [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) の `p0_nextcycle_amazon_2026-04-10_a` を基準に継続し、YMM4 読込結果はオペレータ追記を取り込みながら判定を更新する。
5. 画面演出は [VISUAL-QUALITY-PACKETS.md](VISUAL-QUALITY-PACKETS.md) の A1-A4/B1-B4 を **演出単位パケット**として扱い、PASS パケットのみを本ドラフトへ反映する。

---

## 6. 変更履歴

- 2026-04-09: 画面演出を A1-A4/B1-B4 の演出単位パケットで扱うルールを追加。
- 2026-04-09: PASS 入力のみ反映ルールと未承認 FEATURE 起票境界を明記。
- 2026-04-09: P2/S6 再判定 PASS（見え方 NG 記録 + §2の5条件充足）を反映。実装起票は承認後スライス方式へ更新。
- 2026-04-10: §5 に [CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md) と Prompt パック §3.0 への導線を追加。
- 2026-04-10: P0 次サイクル実行（Amazon・CLI）を次アクションへ反映。P2 は OPEN 条件維持。
- 2026-04-09: 初版。Gate B 確定版に基づくドラフト。
