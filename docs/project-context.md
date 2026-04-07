# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現フェーズ: 方向転換中。Production E2E 実証済み、packaging spec (H-01〜H-04) 一巡完了、timeline (G-11〜G-13) 完了。2026-04-06 フィードバックにより、実制作の3大bottleneck (台本品質/演出配置自動化/視覚効果) に軸を移す。詳細は ROADMAP UPDATE (2026-04-06 rev.2) 参照
- 直近の状態 (2026-04-05):
  - G-06 Production E2E: 60 VoiceItem / 28 IR utterance (row-range) / character-scoped face_map → face 133 changes / YMM4 visual proof OK
  - G-07 idle_face: 待機中表情の TachieFaceItem 挿入。28 件挿入 + carry-forward 動作確認
  - bg section 切替 proof: 2 ラベル (van_dashboard_ai + dark_board) で BG added 2 / YMM4 確認 OK
  - extract-template --labeled: palette.ymmp → character-scoped face_map (魔理沙 6 + 霊夢 5 = 11 表情)
  - row-range: IR 28 発話 ↔ CSV 60 行の粒度差を row_start/row_end で吸収
  - face completion hardening: `validate-ir` が `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_PROMPT_PALETTE_*` / `FACE_LATENT_GAP` を分類し、`apply-production` は row-range unmatched/uncovered・validation error・fatal face patch warning で fail-fast
  - H-01 Packaging Orchestrator brief: `docs/PACKAGING_ORCHESTRATOR_SPEC.md` v0.1 を追加。C-07/C-08 が参照する central brief schema を定義
  - H-02 Thumbnail strategy v2: `docs/THUMBNAIL_STRATEGY_SPEC.md` v0.1 を追加。specificity-first / banned pattern / rotation policy / output contract を定義
  - H-04 Evidence richness score: `docs/EVIDENCE_RICHNESS_SCORE_SPEC.md` v0.1 を追加。7軸の category score、warning class、repair suggestion を定義
  - H-04 proof packet: `docs/verification/H04-evidence-richness-manual-scoring-proof.md` を追加。1 本の実台本で score と repair action を結びつける実行単位を整備
  - H-01 workflow proof packet: `docs/verification/H01-packaging-orchestrator-workflow-proof.md` を追加。sample brief / cue memo / alignment check を束ねた実行手順を整備
  - H-01 dry proof: `docs/verification/H01-packaging-orchestrator-ai-monitoring-dry-proof.md` により、AI監視 sample で brief が opening / title / thumbnail / cue memo の共有契約として機能することを repo-local artifact ベースで確認
  - H-02 dry proof: `docs/verification/H02-thumbnail-strategy-ai-monitoring-dry-proof.md` により、AI監視 sample で specificity-first / banned pattern / rotation recommendation / brief compliance を dry proof し、C-08 prompt に `Specificity Ledger` と `Brief Compliance Check` を追加
  - H-03 Visual density score: `docs/VISUAL_DENSITY_SCORE_SPEC.md` v0.1 を追加。7軸の visual density score、warning class、repair suggestion を定義
  - H-03 dry proof: `docs/verification/H03-visual-density-ai-monitoring-proof.md` により、AI監視 sample で visual stagnation risk と promise visual payoff を warning 化し、S2/S4 の flat risk を repair に変換できることを確認
  - H-04 manual proof: `docs/verification/H04-evidence-richness-ai-monitoring-proof.md` により、AI監視 sample を total 77 / `acceptable` と採点し、warning を anecdote continuity と late payoff の repair に変換できることを確認
- G-12 measurement packet: `docs/verification/G12-timeline-route-measurement.md` と `samples/timeline_route_contract.json` を追加。profile ベースの route contract で current corpus の `motion` / `bg_anim` を固定し、fade-family `transition` route (`VoiceFade*` / `JimakuFade*` / `Fade*`) も mechanical に回収できる状態まで更新
  - G-13 overlay / se insertion packet: `docs/verification/G13-overlay-se-insertion-packet.md`。`overlay` は deterministic `ImageItem` 挿入。`se` は G-18 で `AudioItem` 挿入まで拡張（旧 `SE_WRITE_ROUTE_UNSUPPORTED` は廃止）
  - packaging frontier packet: H-01〜H-04 schema + dry proof 記録済み。H-02 strict GUI rerun proof は 2026-04-06 pass で閉じた
  - `uv run pytest`: 220 passed / 3 xpassed
  - B-12 行バランス重視の字幕分割を実装。`--balance-lines` を追加し、2行字幕向けに自然な改行を opt-in で挿入できるようにした
  - B-12 検証: `build-csv --max-lines 2 --chars-per-line 40 --balance-lines --stats --dry-run` で実データ preview を確認。CSV 1行内の改行保持テストも追加
  - B-12 post-import 再観測: 手動改行 10 / 再分割したい長文 15 / 不自然な単語分割 5。`。` での改行は効いたが、句読点の少ない長文と 1 文字最終行が残った
  - B-13 を実装。`--balance-lines` の内部改善として、句読点が少ない長文の clause-aware split fallback と widow/orphan guard を追加
  - B-13 検証: `uv run pytest` 54 PASS。sample dry-run では 57 発話 → 62 行に再編され、長い一文の一部が節分割されることを確認
  - B-13 post-import 再観測: 手動改行 5 / 再分割したい長文 10 / 不自然な単語分割 5。減りはしたがまだ多く、長い一文が 1 字幕に残るケースは未解決
  - B-14 を実装。複数文発話の中にある単一長文も sentence ごとに再展開し、aggressive clause chunking fallback を追加
  - B-14 検証: sample dry-run では 57 発話 → 95 行に再編、overflow candidates は 3 件まで低減
  - B-14 追加観測: `、` 起点の分割強化により長すぎる行はかなり減り、全字幕は 3 行以内に収まる水準まで改善。残課題は `ー`、`「」`、`202/4` のような数値+記号折り返しなど、境界ケースの改行品質へ移った
  - feasibility audit: 字幕分割以外の候補を再棚卸しし、次の本命候補は S-6 LLM adapter、E-01/E-02 は secondary、quarantine 群は据え置きと整理
  - E-02 (YouTube メタデータ生成): 仕様検討の結果、hold へ移動。単体では価値薄
  - D-02 / F-01 / F-02: 汚染バッチ由来として quarantined のまま
  - C-01 (YMM4 台本読込): Python 機能ではなく確認済み手動工程として info へ整理
  - FEATURE_REGISTRY: done 16 / info 2 / hold 3 / quarantined 3 / rejected 7
  - 8a1c710 で追加された canonical docs は handoff に未反映だったため、今回実内容で補完
  - `docs/ai/*.md` を canonical rules として入口に昇格し、resume prompt は補助に降格
  - `prompt-resume.md` を追加し、docs-only resume packet を repo 内で完結させた
  - Python のスコープは「テキスト変換のみ」で確定済み
  - 動画形式: ゆっくり解説系スタンダード (プロジェクト開始時から不変)
  - サムネイル: YMM4 テンプレートの文字・画像入れ替えで手動制作。非常に重要

---

## ACTIVE ARTIFACT
- Active Artifact: NLM transcript → YMM4 CSV → 演出 IR → ymmp 後段適用 → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → IR (Custom GPT) → patch-ymmp → 演出設定 → レンダリング
- 現在のスライス: face・timeline・H-02/H-03/H-04 を completed として固定。主 frontier は H-01 運用固定と実制作3大bottleneck（`docs/runtime-state.md` 開発プラン参照）
- 成功状態: face+bg 限定の全パイプライン E2E が通り、Level 3 (半自動制作ライン) に到達すること

---

## CURRENT LANE
- 主レーン: Advance（実制作 bottleneck 直接軽減）
- 今このレーンを優先する理由: face・timeline・packaging 採点の mechanical 束は揃った。残る重さは台本→手動配置→視覚効果の人間工程のため、レーンを実制作側へ移す

---

## RECOMMENDED ROADMAP (2026-04-05)

### Phase 0: Tier 3 安定化を先に閉じる
- G-10 を前提に、Custom GPT Instructions v4 差し替えと palette 不足ラベル追加を先に完了する。
- 理由: packaging / marketing を強めても、演出基盤の face/bg 適用が不安定だと downstream の比較がノイズ化するため。

### Phase 1: Packaging の中央制御を作る
- 第一着手は H-01 Packaging Orchestrator brief。
- ここで title promise / thumbnail promise / audience hook / required evidence / forbidden overclaim / alignment check を 1 つの brief に束ねる。
- 理由: 現在の主問題は「良いコピーが出ない」ことより、「台本側がタイトルを侵食し、判断主体が分散する」ことにあるため。
- 2026-04-05 時点で schema v0.1 は定義済み。次に必要なのは、C-07/C-08 実運用で drift が減るかの workflow proof。
- 2026-04-06 時点で workflow proof packet も整備済み。次に必要なのは user 実行による before/after drift 記録。

### Phase 2: サムネ戦略を H-01 配下で強化する
- 第二着手は H-02 Thumbnail strategy v2。
- 具体数値・固有名詞・年数・割合・金額など本文根拠のある具体性を優先し、抽象煽りテンプレへの依存を下げる。
- 同時に構図 / 表情 / 配色 / コピー型の rotation を定義し、固定パターン連打を避ける。

### Phase 3: 内容の強さを採点できるようにする
- 第三着手は H-04 Evidence richness score。
- 逸話 / 具体事例 / 数値 / 学術知 / 最新情報のどれが弱いかを可視化し、サムネやタイトルの promise を本文が支えられているかを見る。
- 理由: 先に内容根拠の診断軸を持たないと、H-02 が click-first に偏るため。

### Phase 4: 視覚密度を診断する
- 第四着手は H-03 Visual density score。
- 初期版は IR / section plan / bg_map / template 使用状況から proxy 算出し、背景切替・静止継続・情報埋め込み・演出配分を warning 化する。
- 理由: これは有効だが、H-01/H-02/H-04 より bottleneck 直撃度が一段低く、先に中央制御と内容側 gate を作る方が効率が高い。

### Phase 5: 配信 metadata は最後に再評価する
- E-02 は H-01/H-02/H-04 の出力を受ける consumer として再評価する。
- 単体で先に進めない。Packaging brief と evidence gate がない metadata 生成は、再び「コピペ先が変わるだけ」の弱い value path に戻るため。

### Deferred / Not First
- F-01/F-02 GUI は引き続き quarantine。H-01〜H-04 の運用で bottleneck が本当に減るか見るまでは戻さない。
- D-02 は主軸に戻さない。素材取得より、何を見せるか / 何を約束するか / 何が足りないかの判断支援が先。

---

## ROADMAP UPDATE (2026-04-06 rev.2)

This section supersedes all previous roadmap blocks.

### 現状認識 (2026-04-06 ユーザーフィードバックに基づく方向転換)

done 35件の大半はテキスト変換パイプラインと spec/proof 整備に集中しており、
実際の動画制作ワークフローで最も重い工程が未自動化のままである。
packaging spec (H-01〜H-04) は一巡完了したが、それは判断支援フレームワークであり、
実制作の手間を直接軽減するものではない。

**実制作の 3大 bottleneck (ユーザー特定):**

1. **台本品質保証** — NotebookLM 出力はそのまま使えない。ゆっくり解説様式への変換、聞き手/解説の話者混同修正、NLM臭の除去、YT視聴者向け調整が毎回必要。台本品質は演出IR品質にも連鎖する (台本が曖昧 → IR も曖昧)
2. **演出配置の自動化** — 最重量工程。IR を生成するところまでは来ているが、IRの通りにYMM4上で素材を配置する作業が全て手動。素材調達、レイアウト、タイミング制御、アニメーション設定を含む。現状の patch-ymmp は face/bg/slot/overlay のみで演出全体の自動配置には程遠い
3. **視覚効果** — サムネイルを1枚も完成させていない。茶番劇風アニメ/図解アニメがゼロ。画像表示のみ

### 今後の方向性

次フェーズでは spec 追加や proof 整備ではなく、上記 3 工程の手間を直接軽減する機能を優先する。
具体的な着手順・手法はユーザーと合意のうえで決定する。

以下は着手候補の整理であり、順序は未確定:

#### 候補A: 台本品質の自動改善
- NLM 出力 → ゆっくり解説様式への自動変換/支援
- 話者混同の検出・修正支援
- NLM臭の除去パターン
- 台本品質が演出IRに連鎖するため、上流改善の効果が大きい
- Python スコープ制約 (テキスト変換のみ) の範囲内で可能
- GUI LLM (Custom GPT 等) での支援も選択肢

#### 候補B: 演出配置の自動化拡張
- 現状 face/bg/slot/overlay → 演出全体への拡張
- 素材調達・配置・タイミング制御のどこをどう自動化するか要設計
- Python スコープ制約との整合 (.ymmp 操作は patch-ymmp の限定範囲のみ)
- YMM4 側の制約 (タイムライン操作 API 非公開) が壁になる可能性

#### 候補C: 視覚効果の実現
- サムネイル制作の実ワークフロー確立
- 茶番劇風アニメ/図解アニメの実現手段の特定
- Python での画像生成は禁止のため、外部ツール or YMM4 内での実現が前提
- C-08 prompt のコピー品質改善 (仕様準拠だが感情フック不足)

#### 完了・維持 (着手不要)
- Packaging spec lane: H-01〜H-04 全て proof 済み。追加 spec 作業なし
- Timeline lane: G-11〜G-13 completed packet。failure class 発生時のみ再オープン
- 字幕分割: B-01〜B-17。残差2件は方針判断待ち (急がない)
- Electron GUI scaffold: Phase 1-5 完了。実運用は上記 bottleneck 解消後

#### 別タスクとして完全分離
- E-01/E-02 YouTube 投稿自動化: 制作パイプラインとは独立。混ぜない

## DECISION LOG

| 日付 | 決定事項 | 選択肢 | 決定理由 |
|------|----------|--------|----------|
| 2026-04-08 | 次以降の推奨プランを `runtime-state.md` に正本化（P0 Phase1 本番 1 本・P1 H-01 運用・P2 演出実戦・P3 サムネ・Parking motion ブランチ）。GUI CSV 同梱診断 JSON を Phase 1 導線に明記 | 暗黙の優先 / 文書固定 | 実制作 bottleneck 軽減レーンを再アンカーし、未承認実装を増やさない |
| 2026-04-07 | G-18 SE `AudioItem` 挿入を実装（`samples/AudioItem.ymmp` readback、`_apply_se_items`、テンプレート deepcopy または最小骨格）。`SE_WRITE_ROUTE_UNSUPPORTED` を廃止 | ゲート維持 / 実装 | サンプルと骨格で write route を確定し、G-13 の `se` を mechanical scope まで拡張 |
| 2026-04-06 | G-15〜G-17 を実装（Micro `bg` 発話スパン / `overlay` 配列 / `--timeline-profile` + motion・transition・bg_anim マップ）。G-18 は AudioItem ymmp サンプル入手まで保留（verification に明記） | 一括 / ゲート付き | P2C に沿い SE write は corpus 確定後。G-12 `timeline_route_contract.json` と契約検証を先に置く |
| 2026-04-06 | 視覚三スタイル（挿絵コマ / 再現PV / 資料パネル）を IR 既存語彙にマッピングし doc 正本化。延伸は G-15〜G-18 proposed | 一括実装 / 文書→テンプレ→Writer→台帳パケット | patch 制約（単一 overlay・セクション bg のみ・motion 未書込）を隠さず、`VISUAL_STYLE_PRESETS.md` と v4 プロンプトで Writer と運用を揃える |
| 2026-04-06 | 将来開発ロードマップを `FUTURE_DEVELOPMENT_ROADMAP.md` に正本化。G-15〜G-18 は proposed のまま承認記録表で管理。feat/phase2-motion-segmentation は P2A-motion-branch-operator-decision で保留 | 未承認を approved に昇格 / 文書のみ | プランに沿いゲートを明文化。実装は承認後のみ |
| 2025 | CLI パイプラインとして構築 | CLI / Web UI / Electron | 最小構成で検証可能 |
| 2025 | IP-01 No-Go | Go / No-Go | 要件未充足 |
| 2025 | Web UI / API / YouTube 連携は後回し | 優先 / 後回し | ロバスト性検証が先 |
| 2026-03-29 | B-10 (--emit-meta) を未承認で混入 | — | 未承認。後に rejected → コード除去 |
| 2026-03-30 | FEATURE_REGISTRY + AUTOMATION_BOUNDARY で機能管理 | 台帳管理 / ad-hoc | 未承認機能混入の再発防止 |
| 2026-03-30 | 自動化レイヤーを L1〜L4+GUI の5層で定義 | 5層 / 3層 / フラット | YMM4内部/外部の境界を明確化 |
| 2026-03-30 | Python での生成・レンダリングを全面禁止 | 全面禁止 / 部分許容 | .ymmp は音声ファイル参照を含み外部生成不可能。この教訓を拡大適用。Python の責務はテキスト変換（CSV / テキストメタデータ文字列）のみに限定。rejected: B-10, C-02, C-03, C-04, C-05, D-01, F-03 |
| 2026-03-30 | 外部メディア取得は分離設計で OK | L1拡張許容 / L2専念 | 取得機能と受け取り機能を分離すれば NLMYTGen に含めてよい。最終的に自動化する方針 |
| 2026-03-30 | WORKFLOW.md を S-0〜S-9 の全工程に再設計 | 全面改訂 / 部分改訂 | 前作業者がrejectedで隔離しただけでYMM4側の代替ワークフローが欠落していた。S-5(演出)が5行だけだった。rejected工程の代替手段を全てWORKFLOW.mdに記載 |
| 2026-03-30 | E-02 を先に仕様定義する | E-02 / A-04 / F-01 / 全件hold | ユーザーが選択。L2変換レイヤーで Python スコープ内に収まる唯一の候補 |
| 2026-03-30 | E-02 は単体では価値が薄い | 着手 / 先送り / E-01とセット | YouTube Studio へのコピペが CLI テンプレートに変わるだけ。E-01 (API投稿) とセットでないと実質的効率化にならない |
| 2026-03-30 | S-5 (字幕はみ出し) が最優先の痛点 | S-5 / S-6 / S-2 | ユーザーフィードバック。S-5/S-6 が最も時間がかかる工程 |
| 2026-03-30 | S-6 トピック分析は stdlib 制約内では精度不足 | パターンマッチ / 軽量NLP / やらない | パターンマッチ30-50%、NLP 40-60%+CLAUDE.md違反。LLM アダプター方式に転換予定 |
| 2026-03-30 | B-04 表示幅ベース分割を実装 | 表示幅 / 文字数維持 | 全角=2,半角=1 の display_width で YMM4 字幕はみ出しを事前防止。--display-width, --max-lines, --chars-per-line 追加 |
| 2026-03-30 | S-6 トピック分析を LLM アダプター方式に転換 | LLM / パターンマッチ / やらない | ユーザー指示。コーパス分析ライブラリはレガシー化しており LLM に統一。モデル切替可能なアダプター設計 |
| 2026-03-30 | サムネイルはYMM4テンプレートの文字・画像入れ替え | テンプレート手動 / Python自動生成 / 外部ツールのみ | 機械的な背景+文字の自動生成は不可。テンプレートの手動カスタマイズが必要。サムネイルは非常に重要 |
| 2026-03-30 | A-04 / D-02 / F-01 / F-02 を quarantined に移す | proposed維持 / hold / quarantined | B-10 混入時の汚染バッチ由来で、個別再審査前に通常 backlog として扱うと再発するため |
| 2026-03-30 | A-04 を done に戻す | quarantined維持 / hold / done | RSS/Atom からタイトル抽出して NotebookLM 検索クエリへ渡す `fetch-topics` は Python のテキスト取得責務に収まり、実装と台帳が一致したため |
| 2026-03-30 | E-02 を hold に移す | proposed維持 / hold / rejected | 価値検証の結果、単体では bottleneck を減らさず、今は進めない方が正確だから |
| 2026-03-30 | C-01 を done ではなく info に整理する | done維持 / info | Python 機能ではなく、確認済みの手動工程だから |
| 2026-03-30 | canonical docs の雛形放置を handoff 不備として扱う | 雛形維持 / 内容補完 | `8a1c710` で docs は追加済みだったが、実内容が薄いままでは resume 時の再アンカー先として機能しない |
| 2026-03-30 | `docs/ai/*.md` を canonical rules として先に読む | helper docs優先 / canonical rules優先 | tool-specific helper docs や prompt より repo 内 canonical rules を先に読む方が再開の一貫性が高い |
| 2026-03-30 | `prompt-resume.md` を docs-only handoff 用に追加 | promptなし / prompts分散 / 単一resume prompt | 次セッション開始手順を repo 内で完結させるため |
| 2026-03-31 | B-11 S-5 workflow proof を approved frontier にする | S-5 workflow proof / S-6 LLM adapter / hold継続 | ユーザーが S-5 を先に進めると承認。最大 pain に近く、Python の責務境界を壊さずに workflow proof を積めるため |
| 2026-03-31 | B-12 行バランス重視の字幕分割を実装する | proposal packet のみ / `--balance-lines` 実装 | S-5 proof で辞書や timing ではなく改行系 pain が支配的と確認できたため、2行字幕向けの自然改行 heuristics を opt-in で実装 |
| 2026-03-31 | B-13 を次候補として proposal 化する | B-12 継続 / clause-aware split + widow guard | B-12 は手動改行を減らしたが、長文再分割 15 件と 1 文字最終行が残り、次の主 pain が節分割と widow/orphan 回避に絞れたため |
| 2026-03-31 | B-13 節分割 + widow/orphan guard を実装する | proposal のみ / `--balance-lines` 内部改善 | 句読点の少ない長文と 1 文字最終行を減らす最短経路で、既存フラグのまま改善できるため |
| 2026-03-31 | B-14 を次候補として proposal 化する | B-13 継続 / aggressive clause chunking | B-13 で手動改行は 5 まで減ったが、再分割 10 と長い一文 1 字幕問題が残り、より積極的な chunking の要否を切り分ける必要があるため |
| 2026-03-31 | B-14 aggressive clause chunking を実装する | proposal のみ / `--balance-lines` 内部改善 | B-13 のままでは複数文発話の中にある単一長文が展開されず、operator pain の主因が残ったため。先に CLI 側でどこまで崩せるかを確かめる価値があった |
| 2026-03-31 | S-6 LLM 活用は API SDK ではなく GUI LLM (Custom GPT / Claude Project 等) を優先する | API adapter / GUI LLM / やらない | ユーザー希望。API SDK 導入は stdlib 制約緩和 ADR が必要で依存が増える。GUI LLM ならプロンプトテンプレートのみで Python 変更不要 |
| 2026-03-31 | B-15 改行コーパス収集を approved にする | B-14 継続 / corpus 収集 / hold | B-14 で bulk overflow 収束後、残 pain は個別ケース。heuristic 追加より corpus → 傾向化 → ルール化が強い |
| 2026-03-31 | C-07 S-6 演出メモ生成を proposed にする | proposed / hold / skip | GUI LLM でプロンプトテンプレートを作成し、実動画 1 本で workflow proof する方式。Python 変更なし |
| 2026-03-31 | B-15 をコーパス収集からトップダウン改行再設計に拡張する | パッチ (P1/P2) / トップダウン再設計 / hold | 初期コーパスの傾向分析で現行ボトムアップ方式の構造的限界 (2層の噛み合い不良、全体を見ない局所最適) を特定。ユーザー提案のトップダウン方式が実装可能かつ管理可能と判断。パッチ積み増しより根本解決を選択 |
| 2026-03-31 | 以前会話内でリジェクトされたトップダウン型分割アルゴリズム案を再評価・採用する | 再採用 / パッチ維持 / 別方式 | 当時のリジェクト理由は DECISION LOG に未記録。現在のコーパスで構造的問題が実証されたため、たたき台として再検討。仕様を精緻化し `reflow_utterance()` として実装する方針 |
| 2026-03-31 | 視覚系タスク (背景動画・アニメーション・サムネイル) への着手意向を記録 | 記録 / 即着手 / 無視 | ユーザー希望。字幕分割に目処がつけば次のペイン。D-02 quarantined / D-01 rejected のため権利・境界の再整理が前提。当面は字幕分割を優先 |
| 2026-04-01 | B-15 手動検証: 小区切り (漢字→ひらがな、カタカナ→ひらがな) を候補から除去 | 除去 / penalty引上 / 維持 | ユーザーフィードバック。「単/なる」「見間違/った」のような切断が発生する。大区切り (句読点) がない場所では分割しない方針を徹底。文字種境界より行長精度を優先 |
| 2026-04-01 | B-15 手動検証結果: 明らかなバランス偏りは解消、若干の違和感は残存 | 継続改善 / done化 / hold | ユーザー評価。4行またがり解消、漢字/カタカナ途中切断は改善中。次頁区切り(話者行分割)と同一ページ内改行の区別が今後の課題 |
| 2026-04-01 | B-15 を一旦区切り、残課題を B-16 として分離する | 区切り / 続行 | ユーザー判断。ページ間分割は改善されたが、行内折り返し制御には「1行/1ページ最大文字数から逆算する外殻」が必要で別タスク。画像関連が完全停止しているため、プラン再構成を優先 |
| 2026-04-01 | 開発プラン再構成: C-07→視覚系→B-16 の順で進行 | C-07優先 / B-16優先 / 視覚系優先 | C-07 (演出メモ) が最も軽く、視覚系の入口にもなる。C-07 結果を踏まえて D-02 再審査と視覚系の具体策を決定。B-16 は並行進行可能。E-02 は hold 継続 (E-01 とセットでないと価値が出ない判断は変わらず) |
| 2026-04-01 | 視覚系タスクの start gate を C-07 workflow proof 完了後に設定 | C-07後 / 即時 / hold | C-07 の背景キーワード有用性が視覚系の価値経路の入口。成功なら D-02 再審査へ、失敗ならプロンプト改善 or 手動継続 |
| 2026-04-01 | D-02 再審査チェックリストを作成 | 作成 / 後回し | 取得元、権利、取得/受取分離、YMM4受渡、価値経路、既存フローの6項目。C-07 proof 後に実施 |
| 2026-04-01 | C-07 v1 proof 結果: 2/3 OK だが背景候補の方向が違う | 方向転換 / v1維持 | ストック素材検索は価値が低い。実際に必要なのは「茶番劇風アニメーション + 図解アニメーション」の演出指示。4パターン (茶番劇/情報埋め込み/雰囲気演出/黒板型) を基軸にプロンプトを v2 に改善 |
| 2026-04-01 | 視覚系の最大ペインは「何を表示するか」の判断 + 情報不足時の取材 | 判断支援 / 配置自動化 / 素材API | ユーザーフィードバック。配置作業自体よりバランス判断と素材集めが重い。D-02 の方向性を「素材API」から「演出判断支援」に転換 |
| 2026-04-01 | C-07 v3: マクロ演出設計 + 素材調達ガイドを追加 | v2維持 / v3拡張 / 別プロンプト | C-07 v2 はミクロ (発話単位) のみ。ユーザーの最大ペイン (何を表示するか + 素材調達) はマクロ判断。Part 1 (全体設計) + Part 3 (調達ガイド) を追加し二層構造に拡張 |
| 2026-04-01 | D-02 再審査チェックリストを演出判断支援向けに改訂 | 旧チェックリスト維持 / 改訂 | 旧6項目は素材API方向のもの。方向転換により不適合。C-07 v3 統合/スコープ/価値経路/実装形態/ワークフロー位置/proof依存度の6項目に置換 |
| 2026-04-01 | D-02 の演出判断支援は C-07 v3 に暫定統合 | 独立機能 / C-07統合 / 両方 | ミクロ/マクロを流動的に組み替える方針。独立機能にするかは proof 結果で判断 |
| 2026-04-01 | 演出支援を5レイヤー (L-macro/L-micro/L-section/L-research/L-thumbnail) で整理 | レイヤー分離 / フラット | タスク ID に固執せず、機能をレイヤーとして捉え、後から統合・分割しやすい構造にする |
| 2026-04-01 | C-07 v3 proof 完了。D-02 を hold に変更 | hold / proposed / rejected | v3 出力レビューで L-macro + L-research が有用と確認。D-02 は C-07 v3 に吸収完了。独立機能不要 |
| 2026-04-01 | 作業時間実態: 10分動画で約1週間。長尺化で10分あたり約25%減衰 | 記録 | 素材再利用・パターン定着により摩擦が逓減する構造 |
| 2026-04-01 | proof は出力レビューで完了とし、実動画制作を要件としない | 軽量proof / 実動画proof | 実動画制作は重すぎてブロッカーになる。計測より実用を優先 |
| 2026-04-01 | YMM4 自動化の経路: プラグイン API 先行 → ymmp 直接編集を補完 | プラグインのみ / ymmp のみ / 二段階 | プラグイン API (IToolPlugin) が公式経路。タイムライン操作可否は未検証のため spike で確認。不可なら ymmp 編集を主経路に切替 |
| 2026-04-01 | YMM4 以外の動画制作パイプラインは検討対象外 | YMM4専念 / 代替検討 | ユーザー指示。ffmpeg/MoviePy 等での独自レンダリングは除外 |
| 2026-04-01 | アニメーション自動化 (G-01~G-04) を最優先フロンティアに設定 | アニメ自動化 / YT自動化 / 字幕改善 | S-6 が制作時間の70%以上を占める。ユーザーが「重い上にまだ何もできていない」と指摘 |
| 2026-04-01 | NotebookLM 自動化は NLMYTGen 外。台本入手後の工程に専念 | NLMYTGen内 / 別システム | 台本入手は折衷案 (前処理自動化 + NLM は読解/音声化のみ) で、動画制作が回り始めてから別途構築 |
| 2026-04-01 | G-01~G-04 を FEATURE_REGISTRY に proposed として登録 | 登録 / 保留 | 調査完了。実装承認は spike 結果を踏まえて判断 |
| 2026-04-01 | YMovieHelper を発見。CSV→ymmp 生成 (表情+動画切替対応) の既存ツール | 自前構築 / 既存ツール活用 | 自前でゼロから構築するより既存ツールと接続する方が現実的 |
| 2026-04-01 | G-01 (IToolPlugin spike) の優先度を最下位に変更 | 最優先維持 / 最下位 | タイムライン操作 API が非公開。.NET 環境構築の投資対効果が不明。YMovieHelper 連携で不十分な場合の代替経路 |
| 2026-04-01 | G-02 を YMovieHelper 詳細調査に再定義し最優先に | G-01先行 / G-02先行 | YMovieHelper が既に背景/表情/動画切替を実現しているため、入力仕様を把握して NLMYTGen と接続するのが最短経路 |
| 2026-04-01 | G-05 (build-ymh) を新規追加 | 追加 / 不要 | C-07 v3 の演出メモ → YMovieHelper 入力形式に変換する Python サブコマンド。G-02 の結果が前提 |
| 2026-04-01 | ymmp 直接編集は控える。完成品の解析研究のみ | 編集許可 / 研究のみ | 過去にデッドファイルが積み上がった経験。研究に没頭して開発から逸れるリスク |
| 2026-04-01 | テンプレート資産蓄積戦略を採用 | テンプレート / 毎回手動 | 制作者がテンプレートを用意→汎用素材化→リソース積み上げ。C-07 v3 がテンプレート選定を提案、build-ymh が仮組立。NLMYTGen は提案と仮組立まで、素材の完全自動生成には踏み込まない |
| 2026-04-01 | ドリフト防止ルールを INVARIANTS に固定 | 記録 | テスト目的化禁止、proof 軽量化、研究2ブロック制限。INTERACTION_NOTES にも開発ドリフト回避セクション追加 |
| 2026-04-01 | YMovieHelper を主軸から参照実装に格下げ (第三次改訂) | 主軸維持 / 参照実装 / 完全除外 | サービス終了済み Web アプリ (Docker+WSL+Go+TS)。CLI ではない。メンテナンス停止。設計思想の回収のみ。ツール依存は作らない |
| 2026-04-01 | 自動化の中核を「演出 IR + テンプレート資産」に転換 | ツール依存 / IR 中心 | 特定ツールに依存せず、NLMYTGen 独自の演出中間表現を定義。LLM は意味ラベルのみ出力し、座標変換はテンプレート定義側で解決 |
| 2026-04-01 | G カテゴリ再定義: G-02=IR語彙定義, G-05=IR出力プロンプト, G-06=接続方式決定 | 再定義 / 据置 | G-01/G-03 は hold。G-02 を YMovieHelper 調査 → IR 語彙定義に変更。build-ymh (旧G-05) は廃止し、IR 出力プロンプト (新G-05) に置換 |
| 2026-04-01 | YMovieHelper に言及する際のルール: 「使う」「接続する」ではなく「参考にする」「観察する」と書く | 記録 | 今後のドキュメントでの勘違い防止 |
| 2026-04-01 | G-02 演出 IR 語彙定義 v1.0 完了 | 完了 | `docs/PRODUCTION_IR_SPEC.md` 作成。9フィールド (template/face/bg/bg_anim/slot/motion/overlay/se/transition)、Macro+Micro 二層構造、JSON/CSV 二重表現、carry-forward ルール。S-6 の6手動工程を全カバー |
| 2026-04-02 | 正本ドキュメント5件を演出IR主軸に更新 | 修正 | README/CLAUDE.md/WORKFLOW/AUTOMATION_BOUNDARY/INVARIANTS から「CSV変換専用ツール」旧理解を除去。再開時の旧理解引き戻しを構造的に防止 |
| 2026-04-02 | G-05 C-07 v4 IR 出力プロンプト作成 | 完了 (proof待ち) | `docs/S6-production-memo-prompt.md` v4 セクション。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の Macro+Micro IR JSON を出力するプロンプト。v3 (自然文) との切替可能。proof はユーザーが Custom GPT で実施 |
| 2026-04-02 | ymmp 後処理の実機検証: 表情パーツ差し替えが動作することを確認 | 実証済み | Python で ymmp JSON のパーツパスを書き換え→YMM4で正常に開ける。音声・字幕は台本読込で確保済みのまま維持。二段階方式 (台本読込→ymmp後処理) が実現可能と確定 |
| 2026-04-03 | YMM4 テンプレートは独立ファイルではなく ItemSettings.json 内の Templates 配列に保存 | 実測確定 | テンプレートの Items 構造は ymmp Items と同一。Adapter ロジック再利用可能。エフェクト・VoiceCache もテンプレートに完全保持 |
| 2026-04-03 | Custom GPT v4 proof 完了 | 実証済み | 28 utterances / 5 sections / 全語彙チェック PASS / Macro-Micro 整合OK。carry-forward は全件フル指定 (省略なし) |
| 2026-04-03 | Custom GPT v4 の IR 出力は 2オブジェクト連結形式 (Macro + Micro) | 実測確定 | load_ir() で単一 JSON と連結形式の両方に対応。CLI patch-ymmp で動作確認済み |
| 2026-04-03 | production-slice patch-ymmp proof 完了、ただし full E2E は実制作 ymmp 不在で未閉塞 | 実証済み / 要再確認 | `samples/test - marisaFX.ymmp` に実IR先頭11発話を適用し face 13 / bg 2 変更を確認。`samples/v4_re.ymmp` は current workspace で未確認のため、28発話 full E2E は次ブロックへ持ち越し |
| 2026-04-03 | Template Registry は visual-review 前提。`extract-template` は棚卸し補助であって意味ラベル推定器ではない | 運用確定 | 表情ラベルは YMM4 上で見え方を確認して人間が命名する。現行 `patch-ymmp` のフラット `face_map` は単一キャラ proof 向けで、複数キャラ案件の最終形は character-scoped registry が必要 |
| 2026-04-05 | face_map を character-scoped に、bg_map は flat を維持 | 実装確定 | face は同じラベルでもキャラごとにパーツが異なる。bg は scene/preset 責務で話者固有ではない |
| 2026-04-05 | Remark フィールドを extract-template --labeled のラベル源に採用 | 実装確定 | Serif は発話テキスト用。Remark は VoiceItem / TachieItem / TachieFaceItem / ImageItem の全てに存在する空きメタデータ欄 |
| 2026-04-05 | row_start / row_end で IR 意味単位と VoiceItem 粒度差を吸収 | 実装確定 | IR を 60 発話に崩す案 (A) とテキストマッチング (C) を却下。IR の意味単位を保ったまま複数 VoiceItem に適用する方式 (B) を採用 |
| 2026-04-05 | idle_face: IR フィールド追加 + TachieFaceItem 挿入方式 | 実装確定 | TachieItem の表情制御ではなく、IR に idle_face を追加して adapter が non-speaker 側に TachieFaceItem を挿入。既存 face 適用経路を崩さず拡張 |
| 2026-04-05 | bg section 切替 proof 成功 (2 ラベル) | 実証済み | 5 セクションのうち 2 ラベルで背景切替を確認。残りはユーザーが bg_map を拡張するだけ |
| 2026-04-05 | `.claude` 側に常設ガードを追加 | 実装確定 | 毎回 prompt に重い禁止を書き足さず、repo-local 入口と hooks で repo 外逸脱 / broad question 停止 / repeated visual proof を抑止する |
| 2026-04-05 | face サブクエストの completion criteria を固定 | 継続調整 / failure class 固定 | face を未整理な改善ループではなく completed subsystem として扱うため。mechanical failure は class 名で止め、人間判断は creative quality に限定 |
| 2026-04-05 | apply-production は partial face output を書かない | patch 先行 / fail-fast | row-range 不整合、validation error、fatal face patch warning を書き出し前に止め、ymmp 化→手動確認ループを再発させないため |
| 2026-04-05 | Packaging / marketing レイヤーを独立 frontier として backlog 化 | C-08 個別改善 / E-02 再開 / packaging layer 新設 | 台本→タイトル侵食を止め、タイトル / サムネ / 台本の整合を 1 つの central brief で管理するため |
| 2026-04-05 | H-01 Packaging Orchestrator brief schema v0.1 を定義 | backlog のみ / schema 定義 | H-01 を abstract な気づきで終わらせず、C-07/C-08/E-02/H-04 が参照できる正本フィールドへ落とすため |
| 2026-04-06 | H-01 workflow proof packet を整備 | schema のみ / proof packet まで整備 | H-01 を `approved` のまま放置せず、user が 1 本の実台本で drift を観測できる実行単位まで前進させるため |
| 2026-04-06 | H-02 Thumbnail strategy v2 schema v0.1 を定義 | backlog のみ / schema 定義 | H-02 を感覚的な運用メモではなく、C-08 が参照できる specificity-first / banned pattern / rotation policy の正本へ落とすため |
| 2026-04-06 | H-04 Evidence richness score schema v0.1 を定義 | backlog のみ / schema 定義 | H-04 を曖昧な「内容が強いか」ではなく、promise_payoff と evidence category に分解された repair-oriented gate にするため |
| 2026-04-06 | H-04 manual scoring proof packet を整備 | schema のみ / proof packet まで整備 | H-04 を机上定義で終わらせず、warning を script/packaging repair に変換できる実行単位まで前進させるため |
| 2026-04-06 | H-02 は dry proof を先に通し、strict GUI rerun proof と分離して扱う | strict proof 待ち / dry proof 先行 | 既存 artifact だけでも specificity-first / banned pattern / rotation contract が機能するかを確認でき、GUI rerun 待ちで packaging lane 全体を止める必要がないため |
| 2026-04-06 | H-01 はまず repo-local dry proof を通し、strict な GUI rerun proof と分離して扱う | dry proof なし / strict proof 待ち / dry proof 先行 | 既存 artifact だけでも brief が共有契約として機能するかは確認でき、strict な before/after rerun 待ちで packaging lane 全体を止める必要がないため |
| 2026-04-06 | H-03 を packaging lane の最後の未定義ピースとして先に定義し、strict GUI rerun とは分離して進める | GUI rerun 完了待ち / H-03 先行定義 | visual stagnation risk は repo-local brief/cue/script だけでも warning 化できるため、外部 GUI 実行待ちで spec 定義全体を止める必要がないため |
| 2026-04-06 | H-04 AI監視 sample は `acceptable` と判定し、主要 warning を anecdote continuity と late payoff に集約 | 高評価でそのまま通す / vague score に留める / warning を repair に落とす | H-04 の価値は数値化より repair 指示にあるため、包装 promise と本文根拠のズレを具体修正へ還元できる形で残す必要があるため |
| 2026-04-06 | G-11 slot patch hardening を実装完了 | proposed 維持 / 実装完了 | timeline edit を broad manual retry loop にせず、slot を deterministic patch + fail-fast validation の packet として閉じるため |
| 2026-04-06 | G-12 は patch 前に readback harness と route contract 照合を先行実装 | 先に patch / 先に measurement harness | native route を未確定のまま `motion` / `transition` / `bg_anim` の adapter write に進むと、file-format risk と creative judgement が再混線するため |
| 2026-04-06 | G-12 の current contract は `test - marisaFX.ymmp` で通し、`production.ymmp` の `bg_anim` miss を failure class として扱う | gap を黙殺 / warning 扱い / failure class 化 | timeline quality 問題を visual impression に戻さず、route gap を mechanical failure として扱うため |
| 2026-04-06 | G-12 measurement packet を追加し、current corpus で route narrowing を先に完了 | harness のみ / packet 化して route narrowing | `motion` / `bg_anim` は current corpus で狭め、manual frontier を `transition` probe 1 本へ縮めると、operator の判断負荷を最小化できるため |
| 2026-04-06 | fade-family `transition` route を ymmp_measure で回収可能にし、G-12 contract を更新 | `transition` を route 不在扱い / fade-family route を corpus-derived contract 化 | repo-local corpus に既にある fade key を拾えば、手動 probe を増やさずに `transition` の主要 family を mechanical に確定できるため |
| 2026-04-06 | G-13 overlay / se insertion packet を completed として閉じる | overlay/se を broad manual frontier に残す / packet として閉じる | `overlay` は registry + timing anchor から deterministic な `ImageItem` 挿入まで閉じた。当時 `se` は timing までで write route 不在を `SE_WRITE_ROUTE_UNSUPPORTED` で fail-fast（G-18 で挿入まで実装） |
| 2026-04-06 | Phase 1 として B-18 台本機械診断と C-09 refinement プロンプトを実装完了 | 保留 / 実装 | `diagnose-script`・`script_diagnostics.py`・`S1-script-refinement-prompt.md`・GUI 品質タブ・B18 dry proof・pytest 拡張まで一括 |
| 2026-04-06 | Next roadmap: P01 運用手順、P2A feat ブランチレビュー（一括マージ不採用）、P2B+G-14 production contract、P2C SE 境界、サムネ 1 枚チェックリスト | 未実施 / 実施 | Phase 2/3 の文書・contract 整備を master に反映 |
| 2026-04-05 | サムネイル戦略は抽象煽りより具体数値・固有名詞優先 + rotation 管理 | 定型煽り / 具体性優先 / 各動画場当たり | 本文根拠とクリック訴求を両立し、固定パターン反復による疲労と硬直を避けるため |
| 2026-04-05 | スコアリングは visual density / evidence richness の2軸から着手 | スコアなし / 単一総合点 / 2軸 | 演出不足と内容不足を別々に診断し、制作改善とマーケ改善の接続点を明確化するため |
| 2026-04-06 | assistant 側の subquest を timeline edit まで拡張するが、packet 単位で進める | timeline を一括実装 / packet 分割 / 維持 | face と同様に mechanical scope を failure class / readback / boundary で切り分けないと、YMM4 手動確認ループへ戻るため。G-11 slot patch → G-12 native-template measurement → G-13 overlay/se insertion の順に進める |

---

## Python のスコープ（確定事項 — 2026-03-30）

**許可:**
- テキストファイルの変換（transcript → CSV）
- テキストメタデータの生成（タイトル・説明・タグ等の文字列）
- 入力テキストの検証・分析
- 外部ソースからのテキスト/メディア取得（L1、取得と受け取りを分離する設計で）

**禁止:**
- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp 生成・操作（音声ファイル参照を含むため外部生成不可能）
- YMM4 テンプレート生成・演出指定（YMM4 内部の責務）
- YMM4 出力の模倣・プレビュー
- 動画レンダリング・音声合成
- 外部 TTS（Voicevox 等）

**根拠:**
YMM4 の .ymmp プロジェクトファイルは音声ファイル（WAV 等）への参照を含む。その音声は YMM4 が台本 CSV を読み込む際に内蔵 TTS で自動合成するもの。NLMYTGen から音声ファイルを生成できないため、完全な .ymmp を外部から作ることは原理的に不可能。この制約から、YMM4 内部の操作（テンプレート・演出・素材配置）を Python から制御するアプローチ全般が成り立たない。

---

## IDEA POOL

FEATURE_REGISTRY.md に統合済み。機能候補は FEATURE_REGISTRY で管理する。

| ID | 旧アイデア | 移行先 |
|----|----------|--------|
| IP-02 | Web UI 化 | CLAUDE.md スコープ外 |
| IP-03 | YouTube 自動アップロード | FEATURE_REGISTRY E-01 (hold) |

---

## HANDOFF SNAPSHOT (2026-04-08 更新)

- Shared Focus: 実制作 bottleneck 軽減レーン継続。G-18・GUI CSV+診断 JSON 同梱まで完了。**正本は `docs/runtime-state.md` の「次以降の推奨プラン (2026-04-08)」** — P0 は Phase 1 を新台本 1 本で完走し [P01](verification/P01-phase1-operator-e2e-proof.md) へ記録。packaging は H-02/H-03/H-04 done、H-01 は approved（運用載せが P1）
- Safe Next Frontier Packet: **P0** Phase 1 本番 1 本（診断→C-09→CSV→YMM4→P01） / **P1** H-01 brief 運用 / **P2** 演出実戦（registry・`--se-map` 等） / **P3** サムネ 1 本 / **Parking** motion ブランチは P2A どおり一括マージしない
- Active Artifact: NLM transcript → YMM4 CSV → Writer IR → Template Registry → YMM4 Adapter → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → IR (Custom GPT) → Registry (JSON) → Adapter (patch-ymmp) → 演出設定 → レンダリング
- Last Change Relation: 推奨プラン正本化 (2026-04-08) + GUI CSV 同梱診断 JSON。履歴コミット参照は git log
- Evidence: Production E2E 実証済み + `uv run pytest`: **266 passed** (2026-04-07)。B-18/C-09・G-14 contract・G-18 SE・P 系 verification。slot/face/timeline regression 維持
- 案件モード: CLI artifact
- 現在の主レーン: 方向転換中 (実制作bottleneck直接軽減へ移行)
- 成熟段階: Level 1 (限定変換器) 到達済み、Level 2 (演出IR適用エンジン) 形成中 → Level 3 接近
- Current Trust Assessment:
  - trusted: B-01~B-17 全字幕スタック (93 PASS)
  - trusted: G-02 IR 語彙 v1.0、G-02b ymmp 構造解析、G-06 patch-ymmp 実機検証
  - trusted: extract-template (face_map/bg_map 自動抽出)
  - trusted: G-05 v4 proof 完了。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の IR を正常出力
  - trusted: load_ir Multi-Object 対応 (2オブジェクト連結形式の読み込み)
  - trusted: face completion hardening (`PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_PROMPT_PALETTE_*` / `FACE_LATENT_GAP`)
  - trusted: G-11 slot patch hardening (`SLOT_UNKNOWN_LABEL` / `SLOT_REGISTRY_GAP` / `SLOT_CHARACTER_DRIFT` / `SLOT_DEFAULT_DRIFT` + TachieItem X/Y/Zoom patch + `off` hide)
  - trusted: G-12 readback harness (`measure-timeline-routes` で `motion` / `transition` / `bg_anim` candidate route を抽出し、`--expect` / `--profile` で route contract miss を検出)
  - trusted: G-12 packet narrowing (`motion=TachieItem.VideoEffects`、`bg_anim=ImageItem.X/Y/Zoom`、effect-bearing bg=`ImageItem.VideoEffects` まで current corpus で狭め済み)
  - trusted: repo-local `.ymmp` 16 本の corpus audit により fade-family `transition` route は観測済み、`template` route は 0 件と確認済み
  - trusted: G-13 overlay insertion (`OVERLAY_*` validation + deterministic `ImageItem` patch)
  - trusted: G-13/G-18 `se` (`SE_*` validation + G-18 `AudioItem` 挿入、`PatchResult.se_plans` = 挿入数)
  - trusted: H-02 done (dry proof + strict GUI rerun proof pass 2026-04-06)
  - trusted: H-03/H-04 done — `score-visual-density` / `score-evidence` CLI + tests (`test_visual_density_score.py`, `test_evidence_score.py`)
  - trusted: B-18 `diagnose-script` + C-09 `docs/S1-script-refinement-prompt.md`（`test_script_diagnostics.py`）
  - resolved (G-14): `production.ymmp` はタイムラインに ImageItem 無しのため bg_anim 未観測。`production_ai_monitoring_lane` で motion/transition のみ required とし contract pass。背景アニメ patch は ImageItem 含有 ymmp で別パケット
  - needs re-check: non-fade / template-backed `transition` の ymmp route は repo 内 sample 不在のため未固定。新しい sample が入ったときだけ再測定する
  - resolved (G-18): `se` の `AudioItem` 挿入は `samples/AudioItem.ymmp` + コード内骨格で固定。運用で YMM4 バージョン差が出たら readback のみ再確認
  - needs re-check: face label inventory そのものが creative quality として十分かは最終制作物で見る
- Recovered Canonical Context:
  - Python はテキスト変換 + 演出 IR 定義 + ymmp 限定後段適用
  - 視覚配置 IR が中心課題。C-07 系が主系統、D-02 は従属的補助論点
  - patch-ymmp は Level 1 限定変換器。ゼロからの ymmp 生成とは区別する
  - 「未実装」は「境界外」ではない。motion/transition/overlay は正式スコープ内の frontier
  - YMM4 テンプレートは独立ファイルではなく ItemSettings.json の Templates 配列に JSON 保存
  - Custom GPT v4 は 2オブジェクト連結形式 (Macro + Micro) で IR を出力する。load_ir() で対応済み
- Authority Return Items:
  - YMM4 大版本更新時: `AudioItem` 構造差分が出たら readback のみ再確認（G-18）
  - E-02: hold 継続。E-01 とセットでのみ再検討
  - F-01/F-02: quarantined 継続
- What Not To Do Next:
  - spec/proof 整備をさらに積み増さない (一巡済み。実制作の手間軽減が先)
  - done 件数で進捗を測らない (35件だが実制作カバレッジは限定的)
  - D-02 を主軸として扱わない (従属的補助論点)
  - quarantined 項目を通常候補としてそのまま spec 化しない
  - face 問題を broad な visual retry loop として再開しない
  - E-01/E-02 を制作パイプラインと混ぜない (別タスクとして完全分離)
- Expansion Risk: なし
## 2026-04-05 Structural Linebreak Redesign Note

- B-17 reflow v2 was reworked around structural major/minor boundaries instead of phrase-specific word lists.
- Page carry-over and in-page line breaks are now evaluated separately: page planning prefers major boundaries first, then falls back to minor boundaries only when necessary.
- Inline break scoring now strongly penalizes breaks inside short hiragana connector tails and around quoted/bracketed labels followed by explanatory nouns.
- Short comma-led intro lines are now penalized by width so that later particle/phrase breaks win when they keep the page visually denser.
- Close-bracket/content fallback candidates and major-vs-all page-plan comparison were added, reducing earlier failures around quoted labels and explanatory nouns.
- Emergency inner-break candidates inside long quoted labels were added as a last resort; remaining residuals are now mostly small 41-48 width overruns rather than gross structural breaks.
- Single-hiragana tails after quoted terms are now scored separately, improving `...最適化」 / と聞くと` type boundaries while keeping `」` at the next-line head suppressed.
- Sample proof on `samples/AI監視が追い詰める生身の労働.txt` improved several screen-facing failures (`では / なく`, `）」 / という`, `） / 」`, `19 / 億`) while leaving a smaller residual cluster around `XというY` and quoted explanatory phrases that still need another structural pass.
- Carry-over scoring is now explicitly separated from in-page line breaks: `close+tail` boundaries and extra-page exact plans are allowed to win when they eliminate overflow without creating sparse fragment pages.
- Exact page-count comparisons now use a target-specific ideal page width instead of reusing the base target, which fixed the `完璧に計算されたアルゴリズムが生身の / 人間という...` class by allowing one more page in the surrounding multi-sentence utterance.
- Current sample residuals are down to 2 mechanical frontier cases in `_tmp_structural_balance.csv`: `誰の汗とリスクを動力にして回り始めるのかを / 解剖していくということですね。` and `自発的にリスクを取らせる罠のようなものです。 / データによると、`. Further automatic tightening risks over-fragmenting page flow more than it helps.
