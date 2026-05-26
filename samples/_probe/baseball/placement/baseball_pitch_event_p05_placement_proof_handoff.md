# Baseball BN-05 insertion proof handoff

Artifact: `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp`

This is a minimal YMM4 transport/readback proof for the Baseball sidequest. It is
not production placement, not a render proof, not creative acceptance, and not a
publish gate.

## What was generated

- One `ImageItem` at frame `1560`, length `1320`, layer `12`.
- Source PNG: `samples/_probe/baseball/static/baseball_pitch_event_p05.png`
- Canvas: `1920x1080`
- Timeline FPS: `60`
- Timeline end frame: `2880`

## Mechanical readback

- status: `passed`
- proof ymmp sha256: `69e4b0f6b03fa66116a9f8f480576f894d3adb094774227cb2b1b7c441be8983`
- failed checks: (none)

## Manual preview gate

Open `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp` in YMM4 and inspect the preview at the Baseball
placement span. PASS means the infographic fills the 16:9 frame without crop,
the scoreboard / strike zone / pitch log / claim remain readable, and no
subtitle or character layer covers the claim. Return one preview screenshot plus
PASS/FIX note.
