# FEATURE REGISTRY — NLMYTGen 機能一覧

このファイルは NLMYTGen の全機能・全候補を一箇所で把握するための台帳。
機能追加はここに登録し、承認を得てから実装する。ここにない機能は追加しない。

---

## ステータス定義

| ステータス | 意味 |
|-----------|------|
| done | 実装済み・動作確認済み |
| approved | 承認済み・未実装 |
| proposed | 提案中・承認待ち |
| hold | 将来候補・現時点では着手しない |
| quarantined | 汚染された提案バッチ由来。通常候補として扱わず、個別再審査が必要 |
| rejected | 明示的に不採用 |
| info | Python 機能ではなく手動工程の記録。WORKFLOW.md 参照 |
| unauthorized | 未承認で実装や文書に混入した機能。レビュー待ち |

---

## 却下理由の補助用語

`rejected` / `hold` は目的そのものを永久に塞ぐとは限らない。汚染パッチ由来の過剰ブロックを避けるため、以下の補助用語で「何が禁止され、何が後継経路として許可されるか」を分ける。

| 用語 | 意味 |
|------|------|
| method-rejected | 当時の手段・実装経路は却下。目的は別手段で再起票できる |
| goal-allowed | 同じ制作目的を、承認済み境界内の別経路で進めてよい |
| successor-lane | 旧案の反省を踏まえ、別 ID / 別 artifact として成立した後継経路 |

---

## 自動化レイヤー

機能がどこで動作するかを明示する。詳細は [AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md) を参照。

| レイヤー | 説明 | 例 |
|---------|------|-----|
| L1-入力取得 | NotebookLM / RSS / 外部ソースからの素材取得 | NotebookLM台本取得 |
| L2-変換 | Python CLI でのテキスト変換・メタデータ生成 | CSV変換、分割 |
| L3-YMM4内部 | YMM4 上での操作・テンプレート・プロジェクト設定 | 台本読込、演出設定 |
| L4-出力配信 | 動画出力後の配信・公開 | YouTube投稿 |
| GUI | NLMYTGen 独自の操作画面 | 分割プレビュー |

---

## 機能一覧

### A. 台本取得 (L1-入力取得)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| A-01 | NotebookLM 元台本テキスト取得（手動コピペ） | done | L1 | 主導線。WORKFLOW.md S-2 |
| A-02 | 音声書き起こし fallback（Whisper / Google Docs） | done | L1 | --unlabeled で対応 |
| A-03 | NotebookLM API 連携（台本自動取得） | hold | L1 | API 未公開。公開時に検討 |
| A-04 | RSS フィード連携（トピック候補取得） | done | L1 | `fetch-topics` サブコマンド。RSS/Atom からタイトル抽出 → NotebookLM 検索クエリとして使用。再審査済み (2026-03-30)、実装完了 |

### B. 台本変換 (L2-変換)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| B-01 | テキスト→YMM4 CSV 変換 (build-csv) | done | L2 | コアパイプライン |
| B-02 | 話者マッピング (--speaker-map) | done | L2 | CLI / ファイル両対応 |
| B-03 | ラベルなし入力 (--unlabeled) | done | L2 | 行交互 Speaker_A/B 割当 |
| B-04 | 長文自動分割 (--max-length) | done | L2 | 文末区切り分割 + 表示幅ベース補助 (`--display-width`, `--max-lines`, `--chars-per-line`) |
| B-05 | 同一話者連続結合 (--merge-consecutive) | done | L2 | |
| B-06 | 入力検証 (validate) | done | L2 | |
| B-07 | 入力分析 (inspect) | done | L2 | 話者統計・ロール推定 |
| B-08 | 話者マップテンプレート生成 (generate-map) | done | L2 | |
| B-09 | 複数ファイル一括処理 | done | L2 | build-csv に複数パス指定 |
| B-10 | 編集支援メタデータ (--emit-meta) | rejected | L2 | **method-rejected**: 旧 `build-csv --emit-meta` sidecar は未承認混入のため復活禁止・コード除去済み。ただし診断 JSON、Production IR、session manifest、packaging brief などの承認済み機械可読 artifact は **goal-allowed** |
| B-11 | S-5 workflow proof パック（字幕 overflow triage + evidence capture） | done | L2 | `build-csv --max-lines --chars-per-line` + 統計（CLI `--stats` または GUI の JSON `stats` / F-04）を起点に、YMM4 取込前のはみ出し候補把握と取込後の修正量記録を repeatable にした。初回 proof で辞書 0 / timing 0 / 改行系 pain 優勢を確認 |
| B-12 | 行バランス重視の字幕分割 | done | L2 | `--balance-lines` を追加。`--max-lines` 使用時に 2 行字幕へ自然な改行を opt-in で挿入し、読点・句点・カギカッコ付近を候補にしつつ行バランスを崩しにくい分割 heuristics を実装。`uv run pytest` 51 PASS。再観測では手動改行は減ったが、句読点の少ない長文と 1 文字最終行は残存。Electron GUI の CSV タブから同フラグを指定可能（新規 F-ID ではない表面化）。運用の正本: [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md) |
| B-13 | 節分割 + widow/orphan guard | done | L2 | `--balance-lines` の内部改善として、句読点が少ない一文を `、` や接続句で節分割する fallback と、1 文字最終行を避ける guard を追加。`uv run pytest` 54 PASS、sample dry-run で 57 発話 → 62 行に再編。post-import 再観測では手動改行 5 / 再分割 10 / 不自然な単語分割 5 で、改善はあるが決定打ではなかった |
| B-14 | aggressive clause chunking | done | L2 | `--balance-lines` の内部改善として、複数文発話の中にある単一長文も sentence ごとに再展開し、通常候補が尽きた場合は引用句・機能語まで使った aggressive chunking fallback を適用。`uv run pytest` 56 PASS、sample dry-run で 57 発話 → 95 行、overflow candidates は 3 件まで減少 |
| B-15 | トップダウン改行 Phase 1: ページ間分割 | done | L2 | ページ間 (話者行) 分割をトップダウン方式に再設計。大区切り限定、閉じ括弧+助詞保護、カタカナ語/数字/漢字連続/括弧ペア内の分断禁止、再帰的 reflow。67テストPASS。ユーザー検証でページ間バランス偏り解消を確認。行内折り返し制御は B-16 へ |
| B-16 | トップダウン改行 Phase 2: 行内折り返し制御 | done | L2 | `insert_inline_breaks()` で chars_per_line ごとに大区切り候補で行内改行 `\n` を挿入。`reflow_subtitles()` の最終段に統合。候補がなければ YMM4 自動折り返しに委ねる。72テストPASS。手動検証待ち |
| B-17 | 字幕改行アルゴリズム v2 (統合リフロー) | done | L2 | B-15/B-16 を統合リフローとして再設計。`reflow_utterance()` ベースの一貫したトップダウン方式。2026-04-28 に YMM4 表示条件へ寄せる opt-in 補正として `--subtitle-font-scale` / `--subtitle-font-source-ymmp` / `--wrap-px` / `--measure-backend` を追加し、GUI CSV タブにも露出。WPF helper は実測幅 backend、EAW は fallback。B-17 残差観測は実害行だけ paired evidence として扱う |
| B-18 | 台本機械診断（NLM→ゆっくり前段） | done | L2 | `diagnose-script` CLI + `src/pipeline/script_diagnostics.py`。`--format json` / `--strict` / `--expected-explainer` / `--expected-listener`。仕様: `docs/SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md`。dry proof: `docs/verification/B18-script-diagnostics-ai-monitoring-sample.md` |

### C. YMM4 連携・演出 (L3-YMM4内部)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| C-01 | YMM4 台本読込（CSV インポート） | info | L3 | Python 機能ではなく手動工程。WORKFLOW.md S-4 の確認済み導線 |
| C-02 | YMM4 演出テンプレート（Python 生成） | rejected | L3 | **method-rejected**: Python が YMM4 native template を外部生成・再発明する案のみ却下。YMM4 で作った native template source を IR / registry で解決し `.ymmp` timeline へ配置する G-24 は **successor-lane / goal-allowed** |
| C-03 | YMM4 プロジェクトファイル (.ymmp) 自動生成 | rejected | L2→L3 | **method-rejected**: 音声・発音情報・字幕配置を含む `.ymmp` のゼロ生成や YMM4 台本読込代替は不可。台本読込後 `.ymmp` に対する限定 patch は **goal-allowed** |
| C-04 | 背景動画の配置自動化（Python 制御） | rejected | L3 | **method-rejected**: Python で YMM4 GUI / 内部配置を万能制御する案のみ却下。IR + `bg_map` / `bg_anim_map` / timeline profile による post-import 限定 patch は **goal-allowed** |
| C-05 | 素材配置の自動指定（Python 制御） | rejected | L3 | **method-rejected**: 任意素材を Python 側判断で直接配置する万能制御は却下。registry / map / template source に固定された overlay・se・skit_group・thumbnail slot patch は **successor-lane / goal-allowed** |
| C-06 | YMM4 演出・レンダリング工程（手動） | info | L3 | Python 機能ではなく手動工程の記録。読み上げ確認(S-5)・背景演出(S-6)・最終確認(S-7)。詳細は WORKFLOW.md 参照 |
| C-07 | S-6 演出メモ生成（GUI LLM プロンプトテンプレート） | done | L3 補助 | v3 確定。Part 1: マクロ演出設計 (全体トーン/ペーシング/背景遷移)、Part 2: ミクロ演出指示 (4パターン/発話単位)、Part 3: 素材調達ガイド。`docs/S6-production-memo-prompt.md`。統合ガイド: `docs/gui-llm-setup-guide.md`。画像例由来のオペレータ意図の言語化正本: [C07-visual-pattern-operator-intent.md](C07-visual-pattern-operator-intent.md) |
| C-08 | S-8 サムネイルコピー生成（GUI LLM プロンプトテンプレート） | done | L3 補助 | キャッチコピー5案 + サブコピー3案 + 表情提案 + 背景方向性。`docs/S8-thumbnail-copy-prompt.md`。現行 C-07 v4 は本編 Production IR 専用なので、サムネコピーは S8/H-02 として別ラウンドまたは別 GPT に分離する |
| C-09 | S-1 台本 refinement 支援プロンプト（GUI LLM） | done | L3 補助 | `docs/S1-script-refinement-prompt.md`。`diagnose-script --format json` + 生台本を GUI LLM に渡す手順。`docs/gui-llm-setup-guide.md` に導線あり |

### D. 素材取得・生成 (L1 + L2)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| D-01 | サムネイル自動生成（Python 画像生成） | rejected | L2 | **method-rejected**: Python 画像生成・画像合成のみ却下。YMM4 サムネテンプレを複製し、H-02 `thumbnail_design` と `thumb.*` slot を `audit-thumbnail-template` / `patch-thumbnail-template` で限定 patch する経路は **successor-lane / goal-allowed** |
| D-02 | 演出判断支援 (方向転換: 素材API → テキスト演出支援) | hold | L1 | 方向転換 (2026-04-01): 素材API検索 → 演出判断支援。C-07 v3 に L-macro + L-research として統合完了。v3 proof 成功 (4/5)。独立機能としては不要。C-07 v3 の改善要望が出た場合に再検討 |

### E. 出力・配信 (L4)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| E-01 | YouTube 投稿自動化 | hold | L4 | YouTube Data API v3 |
| E-02 | YouTube メタデータ生成（タイトル・説明・タグ） | hold | L2 | 旧 standalone metadata template は hold。H-01 / H-02 / H-04 を入力にした YouTube metadata draft は **successor-lane** として再起票可能。E-01 または別の実 integration point と接続するまで自動投稿・本線注入はしない |

### F. 開発インフラ・GUI

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| F-01 | 分割プレビュー GUI | quarantined | GUI | 前セッションの汚染バッチ由来。S-5 の痛点はあるが GUI が最短価値経路か未検証 |
| F-02 | 設定管理 GUI | quarantined | GUI | 前セッションの汚染バッチ由来。設定固定点と F-01 の価値検証前に進めない |
| F-03 | YMM4 出力プレビュー | rejected | GUI | **method-rejected**: Python で YMM4 表示を模倣する preview のみ却下。YMM4 で開く compact review `.ymmp`、readback、audit、placement report は **goal-allowed** |
| F-04 | CSV タブ話者統計・はみ出し候補表示（`build-csv` JSON `stats`） | done | GUI | `--stats` 相当を `--format json` 応答に含め、GUI の Dry Run / Build CSV 結果パネルで表形式表示。制作は GUI のみで取込前の把握が可能 |

#### F-01 / F-02 再審査ゲート（2026-04-06）

- **ステータスは quarantined 維持**（台帳上の承認なしに復活させない）。
- 再開の前提: 制作ウィザード（`start-gui.bat`）＋既存タブ（CSV / 演出適用 / 品質診断）で S-5・S-6 の痛点が十分吸収されるかを、[workflow-proof-template.md](workflow-proof-template.md) に沿った **B-11** 記録で判断する。
- 記録上「分割プレビュー専用 GUI」や「設定の第二 UI」が最短価値だと判断された場合のみ、個別 FEATURE として台帳更新・スコープ確定のうえで再検討する。

### G. YMM4 自動化 (L3 内部工程の効率化)

G-15〜G-18 は **実装済み**。現行ステータスは本台帳の各行を正本とし、履歴・証跡は各 verification doc を参照する（G-18: [G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md)）。

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| G-01 | YMM4 IToolPlugin feasibility spike | hold | L3 | タイムライン操作 API 非公開。優先度最下位。他経路で不十分な場合のみ検討 |
| G-02 | 演出 IR 語彙定義 | done | L2 | `docs/PRODUCTION_IR_SPEC.md` v1.0。template/face/bg/bg_anim/slot/motion/overlay/se/transition の9フィールド。Macro+Micro 二層構造、JSON/CSV 二重表現、carry-forward ルール。語彙と `patch-ymmp` 適用範囲の対照: [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md) |
| G-02b | 完成品 ymmp 構造解析 (研究のみ、1件限定) | done | L3 | 171MB ymmp を解析。VoiceItem 1549件 / VideoItem 140件 / TachieItem 2件。TachieFaceParameter でパーツ単位の表情制御。bg+face 差し替えが最小実用単位。`docs/verification/G02b-ymmp-structure-analysis.md` |
| G-03 | 演出適用ツール (IToolPlugin) | hold | L3 | G-01 が前提。タイムライン操作 API 非公開のため凍結 |
| G-04 | ymmp 背景/表情自動差し替え | hold | L3 | ymmp 直接編集は控える。G-02b + 段階5の判断結果を踏まえて再検討 |
| G-05 | Writer IR 出力プロンプト (C-07 v4) | done | L2 | 三層の第1層 (Writer IR)。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の構造化 IR (scene_preset + override) を出力。`docs/S6-production-memo-prompt.md` v4 セクション（視覚三スタイル補助語彙を含む）。proof 完了 |
| G-06 | YMM4 Adapter (patch-ymmp) | done | L2/L3 | 三層の第3層 (YMM4 Adapter)。face (表情パーツ) を IR→ymmp で差し替え。character-scoped face_map + row-range 対応済み。extract-template --labeled で palette ymmp から face_map 自動生成。production E2E 実証済み (2026-04-05: 60 VoiceItem / 28 IR utterance / face 133 changes) |
| G-07 | 待機中表情の指定 (idle_face) | done | L2/L3 | IR に `idle_face` フィールドを追加。patch-ymmp が各 utterance の開始 Frame に non-speaker キャラの TachieFaceItem を挿入。carry-forward 対応。character-scoped face_map で解決。131 PASS (2026-04-05) |
| G-08 | apply-production ワンコマンド | done | L2 | `apply-production` サブコマンド。palette → face_map 抽出 + row-range 自動付与 + patch-ymmp を 1 コマンドで実行。`validate-ir` を内包し、row-range unmatched/uncovered・validation error・fatal face patch warning (`FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE`) では書き出し前に停止する。--palette / --face-map / --bg-map / --csv / --refresh-maps / --dry-run |
| G-09 | annotate-row-range (row_start/row_end 自動付与) | done | L2 | IR utterance text と CSV 行の段階的 Greedy Forward Match (strict/loose/partial)。NFKC + 句読点除去。speaker 補助チェック。cascade failure 防止。`annotate-row-range` 独立コマンド + `apply-production --csv` 統合。151 PASS (2026-04-05) |
| G-10 | IR 品質 gate (validate-ir) | done | L2 | `validate-ir` サブコマンド + `apply-production` 統合。`FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` を ERROR、`FACE_PROMPT_PALETTE_GAP` / `FACE_PROMPT_PALETTE_EXTRA` / `FACE_LATENT_GAP` / serious 偏り (>40%) / 連続 run (>4) / idle_face 未指定 / bg 未設定 を WARNING として分類する。Custom GPT の face 許可リストと palette の drift report、キャラ別 palette gap report を出力。187 PASS |
| G-11 | slot patch hardening | done | L2/L3 | `slot` registry contract を `validate-ir` / `apply-production` / `patch-ymmp` に統合。`SLOT_UNKNOWN_LABEL` / `SLOT_REGISTRY_GAP` / `SLOT_CHARACTER_DRIFT` / `SLOT_DEFAULT_DRIFT` を事前検出し、TachieItem の X/Y/Zoom を deterministic に反映、`off` は `IsHidden` に落とす。CLI smoke + unit tests 済み。`uv run pytest` 198 PASS (2026-04-06) |
| G-12 | timeline route measurement packet | done | L3 | `measure-timeline-routes` CLI + `--expect` + `--profile` で ymmp の `motion` / `transition` / `bg_anim` candidate route を readback し、repo-local contract を `samples/timeline_route_contract.json` に固定。`docs/verification/G12-timeline-route-measurement.md` により `motion=TachieItem.VideoEffects`、`bg_anim=ImageItem.X/Y/Zoom`、effect-bearing bg は `ImageItem.VideoEffects`、fade-family `transition` は `VoiceItem.VoiceFadeIn/Out` / `VoiceItem.JimakuFadeIn/Out` / `TachieItem.FadeIn/Out` まで mechanical に確定。未確定なのは non-fade / template-backed transition family のみ。**補足:** CSV 読込後の [samples/production.ymmp](samples/production.ymmp) は ImageItem 無し→ **G-14** `production_ai_monitoring_lane` を参照 |
| G-13 | overlay / se timeline insertion adapter | done | L2/L3 | `overlay` / `se` の意味ラベルを registry 解決し、timing anchor と failure class を固定。`overlay` は `--overlay-map` 経由で deterministic な `ImageItem` 挿入まで実装済み。`se` は `--se-map` で label/timing を解決し、G-18 で `AudioItem` 挿入まで実装（テンプレートまたは最小骨格）。`docs/verification/G13-overlay-se-insertion-packet.md` を正本とする |
| G-14 | production lane timeline contract profile | done | L3 | [samples/production.ymmp](samples/production.ymmp)（CSV 読込後・ImageItem 無し）向けに [samples/timeline_route_contract.json](samples/timeline_route_contract.json) に `production_ai_monitoring_lane` を追加。`measure-timeline-routes --expect --profile production_ai_monitoring_lane` で ERROR なし。bg_anim は本 ymmp に観測が無いため required 外とし、ギャップを文書化（`docs/verification/P2B-production-timeline-contract-profile.md`） |
| G-15 | patch-ymmp 発話スパン背景（Micro `bg`） | done | L2/L3 | Micro IR の `bg`（carry-forward 解決後）を Layer 0 に反映。[G15-micro-bg-patch.md](verification/G15-micro-bg-patch.md)。[VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md) |
| G-16 | 複数 overlay / スタック（1 発話複数 ImageItem） | done | L2/L3 | `overlay` を文字列または配列で受け、同一発話に複数 ImageItem。[G16-multi-overlay-patch.md](verification/G16-multi-overlay-patch.md) |
| G-17 | motion / transition / bg_anim の ymmp 書き込み Adapter | done | L2/L3 | `--timeline-profile` + `--motion-map`（`video_effect` 辞書）等。契約失敗時は書き込みスキップ。[G17-motion-adapter-packet.md](verification/G17-motion-adapter-packet.md)。**Phase2（別フラグ）:** `--tachie-motion-map` で VideoEffects 配列台帳＋発話区間による `TachieItem` 分割（`--timeline-profile` 未指定時のみ）。G-14 列挙子 `bg_anim` の X/Y/Zoom キーフレームは micro bg 生成時に別経路で適用 |
| G-18 | SE AudioItem タイムライン挿入（write route 実装） | done | L2/L3 | `patch-ymmp` の `_apply_se_items` が `AudioItem` を挿入。[G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md)。履歴メモ [G18-se-audioitem-deferred.md](verification/G18-se-audioitem-deferred.md)。P2C 参照 |
| G-19 | 立ち絵 複数体素材 × ゆっくり顔（body_variant / face_map 束ね） | done | L2/L3 | **スコープ注意（2026-04-15 明示）**: 本 FEATURE は **ゆっくり系立ち絵（TachieItem）内部の body パーツ束ね**。**外部人物素材（配達員・消防員等）の茶番劇演者**は別系統で扱い、現行主軸は **G-24 template-first**。混同しない。 / 複数の体素材それぞれに、同一系のゆっくり顔パーツを `face_map`（character-scoped 含む）で解決する運用を機械化。**方式**: Option A（ディレクトリ + マニフェスト）。IR に `body_id`（carry-forward）を追加し、`--face-map-bundle` CLI フラグでバンドルレジストリを指定。`validate-ir` に `BODY_ID_UNKNOWN` / `BODY_FACE_MAP_MISS` チェック追加。準備正本: [TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md)。**スコープ**: body_id はシーンレベル（V1）。キャラ別 body_id は別スライス。`--palette` 経路は single-body のまま |
| G-21 | 茶番劇体テンプレ（旧 body_map / ImageItem 挿入案） | hold | L2/L3 | **旧主案。現行の主軸ではない。** 外部素材 body/head を patch 側で直接組み立てる案だったが、2026-04-17 に **template-first 運用**へ整理したため保留。茶番劇演者の正本は [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md)。再開条件: template-first で量産できず、body_map/insert 型の自動化が bottleneck と実証された場合のみ。 |
| G-20 | 立ち絵 顔/体の幾何（反転・平行移動・相対オフセット）IR + patch | approved | L2/L3 | 体と顔をセットで反転・移動し視覚整合を保つ。運用前提は **中央基準 GroupItem テンプレ**（使い捨て Group 化は標準運用にしない）。A案（既存 GroupItem の `X/Y/Zoom` 操作）を優先し、B案（Group生成挿入）は将来比較対象として分離。**スライス1**: `validate-ir` で `group_target` の空・前後空白・改行含有を `GROUP_TARGET_*` として事前エラー化。**スライス2**: `group_motion_map` に `mode: "relative"` を追加（現在値への加算。テンプレ互換性向上）。`_load_group_motion_map` でモード値バリデーション。残候補（C: face_map_bundle 整合チェック、D: テンプレ監査標準化）は [G20 包括レビュー §8](verification/G20-group-and-asset-automation-comprehensive-review-2026-04.md) に起票済み。反転（IsFlipped）は実キー調査後に別スライス。 |
| G-23 | Motion Preset Library | done | L2/L3 | `motion` ラベル → `tachie_motion_map_library.json` → VideoEffects の library。エフェクト原子は `samples/EffectsSamples_2026-04-15.ymmp` (111種) から抽出。仕様正本: [MOTION_PRESET_LIBRARY_SPEC.md](MOTION_PRESET_LIBRARY_SPEC.md)。**適用先は 2 経路**: (1) `motion_target` 未指定時は speaker の `TachieItem` (`_apply_motion_to_tachie_items`)、(2) `motion_target: "layer:N"` 指定時は該当レイヤーの `ImageItem`/`GroupItem` (`_apply_motion_to_layer_items`)。両経路とも同じ `tachie_motion_effects_map` を参照する。 |
| G-22 | Dual-rendering scene_presets（補助経路） | hold | L2/L3 | 立ち絵 TachieItem と書き出し PNG overlay の両運用は **補助経路としては有効**だが、2026-04-17 時点の主軸ではない。茶番劇演者の正本は [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) の GroupItem template-first。必要時に `overlay_render` 補助として再開する。 |
| G-24 | 茶番劇 Group テンプレ生成・解決運用 | approved | L2/L3 | **現行の主軸 frontier。** 配達員などの外部素材演者を `speaker_tachie` と分離し、**repo-tracked YMM4 template source → registry 解決 → patch-ymmp GroupItem 自動配置**の流れを正本化する。開発段階の成果物は YMM4 native template 資産、`skit_group_registry` 台帳、`.ymmp` template source、placement write path。`motion` の direct write 拡張や operator 手順票を主軸にしない。**2026-04-27 v1 completion sync**: v1 planned set 5 件は user-owned export/sample proof + acceptance により `direct_proven` へ昇格。**2026-04-28 source sync**: repo-tracked source に `delivery_nod_v1` を同梱し、v1 5/5 が配置可能になった。**2026-04-28 placement sync**: `--skit-group-only` で face/bg 未解決を切り離して exact / fallback を自動配置できる。**current next**: YMM4 CSV-imported DX `.ymmp` copy に適用し、Layer 9 GroupItem readback で確認する。新テンプレートは production gap が出た時だけ再起票。正本: [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md)。shared registry 雛形: `samples/registry_template/skit_group_registry.template.json`。template source: `samples/templates/skit_group/delivery_v1_templates.ymmp`。 |
| G-25 | YMM4 property-based variation probe | done | L2/L3 | **successor-lane / goal-allowed / production-unusable**: 手動作成済み `.ymmp` の `Remark` 付き Group/Image/Text/Shape clip から、`X/Y/Zoom/Rotation`、反転系 route、`VideoEffects` stack fingerprint を読み取り、保守的な property 派生候補を JSON report 化する。CLI は `probe-ymmp-variations SOURCE.ymmp`。`-o REVIEW.ymmp` 指定時、source が template/stub の場合は `--review-seed` で YMM4 保存済み full project canvas を指定し、その末尾へ compact review 用 variation clip を追加する。2026-04-30 のYMM4確認では、出力は開けるが `nudge / scale / rotate / effect_reuse` は動きのvariationとして使えなかったため、G-24 production placement へ自動接続しない。正本: [G25-animation-variation-acceptance-2026-04-30.md](verification/G25-animation-variation-acceptance-2026-04-30.md)。 |
| G-26 | Motion primitive grammar / compatibility probe | proposed | L2/L3 | G-25 の後継。手動作成済みの `うなずき` / `退場` / `小ジャンプ` / `傾き` などを、座標差分ではなく motion primitive として扱う。`primitive_id`、`motion_role`、`start_pose` / `end_pose`、`dominant_channels`、`reset_policy`、`direction_semantics`、`compatible_after` / `forbidden_after` を機械可読化し、自由な総当たり合成ではなく、ニュートラル復帰・方向意味・終端姿勢が成立する候補だけを JSON compatibility report 化する。最初は production placement に接続せず、review checklist までで止める。これらの primitive 語彙は G-26 preflight の initial candidate であり、手動 `.ymmp` の route readback と設計選択後に確定する。現時点では実装 schema ではない。 **2026-04-30 Route readback 観測 (3 motions)**: `nod` は GroupItem の Rotation 揺れ [0, -6.2, 0] と `CenterPointEffect` (Vertical=Bottom, Horizontal=Custom (X≈525, Y≈137)) anchor の組合せ、`exit_left` は VFX `InOutMoveEffect` 委譲 (route 値はすべて static)、`surprise_oneshot` は Y 揺れ [-57, -107, -57, -57]。motion ごとに dominant channel が異なるため単軸 variant 直積は構造的に却下、option B (motion primitive 一級市民) が第一候補、option C (hybrid + tilt modifier) は手動 tilt 重畳 `.ymmp` の登録待ち。**2026-04-30 Phase 3 仮 contract / screen review**: `_tmp/g26/draft_contracts/*.json` に `nod` / `exit_left` / `surprise_oneshot` の draft contract を作成し、`dominant_channels` の `VFX:<EffectType>` 拡張と `anchor_dependency` 新設を反映。画面確認用に YMM4 保存済み `samples/_probe/g24/real_estate_dx_csv_import_base.ymmp` を seed とし、`_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp` を生成。readback は inserted GroupItems 3 / POSIX asset paths 0 / openability pass。正本: [G26-motion-primitive-contract-screen-review-2026-04-30.md](verification/G26-motion-primitive-contract-screen-review-2026-04-30.md)。 |

G-26 evidence gate note (2026-04-30): current screen review is machine-pass, but visual acceptance is not recorded. A repo-local scan of 53 `.ymmp` files found no tilt or 2-motion chain source Remarks, so `tilt` remains out-of-contract and `compatible_after` / `forbidden_after` remain `unknown`.

G-26 recipe lab correction (2026-04-30): absence of user-authored tilt/chain sources is not a creation ban. Assistant may create purpose-driven review artifacts from existing YMM4-saved canvas + existing GroupItem/ImageItem template source, as long as it does not Python-preview/render, zero-generate `.ymmp`, synthesize new image/effect types, or connect to G-24 production placement. Current lab: `_tmp/g26/recipe_lab/g26_goal_motion_recipe_lab.ymmp` with 12 goal recipes (`nod_*`, `jump_*`, `tilt_*`, `chain_*`), openability pass, POSIX asset paths 0. These are proposed review candidates; `compatible_after` / `forbidden_after` still require YMM4 visual acceptance.

G-26 recipe pipeline v1 (2026-04-30): added CLI artifact route `build-motion-recipes` for intent-first sample creation. It consumes `samples/recipe_briefs/g26_motion_recipe_brief.v1.json`, YMM4 seed/template source, `samples/effect_catalog.json`, `samples/_probe/b2/effect_full_samples.json`, and `samples/tachie_motion_map_library.json`, then writes `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.{ymmp,md}` plus readback JSON. Initial set covers 12 proposed recipes (`nod_*`, `jump_*`, `panic_crash`, `shocked_jump`, `surprised_chromatic`, `anger_outburst`, `shobon_droop`, `lean_curious`). 正本: [G26-motion-recipe-pipeline-2026-04-30.md](verification/G26-motion-recipe-pipeline-2026-04-30.md)。

### H. Packaging / 評価 / オーケストレーション (L2 + L4)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| H-01 | Packaging Orchestrator brief | approved | L2 | タイトル / サムネ / 台本の約束を中央制御する text-only brief。`docs/PACKAGING_ORCHESTRATOR_SPEC.md` v0.1 で schema を定義済み。`promise` / `audience_hook` / `required_evidence` / `forbidden_overclaim` / `alignment_check` を正本化し、台本単体がタイトルを越権決定しないようにする。`docs/verification/H01-packaging-orchestrator-ai-monitoring-dry-proof.md` で repo-local dry proof まで記録済み。旧 code orchestrator パターンの復活ではない。空テンプレ出力: CLI `emit-packaging-brief-template`、GUI 品質診断タブの「H-01 テンプレを保存」。2026-04-28 に production handoff 補助として `build-session-manifest` を追加し、CSV / IR / validate/apply / patched ymmp / `thumbnail_design` の artifact と manual acceptance 状態を 1 枚に束ねられるようにした。**スコープ確定（2026-04）**: ブリーフや manifest は artifact/handoff であり、`build-csv` / `apply-production` への自動注入、スコア結果のクローズドループ反映は **未承認**。**拡張する場合**は本行の「スコープ確定」を更新し、`approved` の下位タスクとして台帳に分割してから実装する。 |
| H-02 | Thumbnail strategy v2 (具体数値優先 + pattern rotation) | done | L2 | C-08 の上位互換候補。`docs/THUMBNAIL_STRATEGY_SPEC.md` v0.1 で specificity-first / banned pattern / rotation policy / output contract を定義済み。dry proof + strict GUI rerun proof (2026-04-06) pass。仕様準拠確認済み (4/5案が preferred_specifics 使用、banned pattern なし、Specificity Ledger・Brief Compliance Check 出力)。2026-04-28 に `thumbnail_design` companion JSON と YMM4 サムネ template slot 契約を分離し、`audit-thumbnail-template` / `patch-thumbnail-template` で既存 `thumb.text.*` / `thumb.image.*` item の限定 patch を実装済み。実サムネ template proof は未完了で、画像生成・PNG 書き出し・サムネ `.ymmp` 新規生成は含めない |
| H-03 | Visual density score | done | L2/L3 | `docs/VISUAL_DENSITY_SCORE_SPEC.md` v0.1 準拠。`score-visual-density` CLI（`src/pipeline/visual_density_score.py`）と GUI の品質診断タブで category スコア集計・total・warning/repair を出力。dry proof は `docs/verification/H03-visual-density-ai-monitoring-proof.md`。ymmp readback 併用は将来拡張 |
| H-04 | Evidence richness score | done | L1/L2 | `docs/EVIDENCE_RICHNESS_SCORE_SPEC.md` v0.1 準拠。`score-evidence` CLI（`src/pipeline/evidence_score.py`）と GUI の品質診断タブ。manual proof は `docs/verification/H04-evidence-richness-ai-monitoring-proof.md`。タイトル / サムネ約束と本文根拠のギャップ診断 |
| H-05 | S-8 thumbnail probe score（レーンE補助判定） | done | L2 | Automation Probe。`score-thumbnail-s8` で手動採点 JSON を機械集約し、PASS/NEEDS_FIX を返す。画像生成・画像解析は行わない。運用正本: `docs/verification/LANE-E-S8-prep-2026-04-09.md`。**承認範囲（2026-04-09）**: CLI 集約と検証記録のみ（`src/pipeline/thumbnail_s8_score.py` / `tests/test_thumbnail_s8_score.py`）。サムネ生成自動化は含めない。**GUI**: 品質診断タブに「CLI のみ」の注記あり。コマンド例は制作手順本文に置かず [docs/dev/CLI_REFERENCE.md](dev/CLI_REFERENCE.md) に集約。 |

---

## 明示的にオミットするもの

| 機能 | 理由 | 根拠 |
|------|------|------|
| Python での画像生成・画像合成 | 視覚的成果物の生成は Python の責務外 | ユーザー指示 (2026-03-30) |
| Python での動画レンダリング | YMM4 の責務 | ADR-0003 |
| Python での .ymmp ゼロからの生成 | 音声ファイル参照を含むため外部生成不可能 | ユーザー指示 (2026-03-30)。ただし台本読込後の ymmp の部分編集 (背景/表情差し替え) は G-02/G-04 で検討中 |
| Voicevox / 外部 TTS | YMM4 内蔵の音声合成を使用 | ADR-0003 |
| MoviePy / ffmpeg (合成目的) | YMM4 の責務 | ADR-0003 |
| PIL / Pillow (画像合成目的) | 視覚的成果物の生成は Python の責務外 | ユーザー指示 (2026-03-30) |
| LLM による主台本生成 | NotebookLM の責務 | ADR-0002 |
| Web UI (現時点) | コアパイプライン優先 | CLAUDE.md |
| API サーバー (現時点) | コアパイプライン優先 | CLAUDE.md |

---

## 運用ルール

1. **機能追加はこの台帳に登録してから実装する。** ここにない機能は追加しない。
2. ステータスが `approved` でない機能は実装しない（`done` の改善は除く）。
3. `proposed` の機能は、ユーザーの承認を得て `approved` に昇格してから実装する。
4. `unauthorized` の機能は次のレビューで承認 / 削除 / 修正のいずれかを判断する。
5. オミットリストに載っている機能を復活させる場合は、新しい ADR を起草する。

### 実装着手前チェック（`src/` 変更前）

作業が **全体ブロック** になるわけではなく、**当該変更が属する FEATURE 行のステータス**でゲートが決まる。着手前に次を照合する。

1. **該当行の特定** — 変更内容がどの ID 行に属するか 1 行で書けること。新規能力なら本台帳に 1 行追加し `proposed` から始める。
2. **`done` または既存 `approved` の延長** — バグ修正・テスト・validate 厳格化・スコープ内の GUI/CLI 改善などは、原則このまま実装してよい（ルール 2 の「`done` の改善は除く」）。
3. **`proposed` の本文スコープ**（例: G-20 の「承認前は `src/` 変更禁止」）— **ユーザー承認と `approved` 昇格（または承認済みスライスへの分割記載）のあと**に `src/` を触る。迷う場合は拡張を起票し、既存行の「スコープ確定」文を更新してから進める。

`docs/runtime-state.md` の「未承認 FEATURE は増やさない」は **優先度・スコープ膨張の指針**であり、上記 2 のような保守・硬化を禁止するものではない。
