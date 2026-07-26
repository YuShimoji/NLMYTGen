# Factory Queues

`four_package_lifecycle_queue_v1.json`は、Factory Contract v2.0 / v2.1を
混在して評価するbounded queueである。

通常のlive evaluation:

```powershell
uv run python -m src.cli.main evaluate-factory-queue `
  --queue production_pilots/factory_queues/four_package_lifecycle_queue_v1.json `
  --check-live --format json
```

validation-only safe stages:

```powershell
uv run python -m src.cli.main evaluate-factory-queue `
  --queue production_pilots/factory_queues/four_package_lifecycle_queue_v1.json `
  --check-live --execute-safe-stages --format json
```

safe stagesは既存package dry-runまたはpre-render planだけを実行する。
source-project generation、YMM4、Electron、render、encode、playback、
private copy、product writeの権限を持たない。

完了packageのlive fileが別端末で見つからない場合は
`recorded_complete_no_live_file`であり、`render_required`へ昇格しない。
