# B-15 Phase 1 Implementation Verification

## Scope

- feature: `B-15 LLM prep packet`
- slice: `build-cue-packet` CLI
- date: 2026-03-31
- status: initial implementation
- owner: `assistant`

## What Changed

- `src/pipeline/cue_packet.py` を追加し、NotebookLM transcript から text-only の cue packet payload / Markdown packet を組み立てられるようにした
- `src/pipeline/cue_proof.py` を追加し、workflow proof 記録用 Markdown 雛形を生成できるようにした
- `src/cli/main.py` に `build-cue-packet` サブコマンドを追加した
- packet には Phase 1 の boundary, output contract, speaker map, role analysis, transcript 本文を含める
- host 話者の話題転換句や発話数を手がかりにした `section_seeds` を packet context に追加した
- `--bundle-dir` により、packet markdown/json と workflow proof 雛形を一括生成できるようにした
- `tests/test_cue_packet.py` を追加し、payload / Markdown / CLI JSON 出力の回帰を追加した

## Verification

| check | result |
|---|---|
| `python3 -m src.cli.main build-cue-packet samples/AI監視が追い詰める生身の労働.txt --format json` | 成功。`packet_version`, `feature_id`, `role_analysis`, `transcript` を含む packet を出力 |
| sample packet write | `samples/AI監視が追い詰める生身の労働_cue_packet.md` と `samples/AI監視が追い詰める生身の労働_cue_packet.json` を生成 |
| proof bundle write | `samples/AI監視が追い詰める生身の労働_cue_workflow_proof.md` を含む bundle を生成 |
| example cue memo | `samples/AI監視が追い詰める生身の労働_cue_memo_example.md` を作成し、output contract の見本を置いた |
| external cue memo response | 実レスポンスを `samples/AI監視が追い詰める生身の労働_cue_memo_received.md` に記録。section 再構成と operator_todos が特に有用 |
| contract refinement | proof を受けて `primary_background`, `supporting_visual`, `sound_cue_optional` へ見直し、背景候補の圧縮と SE optional 化を反映 |
| preference refinement | `response_preferences` を追加し、section 数、背景密度、sound policy、operator_todos 数の上限を packet に埋め込んだ |
| rerun result | `samples/AI監視が追い詰める生身の労働_cue_memo_rerun_received.md` を記録。4 section、primary/supporting 構成、sound cue の減少を確認 |
| targeted sample observation | `utterance_count=28`, `スピーカー1=host`, `スピーカー2=guest` と推定された |
| targeted sample observation | `section_seeds` は 3 件 (`1-10`, `11-13`, `14-28`) を提案 |
| `python3 -m pytest ...` | 未実施。環境に `pytest` が入っていないため `/usr/bin/python3: No module named pytest` |
| `uv run pytest ...` | 未実施。環境に `uv` がないため `/bin/bash: uv: command not found` |

## Assessment

- B-15 Phase 1 の最初の実装として、repo 内で安全に持てる部分は入った
- 現時点では LLM provider や SDK を repo に追加せず、外部 Automation / 手動実行に渡す packet を生成する形に留めている
- `section_seeds` が入ったことで、外部 LLM 側は transcript 全文だけでなく、どこで場面を切るかの当たりも受け取れる
- proof 雛形も同時に出せるため、次の手動 block では「実施して記録する」ことだけに集中できる
- 実際の返答を見る限り、packet は cue memo の叩き台として機能した。次の改善点は section の増減ではなく、背景候補の圧縮とノイズ低減に寄っている
- contract refinement 後は、主背景 + 補助素材の二層と optional sound cue に寄せ、過剰列挙を減らす方向にした
- `response_preferences` により、次の再試行では section 数や operator_todos 数も少し揃えやすくした
- rerun ではその意図が概ね反映され、前回より扱いやすい cue memo になった
- これにより text-only boundary を壊さず、次の workflow proof を取りにいける

## Residual Risk

- まだ実際の cue memo 生成結果を 1 本分で評価していない
- packet の出力 contract は固定したが、section 粒度や cue の粒度は実運用で微調整が必要
- provider / SDK の repo 内実装は未着手
