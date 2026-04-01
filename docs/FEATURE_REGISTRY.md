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
| B-10 | 編集支援メタデータ (--emit-meta) | rejected | L2 | 未承認で混入 → rejected (2026-03-30)。コード除去済み |
| B-11 | S-5 workflow proof パック（字幕 overflow triage + evidence capture） | done | L2 | `build-csv --max-lines --chars-per-line --stats` を起点に、YMM4 取込前のはみ出し候補把握と取込後の修正量記録を repeatable にした。初回 proof で辞書 0 / timing 0 / 改行系 pain 優勢を確認 |
| B-12 | 行バランス重視の字幕分割 | done | L2 | `--balance-lines` を追加。`--max-lines` 使用時に 2 行字幕へ自然な改行を opt-in で挿入し、読点・句点・カギカッコ付近を候補にしつつ行バランスを崩しにくい分割 heuristics を実装。`uv run pytest` 51 PASS。再観測では手動改行は減ったが、句読点の少ない長文と 1 文字最終行は残存 |
| B-13 | 節分割 + widow/orphan guard | done | L2 | `--balance-lines` の内部改善として、句読点が少ない一文を `、` や接続句で節分割する fallback と、1 文字最終行を避ける guard を追加。`uv run pytest` 54 PASS、sample dry-run で 57 発話 → 62 行に再編。post-import 再観測では手動改行 5 / 再分割 10 / 不自然な単語分割 5 で、改善はあるが決定打ではなかった |
| B-14 | aggressive clause chunking | done | L2 | `--balance-lines` の内部改善として、複数文発話の中にある単一長文も sentence ごとに再展開し、通常候補が尽きた場合は引用句・機能語まで使った aggressive chunking fallback を適用。`uv run pytest` 56 PASS、sample dry-run で 57 発話 → 95 行、overflow candidates は 3 件まで減少 |
| B-15 | トップダウン改行 Phase 1: ページ間分割 | done | L2 | ページ間 (話者行) 分割をトップダウン方式に再設計。大区切り限定、閉じ括弧+助詞保護、カタカナ語/数字/漢字連続/括弧ペア内の分断禁止、再帰的 reflow。67テストPASS。ユーザー検証でページ間バランス偏り解消を確認。行内折り返し制御は B-16 へ |
| B-16 | トップダウン改行 Phase 2: 行内折り返し制御 | done | L2 | `insert_inline_breaks()` で chars_per_line ごとに大区切り候補で行内改行 `\n` を挿入。`reflow_subtitles()` の最終段に統合。候補がなければ YMM4 自動折り返しに委ねる。72テストPASS。手動検証待ち |

### C. YMM4 連携・演出 (L3-YMM4内部)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| C-01 | YMM4 台本読込（CSV インポート） | info | L3 | Python 機能ではなく手動工程。WORKFLOW.md S-4 の確認済み導線 |
| C-02 | YMM4 演出テンプレート（Python 生成） | rejected | L3 | YMM4 テンプレートの外部生成・操作インターフェースが存在しない。NLMYTGen の責務（テキスト変換）を超える。**代替:** YMM4 の機能でテンプレートを手動作成・再利用する（WORKFLOW.md S-0） |
| C-03 | YMM4 プロジェクトファイル (.ymmp) 自動生成 | rejected | L2→L3 | .ymmp は音声ファイル参照を含み、音声は YMM4 が台本読込時に内蔵 TTS で生成する。外部から完全な .ymmp を生成することは原理的に不可能 |
| C-04 | 背景動画の配置自動化（Python 制御） | rejected | L3 | Python から YMM4 内部の配置を制御するインターフェースが存在しない。**代替:** YMM4 上で手動配置する（WORKFLOW.md S-6a） |
| C-05 | 素材配置の自動指定（Python 制御） | rejected | L3 | Python から YMM4 内部の素材配置を制御するインターフェースが存在しない。**代替:** YMM4 テンプレートで初期配置を定型化する（WORKFLOW.md S-0） |
| C-06 | YMM4 演出・レンダリング工程（手動） | info | L3 | Python 機能ではなく手動工程の記録。読み上げ確認(S-5)・背景演出(S-6)・最終確認(S-7)。詳細は WORKFLOW.md 参照 |
| C-07 | S-6 演出メモ生成（GUI LLM プロンプトテンプレート） | done | L3 補助 | v3 確定。Part 1: マクロ演出設計 (全体トーン/ペーシング/背景遷移)、Part 2: ミクロ演出指示 (4パターン/発話単位)、Part 3: 素材調達ガイド。`docs/S6-production-memo-prompt.md`。統合ガイド: `docs/gui-llm-setup-guide.md` |
| C-08 | S-8 サムネイルコピー生成（GUI LLM プロンプトテンプレート） | done | L3 補助 | C-07 と同方式。キャッチコピー5案 + サブコピー3案 + 表情提案 + 背景方向性。`docs/S8-thumbnail-copy-prompt.md`。C-07 と統合して Custom GPT / Claude Project に1つのプロンプトとして固定化可能 |

### D. 素材取得・生成 (L1 + L2)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| D-01 | サムネイル自動生成（Python 画像生成） | rejected | L2 | Python での画像生成は禁止。**代替:** YMM4 テンプレートの文字・画像入れ替えによる手動制作（WORKFLOW.md S-8） |
| D-02 | 演出判断支援 (方向転換: 素材API → テキスト演出支援) | hold | L1 | 方向転換 (2026-04-01): 素材API検索 → 演出判断支援。C-07 v3 に L-macro + L-research として統合完了。v3 proof 成功 (4/5)。独立機能としては不要。C-07 v3 の改善要望が出た場合に再検討 |

### E. 出力・配信 (L4)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| E-01 | YouTube 投稿自動化 | hold | L4 | YouTube Data API v3 |
| E-02 | YouTube メタデータ生成（タイトル・説明・タグ） | hold | L2 | 単体では YouTube Studio へのコピペ先が変わるだけ。E-01 または別の実 integration point とセットで再検討 |

### F. 開発インフラ・GUI

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| F-01 | 分割プレビュー GUI | quarantined | GUI | 前セッションの汚染バッチ由来。S-5 の痛点はあるが GUI が最短価値経路か未検証 |
| F-02 | 設定管理 GUI | quarantined | GUI | 前セッションの汚染バッチ由来。設定固定点と F-01 の価値検証前に進めない |
| F-03 | YMM4 出力プレビュー | rejected | GUI | YMM4 の見え方を Python で模倣することは視覚的生成に該当。YMM4 自体で確認すべき |

### G. YMM4 自動化 (L3 内部工程の効率化)

| ID | 機能 | ステータス | レイヤー | 備考 |
|----|------|-----------|---------|------|
| G-01 | YMM4 IToolPlugin feasibility spike | proposed | L3 | タイムライン操作 API が非公開のため優先度最下位。YMovieHelper 連携で不十分な場合の代替経路 |
| G-02 | YMovieHelper 詳細調査 + 入力形式把握 | proposed | L3 | **最優先。** CSV 入力で表情変更 + 動画切り替え対応の既存ツール。入力仕様を把握し NLMYTGen 出力と接続可能か評価 |
| G-02b | 完成品 ymmp 構造解析 (研究のみ) | proposed | L3 | ymmp を編集せず、構造を解析して再現可能性を研究。デッドファイルを作らない |
| G-03 | 演出適用ツール (IToolPlugin) | proposed | L3 | G-01 の結果が前提。タイムライン操作 API 非公開のため実現可能性が低い |
| G-04 | ymmp 背景/表情自動差し替え | hold | L3 | ymmp 直接編集は控える (過去の失敗経験)。G-02b の研究結果を踏まえて再検討 |
| G-05 | C-07 v3 → YMovieHelper 入力変換 (build-ymh) | proposed | L2 | G-02 の結果が前提。演出メモ + CSV を YMovieHelper 入力形式に変換する Python サブコマンド。テンプレート定義ファイル (JSON) の管理を含む。テンプレート名 → 背景/表情/BGM/SE のマッピング解決 |

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
