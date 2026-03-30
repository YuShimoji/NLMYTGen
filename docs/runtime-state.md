# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- lane: Advance
- slice: B-04 分割品質改善 (表示幅ベース) → S-6 LLM アダプター方式検討
- next_action: S-6 トピック分析の LLM アダプター仕様定義 (プロバイダー選定・アーキテクチャ設計)
- 案件モード: CLI artifact

## 主成果物
- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: direct (B-04 表示幅ベース分割改善)

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標
- test_file_count: 5
- mock_file_count: 0
- impl_file_count: 8
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: 全31テスト PASS (既存16 + 新規15)、実データ3モード動作確認
- last_verification_date: 2026-03-30

## Evidence（CLI artifact mode）
- evidence_status: 実データ通過（2件の transcript で CSV E2E 確認済み）
- last_e2e_data: AI監視(51行) + Panopticon(87行) — CSV 生成確認
- external_tool_verification: YMM4 読込成功（2026-03-29、CSV形式）
- final_artifact_reached: Yes（CSV → YMM4 台本読込のパス）
- blocking_dependency: なし

## FEATURE_REGISTRY 状態サマリ (2026-03-30)

- done: 11件（A-01〜A-02, B-01〜B-09, C-01）
- info: 1件（C-06: YMM4 手動工程の記録）
- proposed: 5件（A-04, D-02, E-02, F-01, F-02）
- hold: 2件（A-03, E-01）
- rejected: 8件（B-10, C-02, C-03, C-04, C-05, D-01, F-03 + PIL/画像合成）

## Python のスコープ制約（2026-03-30 確定）
Python の責務はテキスト変換のみ（CSV + テキストメタデータ）。
以下は全て禁止（rejected として記録済み）:
- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp 生成・操作（音声ファイル参照を含むため外部生成不可能）
- YMM4 テンプレート生成・演出指定
- YMM4 出力の模倣・プレビュー
- 動画レンダリング・音声合成

## 外部メディア取得の方針（2026-03-30）
- 取得機能（acquisition）と受け取り機能（receiving）は分離する
- 最終的に自動化したい（ユーザー指示）
- A-04（RSS）と D-02（背景動画取得）は proposed のまま

## Authority Return Items

- S-6 トピック分析の LLM アダプター方式: プロバイダー選定 (Anthropic / OpenAI / OpenAI互換)、アーキテクチャ設計が未決定
- 「stdlib のみ」制約の緩和: LLM SDK 追加には ADR が必要
- E-02 (YouTube メタデータ生成): 単体では価値が薄い。E-01 (API投稿) とセットで再検討
- GUI 技術選定（F-01/F-02）
- proposed 残4件 (A-04, D-02, F-01, F-02) の priority 確認

## 既知の問題

- E-02 は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで、実質的な効率化にならない (E-01 とセットでないと価値が出ない)
- proposed 5件は全て前セッション (B-10 混入時) に一括生成された提案。個別精査が不十分
- S-6 トピック分析: stdlib 制約内のパターンマッチ/NLP は精度不足 (30-60%) で実用性なし → LLM アダプター方式に転換予定

## 一時補助物（作ったら登録。統合/削除したら除去）
| ファイル/モジュール | 種別 | 削除条件 | 寿命 |
|---|---|---|---|
| (なし) | | | |
