# CLI リファレンス（開発・デバッグ）

制作手順の正本は [GUI_MINIMUM_PATH.md](../GUI_MINIMUM_PATH.md)。ここはコマンド索引。

| 用途 | コマンド |
|------|----------|
| build-csv（手元） | `python -m src.cli.main build-csv ...` — `--format json` で `stats`（話者・はみ出し候補） |
| apply-production | `python -m src.cli.main apply-production ...` — GUI の演出適用タブと同じ |
| validate-ir | `python -m src.cli.main validate-ir ...` |
| 制作 manifest | `python -m src.cli.main build-session-manifest --video-id ...` — CSV/IR/YMM4/サムネ設計の handoff artifact |
| サムネ slot 監査 | `python -m src.cli.main audit-thumbnail-template thumb_template.ymmp` — `thumb.text.*` / `thumb.image.*` Remark を確認 |
| サムネ限定 patch | `python -m src.cli.main patch-thumbnail-template thumb_template.ymmp --patch patch.json -o out.ymmp` — 文字・画像パス・最小ジオメトリのみ。保存後 readback も返す |
| H-05 集約 | `python -m src.cli.main score-thumbnail-s8 ...` — GUIボタンなし、必要時のみ |
| B-18 | `python -m src.cli.main diagnose-script ...` — GUI の品質診断からも可 |
| テスト（通常） | `uv run pytest` — **`src/` または `gui/` のロジックを変えたブロックの終わりにだけ**根拠として示す |
| テスト（全件） | `NLMYTGEN_PYTEST_FULL=1 uv run pytest` — 任意（`CLAUDE.md`） |

`python -m src.cli.main <subcommand> --help` でオプション詳細。
