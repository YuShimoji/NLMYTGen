# B-17 一文字改行残差分析（2026-04-28）

## Scope

- 対象: 字幕リフロー（B-17）で、YMM4 取込後に「1 文字だけ次行へ送られる」見え方が頻発する問題。
- 入力例: `samples/不動産DX_魔法の鍵とキュレーション.txt`
- 既存 CSV: `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv`
- 主眼: アルゴリズムを未実装扱いに戻さず、何が伴っていないかを切り分ける。

## Findings

1. **GUI default drift**
   - CLI / 運用手順は `--max-lines 2 --chars-per-line 40 --reflow-v2` を標準としている。
   - 一方で GUI の初期値 / 保存値は `Chars/Line=20` になっていた。
   - `chars_per_line` は「表示幅」なので、20 は日本語全角約 10 文字相当になり、2 行字幕としてはかなり狭い。GUI から作ると行数・WARN が大きく増える。

2. **YMM4 width calibration is not attached**
   - `display_width` は全角=2 / 半角=1 の近似で、YMM4 のフォント・字幕枠・解像度とは 1:1 対応しない。
   - 既存 CSV を機械的に見ると、明示的な 1 文字行は 0 件。ただし 1 行幅が 41〜42 の行があり、実画面上の許容量が 40 より狭い場合は YMM4 側の自動折り返しで 1 文字尾部になり得る。
   - つまり「明示改行が 1 文字を作っている」より、「生成時の幅モデルと YMM4 実表示幅がズレ、YMM4 側の自動折り返しが最後に 1 文字を押し出している」可能性が高い。

3. **Stats does not surface single-tail risk**
   - `build-csv --stats` は `estimate_display_lines > max_lines` だけを WARN にする。
   - 「行幅が実表示幅を 1〜2 display units だけ超え、YMM4 で 1 文字尾部になりやすい」リスクは別集計されない。
   - B-17 残差観測テンプレには `single_char_tail` 欄があるが、GUI / CLI stats の自動指標としては伴っていない。

4. **Regression test guard was too weak**
   - 既存テスト `test_never_emits_single_character_non_last_line` は `display_width >= 2` を見ていた。
   - 日本語 1 文字は display width 2 なので、名前に反して「全角 1 文字行」を防げていなかった。

## Local Measurement

`samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv`:

| assumed actual cap | rows over 2 lines | over-cap line segments | one-character tail risk |
| --- | ---: | ---: | ---: |
| 40 | 18 | 18 | 10 |
| 38 | 32 | 53 | 35 |
| 36 | 48 | 90 | 37 |
| 34 | 61 | 135 | 45 |
| 32 | 74 | 179 | 44 |
| 30 | 92 | 231 | 52 |

Interpretation:

- 現在の標準 `40` でも、候補不足の長文では 41〜42 幅の行が残る。
- 実際の YMM4 字幕枠が 38 以下なら、1 文字尾部リスクは急増する。
- GUI の `20` は標準値としては狭すぎる。今回の同一入力では 506 rows / overflow 163 rows まで増えた。

## Changes Made

- GUI 初期値 / 保存 fallback / repo default settings を `Chars/Line=40` に戻した。
- `WORKFLOW.md` / `GUI_MINIMUM_PATH.md` の GUI 手順も標準 `2 / 40` に揃えた。
- 1 文字行の回帰テストを `display_width >= 2` ではなく `len >= 2` に修正した。
- Follow-up: `--subtitle-font-scale PERCENT` を追加し、字幕フォント倍率に応じて `effective_chars_per_line = floor(chars_per_line * 100 / PERCENT)` を改行計算と stats に使うようにした。GUI からも `Subtitle Font Scale (%)` を指定できる。
- Follow-up: 改行字幕生成時に `YMM4 Subtitle Font Source` を選べるようにし、`.ymmp` 内の字幕 `FontSize` から倍率を自動推定できるようにした。CLI では `--subtitle-font-source-ymmp PATH` / `--subtitle-base-font-size N`。
- Follow-up: `--wrap-px` / `--measure-backend` / `--wrap-safety` を追加し、`display_width` ではなく計測器の幅で改行位置を決める opt-in 経路を追加した。`wpf` backend は Windows WPF `FormattedText` を使い、`eaw` backend は従来近似の fallback。

## Remaining Gap

- WPF 計測は YMM4 実表示に近づける opt-in 経路として実装済み。ただし YMM4 内部レンダラ完全一致ではないため、`wrap_safety` と YMM4 側の自動折り返し OFF/広め設定を併用する。
- `single_char_tail` の個別件数表示は未実装。現時点ではフォント倍率補正で実効幅を狭め、overflow 候補の見積もりに反映する。
- 現段階ではアルゴリズム全体の作り直しではなく、GUI 標準値・フォント倍率補正・YMM4 実表示の cap 対照を伴わせるのが最短。
