# B-15 Proposal: LLM prep packet for constrained rewrite and S-6 cue notes

## Why This Exists

S-5 の bulk subtitle pain は B-14 まででかなり減った。一方、最大 pain のもう一方である S-6 は依然として重く、さらに NotebookLM 台本には次の問題が残る。

- 聞き手と解説役の役割が途中で混線することがある
- 2 本の台本を 1 本の長い動画へ接続したい場合、つなぎの整合性を手で作る必要がある
- 背景・表情・BGM の下調べメモを人手で起こすのが重い

ここで欲しいのは「新しく台本を創作する機能」ではなく、NotebookLM 由来の既存台本を前提にした text-side 補助である。

## Value Path

| 観点 | 狙い |
|---|---|
| どこに効くか | S-2 後の台本整合性確認、S-6 の背景/演出メモ準備 |
| 何を減らすか | 手動での役割混線修正、台本同士の橋渡しメモ作成、背景/演出候補の下調べメモ |
| 手作業は何が残るか | 最終的な creative judgement、YMM4 内操作、採否判断、必要に応じたコピペ |
| なぜ今やるか | S-5 の bulk pain が一段落し、次の大きな pain である S-6 と transcript 整合性補助に焦点を移す自然なタイミングだから |

## Recommended Scope

### Phase 1: cue memo only (recommended)

- transcript 1 本を入力に取り、セクション分割と S-6 用の cue memo を text で返す
- 返す内容は、背景候補、表情候補、BGM/SE メモ、場面転換候補、注意点
- 出力は Markdown / JSON などの text artifact のみ
- YMM4 / `.ymmp` の編集はしない

### Phase 2: constrained rewrite (optional follow-up)

- transcript 1 本または 2 本を入力に取り、既存台本の整合性調整案を返す
- 対象は role consistency 修正、bridge 文案、冗長な接続の整理
- ゼロからの主台本生成はしない
- rewrite の採用は人間が判断する

## Proposal Scope

### やる

- LLM adapter の契約を text-only に固定する
- provider / SDK 境界 / output contract / evaluation を ADR draft と proposal packet に明文化する
- Phase 1 の最小実装対象を「cue memo only」に絞って approval を取りやすくする
- constrained rewrite は scope を定義するが、Phase 1 では未実装扱いにする

### やらない

- LLM による主台本生成
- `.ymmp` / YMM4 project 直接編集
- 画面効果や字幕配置の自動注入
- GUI 実装
- 画像生成、動画生成、音声合成

## Output Contract Draft

### Phase 1 output

- `summary`: 動画全体の要約
- `sections[]`: セクションごとの要約、開始目印、背景候補、表情候補、BGM/SE メモ
- `global_notes`: 全体を通しての演出上の注意
- `operator_todos`: 人間が確認すべき点

### Phase 2 output

- `rewrite_notes`: どこをどう整合させたか
- `bridges[]`: 2 本の台本をつなぐ候補文
- `role_fixes[]`: host/guest の混線候補
- `revised_transcript`: 採用候補としての text

## Workflow Insertion

| step | actor | owner artifact | note |
|---|---|---|---|
| S-2.5 | tool | text memo / revised transcript candidate | NotebookLM transcript を受ける |
| S-3 | assistant/tool | CSV | 採用する場合のみ revised transcript を CSV 化する |
| S-6 | user | YMM4 project | cue memo を見ながら背景・演出を判断する |

## Acceptance

| ID | 条件 |
|---|---|
| AC-1 | 既存の NotebookLM upstream 境界を壊さない |
| AC-2 | 出力は text artifact のみで、YMM4 / `.ymmp` の直接編集を行わない |
| AC-3 | Phase 1 は transcript 1 本で cue memo を生成し、実際の S-6 作業で使える |
| AC-4 | operator が「下調べメモ作成の何分が減ったか」を記録できる |
| AC-5 | Phase 2 を進める場合でも、ゼロ生成ではなく constrained rewrite に限定される |

## Risks

| リスク | 内容 |
|---|---|
| 境界逸脱 | cue memo から YMM4 direct edit へ滑りやすい |
| 過剰生成 | rewrite が主台本創作に近づく恐れがある |
| 評価曖昧化 | 「便利そう」で進み、実際に何分減ったかが残らない |
| 依存追加 | SDK 導入時に stdlib-only 前提が崩れる |

## Recommendation

次 frontier の recommended shape は次の通り。

1. `B-15` を `proposed` として FEATURE_REGISTRY に登録する
2. Phase 1 を `cue memo only` に絞って approval 判断を取る
3. `ADR-0004` で text-only boundary と SDK 判断条件を先に固める
4. constrained rewrite は Phase 2 候補として残し、Phase 1 の workflow proof 後に再承認する

## Minimal Ask

この packet があれば、次の判断はまず 1 点でよい。

- `B-15 Phase 1 (cue memo only) を次 frontier として approved にするか`
