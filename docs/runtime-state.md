# Runtime State

## GPS

- Project: NLMYTGen
- Slice: 実データ E2E 到達 → YMM4 実読込確認
- Branch: master
- Session: 2026-03-27

## Quantitative Metrics

- Source files: 8 (contracts/3 + pipeline/3 + cli/1 + __init__ 4本)
- Test files: 4
- Tests: 15
- Mock files: 0
- TODO/FIXME/HACK: 0
- Commits: 17 (origin) + local uncommitted (--unlabeled 実装)

## Counters

- blocks_completed: 15
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
- pytest 15/15 pass

## Blocking

- ~~ラベルなし入力対応~~ → --unlabeled フラグで解決済み
- YMM4 での実読込未確認（CSV 生成済み、手動確認待ち）

## Pending

- YMM4 での実読込確認 (samples/output_real_nlm.csv)
- WORKFLOW.md: NLM → CSV → YMM4 → 動画 の全工程手順書
- 短行結合閾値のチューニング（現在 ≤3文字。相槌 "はい。" も結合される副作用あり）
