# コア開発 — オペレータ入力の受け入れ・差し戻し（A〜E 移譲後）

正本: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) §1.3。索引: [CORE-DEV-POST-DELEGATION-INDEX.md](CORE-DEV-POST-DELEGATION-INDEX.md)。

---

## 1. 目的

レーン A〜E でオペレータが更新した成果物を、コアが **マージ前に機械的に検証**し、不足があれば **差し戻し条件だけ**を返す。ここに書かない作業（YMM4 実機操作・Custom GPT 編集）はオペレータ責務。

---

## 2. 受け入れチェックリスト

| 入力 | 正本 | 受け入れ条件 | 状態（2026-04-09 監査） |
|------|------|----------------|-------------------------|
| B-11 実測 | [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §5 | 同一ファイルに取込前/後・4 区分空欄なし・代表例 ≥3・§3 Gate 明記 | **PASS** — [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) |
| P01 追記 | [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) | 対象案件の接続判定行が存在 | **PASS** — 表に複数案件・接続判定列あり |
| プロンプト同期 | [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md)、[S6-production-memo-prompt.md](../S6-production-memo-prompt.md) 等 | repo が正本。差分は PR で取り込み | **継続**: 変更のたびに PR レビュー |
| P2 / S6 観測 | [runtime-state.md](../runtime-state.md)、[S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md) §2 | YMM4 見え方 OK/NG の一行＋採用案について S6 の 5 条件 | **OPEN** — オペレータが YMM4 結果と S6 §2 を追記するまでコアは P2 向けコードスライスを起票しない |

---

## 3. 差し戻し条件（コア → オペレータ）

次のいずれかで **マージ保留**または **差し戻し**。

1. **B-11**: §5 の 5 条件のどれかが欠ける（特に 4 区分の数値空欄、代表例 2 件以下、§3 未記入）。
2. **P01**: 新規案件で Phase 1 を回したのに接続判定の行が無い。
3. **プロンプト**: repo 正本と Custom GPT の Instructions が食い違う旨の記録なしで、運用上の正本だけが更新されている（再現不能になるため）。
4. **P2/S6**: 背景アニメの「実装・registry 拡張」を理由にしたコード変更要求が来ているが、S6 §2 の 5 条件が未記入（境界違反リスク）。

---

## 4. コア側のアクション（受け入れ後）

- ドキュメントのみの変更 → レビュー後 `feat/phase2-motion-segmentation` にマージ。
- B-11 §3 Gate が確定したら [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) を更新し、ユーザー承認を待つ（実装は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md)）。

---

## 5. 変更履歴

- 2026-04-09: 初版。AI 監視 B-11・P01 を PASS と記録。P2/S6 は OPEN。
