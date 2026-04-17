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
- 2026-04-16: X-2a 先行実地確認完了 → [X2A-haitatsuin-dryrun-proof-2026-04-16.md](verification/X2A-haitatsuin-dryrun-proof-2026-04-16.md)。配達員 ymmp dry-run で face 15/transition 3/motion 2 件の機械適用を確認、G-21 は当面不要判定（proposed 維持）。Phase 1-D Step 1 同時消化（palette → 2 キャラ face_map、55 パーツ全実在）。
- 2026-04-16: B-1 + B-3 完了。B-1 は [B1-e2e-test-regression-proof-2026-04-16.md](verification/B1-e2e-test-regression-proof-2026-04-16.md) observational close (legacy drift を pipeline が正しく捕捉、e2e_test archived 提案)。B-3 は [B3-production-reproof-2026-04-16.md](verification/B3-production-reproof-2026-04-16.md) で production.ymmp + CHABANGEKI IR で exit 0 / face_changes 139 (2026-04-13 実績 138 から +0.7%) / 決定性確認済。主軸「演出配置自動化の実戦投入」を production.ymmp で再実証、次は B-2 新規エピソード。
- 2026-04-16: B-2 haitatsuin 案件 着手 + 立ち絵表示不可を復旧 (復旧 B)。2026-04-13 commit `17339dd` で placeholder clone を指す migrated_tachie/ にパス migration されていたのを、samples/Mat/ 実パーツへ 15 パス書き換え → [HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](verification/HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md)。user 視覚確認後、face_map / overlay_map (reimu 6 表情) / 10 utterance IR / dry-run に進む。
- 2026-04-16: 視覚効果ツール選定 slice 起点整備。assistant 側 immediate 成果として [VISUAL_EFFECT_SELECTION_GUIDE.md](VISUAL_EFFECT_SELECTION_GUIDE.md)(4 類 × 3 ルート比較・エフェクト 111 種用途別再編・テンプレバンドル 5 種案・ハンズオン 5 ステップ) + [VISUAL_TOOL_DECISION.md](VISUAL_TOOL_DECISION.md)(7 問記入テンプレ) + [MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md)(素材運用ルール記入テンプレ) を新設。ユーザー作業は Step 1 (ツール決定 30 分) → Step 2 (素材ルール 30 分) → Step 3 (YMM4 テンプレ 5 種作成 2-3h) → Step 4 (registry 登録) → Step 5 (1 本 proof → P02 追記)。完了後 runtime-state の優先表で hold → done 昇格可。plan 正本 `C:/Users/PLANNER007/.claude/plans/splendid-popping-horizon.md`。`src/` 変更なし。
- 2026-04-16: **Canva 除外方針を固定**（ユーザー明示、当初からの方針）。視覚効果・サムネイル・作図の選択肢から Canva を除外し、既存 docs ([VISUAL_EFFECT_SELECTION_GUIDE.md](VISUAL_EFFECT_SELECTION_GUIDE.md) / [VISUAL_TOOL_DECISION.md](VISUAL_TOOL_DECISION.md) / [WORKFLOW.md](WORKFLOW.md) §S-8 / [THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md)) から Canva 推奨記述を除去。サムネイルは YMM4 内作成 + 将来 NLMYTGen 側で「素材置き換え自動化」機能を別途実装する前提。素材調達は いらすとや / Pixabay / Pexels + AI 生成（白背景書き出しで立ち絵・小物・背景、イメージイラスト範囲内）。VISUAL_TOOL_DECISION.md の Q1-Q7 全て記入済み（決定日 2026-04-16）。次は Step 2 ([MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md))。
- 2026-04-16: **立ち絵セットアップ非実施方針を固定** (ユーザー明示)。視覚効果 slice の Step 3 以降で「立ち絵を YMM4 上で新規設定 (キャラクター登録・AnimationTachie プラグイン設定) しタイムライン配置」の手順を踏まない。既存の `samples/Mat/新れいむ/` `samples/Mat/新まりさ/` 配下のパーツ・表情で十分。テンプレ化は既存立ち絵入り ymmp (haitatsuin_2026-04-12.ymmp 等) を別名複製して開いた状態で行う。MATERIAL_SOURCING_RULES.md の保存場所・命名・ライセンス・差し替え方針を全項目記入完了。
- 2026-04-16: **G-22 (Dual-rendering scene_presets) proposed 起票**。ユーザー要望「立ち絵での再現と、一枚絵にレンダリング後の素材でも両方で画面反映」を受け、(A) 立ち絵 TachieItem 経路と (B) YMM4 で書き出した立ち絵レンダリング PNG の overlay 経路を **両方サポートする dual-rendering 運用** を FEATURE_REGISTRY に追加。第一候補は **コード変更なし** (既存 G-13 overlay + overlay_map で完結)。使い分けは主要キャラ本編=(A)、背景キャラ・ワンシーン・サムネ素材=(B)。構想正本 [G22-dual-rendering-tachie-and-png-2026-04-16.md](verification/G22-dual-rendering-tachie-and-png-2026-04-16.md)。承認判定は視覚効果 slice Step 5 proof 後に (A)/(B) 併用実績から決定。関連更新: [VISUAL-TOOL-SELECTION-2026-04-16.md](verification/VISUAL-TOOL-SELECTION-2026-04-16.md) §4.2 に運用方針追記、Step 3 補助に PNG 書き出し手順追加。runtime-state.md の next_action を user 側再開地点として明確化 (YMM4 作業 → PNG 書き出し → registry 登録 → proof)。
- 2026-04-17: **B-2 haitatsuin 立ち絵視覚確認 NG**。user 報告「立ち絵全体が表示されていません。新規追加しても表示されなくなっています。参照フォルダは migrated_tachie になっているようです」。ymmp 本体は `verify_paths.py` で 15/15 実在 OK (migrated_tachie 参照 0 件)。原因は **YMM4 側キャラクター登録 (AnimationTachie プラグイン設定) が migrated_tachie/ を指している** と推定。NG 所見+復旧候補 3 案 (A YMM4 設定変更 / B migrated_tachie/ を実パーツで上書き / C ハイブリッド) を [HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](verification/HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 末尾に追記。Phase A (face_map / overlay_map / IR / dry-run) は立ち絵復旧まで**待機**。plan: `C:/Users/thank/.claude/plans/fluffy-greeting-panda.md`。
- 2026-04-17: **視覚効果 slice Step 3 ハンズオン補助 docs 2 件新設**。user が YMM4 作業に入ったときの手戻りを防ぐ目的で (1) [STEP3_YMM4_TEMPLATE_CHECKLIST.md](STEP3_YMM4_TEMPLATE_CHECKLIST.md) — 5 種テンプレ (skit_reaction_jump / board_list_entry / map_pan_zoom / mood_sepia_blur / intro_punch) 各エフェクトの parameter 初期値の目安 + チェックボックス作業リスト + 失敗パターン、(2) [STEP3_TACHIE_RENDERING_PIPELINE.md](STEP3_TACHIE_RENDERING_PIPELINE.md) — G-22 経路 B の透明 PNG 書き出し → overlay_map 登録 → validate-ir 検証までの手順。[MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md) §2-c-i に立ち絵レンダリング PNG の命名規約 (`{speaker}_{emotion}.png`、`_rendered` suffix は衝突時のみ) を追記。[VISUAL-TOOL-SELECTION-2026-04-16.md](verification/VISUAL-TOOL-SELECTION-2026-04-16.md) §5 と [NAV.md](NAV.md) §2 から索引。`src/` 変更なし。
- 2026-04-17: **B-2 haitatsuin CLI dry-run PASS (`b2_haitatsuin_dryrun_2026-04-17`)**。立ち絵発話中非表示問題は道 3 (B-2 dry-run proof 先行) で user 承認し、視覚表示と独立に CLI 経路を固定。face_map_bundles/haitatsuin.json を `migrated_tachie\` → `..\Mat\` 一括書き換え (36 パス) + smile/Mouth の `03.png` → `03b.png` 手動代替 + overlay_map 最小版 + 10 utt IR (face: serious 6 / smile 4。`neutral` は prompt contract 外のため smile へ置換)。結果 exit 0 / fatal 0 / face_changes 18 / transition 10 / motion 3。正本 [B2-haitatsuin-dryrun-proof-2026-04-17.md](verification/B2-haitatsuin-dryrun-proof-2026-04-17.md)、P02 追記済。
- 2026-04-17: **立ち絵発話中非表示問題は user 先行解決済みと判明**。道 1 diff で Items 差分ゼロを観測後、user 発言「既に修正した 4/12 をそのままコピーしたため差分はゼロ。立ち絵アイテム自体を修正後に台本再読み込みで全てのセリフに正常な立ち絵が適用されている」により確定。解決手順は (1) TachieItem (レイヤー 5/6) の設定を samples/Mat/ に修正、(2) YMM4 の台本再読み込み機能で全 VoiceItem の TachieFaceParameter を再構築。道 2/2'/E の実施は不要。本ブロックの全診断結果 (`verify_paths.py` 15/15 / TachieItem == VoiceItem 完全一致 / dry-run PASS) は修正後の正常状態に対する観測で整合。[HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](verification/HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 5 次追記。
- 2026-04-17: **face_map 6 表情拡張 + B-2 dry-run v2 で warning 6 件解消 (`b2_haitatsuin_dryrun_2026-04-17_v2`)**。samples/palette.ymmp を `extract-template --labeled --format json` で抽出、`D:\MovieCreationWorkspace\` → `..\Mat\` 変換後、既存 haitatsuin.json (3 表情) に **7 パターン追加** (魔理沙に surprised/thinking/angry/sad、霊夢に thinking/angry/sad。霊夢 surprised は palette 欠如で skip)。palette 未抽出の Other/Back は既存 neutral から継承、MISSING 0。IR も 6 表情分散版に再構築 (serious 3 / thinking 2 / sad 2 / surprised 1 / smile 1 / angry 1)。dry-run v2: exit 0 / face_changes **50** (+32) / warnings **4** (`FACE_PROMPT_PALETTE_GAP` ×4 と `FACE_LATENT_GAP` (魔理沙) と `FACE_SERIOUS_SKEW` を解消)。残 warning は霊夢 surprised (palette に追加する別作業) / neutral 保持 / idle_face / bg_map の 4 件、全 non-fatal。P02 に v1/v2 両方追記。生成物 [samples/_probe/b2/expand_face_map.py](samples/_probe/b2/expand_face_map.py) / [samples/_probe/b2/haitatsuin_ir_10utt_v2.json](samples/_probe/b2/haitatsuin_ir_10utt_v2.json)。
- 2026-04-17: **茶番劇 Group テンプレを主軸にする方針を固定**。配達員等の外部素材演者は `speaker_tachie` の `motion` と混同せず、**GroupItem テンプレート資産**として扱う。開発段階では **1 canonical template → 小演出テンプレ量産**、実制作では **template 解決 + fallback + 未自動化注記** を返す。G-20 は geometry helper、G-22 は補助経路、G-23 は `speaker_tachie` 専用へ位置づけ直す。正本 [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md)。

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
