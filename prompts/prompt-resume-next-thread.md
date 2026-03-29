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

1. 台本を作成する
2. 台本を YMM4 に流し込む
3. YMM4 上での演出の自動指定や素材配置につなげる

補助線として重要なのは次です。

- 分割プレビューや設定調整の GUI
- YMM4 内部自動化に近づくテンプレート / `.ymmp` 方面の Unlock

逆に、今回は以下を主目的にしないでください。

- 新しい docs 台帳の追加
- sidecar JSON の拡張
- LLM を使った品質生成
- 他プロジェクト由来の知識の持ち込み

## あなたにやってほしいこと

以下を順に行ってください。

1. 現在の `runtime-state` / `project-context` / `FEATURE_REGISTRY` を照合し、今の正しい現在地を短く要約する
2. 前回セッションの逸脱点を、**repo ルール違反 / 未承認混入 / 本筋からのズレ** に分けて整理する
3. `FEATURE_REGISTRY` から、今の主線に最も近い候補を 3 つ選ぶ
   - 優先的に検討する候補:
     - `C-02` YMM4 演出テンプレート
     - `C-03` YMM4 `.ymmp` 直生成 or 調査
     - `F-01` 分割プレビュー GUI
4. 3 候補について、次を比較する
   - 完了すると何が動くようになるか
   - YMM4 内部自動化への距離
   - いまの repo 境界に収まるか
   - 承認が必要か
   - 実装コストと不確実性
5. 推奨案を 1 つ選び、**なぜそれが「本来着手するべき作業」なのか** を説明する
6. もし承認不要で進められるのが `B-10` の撤去・隔離・整理だけなら、そこだけ最小で進める
7. 新機能実装に進む条件が満たされていないなら、勝手に実装せず停止する

## 重要な判断基準

- `FEATURE_REGISTRY` は gate であって、ゴールではない
- `AUTOMATION_BOUNDARY` は整理資料であって、成果物そのものではない
- 今回優先すべきなのは **YMM4 側の自動化に近づく前進** であり、補助的な metadata の足し算ではない
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
