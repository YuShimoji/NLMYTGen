# 次期実装プラン（ドラフト）— B-11 Gate 取り込み後

**ステータス**: **T0 再承認依頼用（本版）**。**コード実装**は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 の **承認済みスライス単位**でのみ着手する。入力: [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) §3。受け入れ記録: [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)（§3.2 T0 再監査含む）。
**反映ルール**: 本書に反映してよいのは **PASS 判定入力のみ**（NEEDS_FIX は差し戻し後に再審査）。

---

## 1. B-11 からの確定事項

| 項目 | 内容 |
|------|------|
| **Gate** | **B**（運用摩擦支配 → 運用側へ移行） |
| **根拠要約** | 4 区分は全編通しで 0 件。顕著な改行・辞書修正なし。overflow 機械候補は残存（監視対象）。 |
| **次投資先（オペレータ記述）** | 背景アニメを 1〜2 セクションで小規模適用し、route と見え方確認。F-01/F-02 は quarantined 維持。 |

---

## 1.5 ユーザー承認依頼（T0・本版）

次の判断について **チャットまたは issue** で回答し、§6 に記録する（**非PASS入力は本文へ反映しない**）。
**T0 の承認対象は §2〜§3 のみ** とし、§5.5 は差し戻し条件の返却専用とする。

1. **判断1**: §2（コア開発での解釈）および §3（FEATURE_REGISTRY 変更案）を **現文のまま承認**するか、差し替え文案を提示するか。
2. **判断2**: §3 に **台帳新規行（コードスライス）** を今サイクルで扱うか。デフォルトは **追加しない**（ドキュメント・サンプルのみ）。
3. **判断3**（任意）: §2.1 の「verification / サンプル JSON」の **具体パス・題材**を T0 で指定するか、**T1 でエージェントが提案**するか。

**本版のT0取り込み方針（ファイル2 §4 判定ルール準拠）**:
- **PASSのみ本文反映**: B-11 実測、P01 追記、P2/S6 観測の PASS 入力だけを本文整合根拠として採用する。
- **非PASSは本文非反映**: 継続監視・NEEDS_FIX は本文の「完了根拠」に昇格しない。
- **返却先を固定**: NEEDS_FIX 入力は §5.5「差し戻し条件」にのみ記載し、本文（§1〜§5）には混在させない。

---

## 1.6 PASS 入力の反映記録（A〜E）

[CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) §3.6 の判定結果に基づき、本文へ反映するのは次の `PASS` 入力のみ。

| レーン | 反映可否 | 反映内容（要約） |
|------|----------|------------------|
| A | 反映可（PASS） | B-11/P01 接続完了入力を T1〜T2 運用根拠として採用 |
| B | 反映可（PASS） | Prompt 同期の再検証（B-2/B-3）と正本差分なしを採用 |
| C | 反映可（PASS） | `_local` 分離前提の機械確認ログ提出を採用 |
| D | 反映可（PASS） | H-01 brief 運用準備クローズを採用 |
| E | 反映可（PASS） | S-8 準備サイクル完了と Probe 契約固定を採用 |

非PASS入力は本文に昇格せず、§5.5 の差し戻し条件でのみ扱う。

---

## 2. コア開発での解釈（投資の割り当て）

Gate B の「運用導線・記録」に合わせ、**次の優先**を推奨する（実装は承認後。起票先は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) に統一）。

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
1. **本版 §2〜§3 をT0承認対象として確認**し、承認または差し替え文案を返す（記録先は §6）。
2. **承認後**: [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 に承認済みスライスを起票し、§2 チェックリスト（明示承認リンク／`FEATURE_REGISTRY` 遷移／`master` 起点／1スライス実装／フル回帰）を満たしたものだけ着手する。
3. コード変更が必要になった場合のみ §3 テンプレに従い FEATURE_REGISTRY で `proposed` → 承認 → 別スライスとして起票する。
4. P0 は [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) の `p0_nextcycle_amazon_2026-04-10_a` を基準に継続し、YMM4 読込結果はオペレータ追記を取り込みながら判定を更新する。
5. 画面演出は [VISUAL-QUALITY-PACKETS.md](VISUAL-QUALITY-PACKETS.md) の A1-A4/B1-B4 を **演出単位パケット**として扱い、PASS パケットのみを本ドラフトへ反映する。

---

## 5.5 差し戻し条件（非PASS入力の返却専用）

ファイル2で **PASS にならない入力**は、次の条件のみ返して再提出を待つ（本ドラフト本文へは反映しない）。

1. **B-11**: §5 の必須要件（取込前/後、4区分空欄なし、代表例≥3、§3 Gate明記）の不足を埋める。
2. **P01**: 対象案件の接続判定行を追記する。
3. **プロンプト同期**: repo正本との差分有無と再現手順（参照コミット/検証コマンド）を記録する。
4. **P2/S6**: 見え方一行（OK/NG）と S6 §2 の5条件をセットで提出する。
5. **画面演出パケット**: スコア条件（対象>=2）と必須チェック all yes を満たし PASS/NEEDS_FIX を明示する。

---

## 6. ユーザー承認記録（T0）

| 承認日 | 承認範囲 | ユーザー参照（要約） | 差し替え要約 |
|--------|----------|----------------------|--------------|
| （承認待ち） | §2・§3 全文 | 本版T0承認依頼（ファイル8 T0 / ファイル2 PASS反映ルール準拠） | （未記入） |

T0 記録時の固定ルール:
- 承認対象は **§2・§3** のみ（非PASS入力は §5.5 返却専用）。
- 承認後の起票先は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 に一本化する。

---

## 7. 変更履歴

- 2026-04-10: File2 §4 判定ルールに文言を統一。NEEDS_FIX 入力の記載先を §5.5 に固定し、本文（§1〜§5）から分離。
- 2026-04-10: T0 再承認依頼版へ更新。非PASS入力は本文へ反映せず、§5.5「差し戻し条件」に限定して返却する運用を明記。
- 2026-04-10: ファイル8 T0 整備として、承認対象（§2〜§3）と承認後導線（POST-APPROVAL-SLICES §1/§2）を明文化。
- 2026-04-11: T0 完了。§1.5 承認依頼、§6 承認記録、ステータスを承認済みへ。§2 を実戦投入 OK と誤読されないよう本文は変更せず（P2 見え方 NG はチェックリスト正本）。
- 2026-04-09: 画面演出を A1-A4/B1-B4 の演出単位パケットで扱うルールを追加。
- 2026-04-09: PASS 入力のみ反映ルールと未承認 FEATURE 起票境界を明記。
- 2026-04-09: P2/S6 再判定 PASS（見え方 NG 記録 + §2の5条件充足）を反映。実装起票は承認後スライス方式へ更新。
- 2026-04-10: §5 に [CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md) と Prompt パック §3.0 への導線を追加。
- 2026-04-10: P0 次サイクル実行（Amazon・CLI）を次アクションへ反映。P2 は OPEN 条件維持。
- 2026-04-09: 初版。Gate B 確定版に基づくドラフト。
