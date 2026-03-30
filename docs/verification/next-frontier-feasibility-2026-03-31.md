# Next Frontier Feasibility Audit

## Scope

- date: 2026-03-31
- purpose: 字幕分割の bulk pain がほぼ収束した後、次に目処が立つ機能を比較する
- mode: feasibility only
- owner: `assistant`

## Current Situation

- 字幕分割は B-14 までで strong win。長すぎる行は大幅に減り、残課題は bulk overflow ではなく境界ケースの改行品質に移った
- そのため、次は字幕分割の heuristic を積み増すより、別機能の value path を検証するほうが自然

## Candidate Comparison

| candidate | current status | value path | blockers | feasibility now |
|---|---|---|---|---|
| S-6 LLM adapter | 未定義 | S-6 は最大 pain の一つで、背景・演出判断の下準備を text layer で補助できる可能性がある | provider 選定、SDK/stdlib 境界、出力 contract、評価方法が未決 | high |
| E-01 YouTube 投稿自動化 | hold | 投稿工程そのものを短縮できる | YouTube Data API 認証、資格情報管理、運用手順の整理が必要 | medium |
| E-02 metadata 生成 | hold | タイトル・説明・タグの叩き台を出せる | 単体ではコピペ先が変わるだけで bottleneck 改善が弱い | low (standalone) |
| D-02 背景動画取得 | quarantined | 素材探しの手間を減らす可能性はある | 権利、取得元 API、受け取り境界が未整理 | low |
| F-01/F-02 GUI | quarantined | 操作性は改善し得る | GUI が最短の価値経路か未証明。現在は quarantine | low |

## Why S-6 Is The Strongest Next Candidate

| point | rationale |
|---|---|
| user pain fit | docs 上でも S-5 と S-6 が最大 pain と明示されている |
| repo boundary fit | Python の責務である text 変換・補助情報生成に寄せれば境界を越えない |
| strategic value | 字幕分割のような局所改善ではなく、次の大きな効率化候補になり得る |
| current gap | 「stdlib 制約では精度不足、LLM adapter 方式に転換予定」までは決まっており、残りは設計確定だけ |

## S-6 Feasibility: What Must Be Decided

| area | decision needed | note |
|---|---|---|
| provider | OpenAI など、どの LLM provider を使うか | repo にはまだ provider 決定がない |
| dependency boundary | stdlib のみを緩和して SDK を入れるか | docs 上で ADR 必須とされている |
| output contract | 何を返すか | 例: 背景候補、演出メモ、セクションごとの cue など |
| operator workflow | 出力をどこで使うか | YMM4 を自動操作せず、人間判断の補助に徹する必要がある |
| evaluation | 良し悪しをどう測るか | 実動画 1 本分の下準備が楽になるかで見るのが自然 |

## Minimal Viable Shape For S-6

- transcript / script を入力に取る
- セクション単位の演出メモまたは背景候補を text として返す
- YMM4 の操作は行わない
- 1 本の動画について「人間の下調べメモを何分減らせたか」で評価する

## E-01 / E-02 Assessment

| item | assessment |
|---|---|
| E-02 only | 依然として弱い。YouTube Studio へのコピペが残るだけで、最大 pain を動かしにくい |
| E-01 + E-02 | セットなら成立余地はある。ただし今の主 bottleneck ではない |
| recommended timing | S-6 の feasibility を見たあとで十分 |

## Recommendation

1. 次の本命候補は `S-6 LLM adapter` とする
2. ただし、いきなり実装ではなく `spec + ADR + value path packet` を先に作る
3. `E-01/E-02` は secondary candidate として維持し、S-6 のあとに再比較する
4. `D-02`, `F-01`, `F-02` は quarantine を崩さない

## Minimal Ask For Next Approval

次に必要な判断は 1 点に絞れる。

- `S-6 LLM adapter の spec/ADR packet を次 frontier として進めるか`
