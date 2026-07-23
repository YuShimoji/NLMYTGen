# New-banknote one-command internal-review video

The accepted speech/timing cut with source-grounded real media is generated
from the repository root with:

```powershell
$env:NLMYTGEN_AUDIO_POLICY = 'silent'
uv run python -m src.cli.main build-episode-video --episode production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_pipeline/new_banknote_real_media_episode_manifest.json --force --render
```

The command verifies protected speech/timing and local source hashes,
materializes nine raster/video cues with their accepted subtitle fragments,
copies the source YMM4 project non-destructively, renders, performs lossless
fast-start normalization, validates the full H.264/AAC file, extracts cue
frames, and writes local receipts.

The input authority is `new_banknote_real_media_episode_manifest.json`. Output
is ignored under `../auto_video_runs/new_banknote_real_media_review_v1/`; the
review carrier is `internal_review_real_media.mp4`.

Use `--dry-run` to recheck protected inputs and the stage plan without writing.
Use `--resume` to verify and continue the same run without overwriting existing
media. Use `--force` to retain the current local run as a `.replaced-*.local`
archive and rebuild the declared run id from protected inputs.

The real-media manifest rejects SVGs and requires source provenance for every
cue. Source media, generated project, MP4, and extracted frames stay ignored.
Official and journalism imagery is authorized only for this local internal
review: rights, production, publication, external upload, merge, and release
remain unapproved.
