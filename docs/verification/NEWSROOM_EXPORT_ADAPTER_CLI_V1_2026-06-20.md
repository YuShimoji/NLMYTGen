# Newsroom Export Adapter CLI v1 - 2026-06-20

Artifact id: `newsroom_export_adapter_cli_v1_2026_06_20`

This slice exposes the existing fake-fixture adapter proof through the
NLMYTGen CLI. It is a scoped diagnostic wrapper around
`src.pipeline.newsroom_export_adapter`; it is not production ingest, not real
packet acceptance, and not a transfer/YMM4 readiness signal.

This slice does not modify `newsroom-yt-pipeline`, fetch sources, open RSS or
Inoreader flows, access live source material, download media, edit `.ymmp`,
generate YMM4 carriers, render media, approve rights, approve production, or
publish/upload output.

## Command

```powershell
uv run python -m src.cli.main adapt-newsroom-export-fixture `
  ../newsroom-yt-pipeline/samples/_probe/newsroom_handoff/newsroom_export_fixture_v1.json `
  --out-packet samples/_probe/newsroom_handoff/adapted_newsroom_export_packet.json `
  --out-readback samples/_probe/newsroom_handoff/newsroom_export_adapter_readback.json `
  --format json
```

## Output Summary

```json
{
  "status": "passed_with_adapter_warnings_transfer_blocked",
  "adapter_version": "newsroom-export-adapter-proof-v1",
  "adapter_packet_validator_status": "passed",
  "adapter_packet_transfer_status": "blocked",
  "adapter_packet_errors": 0,
  "slot_linkage_status": "passed_with_warnings",
  "transfer_planning_status": "blocked",
  "transfer_planning_transfer_status": "blocked",
  "transfer_planning_blocker_count": 13,
  "real_packet_accepted": false,
  "rights_approval": false,
  "media_approval": false,
  "review_approval": false,
  "production_approval": false,
  "ymm4_transfer_ready": false,
  "diagnostic_only": true
}
```

## Artifacts

| Artifact | Path |
| --- | --- |
| CLI entry | `src/cli/main.py` |
| adapter module | `src/pipeline/newsroom_export_adapter.py` |
| adapted packet output | `samples/_probe/newsroom_handoff/adapted_newsroom_export_packet.json` |
| adapter readback output | `samples/_probe/newsroom_handoff/newsroom_export_adapter_readback.json` |
| focused tests | `tests/test_newsroom_export_adapter.py` |
| source newsroom fixture | `../newsroom-yt-pipeline/samples/_probe/newsroom_handoff/newsroom_export_fixture_v1.json` |

## Validation

| Check | Result |
| --- | --- |
| `uv run --with pytest python -m pytest tests/test_newsroom_export_adapter.py` | 10 passed |
| CLI fixture adaptation command | exit 0 |
| adapted packet validator status | passed |
| adapted packet transfer status | blocked |
| slot-linkage status | passed_with_warnings |
| transfer-planning status | blocked |
| real packet accepted | false |
| rights/media/review/production approval | false |
| YMM4 transfer ready | false |

## Review Notes

The command writes JSON only when `--out-packet` and/or `--out-readback` are
provided. It emits a concise status summary to stdout for operator review. Its
success condition is fail-closed: the adapted packet must pass structural
validation, transfer must remain blocked, and real packet / rights / production
/ YMM4 approvals must remain false.
