# Runtime State

## GPS

- Project: NLMYTGen
- Slice: 全工程 E2E 達成。次スライス未定
- Branch: master
- Session: 2026-03-27 (HANDOFF)
- Active Artifact: NLM transcript → YMM4 CSV → YMM4 タイムライン配置
- Last Change Relation: direct

## Quantitative Metrics

- Source files: 8 (contracts/3 + pipeline/3 + cli/1 + __init__ 4本)
- Test files: 4
- Tests: 15
- Mock files: 0
- TODO/FIXME/HACK: 0
- Commits: 19

## Counters

- blocks_completed: 17
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
- **--unlabeled: 実 NLM transcript (143行) → 136 utterances → YMM4 CSV 生成成功**
- **実データ E2E (コード側): confirmed — samples/output_real_nlm.csv (136行, れいむ/まりさ)**
- **YMM4 台本読込: confirmed — タイムライン上に各要素が配置された (YMM4通常版で確認)**
- CSV エンコーディング: UTF-8 BOM 付き (utf-8-sig) に変更済み
- pytest 15/15 pass

## Blocking

- なし (全 blocker 解消済み)

## Pending

- 短行結合閾値のチューニング（現在 ≤3文字。相槌 "はい。" も結合される副作用あり）
- README に --unlabeled の使い方を追記
- 別の NLM transcript でのロバスト性検証
- YMM4 Lite の不具合は NLMYTGen 側の問題ではない (通常版で動作確認済み)
