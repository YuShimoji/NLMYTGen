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

---

## Operational Lock Run (2026-04-07)

P1 の「H-01 brief を運用固定」のため、既存 sample を使って運用手順を固定した。

### Run

| 項目 | 記録 |
|---|---|
| date | 2026-04-07 |
| transcript / source | `samples/AI監視が追い詰める生身の労働.txt` |
| packaging brief | `samples/packaging_brief_ai_monitoring.md` |
| C-07 input path | `docs/S6-production-memo-prompt.md`（brief を先頭制約として添付） |
| C-08 input path | `docs/S8-thumbnail-copy-prompt.md`（brief を先頭制約として添付） |

### Before / After Drift Check（運用固定）

| 観点 | before | after | 判定 |
|---|---|---|---|
| title が台本を侵食していないか | 台本側の論点が title を先に決めがち | `title_promise` を brief で先に固定 | 改善 |
| thumbnail が本文根拠を離れていないか | 抽象煽りへ流れやすい | `preferred_specifics` / `required_evidence` を必須参照 | 改善 |
| abstract hype へ流れていないか | banned 制約が弱い | `banned_copy_patterns` を毎回適用 | 改善 |
| opening が promise を早めに回収しているか | 冒頭が抽象化しやすい | `script_opening_commitment` を先頭チェック | 改善 |
| C-07 が required_evidence を拾えているか | 視覚回収対象が曖昧化 | brief の `required_evidence` を固定入力化 | 改善 |

### Assessment

| 項目 | 記録 |
|---|---|
| useful enough to keep using? | yes |
| strongest improvement | title / thumbnail / script の上流制約が 1 ファイルに統一され、判断の入口がぶれにくくなった |
| residual drift | GUI LLM rerun の before/after 差分は運用者実行時に追記が必要 |
| next improvement inside repo | `docs/verification/H01-packaging-orchestrator-ai-monitoring-dry-proof.md` に運用者実行の差分結果を加筆 |

### Strict Comparison Record (2026-04-07)

同一台本（`samples/AI監視が追い詰める生身の労働.txt`）で、
H-01 brief 制約なし/ありを strict 観点で比較した記録。
`after` 側の根拠は H-02 dry proof の実測値を採用した。

| 指標 | before（brief なし） | after（brief あり） | 判定 |
|---|---|---|---|
| promise 逸脱（title/thumbnail/script） | 発生しやすい（上流制約が分散） | `Brief Compliance Check` で観測可能 | 改善 |
| abstract hype 混入 | `ヤバすぎる` 系へ流れやすい | banned pattern 明示拒否（`docs/verification/H02-thumbnail-strategy-ai-monitoring-dry-proof.md`） | 改善 |
| opening 回収遅れ | abstract opening に寄りやすい | `script_opening_commitment` を明示入力化 | 改善 |
| 具体性（C-08 main copy） | 具体根拠の強制が弱い | 5案中4案が preferred specifics を使用（H-02 strict 記録） | 改善 |

strict 観点では、H-01 brief を毎回前置する運用を継続し、
次は GUI rerun の同条件比較を運用者追記で増やす。

### Strict Comparison Record (`s2_h01_strict_2026-04-08_a`)

同一台本（`samples/AI監視が追い詰める生身の労働.txt`）を固定し、
H-01 brief あり/なしの比較観点を再利用可能テンプレとして確定。

| 観点 | 判定ルール | 形式 |
|---|---|---|
| promise逸脱 | title/thumbnail/script の約束が一致しているか | yes/no |
| abstract hype | banned pattern が混入していないか | yes/no |
| opening回収 | opening で promise の主要根拠を回収しているか | yes/no |
| evidence回収 | required_evidence が本文か演出で拾われているか | yes/no |

運用固定: 今後の比較記録は上表の4観点のみで判定し、
主観メモではなく yes/no 差分で追記する。

---

## Operational Run (`p0_nextcycle_amazon_2026-04-10_a`)

P0 の次サイクル対象台本に対して、動画 1 本分の brief を新規作成し、
**brief 全文を台本全文より先に貼る**運用で C-07/C-08 の上位制約として利用する準備を固定した。

### Run

| 項目 | 記録 |
|---|---|
| date | 2026-04-09 |
| transcript / source | `samples/The Amazon Panopticon Surveillance and the Modern Worker.txt` |
| packaging brief | `samples/packaging_brief_p0_nextcycle_amazon.md` |
| C-07 input path | `docs/S6-production-memo-prompt.md`（1) brief 全文 → 2) 台本全文） |
| C-08 input path | `docs/S8-thumbnail-copy-prompt.md`（1) brief 全文 → 2) 台本全文） |

### Before / After Drift Check（運用固定）

| 観点 | before | after | 判定 |
|---|---|---|---|
| title が台本を侵食していないか | 台本側の語り口が title 方針を先決しやすい | `title_promise` を先頭制約として固定 | 改善 |
| thumbnail が本文根拠を離れていないか | 抽象訴求へ寄りやすい | `thumbnail_promise` と `preferred_specifics` を先に固定 | 改善 |
| abstract hype へ流れていないか | banned 制約未指定だと混入しやすい | `banned_copy_patterns` を brief から明示適用 | 改善 |
| opening が promise を早めに回収しているか | 一般論の導入になりやすい | `script_opening_commitment` で早期回収を固定 | 改善 |
| C-07 が required_evidence を拾えているか | 必須根拠の優先順位が曖昧化しやすい | `required_evidence` を先頭入力で固定 | 改善 |

### Assessment

| 項目 | 記録 |
|---|---|
| useful enough to keep using? | yes |
| strongest improvement | P0 次サイクル台本に対し、C-07/C-08 両方で同一 promise を上流固定できる運用になった |
| residual drift | GUI rerun の生成結果比較（yes/no 記録）は運用実行時に追記が必要 |
| next improvement inside repo | `H01-packaging-orchestrator-ai-monitoring-dry-proof.md` と同形式で nextcycle 台本の strict 比較行を追加する |

### Strict Comparison Record (`p0_nextcycle_amazon_2026-04-10_a`)

同一台本（`samples/The Amazon Panopticon Surveillance and the Modern Worker.txt`）で、
H-01 brief 制約なし/ありの比較観点を nextcycle 案件に適用した記録。

| 観点 | before（brief なし） | after（brief あり） | 判定（yes/no） | メモ |
|---|---|---|---|---|
| promise逸脱 | title/thumbnail/script の約束が分散しやすい | `title_promise` / `thumbnail_promise` を先頭制約で固定 | yes | `samples/packaging_brief_p0_nextcycle_amazon.md` を先頭投入 |
| abstract hype | 抽象煽りコピーが混入しやすい | `banned_copy_patterns` を先に適用 | yes | C-08 入力順を brief 先頭で固定 |
| opening回収 | 冒頭が一般論へ流れやすい | `script_opening_commitment` で早期回収を要求 | yes | C-07 への上流制約として明示 |
| evidence回収 | 必須根拠の優先度が曖昧になりやすい | `required_evidence` を固定して参照 | yes | 71.4% / 19億ドル / 9%増 / 制度名を明示 |

運用判定: **yes（4/4）**。本比較は「入力制約の適用確認」であり、GUI rerun 実出力の差分採点は別 run で追記する。

