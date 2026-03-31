# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- lane: Advance
- slice: B-15 done + C-07 done + C-08 done。GUI LLM 統合プロンプト+セットアップガイド作成済み
- next_action: ユーザーが Custom GPT or Claude Project に統合プロンプトを固定化。その後 B-16 (行内折り返し) に着手
- 案件モード: CLI artifact

## 主成果物
- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: direct (S-5 の主 pain だった字幕改行バランスへ直接効く opt-in 改善を実装した)

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標
- test_file_count: 7
- test_count: 67
- mock_file_count: 0
- impl_file_count: 9
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: `uv run pytest` 67 PASS (56 既存 + 11 B-15 新規)。B-15 トップダウン方式で sample を 94 行に再編、再帰的 reflow でoverflow 11件まで削減。C-07 v2 proof 完了、演出メモプロンプト確定
- last_verification_date: 2026-03-31

## Evidence（CLI artifact mode）
- evidence_status: 実データ通過（2件の transcript で CSV E2E 確認済み）。B-14 後の YMM4 visual evidence は未取得
- last_e2e_data: AI監視(57発話) を `--max-lines 2 --chars-per-line 40 --balance-lines` で再検証し、95 行 / overflow candidates 3 まで低減。YMM4 読込用 CSV も再生成済み
- external_tool_verification: YMM4 読込成功（2026-03-29、CSV形式）
- final_artifact_reached: Yes（CSV → YMM4 台本読込のパス）
- blocking_dependency: なし

## FEATURE_REGISTRY 状態サマリ (2026-03-31)

- done: 19件（A-01〜A-02, A-04, B-01〜B-15, C-07, C-08）
- approved: 0件
- proposed: 1件（B-16 行内折り返し制御）
- info: 2件（C-01, C-06）
- hold: 3件（A-03, E-01, E-02）
- quarantined: 3件（D-02, F-01, F-02）
- rejected: 7件（B-10, C-02, C-03, C-04, C-05, D-01, F-03）

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
- A-04（RSS）は再審査済みで done。D-02（背景動画取得）は quarantined のまま、境界と価値経路の個別再審査が済むまで進めない

## Authority Return Items

- C-07 + C-08 done。統合プロンプト + セットアップガイド作成済み (`docs/gui-llm-setup-guide.md`)。Custom GPT / Claude Project への固定化はユーザー作業
- 視覚系の方向確定: ストック素材検索ではなく茶番劇アニメ+図解の演出指示。C-07 v2 がその入口として機能
- B-16 行内折り返し: proposal 作成済み。視覚系と並行可能
- D-02: 方向転換。素材API検索 → 演出判断支援。再審査チェックリスト6項目は作成済みだが、方向が変わったため再評価が必要
- E-02: hold 継続
- F-01/F-02: quarantined 継続

## 既知の問題

- 直前 handoff は 53f3718 時点の内容で止まっており、後続 commit `8a1c710` で追加された canonical docs とその未充足状態は含んでいなかった
- E-02 は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで、実質的な効率化にならない (E-01 とセットでないと価値が出ない)
- D-02 / F-01 / F-02 は前セッションの汚染バッチ由来で、個別精査前に normal backlog として扱えない
- A-04 は実装済み・再審査済みだが、runtime/context の一部に旧 `quarantined` 記述が残っていたため handoff trust を要再同期
- B-14 後の追加観測では、長すぎる行は大幅に減り、全字幕が 3 行以内に収まる水準まで改善した。残 pain は bulk overflow ではなく、境界ケースの改行品質に移っている
- B-11/B-12/B-13/B-14 により、辞書や timing ではなく字幕改行が支配的な pain だと確認。B-14 後は `ー`、カギ括弧、数値+記号などの individual judgement が主で、次は heuristic を積み増すより corpus-based な例収集へ寄せる方が自然
- 別機能の feasibility を棚卸しした結果、次の本命候補は S-6 LLM adapter。E-01/E-02 は secondary、D-02/F-01/F-02 は引き続き quarantine 境界
- `prompt-resume.md` は作成済みだが、内容の正本は引き続き repo docs 側である

## 一時補助物（作ったら登録。統合/削除したら除去）
| ファイル/モジュール | 種別 | 削除条件 | 寿命 |
|---|---|---|---|
| (なし) | | | |
