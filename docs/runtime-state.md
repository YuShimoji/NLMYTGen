# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- lane: Advance
- slice: ロバスト性検証（別 NLM transcript）
- next_action: [別の NLM transcript で build-csv → YMM4 読込まで通す]
- 案件モード: CLI artifact

## 主成果物
- active_artifact: NLM transcript → YMM4 CSV → 動画1本完成への経路
- artifact_surface: CSV ファイル → YMM4 読込 → レンダリング結果
- last_change_relation: direct

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標（task-scout 計数 / Main session 更新）
- test_file_count: 0
- mock_file_count: 0
- impl_file_count: 0
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: なし
- last_verification_date: なし

## Evidence（CLI artifact mode）
- evidence_status: 未検証
- last_e2e_data: sample transcript（Phase 0〜4 完了）
- external_tool_verification: YMM4 読込未確認
- final_artifact_reached: No
- blocking_dependency: 別 NLM transcript でのロバスト性検証

## Authority Return Items
- 実 NLM transcript のバリエーション提供（ユーザー操作依存）
- YMM4 実読込確認（ユーザー操作依存）

## 一時補助物（作ったら登録。統合/削除したら除去）
# | ファイル/モジュール | 種別 | 削除条件 | 寿命 |
