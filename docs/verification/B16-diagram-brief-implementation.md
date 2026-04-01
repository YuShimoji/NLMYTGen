# B-16 Diagram Brief Implementation

## Scope

- feature: `B-16 Diagram brief packet`
- date: 2026-03-31
- status: initial implementation
- owner: `assistant`

## Implemented

- `src/pipeline/diagram_brief.py`
  - B-16 用の text-only packet payload / Markdown renderer を追加
- `src/pipeline/diagram_proof.py`
  - workflow proof 用の Markdown 雛形を追加
- `src/pipeline/diagram_rerun.py`
  - rerun prompt と diff template の生成を追加
- `src/cli/main.py`
  - `build-diagram-packet` サブコマンドを追加し、bundle 出力へ rerun 補助も含めた
- `tests/test_diagram_brief.py`
  - payload / markdown / CLI / bundle の回帰を追加

## Command Shape

```bash
python -m src.cli.main build-diagram-packet input.txt [--format markdown|json] [-o packet.md]
python -m src.cli.main build-diagram-packet input.txt --bundle-dir samples
```

## Output Shape

- packet markdown
- packet json
- workflow proof template (`*_diagram_workflow_proof.md`)
- rerun prompt (`*_diagram_rerun_prompt.txt`)
- rerun diff template (`*_diagram_rerun_diff_template.md`)
- quickstart (`*_diagram_quickstart.md`)
- baseline notes (`*_diagram_baseline_notes.md`)

## Verification

### Confirmed in this environment

- `python3 -m src.cli.main build-diagram-packet samples/AI監視が追い詰める生身の労働.txt --format json`
  - `feature_id=B-16`, `phase=diagram-brief-only` を確認
- `python3 -m src.cli.main build-diagram-packet samples/AI監視が追い詰める生身の労働.txt --bundle-dir <tmpdir>`
  - markdown / json / workflow proof / rerun prompt / rerun diff template / quickstart / baseline notes の 7 ファイル生成を確認
- `~/.local/bin/uv venv .venv-linux`
- `~/.local/bin/uv pip install -r requirements-dev.txt --python .venv-linux`
- `TMPDIR=/tmp TMP=/tmp TEMP=/tmp .venv-linux/bin/python -m pytest`
  - 65 passed in 2.80s を確認

### Not confirmed

- bare の `python3 -m pytest` は現シェルでは `No module named pytest`。WSL では Linux 側 venv を明示する必要がある

## Notes

- B-16 は図版生成ではなく、図作成前の text-only brief に限定している
- B-15 cue memo と混同しないよう、出力 contract は `diagram_briefs[]` 中心に分離した
- 初回 proof では、diagram planning は 15 分想定から 3 分程度へ短縮し、delta は 12 分だった
- 軽微改善として、background だけで十分な section を diagram brief から外しやすくする response preference を追加した
- `packet_version` は `b16-v2` となり、`skip_sections_better_served_by_backgrounds` / `avoid_repeating_b15_cue_memo` を追加した
- rerun 比較用に `samples/*_diagram_baseline_notes.md` を追加し、前回の良かった点と比較観点を簡単に参照できるようにした
- `build-diagram-packet --bundle-dir` は rerun prompt、rerun diff template、quickstart に加えて baseline notes 雛形も自動生成するようになり、新規 transcript でも最初から比較導線を揃えられる
- rerun 差分を短く残すための `samples/*_diagram_rerun_diff_template.md` も追加した
- rerun では導入専用の図を増やさず、`S1-S2` の監視構造へ統合した 3 図構成になった。背景で足りる区間をさらに外せており、B-16 は大きな追加 tweak なしで収束候補と見なせる
- 次回の手動確認を短くするための `samples/*_diagram_quickstart.md` も追加した
- 次の主論点は、B-16 を close candidate としたうえで、次候補を `asset brief` として proposal 化するかどうかへ移すこと
