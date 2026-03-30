# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現フェーズ: backlog/status hygiene 監査と canonical context 修復完了。approved next frontier を再選定する段階
- 直近の状態 (2026-03-30):
  - B-04 分割品質改善: 表示幅ベース分割 (--display-width, --max-lines, --chars-per-line) 実装完了
  - A-04 RSS フィード連携 (`fetch-topics`): 再審査済み + 実装完了。done へ復帰
  - `uv run pytest`: 46 PASS。feed 系の追加実装を含めて現ワークツリーのテスト再現に成功
  - 実データ dry-run + stats で CLI 動作確認
  - E-02 (YouTube メタデータ生成): 仕様検討の結果、hold へ移動。単体では価値薄
  - D-02 / F-01 / F-02: 汚染バッチ由来として quarantined のまま
  - C-01 (YMM4 台本読込): Python 機能ではなく確認済み手動工程として info へ整理
  - FEATURE_REGISTRY: done 12 / info 2 / hold 3 / quarantined 3 / rejected 7
  - approved frontier は現時点で空。S-5/S-6 まわりは authority return items と workflow proof 候補として保持
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
- 現在のスライス: docs 同期完了。approved frontier が空のため、next frontier 選定待ち
- 成功状態: docs が実態と一致し、46 テスト PASS。次 frontier をユーザーと選定できる状態

---

## CURRENT LANE
- 主レーン: Audit → docs sync 完了。next frontier 選定待ち
- 今このレーンを優先する理由: docs 同期が完了し、approved frontier が空。次の実装対象はユーザー判断 (HUMAN_AUTHORITY)

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

- Shared Focus: docs 同期完了、46 PASS。approved frontier が空のため、次 frontier をユーザーと選定する
- Active Artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → 動画
- Last Change Relation: evidence-only (status/doc 整備とテスト再検証で次 frontier の誤選択を防止)
- Evidence: `uv run pytest` 46 PASS、`python3 -m src.cli.main --help` OK、実データ dry-run/stats 確認
- 案件モード: CLI artifact
- 現在の主レーン: docs sync 完了、next frontier 選定待ち
- Current Trust Assessment:
  - trusted: B-04 実装、A-04 `fetch-topics` 実装、46 PASS の現行テスト、workflow/境界 docs
  - needs re-check: S-5/S-6 の post-import friction と visual evidence の鮮度
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
  - S-5/S-6 については fresh visual evidence がなく、次 frontier の根拠が docs/推論寄り
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
  - approved frontier が空のまま、勢いで別の実装 task を捏造しない
  - handoff に書かれていない placeholder docs を真実の source と誤認しない
- New Fossils:
  - docs/INVARIANTS.md
  - docs/USER_REQUEST_LEDGER.md
  - docs/OPERATOR_WORKFLOW.md
  - docs/INTERACTION_NOTES.md
- Expansion Risk: なし
