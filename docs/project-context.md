# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現フェーズ: B-14 aggressive clause chunking を実装し、post-import visual evidence を待つ段階
- 直近の状態 (2026-03-31):
  - B-04 分割品質改善: 表示幅ベース分割 (--display-width, --max-lines, --chars-per-line) 実装完了
  - A-04 RSS フィード連携 (`fetch-topics`): 再審査済み + 実装完了。done へ復帰
  - `uv run pytest`: 56 PASS。`B-14` を含む現ワークツリーのテスト再現に成功
  - 実データ dry-run + stats で CLI 動作確認
  - B-11 S-5 workflow proof: ユーザー承認で approved frontier に昇格。proof 条件と evidence packet を固定
  - B-11 初回 pre-import 証跡: `samples/AI監視が追い詰める生身の労働.txt` を `--max-lines 2 --chars-per-line 40 --stats --dry-run` で確認し、57 発話 / overflow warnings 34 を記録
  - B-11 初回 post-import 観測: 辞書登録 0、タイミングのみ 0、手動改行 / 再分割したい長文が約30件。S-5 の主因は読みではなく字幕改行のバランスだった
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
- Active Artifact: NLM transcript → YMM4 CSV → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → 動画
- 現在のスライス: B-14 の追加観測まで反映済み。次は S-6 LLM adapter を本命候補として spec/ADR feasibility を詰める
- 成功状態: 字幕分割を局所最適のまま引っ張らず、次 frontier 候補を value path 付きで比較できる

---

## CURRENT LANE
- 主レーン: Advance
- 今このレーンを優先する理由: 字幕分割の bulk pain がほぼ収束し、次の大きな効率化候補として S-6 LLM adapter の feasibility を詰める価値が最も高いため

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

## HANDOFF SNAPSHOT

- Shared Focus: 字幕分割はいったん収束扱いにし、S-6 LLM adapter を次 frontier 候補として feasibility で比較する
- Active Artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → 動画
- Last Change Relation: direct (S-5 の主 pain だった字幕改行バランスへ直接効く opt-in 改善を実装)
- Evidence: `uv run pytest` 56 PASS、`--balance-lines` 付き実データ dry-run/stats 確認、sample は 57 発話 → 95 行に再編、overflow candidates は 3 件、追加観測では全字幕が 3 行以内に収まるまで改善
- Evidence: `docs/verification/next-frontier-feasibility-2026-03-31.md` に候補比較を作成。S-6 が strongest next candidate、E-01/E-02 が secondary と整理
- 案件モード: CLI artifact
- 現在の主レーン: Advance (B-14 aggressive clause chunking implementation)
- Current Trust Assessment:
  - trusted: B-04 実装、A-04 `fetch-topics` 実装、56 PASS の現行テスト、workflow/境界 docs
  - trusted: B-11 の初回 proof（辞書 0、timing 0、改行系 pain が支配的）
  - trusted: B-12 `--balance-lines` 実装。2行字幕向けに自然改行を opt-in で挿入し、CSV 1行内改行保持もテスト済み
  - trusted: B-12 の post-import 再観測により、改善点と残課題が定量化できた
  - trusted: B-13 clause-aware split + widow/orphan guard 実装。sample で 57 発話 → 62 行への再編を確認
  - trusted: B-13 の post-import 再観測により、改善幅と限界が定量化できた
  - trusted: B-14 aggressive clause chunking 実装。sample で 57 発話 → 95 行、overflow candidates 3 件まで低減し、全字幕 3 行以内まで改善
  - needs re-check: 残る境界ケース (`ー`, `「」`, 数値+記号) を heuristic で吸うべきか、corpus として集めるべきか
  - dangerous: status 語彙を曖昧にしたまま次 frontier を選ぶこと、GUI や LLM 案を value path 未検証で前進させること
- Recovered Canonical Context:
  - Python はテキスト変換のみ
  - S-5 / S-6 が最大 pain
  - サムネイルは重要で手動判断を残す
  - approved は仕様定義済み + ユーザー承認済みのみ
- Authority Return Items:
  - S-6 LLM アダプター方式を次 frontier にするかの再承認
  - 「stdlib のみ」制約の緩和 (LLM SDK 追加の ADR)
  - E-02: hold のまま。E-01 または別 integration point とセットでのみ再検討
  - quarantined 3件 (D-02, F-01, F-02) の個別再審査
- 解決済み:
  - feasibility audit: 字幕分割以外の候補を棚卸しし、S-6 LLM adapter が次の本命候補だと整理
  - B-11 S-5 workflow proof: ユーザー承認により approved frontier 化し、初回 proof を完了
  - B-11 初回 post-import 観測: S-5 の主因が読みではなく字幕改行バランスだと確認
  - B-12 行バランス重視の字幕分割: `--balance-lines` を実装し、CLI / tests / docs を同期
  - B-12 post-import 再観測: 手動改行 10 / 再分割 15 / 不自然な単語分割 5。`。` 改行は効くが、句読点の少ない長文と 1 文字最終行が残る
  - B-13 節分割 + widow/orphan guard: `--balance-lines` の内部改善として実装し、54 PASS と sample dry-run で挙動確認
  - B-13 post-import 再観測: 手動改行 5 / 再分割 10 / 不自然な単語分割 5。減りはしたがまだ多く、長い一文 1 字幕問題が残る
  - B-14 aggressive clause chunking: 複数文発話の中にある単一長文も再展開するよう実装し、56 PASS。sample dry-run では 57 発話 → 95 行、overflow candidates 3 件まで低減。追加観測では長すぎる行が大幅に減り、残課題は境界ケースの改行品質へ移行
  - A-04 RSS フィード連携: `fetch-topics` 実装と docs を再審査し、done に復帰
  - B-04 表示幅ベース分割: --display-width, --max-lines, --chars-per-line 実装完了
  - B-10 (--emit-meta): rejected → コード除去済み
  - C-02/C-03/C-04/C-05/D-01/F-03: rejected
  - E-02 仕様検討: 単体では価値薄と判明し hold へ整理
  - S-6 stdlib 制約内分析: 精度不足で断念 → LLM 方式に転換
  - canonical docs (`INVARIANTS`, `USER_REQUEST_LEDGER`, `OPERATOR_WORKFLOW`, `INTERACTION_NOTES`) を実内容で補完
- 既知の問題:
  - S-6 LLM アダプター方式の仕様が未定義 (プロバイダー・アーキテクチャ・stdlib制約緩和)
  - 前回 handoff は `8a1c710` の追加ファイルと placeholder 状態を含んでいなかった
  - B-14 は CLI 側では strong win。次の論点は bulk overflow ではなく、境界ケースを rule で吸うか corpus として管理するか
- Docs-only Resume Packet:
  - AGENTS.md
  - .claude/CLAUDE.md
  - docs/ai/CORE_RULESET.md, docs/ai/DECISION_GATES.md, docs/ai/STATUS_AND_HANDOFF.md, docs/ai/WORKFLOWS_AND_PHASES.md
  - docs/INVARIANTS.md, docs/USER_REQUEST_LEDGER.md, docs/OPERATOR_WORKFLOW.md, docs/INTERACTION_NOTES.md
  - docs/runtime-state.md, docs/project-context.md, docs/FEATURE_REGISTRY.md, docs/AUTOMATION_BOUNDARY.md
  - prompt-resume.md
- 未確定の設計論点: LLM アダプターを本当にやるか、GUI が本当に bottleneck を減らすか
- What Not To Do Next:
  - quarantined 項目 (D-02, F-01, F-02) を通常候補としてそのまま spec 化しない
  - E-02 を standalone の高価値 task として再浮上させない
  - S-6 の spec/ADR feasibility を詰める前に、GUI や quarantine 項目へ横滑りしない
  - handoff に書かれていない placeholder docs を真実の source と誤認しない
- New Fossils:
  - docs/INVARIANTS.md
  - docs/USER_REQUEST_LEDGER.md
  - docs/OPERATOR_WORKFLOW.md
  - docs/INTERACTION_NOTES.md
- Expansion Risk: なし
