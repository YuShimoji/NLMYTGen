# NotebookLM to YMM4 Manual Delivery Package 001

This package is a minimal commercial pilot deliverable for turning a
NotebookLM-style audio overview transcript into YMM4-ready production inputs.
It is designed so a buyer or YMM4 operator can understand the delivery without
reading the source repository.

## What This Package Receives

- A transcript exported or copied from NotebookLM Audio Overview.
- Speaker names as they appear in the transcript.
- The YMM4 character names that should replace those speaker names.

The included sample uses fictional text only. It does not contain customer
data, external article text, private media, or rights-unclear source material.

## What This Package Delivers

- `outputs/transcript_sample_ymm4.csv`: YMM4 script-import CSV.
- `outputs/cue_packet.md`: text-only cue packet for background and support
  material planning.
- `outputs/diagram_packet.md`: text-only diagram brief packet for figure
  planning.
- `speaker_map.example.json`: example speaker mapping usable by the CLI.
- Review and offer documents that define the manual pilot scope.

## How A YMM4 Operator Uses It

1. Open YMM4 and use the script import flow with
   `outputs/transcript_sample_ymm4.csv`.
2. Confirm that `れいむ` and `まりさ` resolve to the expected YMM4 characters.
3. Review line wrapping, speaker continuity, and obvious parse errors.
4. Use `outputs/cue_packet.md` to prepare backgrounds, support materials, and
   manual production notes.
5. Use `outputs/diagram_packet.md` only as a planning brief. It is not a
   finished diagram asset.

## Rebuild Commands

Run these from the repository root:

```powershell
uv run python -m src.cli.main validate commercial_pilot/notebooklm_ymm4_delivery_package_001/sample_input/transcript_sample.txt
uv run python -m src.cli.main build-csv commercial_pilot/notebooklm_ymm4_delivery_package_001/sample_input/transcript_sample.txt -o commercial_pilot/notebooklm_ymm4_delivery_package_001/outputs/transcript_sample_ymm4.csv --speaker-map-file commercial_pilot/notebooklm_ymm4_delivery_package_001/speaker_map.example.json --max-lines 2 --chars-per-line 40 --balance-lines --stats
uv run python -m src.cli.main build-cue-packet commercial_pilot/notebooklm_ymm4_delivery_package_001/sample_input/transcript_sample.txt -o commercial_pilot/notebooklm_ymm4_delivery_package_001/outputs/cue_packet.md --speaker-map-file commercial_pilot/notebooklm_ymm4_delivery_package_001/speaker_map.example.json
uv run python -m src.cli.main build-diagram-packet commercial_pilot/notebooklm_ymm4_delivery_package_001/sample_input/transcript_sample.txt -o commercial_pilot/notebooklm_ymm4_delivery_package_001/outputs/diagram_packet.md --speaker-map-file commercial_pilot/notebooklm_ymm4_delivery_package_001/speaker_map.example.json
```

## Scope Boundary

This package does not upload to YouTube, request OAuth, process payment, grant
rights/legal acceptance, launch the YMM4 GUI, or guarantee final visual
appearance inside YMM4. It is a manual delivery pilot package.
