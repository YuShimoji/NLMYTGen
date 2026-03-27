# Runtime State

## GPS

- Project: NLMYTGen
- Slice: 実データ E2E 到達 (ラベルなし入力対応が前提)
- Branch: master
- Session: 2026-03-27

## Quantitative Metrics

- Source files: 8 (contracts/3 + pipeline/3 + cli/1 + __init__ 4本)
- Test files: 4
- Tests: 15
- Mock files: 0
- TODO/FIXME/HACK: 0
- Commits: 14 (3 initial + 11 previous sessions)

## Counters

- blocks_completed: 14
- blocks_since_user_visible_change: 1
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
- pytest 15/15 pass

## Blocking

- 実 NotebookLM transcript がスピーカーラベルなし形式であることが判明 (2026-03-27)
  - 現パーサーは "Speaker: text" コロン区切り形式のみ対応
  - 実 transcript は行ごとの生テキスト（ラベルなし、2話者が交互に発話）
  - ラベルなし入力の対応方針を決定後、E2E を実施する必要がある
- YMM4 での実読込未確認（CSV 生成後に確認予定）

## Pending

- ラベルなし入力対応: 行交互割当 or プレラベリングツール or 両方 → 要設計判断
- 実 NotebookLM transcript での E2E（ラベルなし対応後）
- YMM4 での実読込確認
