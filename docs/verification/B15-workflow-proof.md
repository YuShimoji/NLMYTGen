# B-15 Workflow Proof

B-15 Phase 1 (`cue memo only`) が、S-6 の下調べメモ作成をどこまで減らせるかを検証するための proof packet。

---

## 目的

- transcript から cue memo を作る下準備を repeatable にする
- S-6 の背景・演出メモ作成が何分減るかを記録する
- LLM / Automation を使っても text-only boundary を守れるか確認する

---

## 境界

| 項目 | 含む | 含まない |
|---|---|---|
| repo 内 | `build-cue-packet` による packet 生成、role analysis、section seed 提案 | provider SDK 内蔵、YMM4 direct edit |
| 外部 LLM / Automation | cue memo の生成 | 主台本のゼロ生成、`.ymmp` 編集、画像/音声/動画生成 |
| YMM4 | cue memo を見ながら背景・演出を人間が設定 | Python / LLM からの直接操作 |

---

## Actor / Owner

| 観点 | 内容 |
|---|---|
| actor | `assistant/tool` が packet を生成し、`user` が外部 LLM/Automation と YMM4 で proof を実施する |
| owner artifact | S-6 用 cue memo と、その時短効果の evidence |
| change relation | `direct`。S-6 の下調べ負荷を直接減らすかの観測 |

---

## 受け入れ条件

| ID | 条件 | 合格の目安 |
|---|---|---|
| AC-1 | 1 件以上の transcript で packet を生成する | packet の入力名と日時が残る |
| AC-2 | cue memo を 1 回生成する | 出力 text が保存または転記される |
| AC-3 | 下調べ時間の before / after を記録する | 分単位の差分が残る |
| AC-4 | cue memo の有用/不要項目を分けて記録する | 「何が効いたか / ノイズだったか」が 1 文ずつある |
| AC-5 | 次に repo 内で直すべき点を 1 件に絞る | packet 粒度 / output contract / section seed のどれか 1 つ |

---

## 実行手順

1. transcript を選ぶ
2. `build-cue-packet` で packet を生成する
3. 外部 LLM / Automation に packet を渡して cue memo を得る
4. cue memo を見ながら S-6 の下調べを行う
5. before / after の時間差と、効いた要素・不要だった要素を記録する
6. 次に repo 内で直すべき点を 1 件に絞る

---

## Evidence Log Template

### Run

| 項目 | 記録 |
|---|---|
| date | |
| transcript / source | |
| packet command | |
| external LLM / Automation path | |

### Packet Quality

| 項目 | 記録 |
|---|---|
| utterance count | |
| section seed count | |
| role analysis looked correct? | |
| missing context | |

### Cue Memo Result

| 項目 | 記録 |
|---|---|
| summary quality | |
| section cues quality | |
| background cue usefulness | |
| emotion / BGM / transition usefulness | |
| operator_todos usefulness | |

### Time Comparison

| 項目 | 分 | メモ |
|---|---:|---|
| before: manual prep estimate | | |
| after: cue memo assisted prep | | |
| delta | | |

### Assessment

| 項目 | 記録 |
|---|---|
| useful enough to keep using? | |
| next improvement inside repo | |
| should remain text-only? | |
| should SDK integration wait? | |

---

## やらないこと

- cue memo proof の前に Phase 2 rewrite 実装へ飛ぶこと
- YMM4 / `.ymmp` direct edit に手を出すこと
- GUI を先に作って value path を曖昧にすること
