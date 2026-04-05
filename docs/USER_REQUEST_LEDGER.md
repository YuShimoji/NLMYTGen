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
- 2026-04-05: face は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class で扱う。broad な manual retry loop に戻さない。
- 推奨ロードマップ順は H-01 workflow proof → H-02 → H-04 → H-03。E-02 はその後に consumer として再評価する。

## 今後明文化すべきこと
- 視覚系タスク (背景動画・アニメーション・サムネイル) の具体的なアプローチと Python 責務境界
- B-16 行内折り返し制御の「1行/1ページ最大文字数から逆算する外殻」の仕様
- 素材取得系 (D-02 中心) の権利・取得元・受け取り境界
- GUI 候補 (F-01 / F-02) が workflow bottleneck を本当に減らすかの workflow proof
- Thumbnail strategy v2 の heuristic 定義 (具体数値優先、抽象煽り blacklist、pattern rotation 軸)
- Visual density score / Evidence richness score の定義、入力データ源、warning threshold
- H-01 brief の workflow proof 条件 (C-07 / C-08 で drift が減るか)

## 運用ルール
- 会話で一度出た要求のうち、次回以降も効くものをここへ残す。
- 単なる感想ではなく、仕様・設計・backlog に効くものを優先する。
