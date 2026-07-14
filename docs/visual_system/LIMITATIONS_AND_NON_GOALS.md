# Limitations and non-goals

## Current limitations

- Static fixture conformance is capped at C2.
- Every fixture now reports the C0 linked-subtitle typography/layout gap derived
  from its required caption reserve; C2 conformance does not conceal that gap.
- The exact short Text / static Image / linked-subtitle layout passed human
  observation, but other text metrics, wrapping, subtitle profiles/layouts and
  callout anchors remain YMM4/human-observation concerns.
- Generic ImageItem paths are same-machine until a portability probe succeeds.
- ShapeItem and callout generation currently exists only in topic-specific
  builders; it is not promoted into generic core.
- Most transform, fade and background-motion routes have code/static evidence
  but no generic runtime observation.
- Strict C4 applies to one exact internal project/render and proxy. It verifies
  media structure and decode, not semantic alignment or design quality.
- C5 is zero. Existing real packets use separate topic builders/contracts.
- The bounded result records no exact YMM4 version and proves no cross-machine
  portability, alternate asset geometry or reusable typography engine.

## Non-goals of this slice

- Build or open the selected Route A final project.
- Launch or inspect YMM4, use Computer Use, capture screenshots, or render.
- Create/download images, fonts, audio or external media.
- Change approved scripts, source claims, cue wording or pilot artifacts.
- Design a universal theme system, production asset library, GUI factory, or
  automatic rights workflow.
- Add topic exceptions, fixed scene/cue counts, or current-pilot timing to the
  generic core.
- Integrate master or claim production/public readiness.

## Recovery rule

When a requested primitive lacks the required evidence level, lower the cue to
its declared static composition or `narration_baseline`. Do not silently upgrade
the evidence or create a topic-specific core branch.
