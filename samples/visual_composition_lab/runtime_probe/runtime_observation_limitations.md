# Runtime observation limitations

The operator observation is limited to the exact same-machine composite identified by
`runtime_observation_receipt.json`: one unchanged VoiceItem with linked subtitle, one
static 640x360 opaque ImageItem, and one short independent TextItem on a 1920x1080,
60 fps canvas with conservative disjoint zones.

It does not generalize to longer or differently styled text, alternate image sizes or
anchors, other subtitle profiles, other machines, motion, fades, effects, transitions,
non-default transforms, render/media validity, heterogeneous topics, production quality,
rights clearance, publication, or Route A/B/C behavior. Cross-machine portability and
C5 reuse remain unknown. If any bounded condition changes, repeat only the relevant
visual gate or fall back to the narration/static baseline.
