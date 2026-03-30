# S-5 Workflow Proof

S-5 の「読み上げ確認・字幕はみ出し修正」を、Python 側でどこまで事前に減らせるかを検証するための proof packet。
B-11 の証跡正本として使う。

---

## 目的

- YMM4 取込後に発生する S-5 修正を「例外処理」へ寄せられるかを確認する
- Python 側で次に直すべき改善点を、推測ではなく evidence から選ぶ
- GUI や YMM4 自動化へ飛ばず、L2 の改善余地を先に詰める

---

## 境界

| 項目 | 含む | 含まない |
|---|---|---|
| Python / CLI | `build-csv --max-lines --chars-per-line --stats` による事前警告、dry-run、統計確認 | YMM4 の自動操作、字幕配置そのものの制御 |
| YMM4 | 台本読込後の確認、残修正の観察と記録 | Python からの演出指定、.ymmp 編集 |
| 証跡 | 取込前の CLI 出力、取込後の残修正分類、次改善候補 | 本制作動画の量産、GUI 要件の拡張 |

---

## Actor / Owner

| 観点 | 内容 |
|---|---|
| actor | `assistant` が proof packet と L2 改善候補の整理を進め、`user` が YMM4 取込後の実観測を行う |
| owner artifact | 動画制作ワークフロー上の S-5 修正量の evidence |
| change relation | `direct` に近い `unblocker`。S-5 の残修正を減らす次改善を選ぶための根拠を作る |

---

## 受け入れ条件

| ID | 条件 | 合格の目安 |
|---|---|---|
| AC-1 | 1 件以上の transcript で proof を実行する | 入力名と日付が記録されている |
| AC-2 | 取込前に CLI 側の warning / stats を保存する | `--stats` の結果が残っている |
| AC-3 | 取込後の残修正を 4 区分以上で分類する | `辞書登録 / 手動改行 / 再分割したい長文 / タイミングのみ` が埋まる |
| AC-4 | 残修正が bulk rework か exception handling かを判定する | どちらかが明記される |
| AC-5 | 次の L2 改善候補を 1 件に絞る | 「何を直すと S-5 が減るか」が 1 文で言える |

---

## 実行手順

1. transcript を選び、S-3 で `build-csv --max-lines 2 --chars-per-line 40 --stats --dry-run` を実行する
2. warning と stats をこのファイルの evidence log に転記する
3. 同条件で CSV を出力し、YMM4 の台本読込を行う
4. S-5 の残修正をカテゴリ別に数える
5. 残修正が多い原因を「split 不足」「読みに問題」「YMM4 側テンプレート」「手動判断」のどれに近いか整理する
6. Python 側で次に直すべき候補を 1 件だけ選ぶ

---

## Evidence Log Template

### Run

| 項目 | 記録 |
|---|---|
| date | |
| transcript / source | |
| command | |
| chars-per-line | 40 |
| max-lines | 2 |

### Pre-import (CLI)

| 項目 | 記録 |
|---|---|
| total utterances | |
| overflow warnings | |
| unmapped speakers | |
| other notable warnings | |

### Post-import (YMM4)

| 区分 | 件数 | メモ |
|---|---:|---|
| 辞書登録 | | |
| 手動改行 | | |
| 再分割したい長文 | | |
| タイミングのみ | | |
| その他 | | |

### Assessment

| 項目 | 記録 |
|---|---|
| bulk rework or exception handling | |
| next L2 improvement candidate | |
| should stay in Python scope? | |
| should remain manual in YMM4? | |

---

## Initial Run — 2026-03-31

### Run

| 項目 | 記録 |
|---|---|
| date | 2026-03-31 |
| transcript / source | `samples/AI監視が追い詰める生身の労働.txt` |
| command | `uv run python -m src.cli.main build-csv "samples/AI監視が追い詰める生身の労働.txt" --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" --max-lines 2 --chars-per-line 40 --stats --dry-run` |
| chars-per-line | 40 |
| max-lines | 2 |

### Pre-import (CLI)

| 項目 | 記録 |
|---|---|
| total utterances | 57 |
| overflow warnings | 34 |
| unmapped speakers | 0 |
| other notable warnings | なし |
| content reduction check | 入力 3098 chars / 発話本文 2805 chars / 出力本文 2805 chars。差分は主に話者ラベルと改行で、本文削減は見られない |

### Post-import (YMM4)

| 区分 | 件数 | メモ |
|---|---:|---|
| 辞書登録 | 0 | 意外にも変な読み間違いはなし |
| 手動改行 | 約30 | 長文が中心。「、」「。」で終わる同一話者文で改行したいことが多い |
| 再分割したい長文 | 約30 | 手動改行とほぼ同じ山。1行16文字、2行32文字程度が実用目安 |
| タイミングのみ | 0 | タイミング関係の違和感はなし |
| その他 | 0 | なし |

### Assessment

| 項目 | 記録 |
|---|---|
| bulk rework or exception handling | bulk rework 寄り。57 発話中およそ30箇所で改行/再分割を検討したくなった |
| next L2 improvement candidate | 総表示幅だけでなく、読点・句点・カギカッコ付近を候補にした「行バランス重視の字幕分割」改善を検討する |
| should stay in Python scope? | Yes |
| should remain manual in YMM4? | YMM4 取込後の最終判断は手動のまま |

### Observed Notes

- 読み間違いがほぼ無いのは収穫で、S-5 の主因は辞書ではなく字幕改行だった
- 気になるのは文字数、句読点、カギカッコ、カタカナ語、および「ということ」の「というこ」で割れるような語中分割
- 単純な固定文字数よりも、全体を見ながら2行を均等に寄せる手動判断が実際には行われている
- `normalize -> assemble` の照合では、本文 2805 chars は出力でも維持されていた。今回の5分程度という尺感は、proof 上は「内容削減」より「テンポ感と改行品質」の論点としていったん扱う

---

## 分解案

| Block | 目的 | 期待する成果 |
|---|---|---|
| Block 1 | proof 条件と証跡テンプレートを固定する | このファイルと canonical docs の同期 |
| Block 2 | 1 件の実データで S-5 残修正を記録する | evidence log が 1 つ埋まる |
| Block 3 | evidence をもとに L2 改善を 1 件に絞る | 実装対象または rejected 理由が明確になる |

---

## やらないこと

- GUI を先に作って pain を説明した気になること
- YMM4 内部を Python から操作しようとすること
- 1 回も実データを見ないまま S-6 や別 frontier に飛ぶこと
