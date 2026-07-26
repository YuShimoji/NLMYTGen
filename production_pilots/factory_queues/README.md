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

`four_package_zero_change_set_v1.json`はqueue-v3の4 packageを検証し、
mutation entryを1件も選ばないexact change-setである。executorは既定で
plan-only、`--execute`を付けてもこのchange-setではbackend dispatchを行わない。

```powershell
uv run python -m src.cli.main execute-factory-queue `
  --queue production_pilots/factory_queues/four_package_lifecycle_queue_v3.json `
  --change-set production_pilots/factory_queues/four_package_zero_change_set_v1.json `
  --execute --format json
```

mutating change-setはpackage、descriptor SHA、content/render/output identity、
lifecycle edge、operation、one-shot authorityをexactに束縛する。executorは
直列実行し、各effect直前に全identityを再確認する。既知failureでは後続を
`skipped_after_failure`にし、結果不明は`effect_unknown`として自動再試行しない。
resumeは同じplan identityのappend-only journalだけを受理する。
