# H-01 Packaging Orchestrator Workflow Proof

H-01 (`Packaging Orchestrator brief`) が、
台本・サムネイル・タイトルの drift をどこまで減らせるかを検証するための proof packet。

---

## 目的

- title / thumbnail / script の約束を 1 枚の central brief へ集約できるか確認する
- C-07 / C-08 が Packaging Orchestrator brief を上流制約として扱えるか確認する
- 「台本がタイトルを決めてしまう」「サムネが本文根拠を離れる」 drift を 1 件以上減らせるか確認する

---

## 境界

| 項目 | 含む | 含まない |
|---|---|---|
| repo 内 | Packaging Orchestrator brief の作成、proof packet、判定軸、sample 記録 | 最終タイトル決定、最終サムネイル決定 |
| GUI LLM | C-07 / C-08 出力を brief 制約つきで再生成 | 主台本ゼロ生成、画像生成、YMM4 direct edit |
| user | brief の妥当性判断、C-07 / C-08 出力の採否、最終 creative judgement | repo 内 schema 変更の単独管理 |

---

## Actor / Owner

| 観点 | 内容 |
|---|---|
| actor | `assistant` が brief schema / proof packet を整備し、`user` が GUI LLM 実行と drift 判定を行う |
| owner artifact | Packaging Orchestrator brief と、その drift 低減 evidence |
| change relation | `direct`。タイトル / サムネ / 台本の整合 drift を直接減らすかの観測 |

---

## 受け入れ条件

| ID | 条件 | 合格の目安 |
|---|---|---|
| AC-1 | 実台本 1 本で brief を作成できる | brief ファイル名と日時が残る |
| AC-2 | C-07 / C-08 の両方で brief を上流制約として使える | 入力手順が repeatable に残る |
| AC-3 | drift を 1 件以上減らせる | before/after で「減った drift」が具体的に 1 件以上ある |
| AC-4 | promise と required_evidence の整合チェックができる | alignment_check に対する yes/no 記録が残る |
| AC-5 | 次に repo 内で直すべき点を 1 件に絞る | H-02 / H-04 / H-03 のどれへ渡すかが明示される |

---

## 実行手順

1. 実台本を 1 本選ぶ
2. Packaging Orchestrator brief を作る
3. brief を台本の前に貼って C-07 を実行する
4. 同じ brief を台本の前に貼って C-08 を実行する
5. 以下を before / after で比較する
   - タイトル promise が本文根拠に支えられているか
   - サムネイルコピーが banned copy pattern に落ちていないか
   - C-07 が required_evidence を視覚回収対象として扱っているか
   - opening が script_opening_commitment を守っているか
6. drift が減った点と、まだ弱い点を 1 件ずつ記録する
7. 次に repo 内で進める frontier を 1 件に絞る

---

## Evidence Log Template

### Run

| 項目 | 記録 |
|---|---|
| date | |
| transcript / source | |
| packaging brief | |
| C-07 input path | |
| C-08 input path | |

### Before / After Drift Check

| 観点 | before | after | 判定 |
|---|---|---|---|
| title が台本を侵食していないか | | | |
| thumbnail が本文根拠を離れていないか | | | |
| abstract hype へ流れていないか | | | |
| opening が promise を早めに回収しているか | | | |
| C-07 が required_evidence を拾えているか | | | |

### Alignment Check

| チェック | yes/no | メモ |
|---|---|---|
| thumbnail promise を支える具体根拠が opening か body 前半にある | | |
| title promise が forbidden overclaim を踏み越えていない | | |
| 台本が title を決めるのではなく、brief の promise を本文で回収している | | |
| サムネコピーが banned_copy_patterns に該当しない | | |
| 導入が script_opening_commitment を守っている | | |

### Assessment

| 項目 | 記録 |
|---|---|
| useful enough to keep using? | |
| strongest improvement | |
| residual drift | |
| next improvement inside repo | |

---

## Sample Packet (AI監視)

この repo には、H-01 の sample packet として以下が揃っている。

| 種別 | ファイル |
|---|---|
| transcript | `samples/AI監視が追い詰める生身の労働.txt` |
| packaging brief | `samples/packaging_brief_ai_monitoring.md` |
| existing C-07 style output reference | `samples/AI監視が追い詰める生身の労働_cue_memo_received.md` |

---

## Sample Dry Assessment (2026-04-06)

まだ user 側の最終 creative judgement は未取得だが、
sample brief を基準に repo 内 artifact を照合すると、以下の改善仮説が強い。

| 観点 | brief なしで起きやすい drift | brief ありで期待できる補正 |
|---|---|---|
| opening | 抽象的な問題提起から入りやすい | `script_opening_commitment` により、吸入器エピソードか 71.4% を早期回収しやすい |
| thumbnail copy | 「ヤバすぎる」系の抽象煽りへ流れやすい | `preferred_specifics` と `banned_copy_patterns` により、71.4% / 19億ドル / 9%増へ寄せやすい |
| C-07 visual plan | 演出は出るが、何を必ず拾うべきかが薄くなりやすい | `required_evidence` により、数値・制度名・逸話を視覚回収対象として固定できる |
| title / body relation | タイトル案が本文の strongest evidence とズレやすい | `title_promise` と `alignment_check` により、promise と本文根拠のズレを点検できる |

### 暫定判定

- AC-1: pass。sample brief が存在する
- AC-2: pass。C-07/C-08 prompt docs は H-01 連携を明記済み
- AC-3: pending。GUI LLM 実行後の before/after 記録が必要
- AC-4: pass。alignment_check schema は定義済み
- AC-5: pending。workflow proof 後に H-02 / H-04 / H-03 のどれへ渡すか確定する

---

## やらないこと

- H-01 proof 前に H-02 / H-04 / H-03 を実装扱いにすること
- brief を最終タイトル決定器として扱うこと
- drift の観測なしに H-01 を done とすること
- packaging proof を理由に画像生成や YMM4 direct edit の境界を広げること

