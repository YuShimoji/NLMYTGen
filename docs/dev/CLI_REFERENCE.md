# CLI リファレンス（開発・デバッグ）

制作手順の正本は [GUI_MINIMUM_PATH.md](../GUI_MINIMUM_PATH.md)。ここはコマンド索引。

| 用途 | コマンド |
|------|----------|
| build-csv（手元） | `python -m src.cli.main build-csv ...` — `--format json` で `stats`（話者・はみ出し候補） |
| fetch-topics (A-04) | `python -m src.cli.main fetch-topics <RSS_OR_ATOM_URL>... [-n 20] [--after YYYY-MM-DD] [--format text\|json]` — L1 のトピック候補取得のみ。RSS/Atom タイトルを NotebookLM 検索クエリ候補にするだけで、NotebookLM 台本取得、`source.wav`、`material_ledger`、`sports_news` provenance は生成しない |
| apply-production | `python -m src.cli.main apply-production ...` — GUI の演出適用タブと同じ |
| validate-ir | `python -m src.cli.main validate-ir ...` |
| validate-background-skit-blueprint | `python -m src.cli.main validate-background-skit-blueprint blueprint.json --script script.txt --ymmp base.ymmp --fps 60 --format json` — 茶番劇の数値表を source-backed artifact として再計算し、IR/YMM4 前に `passed / failed / blocked` を返す |
| Episode Pack handoff | `python -m src.cli.main episode-run-handoff --episode-id ...` — user handoff 前に必須入力の state / what / create / used-by を出す |
| 制作 manifest | `python -m src.cli.main build-session-manifest --video-id ...` — CSV/IR/YMM4/サムネ設計の handoff artifact |
| サムネ slot 監査 | `python -m src.cli.main audit-thumbnail-template thumb_template.ymmp` — `thumb.text.*` / `thumb.image.*` Remark を確認 |
| サムネ限定 patch | `python -m src.cli.main patch-thumbnail-template thumb_template.ymmp --patch patch.json -o out.ymmp` — 文字・画像パス・最小ジオメトリのみ。保存後 readback も返す |
| YMM4 variation probe | `python -m src.cli.main probe-ymmp-variations source.ymmp -o _tmp/variation/review.ymmp --review-seed samples/canonical.ymmp` — 手動作成済み `Remark` clip から `X/Y/Zoom/Rotation`・反転 route・`VideoEffects` fingerprint を読み、YMM4 保存済み full project canvas 上に compact review 派生を作る |
| H-05 集約 | `python -m src.cli.main score-thumbnail-s8 ...` — GUIボタンなし、必要時のみ |
| B-18 | `python -m src.cli.main diagnose-script ...` — GUI の品質診断からも可 |
| テスト（通常） | `uv run pytest` — **`src/` または `gui/` のロジックを変えたブロックの終わりにだけ**根拠として示す |
| テスト（全件） | `NLMYTGEN_PYTEST_FULL=1 uv run pytest` — subprocess / integration coverage が必要なときだけ（[REPO_LOCAL_RULES.md](../REPO_LOCAL_RULES.md)） |

`python -m src.cli.main <subcommand> --help` でオプション詳細。
