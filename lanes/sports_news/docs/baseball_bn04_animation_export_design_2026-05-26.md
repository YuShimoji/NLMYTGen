# Baseball BN-04 frame sequence export (2026-05-26)

BN-04 now starts with a frame-sequence export instead of a video clip. This
keeps the Baseball sidequest deterministic while the visual renderer is still a
sample-only HTML/React capture surface.

## Default export shape

| Decision | Default |
| --- | --- |
| Export mode | `frame_sequence_first` |
| Export command | `cd gui && npm run capture:baseball-frames` |
| Size | `1280x720` |
| FPS metadata | `30` |
| Duration metadata | `1200ms` |
| Frame count | `5` |
| Manifest | `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_manifest.json` |
| Readback | `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_readback.json` |
| Handoff | `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_handoff.md` |

The first sequence compares the previous pitch and current pitch from
`baseball_visual_data.v1`: previous FF context, transition into the current SL
state, and current P05 lock. The renderer must keep DesignCanvas and Tweaks UI
out of every frame.

Generated frame files live under
`samples/_probe/baseball/animation/frames/baseball_pitch_event_p05/` as
`baseball_pitch_event_p05_f000.png` through `baseball_pitch_event_p05_f004.png`.
The output is a deterministic transport/readback artifact. It is still not a
codec clip, not a YMM4 placement proof, and not creative acceptance.

## Failure conditions

- fewer than two pitches in visual data;
- any output frame is not 1280x720 PNG;
- frame count and manifest disagree;
- any frame hash is missing;
- DesignCanvas or Tweaks UI appears;
- the animation artifact is described as a clip, YMM4 proof, creative acceptance, or
  publish readiness.

BN-04 remains separate from BN-05. BN-05 decides placement; BN-04 decides how
to export motion material. The remaining manual operation is the BN-05 YMM4
preview gate, documented in
`lanes/sports_news/docs/baseball_manual_preview_hands_on_2026-05-26.md`.
