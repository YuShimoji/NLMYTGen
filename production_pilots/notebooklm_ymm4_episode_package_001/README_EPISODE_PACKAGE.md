# NotebookLM to YMM4 Episode Production Package 001

This is an internal episode production package for creating a video posting
candidate from a NotebookLM-style transcript. It is a production artifact for
the user's own channel work, not a sales artifact.

## Purpose

The package gives the user enough material to continue video production in
YMM4 without reading the repository:

- a safe representative transcript,
- a speaker map from NotebookLM speaker labels to YMM4 character names,
- a generated YMM4 script-import CSV,
- a cue packet for production judgement,
- a diagram packet for optional figure planning,
- review, posting, limitation, and next-action notes.

## Input

- `real_input/README_REAL_INPUT.md`: where to put a real user-approved
  NotebookLM transcript. No real transcript is present yet.
- `sample_input/transcript_sample.txt`: fictional NotebookLM-style transcript.
- `speaker_map.example.json`: CLI-usable speaker map.

The current generated outputs are from the fictional dry-run sample. They do
not include real customer data, rights-unclear article text, external fetched
data, media files, or private source material.

## Outputs

- `outputs/transcript_sample_ymm4.csv`: generated YMM4 script-import CSV.
- `outputs/cue_packet.md`: text-only cue packet for scene, background, and
  production judgement.
- `outputs/diagram_packet.md`: text-only diagram brief packet for optional
  figure planning.

## YMM4 Connection

1. Open YMM4 manually.
2. Use YMM4's script import flow with `outputs/transcript_sample_ymm4.csv`.
3. Confirm that `れいむ` and `まりさ` resolve to the intended characters.
4. Review subtitle line length, speaker continuity, and obvious parse errors.
5. Use `outputs/cue_packet.md` and `outputs/diagram_packet.md` as planning
   material before render or final upload decisions.

For a real episode, first add
`real_input/episode_001_transcript.txt`, regenerate outputs using
`YMM4_IMPORT_RUNBOOK.md`, then import `outputs/episode_001_ymm4.csv`.

## Rebuild Commands

Run these from the repository root:

```powershell
uv run python -m src.cli.main validate production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt
uv run python -m src.cli.main build-csv production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/transcript_sample_ymm4.csv --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json --max-lines 2 --chars-per-line 40 --balance-lines --stats
uv run python -m src.cli.main build-cue-packet production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/cue_packet.md --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json
uv run python -m src.cli.main build-diagram-packet production_pilots/notebooklm_ymm4_episode_package_001/sample_input/transcript_sample.txt -o production_pilots/notebooklm_ymm4_episode_package_001/outputs/diagram_packet.md --speaker-map-file production_pilots/notebooklm_ymm4_episode_package_001/speaker_map.example.json
```

## Next Production Work

Put one real user-approved NotebookLM transcript in
`real_input/episode_001_transcript.txt`, regenerate the CSV and packets, import
the CSV into YMM4, then decide whether the episode should proceed to render
proof, thumbnail/title/description work, and upload approval.
