# MIGRATION LEDGER

旧リポジトリ (NLMandSlideVideoGenerator) からの移植判定台帳。
Whitelist 方式: 明示的に「参照可」と判定されたもののみ、v2 の設計に合わせて書き直す。

## 判定基準

- **参照可 (reference)**: v2 の責務境界・命名に合わせて書き直す。そのままコピーしない。
- **保留 (hold)**: 現時点では不要。将来スコープに入る可能性あり。
- **禁止 (reject)**: v2 の原則に反する。移植しない。

---

## 参照可 (reference material for Phase 1 rewrite)

| 旧ファイル | 参照する部分 | v2 での使用先 | 注意 |
|-----------|-------------|-------------|------|
| `src/core/csv_assembler.py` (242行) | `_SPEAKER_PREFIX_RE` 正規表現パターン | `src/pipeline/assemble_csv.py` | async 不使用、AnimationAssigner 依存を除去 |
| `src/core/csv_assembler.py` | CSV writer (no header, UTF-8) | `src/contracts/ymm4_csv_schema.py` | 4列→2列に簡素化 |
| `src/notebook_lm/csv_transcript_loader.py` (213行) | CSV 読み取りロジック (2列検出、空行スキップ) | `src/pipeline/normalize.py` | async 不使用、TranscriptInfo/AudioInfo 依存を除去 |
| `samples/basic_dialogue/timeline.csv` | YMM4 台本読込フォーマットのサンプル | `samples/example_dialogue.csv` | フォーマット参照のみ |

## 保留 (hold)

| 旧ファイル | 理由 |
|-----------|------|
| `src/notebook_lm/transcript_processor.py` (547行) | LLM 構造化補助が必要になった場合に参照 |
| `src/core/style_template.py` | YMM4 テンプレート連携が必要になった場合に参照 |
| `ymm4-plugin/` | YMM4 プラグイン開発が必要になった場合に参照 |

## 禁止 (reject)

| 旧ファイル/機能 | 禁止理由 |
|---------------|---------|
| `src/core/visual/stock_image_client.py` (664行) | 画像取得は初期スコープ外 (ADR-0001) |
| `src/core/visual/text_slide_generator.py` (削除済み) | PIL スライド生成は車輪の再発明 |
| `src/core/visual/animation_assigner.py` | アニメーション割当は YMM4 の責務 |
| `src/notebook_lm/audio_generator.py` | 音声生成は NotebookLM/YMM4 の責務 (ADR-0003) |
| `src/core/providers/` | プロバイダーパターンは不使用 |
| `src/web/` | Web UI は初期スコープ外 |
| `src/core/pipeline.py` | 過剰な orchestrator パターン |
| Path B 関連全般 (MoviePy, ffmpeg, Voicevox) | ADR-0001, ADR-0003 |

---

## 運用ルール

- 旧コードの構造・命名・async パターンをそのまま継承しない
- 参照可のコードも、v2 の責務境界に合わせて再設計する
- 新たに移植候補が出た場合は、この台帳に追記してから作業する
