# レーン A（Phase 1）実行準備チェックリスト

[PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) と [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) トラック A に沿った、実行直前の確認用リスト。

## 1. 環境・パス（準備 1）

- [ ] リポジトリ root でシェルを開いている（例: [OPERATOR_LANE_A_ENV.md](OPERATOR_LANE_A_ENV.md)）
- [ ] `uv run python -m src.cli.main --help` が通る
- [ ] 対象 `.txt` のパスと **Speaker Map**（または `--unlabeled` / `--speaker-map-file`）を決めた
- [ ] （任意）`diagnose-script` と `build-csv --dry-run --stats` をサンプルで一度流した

## 2. C-09 / S1 正本同期（準備 3・トラック B と同型）

Custom GPT / Claude Project 等は **オペレータが** GUI 側で開き、repo 正本と突き合わせる。

- [ ] [gui-llm-setup-guide.md](../gui-llm-setup-guide.md) の **S-1（C-09）** を読んだ
- [ ] Instructions に [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md) の「LLM への指示」と入力テンプレが含まっている
- [ ] 診断 JSON と元台本を貼る作業用に、保存先ファイル名（例: `_tmp_script_diag.json`）を決めた

## 3. YMM4（準備 4）

- [ ] S-0 テンプレ複製プロジェクトを開ける
- [ ] [WORKFLOW.md](../WORKFLOW.md) **S-4**（ツール → 台本読み込み）を再確認した
- [ ] **レーン C / P2** と YMM4 を同時にフル稼働しない時間帯を確保した（[PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) §1.1）

## 4. プラン直前ゲート（B-11・別ストリーム）

プラン文書化の前提は [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) §5。

- [ ] 実案件 1 本の `B11-workflow-proof-*.md` が §5 体裁を満たし、YMM4 取込後が実機記録として確定している（[B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) 先頭注記）
- [ ] 取込前・取込後が **同一ファイル**で埋まっている

## 5. 実行後（A-5 / P01）

- [ ] [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) 末尾の表に、必要なら 1 行追記した
