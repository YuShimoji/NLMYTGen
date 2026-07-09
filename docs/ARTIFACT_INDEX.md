# Artifact Index

| Date | Type | Path / URL | Purpose | How to reproduce | Quality notes | Next improvement |
|---|---|---|---|---|---|---|
| 2026-07-10 | validation-log | `artifacts/review/rekickstart_2026-07-10_validation_log.txt` | Material evidence for the re-kickstart BUILD turn | Run the commands recorded in the log from repo root | `compileall_exit=0`, targeted pytest passed 4 tests, `git_diff_check_exit=0` | Add screenshot evidence if the next slice changes a UI/review surface |
| 2026-07-09 | review-pack | `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/` | Current Episode 002 Japanese YMM4 import-ready review surface | `uv run python -m src.cli.main build-ymm4-import-ready-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id nlm-e002-ymm4-import-ready-edit-package-v1-001` | `validation_readback.json` reports `status=passed`; production/public/YMM4 gates remain closed | Add explicit YMM4 observation readback only after the user opens that gate |

## Rule

Generated videos, texts, images, previews, and review outputs must be indexed
here before a BUILD turn is reported complete with artifact evidence.
