# User Request Ledger
# ユーザーの継続要望・差分要求・backlog を保持する台帳。

## 現在有効な要求
- かなり先送りになった機能、実際には未完了なのに完了扱いになっている task、文書だけ存在して実体が弱い項目を包括的に是正する。
- ハンドオフに全コンテキストが本当に残っているか検証し、抜け漏れは明示して報告する。
- 痛点ドリブンで進める。FEATURE_REGISTRY の候補一覧から機械的に次タスクを選ばない。
- `docs/ai/*.md` が存在するなら、tool-specific helper docs より先に canonical rules として扱う。
- project-local canonical docs を先に読んで、既知文脈の再質問を避ける。
- 演出 IR + patch-ymmp パイプラインが実装完了。次は Custom GPT proof と実台本 E2E。
- 手動作業が重くならないよう調整する。微調整を重ねるのではなく目的と実効性を明らかにして効果的な開発プランを維持する。
- ユーザー作業が必要な場合、ハンズオンで解説する。
- face 関連は単発の修正ループではなく独立サブクエストとして閉じ、以後は failure class 単位でのみ再オープンする。
- サムネイル戦略に、抽象煽りより数値・年数・人数・割合・金額・固有名詞などの具体性優先を盛り込む。
- サムネイルは固定テンプレ連打を避け、pattern rotation を管理できるようにする。
- タイトル / サムネ / 台本の整合を中央制御する Packaging Orchestrator を設計し、台本側のタイトル侵食を止める。
- 動画内の視覚密度スコアと内容根拠スコアを定義し、制作判断とマーケ判断の両方に使えるようにする。
- 手動時間の計測は目的から外す。今後は時間差ではなく接続成立・失敗分類・差分証跡を優先する（2026-04-07）。

- 表情指定をテンプレ（YMM4 プリセット名）ベースに切り替える方式の調査・設計（2026-04-13 フィードバック: パーツ個別指定では「カスタム空白」になり実用性が低い）
- 体テンプレ蓄積と IR からの body_template 指定の将来設計（2026-04-13 構想: overlay/bg と同型のレジストリ + ImageItem 挿入）。**2026-04-15 起票完了**: FEATURE_REGISTRY **G-21 `proposed`**。茶番劇運用（配達員・消防員等の外部素材 ImageItem + ゆっくり頭 TachieItem 重畳）。X-2 先行実地確認後に `approved` 昇格判定

## 未反映の是正要求
- `approved` は「仕様定義済み + ユーザー承認済み」のみ。priority と status を混同しない。
- E-02 のような「テンプレート作成」という命題に引っ張られず、実際にどこへ入力され何が減るのかから価値検証する。
- NotebookLM / YMM4 / YouTube Studio の実 integration point を曖昧にしたまま仕様を進めない。

## Backlog Delta
- 2026-04-06: assistant 側の subquest を timeline edit まで拡張する方針を追加。主 frontier は H-01 のまま維持し、次段は G-11 slot patch → G-12 native-template measurement → G-13 overlay/se insertion の packet として扱う
- S-5 字幕はみ出しは B-15/B-16/B-17 で解決済み (トップダウン統合リフロー、91テストPASS)。
- S-6 トピック分析は、API SDK ではなく GUI LLM (Custom GPT / Claude Project 等) を優先する (2026-03-31 ユーザー希望)。C-07 / C-08 は done。次の frontier は packaging / orchestration / scoring への接続。
- 視覚系タスク (背景動画・アニメーション・サムネイル画像) に着手意向あり (2026-03-31)。字幕分割完了後に優先順位を判断。D-02 quarantined / D-01 rejected の再整理が前提。
- 汚染バッチ由来の D-02 / F-01 / F-02 は、個別再審査まで通常 backlog に戻さない。
- 2026-04-05: H-01 schema v0.1 を `docs/PACKAGING_ORCHESTRATOR_SPEC.md` に明文化。H-01 は approved、H-02〜H-04 は proposed backlog とする。
- 2026-04-06: H-02 schema v0.1 を `docs/THUMBNAIL_STRATEGY_SPEC.md` に明文化。H-02 は approved、C-08 は specificity-first / banned pattern / rotation recommendation を出力できる前提へ更新する。
- 2026-04-06: H-02 dry proof を `docs/verification/H02-thumbnail-strategy-ai-monitoring-dry-proof.md` に記録。C-08 には `Specificity Ledger` と `Brief Compliance Check` を追加し、strict proof では「5案中3案が preferred_specifics を使い、banned pattern を避けるか」の 1 点だけを見る。
- 2026-04-06: H-03 schema v0.1 を `docs/VISUAL_DENSITY_SCORE_SPEC.md` に明文化し、`docs/verification/H03-visual-density-ai-monitoring-proof.md` で AI監視 sample の dry proof を記録。visual stagnation risk と packaging promise の on-screen payoff を分けて warning 化できる状態にした。
- 2026-04-06: H-04 schema v0.1 を `docs/EVIDENCE_RICHNESS_SCORE_SPEC.md` に明文化。H-04 は approved とし、7軸 score・warning class・repair suggestion を正本化する。
- 2026-04-06: H-04 manual scoring proof packet を `docs/verification/H04-evidence-richness-manual-scoring-proof.md` に整備。実台本 1 本で warning を script/packaging repair に変換できるか検証できる状態にする。
- 2026-04-06: `AI監視が追い詰める生身の労働` を用いて H-01 dry proof と H-04 manual proof を記録。H-01 は `docs/verification/H01-packaging-orchestrator-ai-monitoring-dry-proof.md`、H-04 は `docs/verification/H04-evidence-richness-ai-monitoring-proof.md` を正本とし、その後 H-02/H-03 の dry proof まで進めたうえで、残る strict 未解決を H-02 GUI rerun proof に絞る。
- 2026-04-06: G-12 で fade-family `transition` route (`VoiceFade*` / `JimakuFade*` / `Fade*`) を ymmp_measure で回収できるようにし、repo-local contract を更新。非 fade / template-backed transition family のみを未確定として残す。
- 2026-04-08: 次以降の推奨プランを [runtime-state.md](runtime-state.md) 「次以降の推奨プラン (2026-04-08)」に固定（P0 Phase1 本番 1 本〜Parking motion）。HANDOFF / DECISION LOG を同期。
- 2026-04-07: G-18 で `se` の `AudioItem` 挿入を実装（`_apply_se_items`）。`SE_WRITE_ROUTE_UNSUPPORTED` は廃止。正本 [G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md)。
- 2026-04-06: G-13 を completed packet とし、`overlay` は deterministic `ImageItem` 挿入まで閉じ、`se` は route 不在を `SE_WRITE_ROUTE_UNSUPPORTED` で fail-fast 化する。timeline lane は broad retry loop に戻さない。
- 2026-04-05: face は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class で扱う。broad な manual retry loop に戻さない。
- 推奨ロードマップ順は 2026-04-06 rev.2 で刷新。packaging spec lane は一巡完了 (H-02 pass)。次フェーズは実制作の3大bottleneck (台本品質/演出配置自動化/視覚効果) に軸を移す。E-01/E-02 は制作パイプラインと完全分離。
- 2026-04-06: ユーザーフィードバックにより実制作ワークフローの自動化カバレッジを棚卸し。done 35件だが最重量工程 (演出配置・視覚効果・台本品質) が未自動化。runtime-state.md に工程別カバレッジと3大bottleneckの詳細を記録。project-context.md ROADMAP を方向転換版に全面刷新。
- 2026-04-15: メンテ並行委任 Prompt 4 件（H-01 brief / H-02 サムネ one-sheet / B-17 改行残差観測 / B-18 台本診断観測）を `docs/prompts/` に durable 化。別セッション・Custom GPT・user GUI 作業で再利用できる正本として分離し、[CORE-PARALLEL-HUB §7](verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md) から索引する構成に固定。

## 今後明文化すべきこと
- 台本品質保証の具体的アプローチ (NLM臭除去、話者混同修正、ゆっくり解説様式変換)
- 演出配置自動化の技術的アプローチと Python/YMM4 責務境界
- 視覚効果 (茶番劇風アニメ・図解アニメ・サムネイル) の実現手段
- B-16 行内折り返し制御の「1行/1ページ最大文字数から逆算する外殻」の仕様
- 素材取得系 (D-02 中心) の権利・取得元・受け取り境界
- GUI 候補 (F-01 / F-02) が workflow bottleneck を本当に減らすかの workflow proof
- Thumbnail strategy v2 の heuristic 定義 (具体数値優先、抽象煽り blacklist、pattern rotation 軸)
- Visual density score / Evidence richness score の定義、入力データ源、warning threshold
- H-01 brief の workflow proof 条件 (C-07 / C-08 で drift が減るか)
- H-02 の workflow proof 条件 (specificity-first へ寄り、abstract hype が減るか)
- H-04 の運用結果を何本か蓄積した時の warning threshold 見直し条件
- H-03 を将来 ymmp readback と接続するときの測定項目 (静止秒数、背景切替、overlay 数など)

## 運用ルール
- 会話で一度出た要求のうち、次回以降も効くものをここへ残す。
- 単なる感想ではなく、仕様・設計・backlog に効くものを優先する。
