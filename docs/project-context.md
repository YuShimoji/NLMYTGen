# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現フェーズ: B-15 / B-16 の初回 proof を踏まえ、micro-fix を止めて次の evidence-driven 判断へ進む段階
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
  - ユーザーメモを反映し、LLM は主台本のゼロ生成には使わず、NotebookLM 由来の既存台本に対する接続・役割整合性調整・再編集指示の自動化を将来候補として扱う方針を canonical docs に固定
  - 改行アルゴリズムの追加案は、即 heuristic 化せず、引用・括弧・数値+記号・文字種境界・早め折り返しを字幕 corpus / 評価観点として先に蓄積する方針に整理
  - feasibility audit: 字幕分割以外の候補を再棚卸しし、次の本命候補は S-6 LLM adapter、E-01/E-02 は secondary、quarantine 群は据え置きと整理
  - `B-15 LLM prep packet` を FEATURE_REGISTRY に `proposed` として登録。Phase 1 は cue memo only、Phase 2 は constrained rewrite 候補として packet 化
  - `docs/verification/B15-llm-prep-packet-proposal.md` と `docs/ADR/0004-llm-text-assist-boundary.md` を追加し、text-only boundary と approval 条件を明文化
  - ユーザー承認により B-15 Phase 1 (cue memo only) を approved に昇格
  - `build-cue-packet` CLI を実装し、NotebookLM transcript から外部 LLM / Automation に渡す cue packet を生成できるようにした
  - packet context に `section_seeds` を追加し、host の話題転換句と発話数をもとにした暫定セクション境界も外部 LLM 側へ渡せるようにした
  - sample で `build-cue-packet --format json` の出力を確認し、`samples/AI監視が追い詰める生身の労働_cue_packet.md/.json` を生成。`samples/AI監視が追い詰める生身の労働_cue_memo_example.md` に output contract 見本も作成。環境に `uv` / `pytest` がないため自動テストは未実施
  - `--bundle-dir` を追加し、sample の packet markdown/json と workflow proof 雛形を一括生成できるようにした
  - 外部 LLM からの実 cue memo を受領し、`samples/AI監視が追い詰める生身の労働_cue_memo_received.md` に保存。section 再構成と operator_todos が特に有用だと確認
  - 初回 proof では、S-6 の方針メモ化が 30〜60 分想定から 5 分へ短縮。役に立ったのは全体構成・粒度・具体例・方向性で、ノイズは主に SE 関連
  - ただし、素材選定・図作成・動画素材の尺つなぎ・フリー素材探索は別 bottleneck として強く残ることも確認
  - これを受けて、cue contract を `primary_background` / `supporting_visual` / `sound_cue_optional` へ更新し、背景候補の圧縮と SE optional 化を反映
  - さらに `response_preferences` を追加し、section 数、背景密度、operator_todos 数の上限も packet 側から誘導できるようにした
  - rerun では 4 section に収まり、background が primary/supporting に揃い、sound cue も減少。contract 改善の効果を確認
  - B-15 が削れたのは主に「方針メモ化」であり、S-6 に残る素材選定・図作成・フリー素材探索・動画素材の尺つなぎは別 bottleneck だと整理
  - `docs/verification/S6-material-bottleneck-feasibility-2026-03-31.md` を追加し、次に proposal 化するなら automated acquisition ではなく text-only の `asset / diagram brief` 系が自然だと整理
  - `docs/verification/S6-text-brief-candidate-comparison-2026-03-31.md` を追加し、narrow candidate の比較では `diagram brief` が最初の proposal 候補として最も説明しやすいと整理
  - `docs/verification/diagram-brief-proposal-draft-2026-03-31.md` を追加し、B-15 との差分、output contract、acceptance、non-goals を備えた draft を作成
  - ユーザー承認により `docs/verification/B16-diagram-brief-proposal.md` を追加し、B-16 `Diagram brief packet` を FEATURE_REGISTRY に `proposed` 登録した
  - 続く承認により B-16 を `approved` に進め、`build-diagram-packet` の初手実装と workflow proof 雛形を追加した
  - sample で `build-diagram-packet --format json` と `--bundle-dir samples` の出力を確認し、`samples/AI監視が追い詰める生身の労働_diagram_packet.md/.json` と proof 雛形を生成した
  - B-16 の初回レスポンスを受領し、3 図構成・`goal` / `must_include` / `avoid_misread` の有用性が高いことを確認。残る未記入は時間差のみ
  - B-16 初回 proof の時間差も埋まり、diagram planning は 15 分想定から 3 分程度へ短縮、delta は 12 分と記録した
  - 軽微改善として、background だけで十分な section を diagram brief から外しやすくする response preference を B-16 packet に追加した
  - その後の `b16-v2` でも Linux 側 venv 経由の full pytest を再実行し、65 passed を確認した
  - さらに `build-diagram-packet --bundle-dir` で rerun prompt、rerun diff template、quickstart、baseline notes も自動生成するようにし、B-16 rerun の手動準備を packet bundle 側へ寄せた
  - `docs/verification/development-plan-reset-2026-03-31.md` を追加し、次の順序を「B-16 rerun 回収 → B-16 収束判断 → `asset brief` / `search query brief` 比較 → 1件だけ proposal 化」に立て直した
  - `docs/verification/asset-vs-search-brief-comparison-2026-03-31.md` を追加し、B-16 後の本命候補は現状 `asset brief`、ただし search 起点へ反転する条件も残した
  - B-16 rerun を受領し、導入専用図を減らして `S1-S2` の監視構造へ統合する形で絞り込みが進んだため、B-16 は大きな追加 tweak なしで収束候補と見なせる状態になった
  - `docs/verification/asset-brief-proposal-draft-2026-03-31.md` を追加し、次候補を `asset brief` として proposal 化するための draft を用意した
  - `docs/verification/B17-asset-brief-proposal.md` を追加し、B-17 `Asset brief packet` を `proposed` として formalize した
  - rerun 前に比較しやすいよう、`samples/AI監視が追い詰める生身の労働_diagram_baseline_notes.md` を追加した
  - rerun 差分を短く残せるよう、`samples/AI監視が追い詰める生身の労働_diagram_rerun_diff_template.md` を追加した
  - さらに `samples/AI監視が追い詰める生身の労働_diagram_quickstart.md` を追加し、次回の手動確認を最短手順に圧縮した
  - WSL では repo 直下の `.venv` が Windows 形式だったため、`~/.local/bin/uv venv .venv-linux` と `uv pip install -r requirements-dev.txt --python .venv-linux` を使って Linux 側 pytest 実行経路を再現し、65 passed を確認した
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
- 現在のスライス: rerun まで反映済み。B-15 Phase 1 はいったん収束候補で、B-16 は初回 proof まで完了
- 成功状態: B-15 の改善で、方針メモ化の短縮と cue density の圧縮が両方確認できている。B-16 も diagram planning を 15 分想定から 3 分程度まで短縮できた

---

## CURRENT LANE
- 主レーン: Advance
- 今このレーンを優先する理由: 初回 proof で value path は立ったため、次はノイズ削減と bottleneck の切り分けを進める価値が高いため

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
| 2026-03-31 | LLM 利用の境界を「主台本のゼロ生成は禁止、既存台本の constrained rewrite は候補」に明確化 | 全面禁止 / constrained rewrite 許容 | NotebookLM を upstream に保ちつつ、2 本の台本接続や役割整合性調整の自動化余地を残すため |
| 2026-03-31 | YMM4 / `.ymmp` direct edit は避け、Automation はまず text-side 補助から始める | direct edit 試行 / text-side 補助優先 | 文字列編集で壊れやすく、ハマるリスクが高いため。プリセット再利用やコピペ補助から workflow proof を積む方が安全 |
| 2026-03-31 | 字幕改行の追加案は heuristic 即実装ではなく corpus-first で扱う | heuristic 先行 / corpus 先行 | 残 pain が individual judgement 段階に移っており、固定ルールを増やす前に評価例を集める方が自然なため |
| 2026-03-31 | B-15 は Phase 1 を cue memo only、Phase 2 を constrained rewrite に分けて proposal 化する | 一括提案 / 段階分割 | value path を明確にしつつ、主台本生成境界を壊さず approval を取りやすくするため |
| 2026-03-31 | B-15 Phase 1 の初手は provider 内蔵ではなく `build-cue-packet` で進める | SDK 先行 / packet 先行 | text-only boundary を守ったまま外部 Automation / 手動実行で workflow proof を取りやすいため |
| 2026-03-31 | B-15 初回 proof の次改善は SE optional 化と背景候補の圧縮に寄せる | 機能追加 / contract 改善 | value は確認できたが、ノイズと過剰列挙を減らした方が次の運用に効くため |
| 2026-03-31 | `diagram brief` を B-16 として `proposed` 登録する | draft 止まり / proposed 登録 | 図作成 bottleneck は B-15 と役割分離しやすく、text-only narrow candidate として approval 判断に載せられる粒度まで整理できたため |
| 2026-03-31 | B-16 を approved に進め、`build-diagram-packet` を初手実装する | docsのみ / 初手実装 | B-15 と同様に、まずは text-only packet + proof template を持つ形が最短で workflow proof に繋がるため |

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

- Shared Focus: B-15 Phase 1 の成果を維持しつつ、素材取得系 bottleneck を narrow な text-only candidate へ切り出せるか見極める
- Active Artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → 動画
- Last Change Relation: direct (B-16 の diagram brief 準備に直接使える CLI を実装)
- Evidence: `uv run pytest` 56 PASS、`--balance-lines` 付き実データ dry-run/stats 確認、sample は 57 発話 → 95 行に再編、overflow candidates は 3 件、追加観測では全字幕が 3 行以内に収まるまで改善
- Evidence: `docs/verification/next-frontier-feasibility-2026-03-31.md` に候補比較を作成。S-6 が strongest next candidate、E-01/E-02 が secondary と整理
- Evidence: `docs/verification/B15-llm-prep-packet-proposal.md` と `docs/ADR/0004-llm-text-assist-boundary.md` を追加し、Phase 1 / Phase 2 / text-only boundary / approval 条件を明文化
- Evidence: `python3 -m src.cli.main build-cue-packet samples/AI監視が追い詰める生身の労働.txt --format json` が成功し、sample packet を出力できた
- Evidence: `samples/AI監視が追い詰める生身の労働_cue_packet.md` と `samples/AI監視が追い詰める生身の労働_cue_packet.json` を生成し、`section_seeds` 3 件を確認
- Evidence: `samples/AI監視が追い詰める生身の労働_cue_workflow_proof.md` を生成し、proof 記録先まで含めて artifact を揃えた
- Evidence: `samples/AI監視が追い詰める生身の労働_cue_memo_example.md` に cue memo の見本を作成し、output contract の実用粒度を確認できる状態にした
- Evidence: `samples/AI監視が追い詰める生身の労働_cue_memo_received.md` に実レスポンスを記録。background 候補の過剰列挙を減らすとさらに扱いやすい、という改善方向も見えた
- Evidence: 初回観測では S-6 方針メモ化が 30〜60 分想定から 5 分へ短縮し、B-15 の value path が成立
- Evidence: packet に `response_preferences` を加え、次の再試行で section 数や operator_todos 数の揺れを減らせる状態にした
- Evidence: rerun では 4 section に収まり、primary/supporting と optional sound cue の方針が概ね守られた
- Evidence: `python3 -m src.cli.main build-diagram-packet samples/AI監視が追い詰める生身の労働.txt --format json` が成功し、B-16 packet を出力できた
- Evidence: `samples/AI監視が追い詰める生身の労働_diagram_packet.md`、`samples/AI監視が追い詰める生身の労働_diagram_packet.json`、`samples/AI監視が追い詰める生身の労働_diagram_workflow_proof.md` を生成した
- Evidence: `samples/AI監視が追い詰める生身の労働_diagram_brief_received.md` に実レスポンスを保存し、diagram planning 用として質が高いことを確認した
- Evidence: `samples/AI監視が追い詰める生身の労働_diagram_workflow_proof.md` に before 15 / after 3 / delta 12 を記録した
- Evidence: 更新後 `tests/test_diagram_brief.py` を `TMPDIR=/tmp TMP=/tmp TEMP=/tmp .venv-linux/bin/python -m pytest tests/test_diagram_brief.py` で再実行し、4 passed を確認した
- Evidence: さらに `TMPDIR=/tmp TMP=/tmp TEMP=/tmp .venv-linux/bin/python -m pytest` を再実行し、65 passed を確認した
- Evidence: baseline notes を sample に追加し、次の B-16 rerun は proof log 全文ではなく baseline 差分中心で見られるようにした
- Evidence: rerun diff template を sample に追加し、次回は差分記録を 1 ファイルで完結できるようにした
- Evidence: quickstart を sample に追加し、次回の B-16 rerun は 1 ファイル読むだけで始められるようにした
- Evidence: `TMPDIR=/tmp TMP=/tmp TEMP=/tmp .venv-linux/bin/python -m pytest` で 65 passed を確認。bare の `python3 -m pytest` は現シェルでは使えず、WSL 側 venv 明示が必要
- 案件モード: CLI artifact
- 現在の主レーン: Advance (B-16 initial implementation)
- Current Trust Assessment:
  - trusted: B-04 実装、A-04 `fetch-topics` 実装、56 PASS の現行テスト、workflow/境界 docs
  - trusted: B-11 の初回 proof（辞書 0、timing 0、改行系 pain が支配的）
  - trusted: B-12 `--balance-lines` 実装。2行字幕向けに自然改行を opt-in で挿入し、CSV 1行内改行保持もテスト済み
  - trusted: B-12 の post-import 再観測により、改善点と残課題が定量化できた
  - trusted: B-13 clause-aware split + widow/orphan guard 実装。sample で 57 発話 → 62 行への再編を確認
  - trusted: B-13 の post-import 再観測により、改善幅と限界が定量化できた
  - trusted: B-14 aggressive clause chunking 実装。sample で 57 発話 → 95 行、overflow candidates 3 件まで低減し、全字幕 3 行以内まで改善
  - trusted: B-15 packet により、LLM 利用範囲を text-only assist に固定し、Phase 1 と Phase 2 を分離できた
  - trusted: `build-cue-packet` が sample transcript から packet を出力できること
  - trusted: `section_seeds` により、外部 LLM 側へ暫定セクション境界も渡せるようになった
  - trusted: proof bundle により、workflow proof の記録先まで一括生成できること
  - trusted: 実 cue memo レスポンスは section 構造と operator_todos が有用で、B-15 の value path が概ね成立していること
  - trusted: 時間短縮は大きいが、これは主に「方針決め」の短縮であり、素材取得 bottleneck まで消したわけではない
  - trusted: 次改善が contract 圧縮であることは明確
  - trusted: 追加の軽微改善で response の振れ幅も抑えにいける
  - trusted: rerun で cue density の圧縮が効いた
  - trusted: 次に狙うべき未解決 pain は、取得自動化そのものではなく、素材選定・図作成の手前にある判断材料の不足である
  - trusted: B-16 `build-diagram-packet` が sample transcript から packet と workflow proof 雛形を生成できること
  - trusted: B-16 の初回レスポンスは、図に向く区間の絞り込み、`must_include`、`avoid_misread` の粒度が良く、B-15 とは別役割として成立していること
  - trusted: B-16 初回 proof では、diagram planning の白紙時間を 12 分程度短縮できたこと
  - trusted: 軽微改善後も B-16 の packet 生成と diagram brief テストは壊れていないこと
  - trusted: `b16-v2` の軽微改善後も full test suite は green であること
  - needs re-check: 残る境界ケース (`ー`, `「」`, 数値+記号) を heuristic で吸うべきか、corpus として集めるべきか
  - trusted: LLM は主台本のゼロ生成には使わず、既存台本の接続や役割整合性調整の constrained rewrite を候補に含める、という境界整理
  - needs re-check: cue packet の section 粒度と output contract が実運用に十分か
  - dangerous: status 語彙を曖昧にしたまま次 frontier を選ぶこと、GUI や LLM 案を value path 未検証で前進させること
- Recovered Canonical Context:
  - Python はテキスト変換のみ
  - S-5 / S-6 が最大 pain
  - サムネイルは重要で手動判断を残す
  - approved は仕様定義済み + ユーザー承認済みのみ
  - LLM は主台本のゼロ生成には使わず、NotebookLM 由来台本の constrained rewrite は将来候補に含める
- Authority Return Items:
  - B-16 の次改善を contract 圧縮に寄せるか、このままもう1本 proof を取るか
  - 「stdlib のみ」制約の緩和 (LLM SDK 追加の ADR)
  - E-02: hold のまま。E-01 または別 integration point とセットでのみ再検討
  - quarantined 3件 (D-02, F-01, F-02) の個別再審査
- 解決済み:
  - feasibility audit: 字幕分割以外の候補を棚卸しし、S-6 LLM adapter が次の本命候補だと整理
  - B-15 proposal packet: Phase 1 を cue memo only、Phase 2 を constrained rewrite 候補として切り分け、approval に必要な文書を作成
  - B-15 Phase 1: ユーザー承認で approved 化し、`build-cue-packet` CLI を実装
  - B-15 packet improvement: `section_seeds` を追加し、sample packet files も生成
  - B-15 example output: cue memo の見本 artifact を sample に追加
  - B-15 proof support: workflow proof 雛形を bundle 出力できるようにした
  - B-15 external response: 実 cue memo を受領し、残る主検証が時間差の観測に絞られた
  - B-15 initial proof: 30〜60 分想定の方針メモ化を 5 分まで短縮できた
  - B-15 contract refinement: 背景候補の圧縮と SE optional 化へ舵を切った
  - B-15 rerun: 4 section、primary/supporting 構成、sound cue の減少を確認
  - S-6 material bottleneck feasibility: B-15 後に残る pain を、素材選定 / 図作成 / フリー素材探索 / 尺つなぎへ分解し、次候補は automated acquisition ではなく `asset / diagram brief` 系が自然だと整理
  - S-6 text brief candidate comparison: `diagram brief` / `asset brief` / `search query brief` / `pacing brief` を比較し、最初の候補は `diagram brief` が自然だと整理
  - diagram brief proposal draft: B-15 との差分、最小 scope、output contract、acceptance を備えた draft まで作成
  - B-16 proposal: `Diagram brief packet` を `proposed` として登録し、approval 用 packet を固定
  - B-16 initial implementation: `build-diagram-packet` と workflow proof 雛形を追加し、sample transcript で packet 生成を確認
  - B-16 first response: diagram brief の実レスポンスを保存し、質的評価を proof log に反映
  - B-16 first proof timing: before 15 / after 3 / delta 12 を記録
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
  - B-16 は初回 proof まで完了したが、contract をさらに絞るべきかは未判断
  - 前回 handoff は `8a1c710` の追加ファイルと placeholder 状態を含んでいなかった
  - B-14 は CLI 側では strong win。次の論点は bulk overflow ではなく、境界ケースを rule で吸うか corpus として管理するか
- Docs-only Resume Packet:
  - AGENTS.md
  - .claude/CLAUDE.md
  - docs/ai/CORE_RULESET.md, docs/ai/DECISION_GATES.md, docs/ai/STATUS_AND_HANDOFF.md, docs/ai/WORKFLOWS_AND_PHASES.md
  - docs/INVARIANTS.md, docs/USER_REQUEST_LEDGER.md, docs/OPERATOR_WORKFLOW.md, docs/INTERACTION_NOTES.md
  - docs/runtime-state.md, docs/project-context.md, docs/FEATURE_REGISTRY.md, docs/AUTOMATION_BOUNDARY.md
  - prompt-resume.md
- 未確定の設計論点: 素材取得 bottleneck への接続点、SDK を repo 内へ入れるか、GUI が本当に bottleneck を減らすか
- What Not To Do Next:
  - quarantined 項目 (D-02, F-01, F-02) を通常候補としてそのまま spec 化しない
  - E-02 を standalone の高価値 task として再浮上させない
  - 素材取得 bottleneck まで B-15 が解決したかのように扱わない
  - SDK 導入や Phase 2 rewrite 実装へ飛び込まない
  - GUI や quarantine 項目へ横滑りしない
  - handoff に書かれていない placeholder docs を真実の source と誤認しない
- New Fossils:
  - docs/INVARIANTS.md
  - docs/USER_REQUEST_LEDGER.md
  - docs/OPERATOR_WORKFLOW.md
  - docs/INTERACTION_NOTES.md
  - 2026-03-31 のユーザーメモ反映: LLM constrained rewrite 境界 / Automation 許容範囲 / 字幕 corpus-first 方針
  - docs/verification/B15-llm-prep-packet-proposal.md
  - docs/ADR/0004-llm-text-assist-boundary.md
  - docs/verification/B15-cue-packet-implementation.md
  - docs/verification/B15-workflow-proof.md
  - docs/verification/S6-material-bottleneck-feasibility-2026-03-31.md
  - docs/verification/S6-text-brief-candidate-comparison-2026-03-31.md
  - docs/verification/diagram-brief-proposal-draft-2026-03-31.md
  - docs/verification/B16-diagram-brief-proposal.md
  - docs/verification/B16-diagram-brief-implementation.md
  - docs/verification/B16-rerun-checklist.md
  - samples/AI監視が追い詰める生身の労働_diagram_brief_received.md
- Expansion Risk: なし
