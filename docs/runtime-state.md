# Runtime State

## GPS

- Project: NLMYTGen
- Slice: IP-01 話者割当精度 評価完了 (No-Go) + ロール推定機能
- Branch: master
- Session: 2026-03-29
- Active Artifact: NLM transcript → YMM4 CSV → 動画（最終成果物到達経路）
- Last Change Relation: direct

## Quantitative Metrics

- Source files: 8 (contracts/3 + pipeline/3 + cli/1 + __init__ 4本)
- Test files: 4
- Tests: 16
- Mock files: 0
- TODO/FIXME/HACK: 0
- Commits: 22

## Counters

- blocks_completed: 21
- blocks_since_user_visible_change: 0
- blocks_since_visual_audit: N/A (CLI project)
- visual_evidence_status: N/A (CLI project)
- last_visual_audit_path: N/A

## Evidence

- CLI build-csv: sample data E2E confirmed (txt + csv)
- CLI validate: sample data confirmed (txt + csv)
- CLI inspect: sample data confirmed
- CLI generate-map: text + json format confirmed
- --dry-run: confirmed
- --stats: confirmed
- --merge-consecutive: confirmed (12->11 utterances with consecutive merge)
- --speaker-map-file: JSON confirmed
- --speaker-map: CLI string confirmed
- BOM UTF-8 input: confirmed
- CSV header auto-skip: confirmed
- unmapped speaker warning: confirmed
- **--unlabeled: 実 NLM transcript (143行) → 142 utterances → YMM4 CSV 生成成功**
- **実データ E2E (コード側): confirmed — samples/output_real_nlm.csv (142行, れいむ/まりさ)**
- **短行結合チューニング: 句読点終端の相槌("はい。"等)を独立発話として保持 (136→142行)**
- **一括処理 (IP-04): build-csv で複数入力ファイルをサポート。各ファイル独立処理+サマリー**
- **YMM4 台本読込: confirmed — タイムライン上に各要素が配置された (YMM4通常版で確認)**
- CSV エンコーディング: UTF-8 BOM 付き (utf-8-sig) に変更済み
- pytest 16/16 pass
- **話者割当分析 (Phase 0): 行交互の疑わしい箇所 22件特定。相槌パターン38.7%が両話者共通**
- **評価基盤: gold_set_template.json + evaluate_diarization.py + Go/No-Go 判定基準**
- **話者ロール推定: inspect/generate-map --unlabeled でhost/guest自動推定**
- **Gold set 評価: パターン正答率92.3%。LLM(IP-01)はNo-Go判定**

## Blocking

- なし（全 blocker 解消済み）

## Pending

- 別の NLM transcript でのロバスト性検証（汎化性確認。1件のデータでは限定的）
- YMM4 Lite の不具合は NLMYTGen 側の問題ではない (通常版で動作確認済み)

## Completed Evaluations

- IP-01 (LLM構造化補助): **No-Go** — パターン正答率92.3%。行交互は高精度でLLM費用対効果が低い
- Gold set: 65行の正解ラベル付きデータ作成済み (tools/gold_set.json)
- 評価ツール: tools/evaluate_diarization.py で3手法を自動比較可能
