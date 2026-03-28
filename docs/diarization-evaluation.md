# 話者割当 精度評価計画

## 目的

行交互割当の実際の精度を測定し、LLM（Gemini）導入の採否を数値に基づいて判断する。

## 評価手順

### Step 1: Gold Set 作成（手動）

1. NotebookLM Audio Overview の音声を再生する
2. `tools/gold_set_template.json` の speaker 欄を A/B で埋める
3. 最低 30 行、できれば 50 行のラベルが必要
4. 優先すべき行:
   - 分析で「疑わしい」と判定された 22 箇所の前後
   - 超短応答（「はい。」「ええ。」）の前後
   - 話題転換の前後（L11-14, L74-78, L130-136）

### Step 2: 評価実行

```bash
python -X utf8 tools/evaluate_diarization.py tools/gold_set_template.json
```

3 手法を自動比較:
- `alternating`: 行交互（現行）
- `rule_v1`: 文分断検出（カスケードあり）
- `rule_v2_resync`: 文分断検出 + 再同期（カスケード緩和）

### Step 3: 判定

## Go/No-Go 判定基準

### Gemini PoC に進む条件（Go）

以下の **全て** を満たす場合:

1. **行交互の正答率が 85% 未満**
   → 改善の余地がある
2. **rule_v2 の正答率が行交互 +10pt 未満**
   → ルールベースでは十分に改善できない
3. **行交互の誤り箇所が文脈で判断可能なパターンに集中**
   → LLM の文脈理解で改善が見込める
4. **別 NLM transcript でも同様の傾向が確認される**
   → 1 件のデータ固有の問題ではない

### Gemini PoC に進まない条件（No-Go）

以下の **いずれか** に該当する場合:

1. **行交互の正答率が 85% 以上**
   → LLM 導入の費用対効果が低い。現行で十分
2. **行交互の正答率が 50% 以下**
   → 入力品質の問題。LLM より S-2（書き起こし品質）改善が先
3. **rule_v2 が行交互 +10pt 以上改善**
   → ルールベースで十分。外部 API 不要
4. **誤りがランダムで文脈的パターンがない**
   → LLM でも改善が見込めない

### 判定後の分岐

| 結果 | 次のアクション |
|------|---------------|
| Go | ADR-0004 起票 → urllib で Gemini Flash-Lite PoC → gold set で精度比較 |
| No-Go (高精度) | 行交互を維持。他の改善（S-2 自動化等）に注力 |
| No-Go (低精度) | S-2 の書き起こし品質改善を先行。話者付き書き起こしの検討 |
| No-Go (rule_v2 十分) | rule_v2 を normalize.py に統合。LLM なし |

## 必要な追加データ

### 別 NLM transcript の必要性

**最小 1 件、推奨 2 件。**

理由:
- 現在の 1 件だけでは、パターンの汎化性が不明
- NotebookLM の対話スタイルはトピックによって変動する可能性がある
- 短い transcript と長い transcript で挙動が異なる可能性がある

条件:
- NotebookLM Audio Overview から生成された書き起こしテキスト
- 現在のサンプルとは異なるトピック
- 可能なら異なる長さ（短い: 50行以下、長い: 100行以上）

## ファイル構成

```
tools/
  analyze_diarization.py     # 定性分析（疑わしい箇所の特定）
  evaluate_diarization.py    # 定量評価（gold set との精度比較）
  gold_set_template.json     # 正解ラベルテンプレート（手動記入用）
docs/
  diarization-evaluation.md  # この文書
```
