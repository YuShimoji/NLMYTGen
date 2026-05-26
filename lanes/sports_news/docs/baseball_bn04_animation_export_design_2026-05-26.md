# Baseball BN-04 animation export design (2026-05-26)

BN-04 starts with a frame-sequence contract instead of a video clip. This keeps
the Baseball sidequest deterministic while the visual renderer is still a
sample-only HTML/React capture surface.

## Default export shape

| Decision | Default |
| --- | --- |
| Export mode | `frame_sequence_first` |
| Planned size | `1280x720` |
| Planned fps | `30` |
| Planned duration | `1200ms` |
| Planned frame count | `5` |
| Planned manifest | `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_manifest.json` |
| Planned readback | `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_readback.json` |

The first sequence should compare the previous pitch and current pitch from
`baseball_visual_data.v1`: previous FF context, transition into the current SL
state, and current P05 lock. The renderer must keep DesignCanvas and Tweaks UI
out of every frame.

## Failure conditions

- fewer than two pitches in visual data;
- any output frame is not 1280x720 PNG;
- frame count and manifest disagree;
- any frame hash is missing;
- DesignCanvas or Tweaks UI appears;
- the animation artifact is described as YMM4 proof, creative acceptance, or
  publish readiness.

BN-04 remains separate from BN-05. BN-05 decides placement; BN-04 decides how
to export motion material.
