# T1-RUNBOOK-GUI — 用語・導線整合の検証記録（正本）

**スライス**: [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 の **T1-RUNBOOK-GUI**。  
**目的**: runbook と GUI ガイドの文言・導線を、コアフェーズ T1（文書・サンプル先行）の範囲で機械的に照合し、運用時の解釈ブレを防ぐ。  
**境界**: 本スライスは **ドキュメント整備のみ**。新規 FEATURE 実装・新タブ追加・F-01/F-02 復帰は行わない。

---

## 1. 検証対象

| 区分 | 対象ファイル | 照合観点 |
|------|--------------|----------|
| runbook 正本 | [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) | トラック A/B の実行順、用語定義、参照先 |
| GUI 導線正本 | [gui-llm-setup-guide.md](../gui-llm-setup-guide.md) | Electron 表記、C-09 導線、v4 正本の固定先 |
| 判定基準 | [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) | 受け入れ条件との整合（文書更新のみ） |

---

## 2. 機械照合チェック（T1）

### 2.1 台本診断 JSON（B-18）用語の一致

- runbook 側に「台本診断 JSON（B-18）」を明示し、`diagnose-script` 出力と Electron 同梱 JSON を同一成果物として扱う記述がある。  
- GUI ガイド側に「台本診断 JSON も保存」のチェックボックス文言と保存先ルールがある。  
- 両者とも C-09 入力への接続点を明示している。

判定: **PASS**

### 2.2 トラック A の工程順一致

- runbook 側は `diagnose-script` → refinement（C-09）→ `validate` / `build-csv` の順。  
- GUI ガイド側も同順で、CSV 変換タブと品質診断タブの位置づけを分離している。  
- CLI / GUI で Speaker Map を揃える注意点が両者で矛盾しない。

判定: **PASS**

### 2.3 トラック B（v4 正本）導線一致

- runbook 側は S-6 正本を [S6-production-memo-prompt.md](../S6-production-memo-prompt.md) に固定。  
- GUI ガイド側も同じ正本固定（v4 フェンス内全文）を明示。  
- B-5（サムネコピー）を別正本 [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md) として切り出す運用が一致。

判定: **PASS**

### 2.4 T1-P2-DOCSAMPLE 参照導線

- runbook 側に [T1-P2-DOCSAMPLE-p2-staged-rollout-mechanical-proof.md](T1-P2-DOCSAMPLE-p2-staged-rollout-mechanical-proof.md) 参照があり、P2 機械検証の正本が一意。  
- GUI ガイド側は P2 手順を重複記述せず、runbook 参照で導線を統一している。

判定: **PASS**

### 2.5 境界ルール（未承認 FEATURE 禁止）

- runbook / GUI ガイドの更新範囲は用語・順序・参照リンクに限定し、機能追加提案に踏み込んでいない。  
- `F-01` / `F-02`（quarantined）を復活させる文言、または新規タブ追加の導線は含まれていない。  
- 実装変更が必要な場合は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 の承認済みスライスに分離する方針を維持している。

判定: **PASS**

---

## 3. T1 判定

- 未承認 FEATURE 実装: **なし**  
- 新規コード変更: **なし**  
- 文書・導線整備: **完了（PASS）**

結論: **T1-RUNBOOK-GUI は「文書・サンプル先行」ポリシーに適合**。

---

## 4. 変更履歴

- 2026-04-10: 初版。T1 フェーズ用に runbook / GUI 用語・導線の一致確認を正本化。
