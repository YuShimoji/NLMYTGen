# B-11 実測パック（プラン策定直前用）

## このパックの目的

次プランを感覚ではなく実測で決めるために、B-11 を **実案件 1 本**で埋め切る。
完了条件は「4 区分件数 + 代表例 + 次投資先メモ」が 1 ファイルに揃うこと。

---

## 中断から再開（いまの位置）

- **オペレータ向けの全文ハンズオン**（YMM4 手順〜4 区分の数え方〜プラン下準備）: [B11-operator-hands-on-and-recommended-plan-prep.md](B11-operator-hands-on-and-recommended-plan-prep.md)
- **済み**: B-11 下地レビューと本パックは `feat/phase2-motion-segmentation` にコミット済み（`1df3028` 付近）。
- **未完（ここから）**: 既存の進行中 proof で **セクション 2 だけ未記入**。
  - 正本: [`B11-workflow-proof-ai-monitoring-labor.md`](B11-workflow-proof-ai-monitoring-labor.md)
  - 取込用 CSV: `samples/AI監視が追い詰める生身の労働_B11_ymm4.csv`（リポジトリ同梱）
  - 手順: 同ファイル内「YMM4 側の次ステップ」→ [B11-manual-checkpoints.md](../B11-manual-checkpoints.md) に沿って通し確認し、**2.1〜2.3 を実数で埋める**。
- **別ルート**: 新台本で実案件 1 本を取る場合は下記 §0 から新規 `B11-workflow-proof-<案件>.md` を切る（AI 監視を完了させなくても可だが、最短は上記の §2 埋め）。

---

## 0. 作成物（先に決める）

- 記録ファイル: `docs/verification/B11-workflow-proof-<案件名>-<日付>.md`
- 入力台本: 実案件で使う `.txt`
- 出力 CSV: `samples/<案件名>_B11_ymm4.csv`（任意の命名で可）

---

## 1. 取込前（CLI 10分）

`build-csv` の stats と overflow 候補を取得して、記録ファイルの「1. 取込前」に貼る。

```text
uv run python -m src.cli.main build-csv "<INPUT.txt>" -o "<OUTPUT.csv>" --max-lines 2 --chars-per-line 40 --reflow-v2 --stats --format json
```

### チェック基準（取込前）

- Stats が出力されている
- Overflow 警告の有無が明記できる
- `--format json` の最終行を貼れる

---

## 2. 取込後（YMM4 通し確認 20〜40分）

`docs/B11-manual-checkpoints.md` の順序で通し確認し、記録ファイルの「2. 取込後」を埋める。

### 記録する最小項目

- 4 区分の件数
  - 辞書登録
  - 手動改行
  - 再分割したい長文
  - タイミングのみ
- 代表例 3〜5 件（可能なら CSV 行番号付き）

---

## 3. プラン直前判定（5分）

同じ記録ファイルの「3. 判断メモ」に、次投資先を 1〜3 行で確定する。

### 判定テンプレ（コピペ可）

```text
- 判定: Gate A / Gate B / Gate C
- 根拠: （4 区分の件数サマリ）
- 次投資先: （L2 改行改善 / 運用導線強化 / S-5 後段運用）
```

---

## 4. Gate 判定ルール（簡易）

### Gate A（改行支配）

- 目安: 手動改行 + 再分割が他区分より明確に多い
- 次プラン: L2 改行改善（コーパス追加・ルール改善）を優先

### Gate B（運用摩擦支配）

- 目安: 4 区分は軽微だが、確認導線や記録運用で迷いが出る
- 次プラン: 既存 GUI / runbook / 記録導線の強化を優先

### Gate C（辞書・タイミング支配）

- 目安: 改行より辞書・タイミング修正の割合が高い
- 次プラン: S-5 後段の運用整備（辞書・読み確認）を優先

---

## 5. 完了チェック（プラン策定に入って良い条件）

- 実案件 1 本の B-11 記録が `docs/verification` にある
- 取込前/取込後が同一ファイルで埋まっている
- 4 区分件数が空欄なし
- 代表例が 3 件以上ある
- Gate 判定と次投資先が明文化されている

上記を満たした時点で「プラン策定直前」状態に到達。