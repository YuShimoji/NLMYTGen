# B-11 下地記録レビュー（次プラン設計準備・2026-04-07）

## 目的

B-11 の既存記録を「次のプラン設計でそのまま判断材料に使える形」に整理する。
本書は **記録の正本を置き換えるものではなく**、正本の差分確認と次アクションの準備メモ。

---

## 1) 既存の下地記録（確認済み）

### 正本・運用ルール

- テンプレ正本: `docs/workflow-proof-template.md`
- 手動確認タイミング: `docs/B11-manual-checkpoints.md`
- B-11 運用基準: `docs/OPERATOR_WORKFLOW.md` の「現在の workflow proof 条件」

### 実記録（verification）

- `docs/verification/B11-workflow-proof-ai-monitoring-labor.md`
  - 取込前（`build-csv --stats --format json`）は記録済み
  - **取込後 4 区分は未記入**
- `docs/verification/B11-workflow-proof-plan-synthesis-2026-04.md`
  - 開発プラン合成用の下地として、取込前は記録済み
  - **取込後 4 区分は未記入**
- `docs/verification/B11-workflow-proof-sample-example-dialogue.md`
  - サンプル記入例（運用見本）
  - 実案件の判断材料としては弱い（短文・overflow 0 件）

---

## 2) 次プラン設計に対する現状評価

## 使える材料（既にある）

- 取込前の機械指標（話者数、総行数、overflow 警告）
- B-11 の記録フォーマットと手動確認手順
- S-5 pain の主因が「改行系」である過去観測の履歴

## 足りない材料（次判断で必須）

- 実案件 1 本での **取込後 4 区分の実測値**
  - 辞書登録
  - 手動改行
  - 再分割したい長文
  - タイミングのみ
- 代表例（CSV 行番号付き）の最小サンプル
- 「例外処理レベルに収束したか」の一文判定

---

## 3) 計画設計前に埋める最小データセット

以下が埋まれば、次プランの優先度判断を deterministic にできる。

1. 実案件 1 本で B-11 テンプレを作成し、取込前 stats を貼る  
2. YMM4 通し確認後、4 区分の件数を埋める  
3. 手動改行と再分割の代表例を 3〜5 件メモする  
4. 判断メモに「次の投資先（L2 改行 / GUI / 運用）」を 1〜3 行で記載する  

---

## 4) 次プラン分岐（この記録を使った判断ゲート）

## Gate A: 改行系が依然支配的

- 条件例: 手動改行 + 再分割が高止まり
- 次プラン: L2 改行改善（コーパス追加・ルール改善）を優先

## Gate B: 改行が収束し、運用摩擦が支配的

- 条件例: 4 区分の多くが軽微、しかし確認導線に迷いが残る
- 次プラン: 既存 GUI / runbook の運用導線強化（新機能追加は最小）

## Gate C: タイミング・辞書が主因へ遷移

- 条件例: 改行より辞書・タイミング修正が目立つ
- 次プラン: B-11 の主眼を維持しつつ、S-5 後段（辞書運用・読み確認手順）を明確化

---

## 5) 実行時チェック（準備漏れ防止）

- `docs/workflow-proof-template.md` をコピーして案件名で作成したか
- `build-csv` 実行オプションが `--max-lines 2 --chars-per-line 40 --stats` を含むか
- 取込前と取込後を **同一ファイル** に記録したか
- 4 区分件数が空欄のままになっていないか
- 次投資先の仮説を 1 行以上残したか

---

## 6) 参照（この準備メモの根拠）

- `docs/OPERATOR_WORKFLOW.md`
- `docs/workflow-proof-template.md`
- `docs/B11-manual-checkpoints.md`
- 実行パック: `docs/verification/B11-pre-plan-execution-pack-2026-04-07.md`
- オペレータハンズオン＋プラン下準備: `docs/verification/B11-operator-hands-on-and-recommended-plan-prep.md`
- `docs/verification/B11-workflow-proof-ai-monitoring-labor.md`
- `docs/verification/B11-workflow-proof-plan-synthesis-2026-04.md`
- `docs/verification/B11-workflow-proof-sample-example-dialogue.md`
