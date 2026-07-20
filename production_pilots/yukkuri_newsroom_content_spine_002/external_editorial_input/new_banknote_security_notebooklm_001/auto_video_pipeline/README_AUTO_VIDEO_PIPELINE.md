# New-banknote one-command internal-review video

Run from the repository root with the silent development policy:

```powershell
$env:NLMYTGEN_AUDIO_POLICY = 'silent'
uv run python -m src.cli.main build-episode-video --episode production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_pipeline/new_banknote_episode_manifest.json --render
```

The command performs preflight, deterministic SVG-to-PNG materialization,
non-destructive YMM4 project generation, YMM4 video output, H.264/AAC review
lossless fast-start normalization, full-file decode validation, cue/text-bound
representative-frame extraction,
and receipt generation. Typical runtime is 10–25 minutes on the observed local
machine; failures are recorded in `run.log` in the run directory.

The input authority is `new_banknote_episode_manifest.json`. Local output is
written under
`../auto_video_runs/new_banknote_internal_review_v1/`; the directory is ignored
and contains the generated project, MP4, assets, frames, and receipts.

Use `--dry-run` to recheck protected inputs and the stage plan without writing.
Use `--resume` to verify and continue the same run without overwriting existing
media. Use `--force` to retain the current local run as a `.replaced-*.local`
archive and rebuild the declared run id from protected inputs.

Every SVG must bind its exact cue id, scene id, and approved subtitle in the
root metadata. Cues 2, 7, and 8 use dedicated tracked proxy SVGs so a shared
layout cannot accidentally burn in another cue's subtitle.

The output is an internal-review proxy only. The command does not approve
visual quality or rights, publish, upload, open a PR, or merge to master.
