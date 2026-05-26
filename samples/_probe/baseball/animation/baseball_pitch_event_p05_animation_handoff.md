# Baseball BN-04 frame sequence handoff (2026-05-26)

BN-04 now has a deterministic frame-sequence export for the sample pitch event.
This is not a video clip, not a YMM4 placement proof, and not creative
acceptance.

Boundary phrase for readback: not creative acceptance.

## Generated artifacts

- manifest: `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_manifest.json`
- readback: `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_readback.json`
- frames: `samples/_probe/baseball/animation/frames/baseball_pitch_event_p05/baseball_pitch_event_p05_f000.png` through `f004.png`

The sequence is a transport/readback proof for the previous-pitch to
current-pitch comparison. It remains sample-only and should be visually checked
before any clip export or production timing work.

## Next safe moves

| Entry | Why it helps | What becomes possible |
| --- | --- | --- |
| Verify BN-05 manual preview | Confirms crop, text size, and layer overlap in real YMM4 | Decide whether the static placement contract is usable. |
| Inspect BN-04 frames | Confirms the frame sequence reads as a pitch update | Decide whether to keep frame sequence or build a clip. |
| Advance clip export | Tests codec/timing only after frame readback passes | Prepare animation material for YMM4 placement. |
