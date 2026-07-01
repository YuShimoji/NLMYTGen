# Episode Review Checklist

Use this before treating the package as a viable video posting candidate.

Current state: real transcript is not present yet. The checked outputs are from
the fictional dry-run sample until `real_input/episode_001_transcript.txt` is
added and regenerated.

## YMM4 CSV

- [ ] `outputs/transcript_sample_ymm4.csv` exists.
- [ ] For a real episode, `outputs/episode_001_ymm4.csv` exists after
  regeneration.
- [ ] The CSV has two columns: YMM4 character name and utterance text.
- [ ] The CSV has no header row.
- [ ] The CSV can be selected in YMM4's script import flow.
- [ ] Imported rows appear in the expected order.

## Speaker Continuity

- [ ] `Host1` maps to `れいむ`.
- [ ] `Host2` maps to `まりさ`.
- [ ] Speaker alternation still makes sense after wrapping/splitting.
- [ ] No speaker swap or unknown speaker remains.

## Subtitle Readability

- [ ] No line is obviously too long for a first YMM4 import pass.
- [ ] Long terms such as `NotebookLM` and `YMM4` are still readable.
- [ ] The CSV has no obvious duplicate fragments.
- [ ] The CSV has no obvious parse errors.

## Production Judgement

- [ ] `outputs/cue_packet.md` gives enough direction for background and scene
  planning.
- [ ] `outputs/diagram_packet.md` is useful only where a figure would clarify
  the episode.
- [ ] The material has a clear viewer value hypothesis before render work.
- [ ] Missing assets, examples, or visuals are listed before final production.

## Still Missing Before Posting

- [ ] Real transcript added at `real_input/episode_001_transcript.txt`.
- [ ] YMM4 GUI import confirmation.
- [ ] Render proof.
- [ ] Thumbnail/title/description draft.
- [ ] Rights/legal check by the user.
- [ ] Explicit upload approval.
