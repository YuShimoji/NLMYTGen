# ADR-0004: LLM Text-Only Assist Boundary for Prep Packets

## Status
Accepted

## Context

S-5 の字幕改行 bulk pain は B-14 までで大きく減ったが、S-6 の背景・演出設定は依然として重い。
また、NotebookLM 由来台本には role consistency の揺れや、複数台本を 1 本に接続したい場面がある。

一方で、次の境界は既に accepted である。

- NotebookLM が upstream であり、LLM は主台本を生成しない (`ADR-0002`)
- Python は動画生成や `.ymmp` 直接編集を行わない (`ADR-0003`)

このため、LLM を導入するとしても「既存台本を前提にした text-only assist」に境界を固定する必要がある。

## Decision

もし LLM adapter を導入する場合、その責務は text-only assist に限定する。

- 入力は NotebookLM 由来の transcript / script / notes
- 出力は Markdown / JSON / plain text のみ
- 許可する用途は、section cue memo、role consistency の指摘、2 本の台本接続における constrained rewrite 候補
- 禁止する用途は、主台本のゼロ生成、`.ymmp` / YMM4 project 直接編集、画面効果の自動注入、画像/音声/動画生成

SDK の追加は自動承認しない。次の条件を満たした場合のみ別 block で実施する。

1. `B-15` もしくは後継 feature が explicit approval を得ている
2. provider と認証方式が決まっている
3. 実運用で何分削減するかの評価方法が定義されている
4. repo 内実装でやる理由が、外部 Automation / 手動コピペ運用より明確に強い

## Consequences

- Phase 1 の最小実装は cue memo 生成などの text artifact に寄せる
- constrained rewrite は許容されるが、主台本生成と混同しないよう scope を限定する
- `.ymmp` や YMM4 内データの direct edit は引き続き対象外
- SDK 導入前に、外部 Automation や manual-assisted path と比較した value path を説明する必要がある

## Alternatives Considered

### 1. LLM を全面禁止する

- 利点: 境界が単純
- 欠点: S-6 と transcript 整合性補助の自動化余地を捨てる

### 2. LLM に rewrite と cue 生成を広く任せる

- 利点: 省力化余地が大きい
- 欠点: 主台本生成や creative ownership の境界を壊しやすい

### 3. YMM4 / `.ymmp` に直接メモや演出を流し込む

- 利点: うまくいけば手作業が減る
- 欠点: 壊れやすく、ハマるリスクが高い。現時点では workflow proof がない

## Follow-Up

- `docs/verification/B15-llm-prep-packet-proposal.md` を approval packet として使う
- 承認された場合のみ、provider 選定と adapter interface を別 implementation block で扱う
