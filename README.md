# NLMYTGen

NotebookLM の出力を YMM4 (ゆっくりMovieMaker4) 用 CSV に変換し、演出 IR (中間表現) で S-6 (背景・演出設定) の半自動化を目指すパイプライン。

**GUI**: リポジトリ直下の [`start-gui.bat`](start-gui.bat) は **Shift_JIS (CP932) で保存**すること（UTF-8 / UTF-8-BOM にすると cmd で壊れる場合があります）。起動の速さのため、**`.venv` が既にあるときは `uv sync` をスキップ**します（強制したいときは `set NLMYTGEN_FORCE_UV_SYNC=1` のうえで実行）。初回はrepo rootで `npm --prefix gui ci` を実行すると、tracked lockどおりの `node_modules\.bin\electron` が使われる。

## ドキュメント最短経路（初日）

1. [AGENTS.md](AGENTS.md) — 短い入口ポインタ
2. [docs/REPO_LOCAL_RULES.md](docs/REPO_LOCAL_RULES.md) — 日常の実行・質問・検証・Git ルール
3. [docs/runtime-state.md](docs/runtime-state.md) — 160行以内の現在位置と次の decision point

GitHub 上で現在地だけを読む場合は
[docs/PROJECT_COCKPIT.md](docs/PROJECT_COCKPIT.md) を開いてください。機能全件は
[docs/FEATURE_REGISTRY.md](docs/FEATURE_REGISTRY.md)、複数 repo / worktree / sidequest の責務は
[docs/LANE_REGISTRY.md](docs/LANE_REGISTRY.md) にあります。詳細な文書地図は
[docs/NAV.md](docs/NAV.md) を参照してください（Claude Code 入口は
[.claude/CLAUDE.md](.claude/CLAUDE.md)）。

## 目的

1. NotebookLM で生成した Audio Overview のトランスクリプトを、YMM4 の台本読込フォーマットに変換する (CSV 変換 -- 実装済み)
2. 台本から演出 IR を定義し、LLM (Custom GPT) が構造化された演出指示を出力できるようにする (IR 仕様・prompt・validator -- 基盤実装済み)
3. 演出 IR + Template Registry + YMM4 Adapter で、S-6（背景・演出設定）の face / bg / slot / overlay / SE / 一部 motion・transition・skit group を capability matrix の範囲で半自動化する (基盤実装済み、最終 creative judgement は手動)

音声・字幕投入は YMM4 台本読込が不動の主経路。Python の責務は「テキスト変換 + 演出 IR 定義」であり、台本の品質は NotebookLM が生成する。

## 非目的

以下はこのプロジェクトの現行実装には含まれない:

- Python / Voicevox / MoviePy による直接動画生成
- NotebookLM を迂回した LLM による主台本生成
- ブラウザ向け **Web UI** / **API サーバー**（デスクトップの Electron GUI はスコープ内。[`gui/`](gui/)）
- YouTube 連携 / アップロード自動化 (台帳上は hold)
- RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection (`newsroom-yt-pipeline` 側の上流編集責務)
- 自前の音声合成 / TTS
- サムネイル生成
- .ymmp のゼロからの生成 (音声ファイル参照を含むため外部生成不可能。台本読込後の限定的な後段適用は patch-ymmp で実施)
- 素材の自動取得・ダウンロード (素材選定・収集は人間の責務)
- 多バックエンド対応 / プラグイン機構

## パイプライン

```
NotebookLM          Python (this repo)         LLM (Custom GPT)        YMM4
───────────         ──────────────────         ────────────────        ────
ソース投入 →
Audio Overview →
テキスト化 →        入力ファイル受取 →
                    パース・正規化 →
                    構造化スクリプト →
                    話者マッピング →
                    CSV 生成 →                                         台本読込 →
                    バリデーション →                                    音声合成 →
                                                                       字幕配置 →
                    台本テキスト ───→ Writer IR 生成 ──→                       ↓
                                      (scene_preset +                  [ymmp]
                                       optional override)                ↓
                                                  ↓                      ↓
                    Template Registry ── 意味ラベル→リソース解決           ↓
                                                  ↓                      ↓
                    YMM4 Adapter (patch-ymmp) ── face/bg 差し替え ──→ [ymmp']
                                                                       ↓
                                                            ──→ S-6 演出微調整 →
                                                                       レンダリング
```

**Path A (実装済み):** CSV 変換 → YMM4 台本読込 → 音声 + 字幕
**Path B (三層責務):** 台本 → Writer IR (LLM) → Template Registry (解決) → YMM4 Adapter (patch-ymmp) → S-6 微調整

## 入力

NotebookLM 由来のテキストファイル。以下のフォーマットを受け付ける:

- **CSV** (.csv): 2列 (話者名, テキスト)。ヘッダー行は自動スキップ
- **テキスト** (.txt): 話者タグ付き対話 (`Speaker: text` 形式)
- **ラベルなしテキスト** (.txt + `--unlabeled`): 話者タグなしの生テキスト。行交互で 2 話者 (Speaker_A/Speaker_B) に自動割当
- BOM 付き UTF-8 も自動対応

## 出力

YMM4 台本読込用 CSV:
- 2列、ヘッダーなし、UTF-8、カンマ区切り
- 列1: YMM4 キャラクター名
- 列2: 発話テキスト

## 使い方

### H-01 Packaging Brief の空テンプレ（品質診断の前段）

```bash
# Markdown テンプレ（仕様 v0.1 §5 相当）をファイルへ
python -m src.cli.main emit-packaging-brief-template -o packaging_brief.md

# 最小 JSON 骨格（score-evidence 等でそのまま読める形）
python -m src.cli.main emit-packaging-brief-template --format json -o packaging_brief.json
```

### CLI 一覧（抜粋）

```bash
# Episode 002 local reviewer packet (no YMM4 launch/import/render)
python -m src.cli.main build-surface-reviewer-packet --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_surface_alignment_repair_and_reviewer_packet_v1

# Episode 002 focused dark review brief (prior source record)
python -m src.cli.main build-focused-review-brief --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_focused_review_brief_dark_surface_v1

# Episode 002 compact review cockpit (weak-pass evaluated prototype)
python -m src.cli.main build-review-cockpit-compact --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_review_cockpit_compact_v1

# Episode 002 review layout research (pattern benchmark and wireframes)
python -m src.cli.main build-review-layout-research --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_review_layout_research_and_pattern_benchmark_v1

# CSV 生成
python -m src.cli.main build-csv input.txt -o output.csv --speaker-map Host1=れいむ,Host2=まりさ

# 話者マッピングファイルを使用 (JSON or key=value テキスト)
python -m src.cli.main build-csv input.txt --speaker-map-file speakers.json

# プレビュー (CSV を書かずに結果を確認)
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ --dry-run

# 統計表示付き
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ --stats

# 入力検証
python -m src.cli.main validate input.txt

# 入力の詳細分析 + マッピングプレビュー
python -m src.cli.main inspect input.txt --speaker-map Host1=れいむ,Host2=まりさ

# 話者マッピングテンプレートを自動生成
python -m src.cli.main generate-map input.txt > speakers.txt
# speakers.txt を編集して --speaker-map-file で使用

# B-15 Phase 1: 外部 LLM / Automation に渡す cue packet を生成
python -m src.cli.main build-cue-packet input.txt -o cue_packet.md

# JSON packet として出力
python -m src.cli.main build-cue-packet input.txt --format json -o cue_packet.json

# packet markdown/json と workflow proof 雛形をまとめて出力
python -m src.cli.main build-cue-packet input.txt --bundle-dir samples

# B-16: 外部 LLM / Automation に渡す diagram brief packet を生成
python -m src.cli.main build-diagram-packet input.txt -o diagram_packet.md

# diagram packet markdown/json と workflow proof 雛形をまとめて出力
python -m src.cli.main build-diagram-packet input.txt --bundle-dir samples

# 同一話者の連続発話を結合
python -m src.cli.main build-csv input.txt --merge-consecutive --speaker-map Host1=れいむ

# 表示幅ベースで字幕はみ出しを抑える
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ,Host2=まりさ --max-lines 2 --chars-per-line 40 --stats

# 2行字幕向けに自然な改行を入れつつ、長い一文は節単位で積極的に分ける
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ,Host2=まりさ --max-lines 2 --chars-per-line 40 --balance-lines --stats

# ラベルなし NLM transcript (話者タグなしの生テキスト)
python -m src.cli.main build-csv transcript.txt --unlabeled --speaker-map Speaker_A=れいむ,Speaker_B=まりさ

# ラベルなし + 連続結合 + 統計
python -m src.cli.main build-csv transcript.txt --unlabeled --merge-consecutive --speaker-map Speaker_A=れいむ,Speaker_B=まりさ --stats

# 複数ファイル一括処理 (各ファイルに {stem}_ymm4.csv を生成)
python -m src.cli.main build-csv file1.txt file2.txt file3.txt --speaker-map Host1=れいむ,Host2=まりさ
```

## 開発環境とテスト

このリポジトリは `uv` を推奨する。`pytest` は `pyproject.toml` の
optional `dev` にあるため、開発 checkout では extra を明示する。
`uv.lock` と `gui/package-lock.json` はtracked dependency authorityであり、
fresh checkoutでも必ずlocked installを使う。

```bash
uv sync --extra dev --locked
npm --prefix gui ci
npm --prefix gui ls --depth=0
node -p "require('./gui/node_modules/electron/package.json').version"
uv run python scripts/check_project_state_sync.py
```

状態面を変更したときは上記 checker を明示的に実行すると、runtime と cockpit の
共有フィールド、更新日、README からの導線を検査できる。自動 Stop hook ではない。

現在の green baseline は、変更対象の narrow test を選ぶ方式です。今回の
state alignment と Episode 002 観測経路は次で検証できます。

```powershell
uv run pytest tests/test_guardrails.py tests/test_project_state_sync.py tests/test_ymm4_observation_readback_pack.py tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_real_input_replacement_readiness_pack.py -q
```

`uv run pytest` の全体 baseline には、生成済み artifact / 旧絶対 path の既知 drift
（2026-07-10 の監査実行で 22 failures）があり、一部の生成テストは
追跡済み fixture を書き換える。通常開発の既定 gate にはせず、明示した Integrity /
Triage slice で clean-state snapshot を取ってから隔離・修復する。

pytest は `src/` または `tests/` を変更したブロックの終わりに、変更対象の narrow
test から走らせる。integration テストは `conftest.py` で default-skip、全件走らせたい
時だけ `NLMYTGEN_PYTEST_FULL=1 uv run pytest`。上記の既知 full-suite drift と tracked
fixture write を解消するまでは、通常 closeout で全体実行しない。

WSL で実行する場合は `TMPDIR=/tmp TMP=/tmp TEMP=/tmp` を設定してから `pytest` を実行すると一時ファイルのパスずれを避けられる。

## LLM の役割

このプロジェクトで LLM を使う場合、責務は以下に限定する:

- transcript / notes の構造化
- セグメント化
- タイトル・見出し・要約の補助
- CSV 向けフィールド整形

LLM は NotebookLM の代替としての主台本生成には使わない。
LLM の主要な新しい役割は、台本から演出 IR (構造化 JSON) を生成すること (G-05 v4 プロンプト)。IR は意味ラベルのみを含み、座標・ファイルパスはテンプレート定義側で解決する。
Phase 1 では `build-cue-packet` により、外部 LLM / Automation に渡す text-only cue packet を生成する。
現在の cue contract は、section ごとに `主背景 1 つ + 補助素材 1 つ` を基本とし、音の cue は optional 扱いに寄せている。
図作成 bottleneck 向けには `build-diagram-packet` により、図版そのものではなく「図作成前の text-only brief」を生成できる。
