# Evidence Richness Proof

> Date: 2026-04-06
> Sample: `AI監視が追い詰める生身の労働`
> Inputs: script + packaging brief + cue memo reference

- score_version: 0.1
- video_id: amazon_ai_monitoring
- total_score: 77
- band: acceptable

## Category Scores

| Category | Score | Notes |
|---|---|---|
| `number` | 3 | `71.4%`, `66%`, `1.61倍`, `気温+1度で9%増`, `19億ドル`, `2025年10月` があり、包装 promise を直接支える |
| `named_entity` | 3 | Amazon, `タイム・オフ・タスク`, UNI Global Union, カリフォルニア大学バークレー校, DSP が明示される |
| `anecdote` | 1 | 吸入器エピソードは強いが、以後の中盤・後半で human-scale anecdote が継続しない |
| `case` | 3 | 倉庫監視、路上インセンティブ、PR / 労組反応まで concrete case が複数ある |
| `study` | 3 | 労組調査、博士論文データ、ポーランド調査など expert framing が機能している |
| `freshness` | 2 | `2025年から2026年`, `2024年`, `2025年10月` があるため current relevance は見えるが、"なぜ今か" の一本化はやや弱い |
| `promise_payoff` | 2 | title promise は回収できているが、thumbnail-first な contrast (`71.4%` と `19億ドル`) は opening で同時に立ち上がっていない |

## Warnings

- `EVIDENCE_REQUIRED_WEAK`

## Best Supports

- `71.4%` が監視強度を即座に可視化する
- `タイム・オフ・タスク` が抽象論を制度名に落とす
- `19億ドル` が PR と現場実態のギャップを一撃で示せる
- `気温+1度で9%増` が人間の生理限界を無視する構造を具体化する

## Missing Or Weak Evidence

- opening 後も引っ張れる worker-scale anecdote が不足している
- current relevance は dates で見えるが、"なぜ今このテーマを扱うのか" の framing が opening ではやや分散する
- money-forward thumbnail を選ぶ場合、`19億ドル` の payoff が body 後半寄りで遅い

## Recommended Repairs

- script:
  - S2 か S3 に、もう一つ人間サイズの scene を追加する。例: `タイム・オフ・タスク` のカウントを見ながら体調不良やトイレを我慢する具体場面を 1 つ差し込む
  - opening か S1 終端で `2025年から2026年` の time anchor を短く言い切り、"今起きている問題" を一本化する
  - money contrast を強く使う場合は、S1 末尾か S2 冒頭で「後半で 19億ドルのPR投資も見る」と予告して payoff を前倒しする
- packaging:
  - サムネが `19億ドル` を前面に出す場合は、title か subcopy に `71.4%` か `タイム・オフ・タスク` を残し、 money-only hype にしない
  - human-cost を強く押すコピーを使う場合は、吸入器エピソードを opening で確実に見せる前提にする
  - "最新" や "今" を強く使うなら、説明文や冒頭ナレーションでも `2025年-2026年` の anchor を落とさない

## Pass Conditions

| Condition | Result | Notes |
|---|---|---|
| all 7 category scores assignable | pass | extra axes were not needed |
| at least one warning maps to a clear script repair | pass | anecdote weakness maps to adding one worker-scale scene |
| at least one warning maps to a packaging adjustment | pass | money-forward packaging needs a stronger early payoff plan |
| result explains why the promise feels weak | pass | weakness is not generic quality loss; it is late or thin payoff for specific packaging claims |

## Assessment

| Item | Result |
|---|---|
| useful enough to keep using | yes |
| strongest improvement | it pinpoints that the script is concrete overall but still under-serves human-scale continuity |
| residual drift | anecdote continuity and early payoff for `19億ドル` remain weaker than the best packaging version would want |
| next improvement inside repo | use this proof output as the repair gate for the next H-02 thumbnail workflow proof |
