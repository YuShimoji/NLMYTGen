# Claude Code Resume Prompt — Corrective Advance

この repo は `NLMYTGen` です。作業開始時は **この repo 内だけ** を読んで再アンカーしてください。

## 最初に必ず読む順序

1. `AGENTS.md`
2. `.claude/CLAUDE.md`
3. `docs/runtime-state.md`
4. `docs/project-context.md`
5. `docs/FEATURE_REGISTRY.md`
6. `docs/AUTOMATION_BOUNDARY.md`
7. 必要に応じて `docs/WORKFLOW.md` / `docs/ARCHITECTURE.md` / `docs/PIPELINE_SPEC.md`

最初に以下の形式で全景確認を出してください。

`📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]`
`🏷️ 案件モード: CLI artifact`

## このセッションで絶対に外さないこと

- **この repo 以外の project-memory / docs / files を読まない。書かない。**
- HoloSync / NLMandSlideVideoGenerator / 他PJの memory を参照しない
- `.claude/CLAUDE.md` の `CLI artifact mode` を優先する
- docs 整備を Advance の主軸にしない
- 未承認機能を勝手に追加しない
- `B-10 (--emit-meta)` は **rejected**（コード除去済み）。復活させない
- `expression_hint` のような枝葉機能を足さない
- **Python での生成・レンダリングは全面禁止**（画像合成・.ymmp生成・演出指定を含む）
- YMM4 内部でやるべきことと、Python 側でやるべきことを混同しない
- Python の責務は**テキスト変換のみ**（CSV + テキストメタデータ文字列）

## 前回作業の問題点

前回は歩数の割に自走距離が短かった。理由は以下です。

1. docs 整備や補助物の追加に寄り、本筋の前進が細くなった
2. `--emit-meta` と `expression_hint` を未承認で混入させた
3. repo 外の memory 書き込みという境界違反があった
4. 「何を今やるか」より「整備しやすい作業」に流れた

今回の目的は、これを繰り返さず、**本来着手するべき作業に戻すこと**です。

## いま本来見るべき主線

ユーザーが欲しい主線は次です。

1. 台本を作成する (S-1〜S-3)
2. 台本を YMM4 に流し込む (S-4)
3. YMM4 上で動画を完成させる (S-5〜S-7) -- ここが最も工数がかかる
4. サムネイルを制作する (S-8) -- 非常に重要視されている

全工程は WORKFLOW.md (S-0〜S-9) に記載済み。Python (NLMYTGen) が担当するのは S-3 のみ。

逆に、以下を主目的にしないでください。

- 新しい docs 台帳の追加
- sidecar JSON の拡張
- LLM を使った品質生成
- 他プロジェクト由来の知識の持ち込み
- Python から YMM4 内部を制御する試み (.ymmp 生成・操作は原理的に不可能)

## あなたにやってほしいこと

以下を順に行ってください。

1. 現在の `runtime-state` / `project-context` / `FEATURE_REGISTRY` を照合し、今の正しい現在地を短く要約する
2. 前回セッションの逸脱点を、**repo ルール違反 / 未承認混入 / 本筋からのズレ** に分けて整理する
3. `FEATURE_REGISTRY` から、proposed/approved の候補を確認する
   - **注意:** C-02, C-03, C-04, C-05, D-01 は全て **rejected** (2026-03-30)。復活させない
   - 検討対象は proposed (A-04, D-02, E-02, F-01, F-02) と done の改善のみ
4. 候補について、次を比較する
   - 完了すると何が動くようになるか
   - ワークフロー全体 (S-0〜S-9) のどの工程を改善するか
   - いまの repo 境界に収まるか
   - 承認が必要か
   - 実装コストと不確実性
5. 推奨案を選び、**なぜそれが「本来着手するべき作業」なのか** を説明する
6. 新機能実装に進む条件が満たされていないなら、勝手に実装せず停止する

## 重要な判断基準

- `FEATURE_REGISTRY` は gate であって、ゴールではない
- `AUTOMATION_BOUNDARY` は整理資料であって、成果物そのものではない
- 今回優先すべきなのは **ワークフロー全体 (S-0〜S-9) の中で最も摩擦が大きい工程の改善** であり、補助的な metadata の足し算ではない
- `CLI artifact mode` では、最終成果物到達経路に近い前進を優先する
- docs を更新するなら、実装や判断に直接必要な範囲にとどめる

## 期待する出力形式

この順で返してください。

1. 全景確認
2. 現在地の要約
3. 前回セッションの問題点整理
4. 本来着手すべき作業候補 3 件
5. 推奨案 1 件
6. その場で進めてよい最小作業
7. 必要なら更新するファイル一覧

## 補足

- `B-10 (--emit-meta)` は `docs/FEATURE_REGISTRY.md` では `rejected` です（コード除去済み）。復活させないでください。
- `docs/runtime-state.md` の `Authority Return Items` と `project-context.md` の `HANDOFF SNAPSHOT` は必ず確認してください。
- もし `.ymmp` 調査が repo 内情報だけでは進まないなら、その事実を明示して止まってください。想像で仕様を作らないでください。
