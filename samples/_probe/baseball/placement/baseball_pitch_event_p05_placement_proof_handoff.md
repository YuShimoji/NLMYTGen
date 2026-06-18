# Baseball BN-05 insertion proof handoff

Artifact: `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp`

This is a minimal YMM4 transport/readback proof for the Baseball sidequest. It is
not production placement, not a render proof, not creative acceptance, and not a
publish gate.

## What was generated

- One `ImageItem` at frame `1560`, length `1320`, layer `12`.
- YMM4 item FilePath: `../static/baseball_pitch_event_p05.png`
- FilePath resolution base: `proof_ymmp_directory`
- Resolved source PNG: `samples/_probe/baseball/static/baseball_pitch_event_p05.png`
- Canvas: `1920x1080`
- Timeline FPS: `60`
- Timeline end frame: `2880`

## Mechanical readback

- status: `passed`
- proof ymmp sha256: `6fde310052ae642e6cec062f64d0d1b5f589d73188983eacbdb6ea287b550a7a`
- failed checks: (none)

## Manual preview gate

Open `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof.ymmp` in YMM4 from the repo checkout. If your YMM4
installation does not resolve relative media paths, run
`lanes/sports_news/scripts/open_baseball_bn05_preview.ps1`; it creates an ignored local preview copy with an absolute
PNG path resolved from the current repo root. Inspect frame `1560` /
`00:26.00`. Return one preview screenshot plus any short freeform comment.
Fixed labels are not required.
