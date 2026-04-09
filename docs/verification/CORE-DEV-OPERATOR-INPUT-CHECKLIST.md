# コア開発 — オペレータ入力の受け入れ・差し戻し（A〜E 移譲後）

正本: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) §1.3。索引: [CORE-DEV-POST-DELEGATION-INDEX.md](CORE-DEV-POST-DELEGATION-INDEX.md)。

---

## 1. 目的

レーン A〜E でオペレータが更新した成果物を、コアが **マージ前に機械的に検証**し、不足があれば **差し戻し条件だけ**を返す。ここに書かない作業（YMM4 実機操作・Custom GPT 編集）はオペレータ責務。

---

## 2. 受け入れチェックリスト


| 入力         | 正本                                                                                                                                             | 受け入れ条件                                  | 状態（2026-04-10 監査）                                                                                                                               |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| B-11 実測    | [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §5                                                      | 同一ファイルに取込前/後・4 区分空欄なし・代表例 ≥3・§3 Gate 明記 | **PASS** — [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md)                                               |
| P01 追記     | [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md)                                                                           | 対象案件の接続判定行が存在                           | **PASS** — `p0_nextcycle_amazon_2026-04-10_a` を追記済み（CLI 接続判定）                                                                                   |
| レーンD証跡受領 | [H01-packaging-orchestrator-workflow-proof.md](H01-packaging-orchestrator-workflow-proof.md)                                                   | `p0_nextcycle` の Operational Run と strict比較4観点が記録済み | **PASS** — `p0_nextcycle_amazon_2026-04-10_a` の `Operational Run` と `Strict Comparison Record` を受領（brief先頭 C-07/C-08 上位制約運用） |
| プロンプト同期    | [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md)、[S6-production-memo-prompt.md](../S6-production-memo-prompt.md) 等          | repo が正本。差分は PR で取り込み                   | **継続**: 変更のたびに PR レビュー                                                                                                                          |
| P2 / S6 観測 | [runtime-state.md](../runtime-state.md)、[S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md) §2 | YMM4 見え方 OK/NG の一行＋採用案について S6 の 5 条件    | **OPEN 継続** — 2026-04-10 再判定: `YMM4見え方=NG（未実施: YMM4実測ログ未提出）`、`S6§2(5条件)=充足（条件4/5は docs/verification/P2-CONDITION45-PRECHECK-TEMPLATE.md を根拠に確認済み）`。**OPEN理由は YMM4実測待ちの1点のみ**。READY 条件 `OK + 5条件充足` を未達のため、コアは P2 向けコードスライスを起票しない。 |


---

## 2.1 P2 READY 入力フォーマット（分岐C）

P2/S6 観測の入力は [P2-READY-INPUT-TEMPLATE.md](P2-READY-INPUT-TEMPLATE.md) を使って統一する。

- 必須 2 行:
  - `YMM4見え方: OK|NG - <一言>`
  - `S6§2(5条件): 充足|未充足 - <根拠>`
- 判定:
  - 2 行充足かつ `OK + 充足` のみ READY
  - それ以外は OPEN 継続

## 2.2 P2 入力の先行記入（YMM4 を今見られない場合）

YMM4 実機確認が端末制約で実施できない場合でも、以下は先に記入してよい。

- `S6§2(5条件)` 側の根拠整理（リンク・不足項目）
- `YMM4見え方` は `未実施（環境制約）` と明記
- 判定は必ず **OPEN 継続**

記入テンプレ（暫定）:

- `YMM4見え方: NG - 未実施（環境制約: テスト端末でYMM4リソース共有不可）`
- `S6§2(5条件): 未充足 - <不足項目 or 根拠リンク>`

YMM4 を確認できる端末で再実測後、1 行目を `OK|NG` の実測値に更新して再判定する。

## 2.3 確認なしで先に進める下準備タスク（分岐C）

`YMM4見え方` の実測前でも、次は先行実行してよい（P2 は OPEN 継続のまま）。

1. **S6 §2 条件4（PoC 合格条件の機械判定可能）ログを添付**
  - 最低 1 本、`apply-production --dry-run` か `measure-timeline-routes --expect --profile ...` の実行ログを残す。
2. **S6 §2 条件5（既存運用接続点）を明記**
  - `CSV -> YMM4 -> apply-production` のどこに繋ぐかを 1 行で記録する。
3. **P2/S6 行へ暫定 2 行を記入**
  - `YMM4見え方` は環境制約を明記して暫定記入。
  - `S6§2(5条件)` は不足項目と根拠リンクを明記。

この 3 つを満たしたら、残タスクは YMM4 実測 1 行のみになる。
実施テンプレ: [P2-CONDITION45-PRECHECK-TEMPLATE.md](P2-CONDITION45-PRECHECK-TEMPLATE.md)

---

## 3. 差し戻し条件（コア → オペレータ）

次のいずれかで **マージ保留**または **差し戻し**。

1. **B-11**: §5 の 5 条件のどれかが欠ける（特に 4 区分の数値空欄、代表例 2 件以下、§3 未記入）。
2. **P01**: 新規案件で Phase 1 を回したのに接続判定の行が無い。
3. **プロンプト**: repo 正本と Custom GPT の Instructions が食い違う旨の記録なしで、運用上の正本だけが更新されている（再現不能になるため）。
4. **P2/S6**: 背景アニメの「実装・registry 拡張」を理由にしたコード変更要求が来ているが、S6 §2 の 5 条件が未記入（境界違反リスク）。

---

## 4. コア側のアクション（受け入れ後）

- ドキュメントのみの変更 → レビュー後 `master` 起点のトピックブランチでマージ。
- B-11 §3 Gate が確定したら [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) を更新し、ユーザー承認を待つ（実装は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md)）。

---

## 5. 変更履歴

- 2026-04-10: P2/S6 観測行を更新。条件4ログの最新実績（2026-04-10）を反映しつつ OPEN 継続を維持。
- 2026-04-10: レーンD証跡受領行を追加。`p0_nextcycle_amazon_2026-04-10_a` の H-01 Operational Run / strict比較4観点を受領済みとして記録。
- 2026-04-10: P2/S6 観測行に最新入力（YMM4 未実施 NG / S6 条件4・5未充足）を反映。判定は OPEN 継続。
- 2026-04-10: §2.1 追加。P2 READY 入力フォーマットをテンプレ化（分岐C）。
- 2026-04-10: 監査日更新。P01 `p0_nextcycle_amazon_2026-04-10_a` を反映、P2/S6 は OPEN 継続を明文化。
- 2026-04-10: §4 を master 起点のトピックブランチ運用へ更新。
- 2026-04-09: 初版。AI 監視 B-11・P01 を PASS と記録。P2/S6 は OPEN。

