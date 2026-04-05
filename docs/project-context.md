# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現フェーズ: Production E2E 実証完了。face + bg + idle_face パイプライン全通。Tier 3 (安定化) へ
- 直近の状態 (2026-04-05):
  - G-06 Production E2E: 60 VoiceItem / 28 IR utterance (row-range) / character-scoped face_map → face 133 changes / YMM4 visual proof OK
  - G-07 idle_face: 待機中表情の TachieFaceItem 挿入。28 件挿入 + carry-forward 動作確認
  - bg section 切替 proof: 2 ラベル (van_dashboard_ai + dark_board) で BG added 2 / YMM4 確認 OK
  - extract-template --labeled: palette.ymmp → character-scoped face_map (魔理沙 6 + 霊夢 5 = 11 表情)
  - row-range: IR 28 発話 ↔ CSV 60 行の粒度差を row_start/row_end で吸収
  - `uv run pytest`: 131 PASS (10 ファイル)
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
- 現在のスライス: G-06 done + extract-template done。パイプライン実装完了。Custom GPT v4 proof + 実台本 E2E が次
- 成功状態: face+bg 限定の全パイプライン E2E が通り、Level 3 (半自動制作ライン) に到達すること

---

## CURRENT LANE
- 主レーン: Advance
- 今このレーンを優先する理由: 演出 IR パイプライン (G-02→G-05→G-06) が実装完了し、Custom GPT v4 proof → 実台本 E2E で Level 3 到達を目指す段階のため

---

## DECISION LOG

| 日付 | 決定事項 | 選択肢 | 決定理由 |
|------|----------|--------|----------|
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

## HANDOFF SNAPSHOT (2026-04-03 更新)

- Shared Focus: G-05 v4 proof 完了 + production-slice patch-ymmp proof 完了 + Multi-Object IR 読み込み対応。次は実制作 28発話 ymmp を特定して extract-template → patch-ymmp full E2E
- Active Artifact: NLM transcript → YMM4 CSV → Writer IR → Template Registry → YMM4 Adapter → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → IR (Custom GPT) → Registry (JSON) → Adapter (patch-ymmp) → 演出設定 → レンダリング
- Last Change Relation: direct (load_ir Multi-Object 対応実装。G-05 v4 proof + production-slice patch-ymmp proof 完了)
- Evidence: 93 PASS。Custom GPT v4 IR 出力 (28 utterances, 全語彙チェック PASS)。production-slice patch-ymmp proof で face 13 / bg 2 変更を確認。YMM4 テンプレート構造 (ItemSettings.json) 実測確定。full E2E 用の実制作 ymmp は current workspace で未確認
- 案件モード: CLI artifact
- 現在の主レーン: Advance (演出パイプライン E2E)
- 成熟段階: Level 1 (限定変換器) 到達済み、Level 2 (演出IR適用エンジン) 形成中 → Level 3 接近
- Current Trust Assessment:
  - trusted: B-01~B-17 全字幕スタック (93 PASS)
  - trusted: G-02 IR 語彙 v1.0、G-02b ymmp 構造解析、G-06 patch-ymmp 実機検証
  - trusted: extract-template (face_map/bg_map 自動抽出)
  - trusted: G-05 v4 proof 完了。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の IR を正常出力
  - trusted: load_ir Multi-Object 対応 (2オブジェクト連結形式の読み込み)
  - needs re-check: motion/transition/overlay の ymmp 適用は未実装 (正式スコープ内の frontier)
  - needs re-check: 実制作 28発話 ymmp での face/bg 差し替え full E2E は未実施
  - needs re-check: VoiceItem が `TachieFaceParameter` を持たない箇所は face 差し替え対象外。テンプレート側前提の確認が必要
- Recovered Canonical Context:
  - Python はテキスト変換 + 演出 IR 定義 + ymmp 限定後段適用
  - 視覚配置 IR が中心課題。C-07 系が主系統、D-02 は従属的補助論点
  - patch-ymmp は Level 1 限定変換器。ゼロからの ymmp 生成とは区別する
  - 「未実装」は「境界外」ではない。motion/transition/overlay は正式スコープ内の frontier
  - YMM4 テンプレートは独立ファイルではなく ItemSettings.json の Templates 配列に JSON 保存
  - Custom GPT v4 は 2オブジェクト連結形式 (Macro + Micro) で IR を出力する。load_ir() で対応済み
- Authority Return Items:
  - 実制作 28発話 ymmp の所在確定 → face/bg 差し替え full E2E → YMM4 で開いて確認
  - motion/transition/overlay の ymmp 適用を次に進めるかの判断
  - E-02: hold 継続。E-01 とセットでのみ再検討
  - F-01/F-02: quarantined 継続
- What Not To Do Next:
  - D-02 を主軸として扱わない (従属的補助論点)
  - patch-ymmp を「研究か実用か」の二択で裁定しない (成熟段階モデルで評価)
  - motion/transition/overlay を「未実装だから境界外」と誤分類しない
  - quarantined 項目を通常候補としてそのまま spec 化しない
  - 素材取得/API 検討を再び中心にしない
- Expansion Risk: なし
## 2026-04-05 Structural Linebreak Redesign Note

- B-17 reflow v2 was reworked around structural major/minor boundaries instead of phrase-specific word lists.
- Page carry-over and in-page line breaks are now evaluated separately: page planning prefers major boundaries first, then falls back to minor boundaries only when necessary.
- Inline break scoring now strongly penalizes breaks inside short hiragana connector tails and around quoted/bracketed labels followed by explanatory nouns.
- Sample proof on `samples/AI監視が追い詰める生身の労働.txt` improved several screen-facing failures (`では / なく`, `）」 / という`, `） / 」`, `19 / 億`) while leaving a smaller residual cluster around `XというY` and quoted explanatory phrases that still need another structural pass.
