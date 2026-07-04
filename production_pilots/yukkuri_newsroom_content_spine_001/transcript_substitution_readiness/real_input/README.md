# Real Input Drop-Zone

Place a real NotebookLM or human-reviewed transcript here as UTF-8 `.txt` or `.csv`, then rerun:

`python -m src.cli.main build-transcript-substitution --package production_pilots/yukkuri_newsroom_content_spine_001`

Accepted text shapes:

- `Speaker: text`
- `[00:00] Speaker: text`
- two-column CSV: `speaker,text`
- unlabeled alternating lines only when rerun with `--unlabeled` and a speaker map

Do not place source media, credentials, OAuth tokens, paid API data, or rights-uncleared public assets here.
