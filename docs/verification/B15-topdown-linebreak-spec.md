# B-15: トップダウン改行アルゴリズム仕様

## 1. 背景と動機

### 現在の問題

現在の改行処理は2層構造で、各層が独立に動作する:

- 第1層 `split_long_utterances()`: max_length (80幅) 超過時に句点や節で分割
- 第2層 `balance_subtitle_lines()`: 各行を chars_per_line (40幅) で2行バランス調整

2つの層が全体を見ずに局所最適を繰り返すため、以下の問題が発生する:

| 問題 | 原因 | 例 |
|------|------|-----|
| 単語途中切断 | chars_per_line の強制切断 | `見せつけられなが\nら` |
| 閉じ括弧+助詞の分離 | `」` が候補文字として分割される | `「最適化」\nと聞くと` |
| 左側が極端に短い | 最初の候補に飛びつく | `例えば、\n一定時間...` (4文字) |
| 括弧ペアの分断 | 閉じ括弧が次行に漏出 | `（DSP）\n」プログラム` |

### 解決方針

テキスト全体の幅を先に見て「理想的な各行の長さ」を計算し、その近傍で最適な区切りを探す**トップダウン方式**に再設計する。

---

## 2. アルゴリズム概要

```
入力: text (話者の1発話), chars_per_line, max_lines

Step 1: 総幅を測定し、必要行数を決定
  total_width = display_width(text)
  needed_lines = ceil(total_width / chars_per_line)
  needed_lines = min(needed_lines, max_lines)
  if needed_lines <= 1: return [text]  -- 分割不要

Step 2: 理想行長を計算
  ideal_line_width = total_width / needed_lines

Step 3: 区切り候補を全列挙
  大区切り (priority 高): 句点、読点、閉じ括弧+助詞セット
  小区切り (priority 低): カタカナ/ひらがな境界、数字/非数字境界

Step 4: 各行末の理想位置の近傍で最適な区切りを選択
  for i in 1..needed_lines-1:
    target_pos = 理想行長 * i の累積幅位置
    search_range = target_pos ± chars_per_line/4
    候補 = search_range 内の区切り候補
    最適 = スコア最小の候補を選択

Step 5: ガード検証
  各行が min_line_width (6幅 or chars_per_line/6) 以上か?
  NG なら隣の区切りに移動

Step 6: 分割実行
  選択した位置で改行を挿入し、行リストを返す
```

---

## 3. 区切り候補の定義

### 大区切り (major breaks)

自然な改行点。優先的に使う。

| 候補 | penalty | 条件 |
|------|---------|------|
| `。` `！` `？` `!` `?` の直後 | 0 | -- |
| `、` `,` `，` の直後 | 1 | -- |
| `」` `』` `）` `)` `】` + 助詞の直後 | 1 | 閉じ括弧の直後に助詞 (と/を/が/は/に/で/も/の/や/へ) が続く場合、助詞の後を候補とする。閉じ括弧単体では候補にしない |
| `」` `』` `）` `)` `】` の直後 (助詞なし) | 2 | 次の文字が助詞でない場合のみ |
| 接続句 (しかし/なので/ため/一方で 等) の直前 | 2 | -- |

**重要な変更**: 現在の実装では `」` 直後が一律で候補になるが、新方式では **閉じ括弧+助詞をセットで保護**する。`「最適化」と` の `」と` の間では切らず、`と` の後を候補にする。

### 小区切り (minor breaks)

大区切りが理想位置の近傍に存在しない場合のフォールバック。

| 候補 | penalty | 判定方法 |
|------|---------|---------|
| カタカナ→ひらがな の境界 | 4 | `is_katakana(text[i]) and is_hiragana(text[i+1])` |
| ひらがな→カタカナ の境界 | 4 | `is_hiragana(text[i]) and is_katakana(text[i+1])` |
| 数字→非数字 の境界 | 4 | `text[i].isdigit() and not text[i+1].isdigit()` |
| 漢字→ひらがな の境界 | 5 | CJK Unified Ideographs → hiragana |
| マーカー句 (という/として/により 等) の直後 | 3 | 既存の `_AGGRESSIVE_BREAK_AFTER_MARKERS` を再利用 |

### 候補にしないもの (禁止位置)

| 禁止 | 理由 |
|------|------|
| 括弧ペアの内側 (`「...」` の途中) | 括弧の対応を壊さない |
| カタカナ連続の途中 | カタカナ語 (外来語) の途中で切ると読めない |
| 数字連続の途中 | `202/4` のような分断を防ぐ |
| `ー` (長音符) の直前・直後 | `アルゴリズ\nム` のような分断を防ぐ |

---

## 4. スコアリング

各候補のスコアを以下で計算し、最小スコアの候補を選ぶ:

```
score = distance_penalty + break_penalty + balance_penalty

distance_penalty = abs(candidate_pos - ideal_pos)
  -- 理想位置からの距離。近いほど良い

break_penalty = 候補の penalty × 3
  -- 大区切り (0-2) は低い、小区切り (3-5) は高い

balance_penalty:
  resulting_line_width < min_line_width → +50 (ガード違反)
  otherwise → 0
```

---

## 5. 処理フロー (統合版)

現在の2層 (`split_long_utterances` → `balance_subtitle_lines`) を、**1つの関数に統合**する:

```python
def reflow_utterance(
    text: str,
    *,
    chars_per_line: int,
    max_lines: int,
) -> list[str]:
    """話者の1発話を、画面表示に最適化された複数行に分割する。

    トップダウン方式:
    1. 総幅から必要行数を決定
    2. 理想行長を計算
    3. 各行末の理想位置近傍で最適な区切りを選択
    """
```

### 呼び出し側の変更

```python
# 現在 (2段階)
output = split_long_utterances(output, max_length=effective_max, use_display_width=True)
if balance_lines:
    output = balance_subtitle_lines(output, chars_per_line=cpl, max_lines=ml)

# 新方式 (1段階)
output = reflow_subtitles(output, chars_per_line=cpl, max_lines=ml)
```

### 後方互換

- `--balance-lines` フラグは維持。指定時に新方式を使う
- `--balance-lines` なしの場合は現在の `split_long_utterances` をそのまま使用
- 既存テストは新方式でも同等以上の結果を出すことを確認

---

## 6. 複数文発話の扱い

1発話に複数文 (句点区切り) が含まれる場合:

```
Step 0: 句点で文を分離 (現在の _SENTENCE_ENDS.split と同じ)
Step 1: 各文に対して reflow_utterance を適用
Step 2: 結果を話者行として展開
```

これは現在の `split_long_utterances` の「句点分割 → 各文処理」と同じ構造を維持する。
変わるのは「各文の内部処理」がトップダウンになる点のみ。

---

## 7. 具体例での動作

### 例1: 閉じ括弧+助詞 (現在 bad-split)

```
入力: "私たちが普段「アルゴリズムによる最適化」と聞くと、効率的でクリーンな魔法を想像しがちですが、"
幅:   約100

Step 1: needed_lines = ceil(100/40) = 3, min(3, 2) = 2
Step 2: ideal_line_width = 100/2 = 50
Step 3: 候補列挙
  - 「、」(pos≈28): penalty 1 (大区切り)
  - 「」と」→ 「と」の後 (pos≈37): penalty 1 (閉じ括弧+助詞セット)
  - 「、」(pos≈50): penalty 1 (大区切り) ← ideal に最も近い
Step 4: ideal=50 の近傍で 「、」(pos≈50) を選択
  score = |50-50| + 1*3 + 0 = 3

結果: "私たちが普段「アルゴリズムによる最適化」と聞くと、\n効率的でクリーンな魔法を想像しがちですが、"
```

現在の出力 `「最適化」\nと聞くと、` と比べて大幅に改善。

### 例2: 左側が短すぎる (現在 bad-split)

```
入力: "例えば、一定時間アイテムをスキャンしないと、画面上で..."
幅:   約70

Step 1: needed_lines = ceil(70/40) = 2
Step 2: ideal_line_width = 70/2 = 35
Step 3: 候補
  - 「、」(pos≈5): penalty 1 -- ideal=35 から距離30
  - 「、」(pos≈30): penalty 1 -- ideal=35 から距離5 ← 最適
Step 4: pos≈30 の「、」を選択
  score = |30-35| + 1*3 + 0 = 8

結果: "例えば、一定時間アイテムをスキャンしないと、\n画面上で..."
```

現在の `例えば、\n...` (左4文字) と比べて大幅に改善。

### 例3: カタカナ語保護 (現在 bad-split)

```
入力: "完璧に計算されたアルゴリズムが生身の..." (幅60, chars_per_line=40)

Step 1: needed_lines = 2
Step 2: ideal = 30
Step 3: 候補
  - カタカナ「ア」→ひらがな「が」境界 (pos≈28): penalty 4 (小区切り)
  ※ 「アルゴリズム」の途中は禁止 → 候補にならない
Step 4: pos≈28 を選択

結果: "完璧に計算されたアルゴリズムが\n生身の..."
```

現在の `アルゴリズ\nムが` のような単語途中切断を防止。

---

## 8. 受け入れ条件

| ID | 条件 |
|----|------|
| AC-1 | 既存の56テストを壊さない (分割関連テストの期待値は必要に応じて調整可) |
| AC-2 | 初期コーパスの bad-split 10件のうち、少なくとも7件以上が改善される |
| AC-3 | 初期コーパスの good 4件が悪化しない |
| AC-4 | カタカナ語途中、数字途中、括弧ペア内での分割が発生しない |
| AC-5 | `--balance-lines` なしの既定動作は後方互換を維持 |
| AC-6 | sample の `AI監視が追い詰める生身の労働.txt` で再検証し、手動修正箇所が減る |

---

## 9. 実装計画

| Step | 内容 | 成果物 |
|------|------|--------|
| 1 | `reflow_utterance()` のコア実装 | assemble_csv.py に関数追加 |
| 2 | 区切り候補列挙 (`_find_major_breaks`, `_find_minor_breaks`) | 既存の4辞書を2つに再編 |
| 3 | 禁止位置判定 (`_is_protected_position`) | カタカナ連続、数字連続、括弧ペア内 |
| 4 | `reflow_subtitles()` で統合呼び出し | split_long_utterances + balance をラップ |
| 5 | 既存テストの調整 + 新テスト追加 | コーパスの bad-split 例をテスト化 |
| 6 | sample 再検証 | CSV再生成 + コーパス再評価 |

---

## 10. リスク

| リスク | 軽減策 |
|--------|--------|
| テスト期待値の大量変更 | `--balance-lines` 時のみ新方式。既定動作は変更なし |
| 小区切りの判定精度 | Unicode カテゴリで判定。stdlib `unicodedata` のみ使用 |
| 過剰分割 (行数が増えすぎ) | `max_lines` で上限制御。現在と同じ |
| 大区切りがない超長文 | 小区切りフォールバック → それもなければ現在と同じ force split |

---

## 11. 現在の定数との対応

| 現在 | 新方式での位置づけ |
|------|------------------|
| `_LINE_BREAK_AFTER` | 大区切りに統合 |
| `_CLAUSE_BREAK_AFTER` | 大区切りに統合 |
| `_CLAUSE_BREAK_BEFORE` | 大区切り (接続句直前) に統合 |
| `_AGGRESSIVE_BREAK_AFTER` | 廃止。小区切り (文字種境界) で代替 |
| `_AGGRESSIVE_BREAK_AFTER_MARKERS` | 小区切り (マーカー句) に統合 |

4つの辞書 + 1つのタプル → **2つの辞書** (大区切り、小区切り) に整理。
