# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- lane: Advance
- slice: B-15 / B-16 はともに proof positive。B-16 rerun でも対象区間の絞り込みは改善したため、B-16 は収束候補として扱い、次候補を `asset brief` 側へ寄せる段階
- next_action: B-17 `Asset brief packet` を `proposed` として formalize したので、次は approval 判断に必要な最小差分だけを示す
- 案件モード: CLI artifact

## 主成果物
- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: unblocker (B-16 rerun 結果を固定し、次候補へ安全に接続する判断材料を整えた)

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標
- test_file_count: 7
- mock_file_count: 0
- impl_file_count: 9
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: B-16 diagram brief の初回 proof で、diagram planning は 15 分想定から 3 分程度へ短縮、delta は 12 分。レスポンス品質も 3 図構成・goal / must_include / avoid_misread が良好。bundle 拡張後は `build-diagram-packet --bundle-dir samples` で rerun prompt / diff template / quickstart / baseline notes を含む 7 ファイル生成を確認し、`TMPDIR=/tmp TMP=/tmp TEMP=/tmp .venv-linux/bin/python -m pytest tests/test_diagram_brief.py` は 4 passed、full suite は 65 passed。bare の `python3 -m pytest` は現シェルでは未解決
- last_verification_date: 2026-03-31

## Evidence（CLI artifact mode）
- evidence_status: 実データ通過（2件の transcript で CSV E2E 確認済み）。B-14 後の YMM4 visual evidence は未取得
- last_e2e_data: AI監視(57発話) を `--max-lines 2 --chars-per-line 40 --balance-lines` で再検証し、95 行 / overflow candidates 3 まで低減。YMM4 読込用 CSV も再生成済み
- external_tool_verification: YMM4 読込成功（2026-03-29、CSV形式）
- final_artifact_reached: Yes（CSV → YMM4 台本読込のパス）
- blocking_dependency: なし

## FEATURE_REGISTRY 状態サマリ (2026-03-31)

- done: 16件（A-01〜A-02, A-04, B-01〜B-14）
- approved: 2件（B-15, B-16）
- proposed: 1件（B-17）
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

- B-16 `Diagram brief packet`: approved と初手実装、初回 proof まで完了。次は contract をさらに絞るかを見極める
- 「stdlib のみ」制約の緩和: LLM SDK 追加には ADR が必要
- E-02 (YouTube メタデータ生成): hold。単体では価値が薄く、E-01 または別 integration point とセットで再検討
- quarantined 項目 (D-02, F-01, F-02): 通常候補に戻す前に個別再審査が必要
- GUI 技術選定は F-01/F-02 の価値証明後に行う

## 既知の問題

- 直前 handoff は 53f3718 時点の内容で止まっており、後続 commit `8a1c710` で追加された canonical docs とその未充足状態は含んでいなかった
- E-02 は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで、実質的な効率化にならない (E-01 とセットでないと価値が出ない)
- D-02 / F-01 / F-02 は前セッションの汚染バッチ由来で、個別精査前に normal backlog として扱えない
- A-04 は実装済み・再審査済みだが、runtime/context の一部に旧 `quarantined` 記述が残っていたため handoff trust を要再同期
- B-14 後の追加観測では、長すぎる行は大幅に減り、全字幕が 3 行以内に収まる水準まで改善した。残 pain は bulk overflow ではなく、境界ケースの改行品質に移っている
- B-11/B-12/B-13/B-14 により、辞書や timing ではなく字幕改行が支配的な pain だと確認。B-14 後は `ー`、カギ括弧、数値+記号などの individual judgement が主で、次は heuristic を積み増すより corpus-based な例収集へ寄せる方が自然
- 別機能の feasibility を棚卸しした結果、次の本命候補だった `B-15 LLM prep packet` は Phase 1 を approved に進め、初手の `build-cue-packet` を実装した
- sample packet (`_cue_packet.md` / `_cue_packet.json`) を生成済みで、次はこの artifact を使った workflow proof に進める
- sample proof 雛形 (`_cue_workflow_proof.md`) と実 cue memo / 初回観測が揃い、残論点は contract 改善に移った
- B-15 rerun まで positive だったため、次の論点は packet 自体よりも、素材選定・図作成・フリー素材探索・動画素材の尺つなぎをどう text-only 支援へ分解するかに移った
- ユーザー承認により B-16 を `approved` に進め、`build-diagram-packet` の初手実装を追加した。diagram brief の初回 proof では 15 分想定から 3 分程度へ短縮し、次の判断点は contract をさらに絞るかどうかである
- `build-diagram-packet --bundle-dir` は workflow proof に加えて rerun prompt / rerun diff template / quickstart / baseline notes も自動生成するようになり、B-16 rerun の手動準備を sample 固有の追記なしで再現しやすくなった
- `docs/verification/development-plan-reset-2026-03-31.md` を追加し、次は B-16 rerun 回収 → B-16 収束判断 → `asset brief` / `search query brief` 比較、という順で進める方針を固定した
- `docs/verification/asset-vs-search-brief-comparison-2026-03-31.md` を追加し、B-16 後の本命候補は現時点では `asset brief` が優勢、ただし `search query brief` に反転する条件も明記した
- B-16 rerun では、導入を単独図にせず `S1-S2` の監視構造として統合し、背景で足りる区間をさらに外せた。大きな追加 tweak なしで収束候補とみなせる
- `docs/verification/asset-brief-proposal-draft-2026-03-31.md` を追加し、次候補を `asset brief` として proposal 化するための下書きを作成した
- `docs/verification/B17-asset-brief-proposal.md` を追加し、B-17 `Asset brief packet` を `proposed` として formalize した
- pytest は `requirements-dev.txt` と uv ベースの Linux venv で再現確認できた。repo 直下の `.venv` は Windows 形式のため、WSL ではそのまま使えない
- `~/.local/bin/uv` を使えば Linux 側 venv を切って `pytest` を再現できるが、bare の `python3 -m pytest` は現シェルでは未解決
- `prompt-resume.md` は作成済みだが、内容の正本は引き続き repo docs 側である

## 一時補助物（作ったら登録。統合/削除したら除去）
| ファイル/モジュール | 種別 | 削除条件 | 寿命 |
|---|---|---|---|
| (なし) | | | |
