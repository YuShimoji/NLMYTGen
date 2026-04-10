# コア開発 — オペレータ入力の受け入れ・差し戻し（A〜E 移譲後）

正本: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) §1.3。索引: [CORE-DEV-POST-DELEGATION-INDEX.md](CORE-DEV-POST-DELEGATION-INDEX.md)。即実行 Prompt は [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md) を参照。

---

## 1. 目的

レーン A〜E でオペレータが更新した成果物を、コアが **マージ前に機械的に検証**し、不足があれば **差し戻し条件だけ**を返す。ここに書かない作業（YMM4 実機操作・Custom GPT 編集）はオペレータ責務。

---

## 2. 受け入れチェックリスト

| 入力 | 正本 | 受け入れ条件 | 状態（2026-04-10 監査） |
|------|------|----------------|-------------------------|
| B-11 実測 | [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §5 | 同一ファイルに取込前/後・4 区分空欄なし・代表例 ≥3・§3 Gate 明記 | **PASS** — [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md)。**NEEDS_FIX（Amazon 別紙）** — [B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) は §1・代表例・§3 まで記載済みだが **§2 取込後が YMM4 未実施の暫定**（Gate は「保留」）。オペレータが実機通しで §2.1 を実測し §3 を確定 Gate に更新したら本 PASS。 |
| P01 追記 | [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) | 対象案件の接続判定行が存在 | **PASS** — `p0_nextcycle_amazon_2026-04-10_a`（CLI）および `lane_a_amazon_2026-04-10_b`（CLI+refined・[B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) 参照）を追記済み |
| プロンプト同期 | [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md)、[S6-production-memo-prompt.md](../S6-production-memo-prompt.md) 等 | repo が正本。差分は PR で取り込み | **継続**: 変更のたびに PR レビュー。[LANE-B-execution-record-2026-04-09.md](LANE-B-execution-record-2026-04-09.md) §7（2026-04-10）で `validate-ir` / `apply-production --dry-run` 再検証・参照コミット固定 |
| P2 / S6 観測 | [runtime-state.md](../runtime-state.md)、[S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md) §2 | YMM4 見え方 OK/NG の一行＋採用案について S6 の 5 条件 | **PASS（2026-04-09）** — 見え方一行: **NG（本番投入は保留）**。`test_verify_4_bg.ymmp` 系の機械観測を根拠に S6 §2 の 5 条件を本表下の「P2/S6 充足証跡」で記入完了。未承認 FEATURE を増やさず、まずはコア幹の回帰・承認済みバグ修正へ復帰。 |
| 画面演出パケット（A1-A4/B1-B4） | [VISUAL-QUALITY-PACKETS.md](VISUAL-QUALITY-PACKETS.md) | 各パケットで「対象スコア >=2」かつ必須チェック全 `yes`。判定は PASS/NEEDS_FIX 明示。 | **継続**: PASS 入力のみドラフト反映（NEEDS_FIX は差し戻し）。 |

---

## 3. 差し戻し条件（コア → オペレータ）

次のいずれかで **マージ保留**または **差し戻し**。

1. **B-11**: §5 の 5 条件のどれかが欠ける（特に 4 区分の数値空欄、代表例 2 件以下、§3 未記入）。
2. **P01**: 新規案件で Phase 1 を回したのに接続判定の行が無い。
3. **プロンプト**: repo 正本と Custom GPT の Instructions が食い違う旨の記録なしで、運用上の正本だけが更新されている（再現不能になるため）。
4. **P2/S6**: 背景アニメの「実装・registry 拡張」を理由にしたコード変更要求が来ているが、S6 §2 の 5 条件が未記入（境界違反リスク）。
5. **未承認機能の混入**: FEATURE_REGISTRY で `approved` / `done` になっていない機能がコードに実装されている。
6. **前面排除違反**: 提出パケットの主タスクに `hold` / `quarantined` / `rejected` 項目が含まれている（候補棚に隔離されていない）。

---

## 3.1 再判定サマリ（2026-04-09）

- B-11 実測: **PASS**
- P01 追記: **PASS**
- プロンプト同期: **継続監視（NEEDS_FIX なし）**
- P2/S6 観測: **PASS（見え方 NG を明示し、実装拡張は保留）**

判定: **コア開発幹への復帰可**（未承認 FEATURE を増やさず、回帰・文書整合・承認済みバグ修正に限定）

---

## 3.2 T0 再監査（ドラフト反映用・2026-04-11）

[CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) §2〜§3 へ **PASS のみ**反映する前提の区分。

| 入力 | T0 判定 | ドラフトへの扱い |
|------|---------|------------------|
| B-11 実測 | **PASS** | §1 と整合済み。追記不要 |
| P01 追記 | **PASS** | §5 次アクションと整合。追記不要 |
| プロンプト同期 | **継続**（NEEDS_FIX なし） | 新規実測なし。§2 に差し込まない |
| P2 / S6 観測 | **PASS**（File2 の2行入力で記録済み） | [P2-READY-INPUT-TEMPLATE.md](P2-READY-INPUT-TEMPLATE.md) §1/§4 の 2 行（`YMM4見え方`・`S6§2(5条件)`）を根拠に判定。実戦投入 OK とは書かない |
| 画面演出パケット | **継続** | 全パケット PASS が揃うまで §2 を「パケット完了」とは更新しない（§5 ルールどおり） |

結論: **NEEDS_FIX によるドラフト差し止めなし**。T0 は承認記録の固定と T1 スライス起票へ進める。

運用固定（File2 準拠）:
- 判定入力は常に 2 行セット（`YMM4見え方` / `S6§2(5条件)`）。
- `OK + 充足` の組み合わせのみ READY。その他は OPEN 継続。
- OPEN/READY 判定の一次記録は [P2-READY-INPUT-TEMPLATE.md](P2-READY-INPUT-TEMPLATE.md)、反映先は本書の P2/S6 行。

補足（2026-04-10・レーンA Amazon）: [B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) は取込後未測のため、**T0 でプラン根拠に使う B-11 は引き続き AI 監視本編のみ**とする（Amazon 紙は CLI 前処理・次サイクル入力用）。

---

## 3.3 自己照合サマリ（2026-04-10・ファイル4レーンA Amazon）

| 照合項目 | 結果 |
|----------|------|
| B-11 §1 取込前（stats・JSON・コマンド） | **PASS** |
| B-11 §2 取込後（4 区分の実測・Gate 確定） | **NEEDS_FIX**（YMM4 実機未実施。暫定 0 と「保留」を明記） |
| 代表例 ≥3・§3 記載 | **PASS**（代表例は overflow 候補ベース、§3 は「保留」明示） |
| P01 行 `lane_a_amazon_2026-04-10_b` | **PASS** |

---

## 3.4 自己照合サマリ（2026-04-10・ファイル4レーンA Amazon 完了版）

| 照合項目 | 結果 |
|----------|------|
| B-11 §1 取込前（stats・JSON・コマンド） | **PASS** |
| B-11 §2 取込後（B-11形式: 4区分の件数記入） | **PASS**（`辞書0 / 手動改行10 / 再分割4 / タイミング0`） |
| 代表例 ≥3・§3 Gate 明記 | **PASS**（代表例4件、Gate A を確定） |
| P01 行 `lane_a_amazon_2026-04-10_c` | **PASS** |
| ファイル2 受け入れ条件（B-11 / P01）総合 | **PASS** |

コア提出添付要約（1行）: 「レーンA Amazon は B-11 取込前/後・4区分・Gate 記録、および P01 接続判定追記まで完了。ファイル2受け入れ条件に自己照合し PASS。」

---

## 3.5 P2/S6 充足証跡（2026-04-09）

採用対象: `p2_bg_anim_small_scope`（小規模適用・本番投入前の検証パス）

- **YMM4 見え方一行（OK/NG）**: **NG**（本番投入可否の最終視覚判定は未完。現時点では実装拡張を起票しない）
- 一次情報の根拠リンク:
  - [LANE-B-execution-record-2026-04-09.md](LANE-B-execution-record-2026-04-09.md)（`apply-production --dry-run` 実行ログ）
  - [G12-timeline-route-measurement.md](G12-timeline-route-measurement.md)（`test_verify_4_bg.ymmp` の route 観測）
- 境界適合判定: **条件付き適合**（L2/L3 境界内。Python 画像生成・.ymmp ゼロ生成・非公開 API 依存なし）
- 失敗モード（failure class）:
  - `BG_ANIM_MAP_MISS`
  - `TRANSITION_MAP_MISS`
  - `BG_ANIM_NO_LAYER0`
  - `BG_ANIM_SPEC_INVALID`
- PoC 合格条件（機械判定）:
  - `apply-production --dry-run` が exit code 0
  - `Timeline adapter` 出力で `bg_anim` / `transition` の write 件数が 1 件以上
- 既存運用への接続点:
  - `CSV -> YMM4 -> apply-production` の既存導線上で実施（runbook/P2 文脈と整合）

---

## 3.6 A〜E 入力の受け入れ判定（ファイル8 §2/§3 準拠・2026-04-10）

`ファイル8`（[CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md)）の運用に合わせ、A〜E レーン入力を本表で判定する。  
**ルール**: `PASS` のみ [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) に反映し、`NEEDS_FIX` は条件のみ返却する。

| レーン | 判定 | 根拠 | NEEDS_FIX 時に返す条件（条件のみ） |
|--------|------|------|------------------------------------|
| **A** | **PASS** | [B11-workflow-proof-amazon-panopticon-2026-04-10.md](B11-workflow-proof-amazon-panopticon-2026-04-10.md) の取込前/後・4区分・Gate 記録、および [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) `lane_a_amazon_2026-04-10_c` | B-11 §5 必須（取込前/後、4区分空欄なし、代表例>=3、§3 Gate 明記）と P01 接続行を同一 run で満たすこと |
| **B** | **PASS** | [LANE-B-execution-record-2026-04-09.md](LANE-B-execution-record-2026-04-09.md) §8（B-2/B-3 の再実行 exit 0、2体分離継続、repo 正本との差分なし） | 参照コミット固定、`validate-ir` と `apply-production --dry-run` の実行結果、GUI 側突合結果の3点を揃えること |
| **C** | **PASS** | [LANE-C-file6-local-mechanical-proof-2026-04-10.md](LANE-C-file6-local-mechanical-proof-2026-04-10.md)（`validate-ir`/`apply-production --dry-run` exit 0、_local 方針順守） | `_local` 経路で案件ローカル差分を隔離し、機械確認ログ（exit code と集計）を提出すること |
| **D** | **PASS** | [H01-lane-d-prep-2026-04-09.md](H01-lane-d-prep-2026-04-09.md) §6 完了（brief 先頭投入・正本整合・運用クローズ） | brief 先頭投入、B-3 正本同期、Evidence Log の3点を満たすこと |
| **E** | **PASS** | [LANE-E-S8-prep-2026-04-09.md](LANE-E-S8-prep-2026-04-09.md)（準備サイクル完了、Probe 契約と判定基準固定） | runbook トラックEに沿い、実行証跡（run_id/出力/判定）を P03 へ追記すること |

注記: 途中提出が条件未充足の場合は本表の `PASS` を維持せず `NEEDS_FIX` 扱いに戻す。ドラフト本文には反映しない。

---

## 4. コア側のアクション（受け入れ後）

- **PASS のみ反映**: [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) には PASS 判定の入力だけを反映する。NEEDS_FIX は反映しない。
- **前面タスクのフィルタ**: 実行 Prompt と次アクションには `done` 運用改善または `approved` のみ採用し、`hold` / `quarantined` / `rejected` は候補棚へ分離する。
- ドキュメントのみの変更 → レビュー後 `master` 起点のトピックブランチでマージ。
- B-11 §3 Gate が確定したら [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) を更新し、ユーザー承認を待つ（実装は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md)）。
- **H-05（2026-04-09）**: `score-thumbnail-s8` は FEATURE_REGISTRY で実装済みとして整合済み。検収時は「CLI 集約のみ（画像生成/解析なし）」の境界を維持しているかを確認する。

---

## 5. 変更履歴

- 2026-04-11: §3.2 T0 再監査（PASS/継続の区分）を追加。
- 2026-04-10: §3.3 自己照合（レーンA Amazon）、§3.2 補足、B-11/P01 受け入れ行を Amazon B-11・`lane_a_amazon_2026-04-10_b` 追記に合わせて更新。
- 2026-04-10: 監査日更新。P01 `p0_nextcycle_amazon_2026-04-10_a` を反映、P2/S6 は OPEN 継続を明文化。
- 2026-04-10: §4 を master 起点のトピックブランチ運用へ更新。
- 2026-04-10: 「プロンプト同期」受け入れ状態に [LANE-B-execution-record-2026-04-09.md](LANE-B-execution-record-2026-04-09.md) §7（レーンB再検証）への参照を追記。
- 2026-04-09: 画面演出パケット（A1-A4/B1-B4）のスコア＋チェックリスト受け入れ行を追加。
- 2026-04-09: `hold/quarantined/rejected` の前面排除ルールを差し戻し条件とコア運用に追加。
- 2026-04-09: 未承認機能混入の差し戻し条件を追加。H-05 承認整合（CLI 集約のみ）を反映。
- 2026-04-09: Prompt パック参照と「PASS のみ反映」ルールを明記。
- 2026-04-09: P2/S6 観測を PASS 化。YMM4 見え方一行（NG）と S6 §2 の 5 条件を「3.5 P2/S6 充足証跡」に追記。
- 2026-04-09: 初版。AI 監視 B-11・P01 を PASS と記録。P2/S6 は OPEN。
