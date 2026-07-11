# Episode 002 YMM4 Diagnostic Placeholder Proof

Status: diagnostic-only; not final; not production/public-ready.

This pack separates two gates:

1. the CSV receipt proves automatic VoiceItem plus linked-subtitle import;
2. this pack proves a separate `.ymmp` route with one ImageItem and one independent TextItem for each of S1/S2/S3.

Scene spans come from actual VoiceItem frames and cue boundaries. They do not reuse provisional four-second blocks.

The local project is `episode_002_diagnostic_placeholder.local.ymmp`. It is intentionally ignored and not committed because current YMM4 ImageItems use an absolute local asset path. Regenerate it with:

```powershell
uv run python -m src.cli.main build-ymm4-diagnostic-placeholder-proof --package production_pilots/yukkuri_newsroom_content_spine_002 --source-ymmp <local-import-base.ymmp> --csv-gate-receipt <csv-gate-receipt-v2.json>
```

Tracked evidence:

- `diagnostic_project_manifest.json`
- `diagnostic_project_readback.json`
- `diagnostic_project_receipt.json`
- `assets/diagnostic_placeholder.png`

No render/export, production `.ymmp`, real input, external media, rights/public approval, or upload is performed here.
