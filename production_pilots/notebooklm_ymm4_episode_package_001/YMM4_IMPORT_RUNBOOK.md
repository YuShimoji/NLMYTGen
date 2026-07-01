# YMM4 Import Runbook

This runbook explains the manual import check after a real transcript has been
added. Codex must not launch YMM4, render, upload, or change YouTube visibility.

## Current State

- Real transcript: not present yet.
- Dry-run sample transcript: `sample_input/transcript_sample.txt`.
- Dry-run output CSV: `outputs/transcript_sample_ymm4.csv`.
- Real intake slot: `real_input/episode_001_transcript.txt`.

## Rebuild From Current Dry-Run Sample

Use these commands to confirm the package route still works:

```powershell
uv run python -m src.cli.main validate production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt
uv run python -m src.cli.main build-csv production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/transcript_sample_ymm4.csv --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json --max-lines 2 --chars-per-line 40 --balance-lines --stats
uv run python -m src.cli.main build-cue-packet production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/cue_packet.md --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json
uv run python -m src.cli.main build-diagram-packet production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/diagram_packet.md --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json
```

## Rebuild After Real Transcript Is Added

After `real_input/episode_001_transcript.txt` exists and the speaker map is
correct, use the same route with real-output filenames:

```powershell
uv run python -m src.cli.main validate production_pilots/notebooklm_ymm4_episode_package_001/real_input/episode_001_transcript.txt
uv run python -m src.cli.main build-csv production_pilots/notebooklm_ymm4_episode_package_001/real_input/episode_001_transcript.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/episode_001_ymm4.csv --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json --max-lines 2 --chars-per-line 40 --balance-lines --stats
uv run python -m src.cli.main build-cue-packet production_pilots/notebooklm_ymm4_episode_package_001/real_input/episode_001_transcript.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/episode_001_cue_packet.md --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json
uv run python -m src.cli.main build-diagram-packet production_pilots/notebooklm_ymm4_episode_package_001/real_input/episode_001_transcript.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/episode_001_diagram_packet.md --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json
```

## Manual YMM4 Import Check

1. Open YMM4 manually.
2. Import the generated CSV:
   `outputs/episode_001_ymm4.csv` for real input, or
   `outputs/transcript_sample_ymm4.csv` for dry-run sample input.
3. Confirm the YMM4 character names resolve as expected.
4. Confirm row order, speaker continuity, and subtitle wrapping.
5. Check whether any line is too long, too split, duplicated, or assigned to
   the wrong speaker.
6. Keep the cue packet open while checking whether the episode has enough
   production direction for backgrounds, supporting visuals, and diagram needs.

## What To Record After Import

Return these observations for the next correction pass:

- Imported CSV path.
- YMM4 import result: success, partial success, or failed.
- Row count shown in YMM4, if visible.
- Speaker mapping issues.
- Lines that are too long or awkwardly split.
- Missing or unnecessary cue packet items.
- Whether a diagram packet is useful for this episode.
- Next decision: revise CSV, revise speaker map, revise cue packet, proceed to
  render proof, or stop this episode.
