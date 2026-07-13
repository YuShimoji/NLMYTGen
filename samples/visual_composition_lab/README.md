# Visual Composition Lab

This neutral sample package demonstrates schema invariance, not runtime or
production capability.

| Fixture | Role | Scenes | Cues |
| --- | --- | ---: | ---: |
| `inspection_route_A.json` | selected Route A as data-only inspection fixture | 3 | 9 |
| `process_generic.json` | unrelated fictional process | 4 | 5 |
| `comparison_generic.json` | unrelated fictional comparison | 2 | 4 |

All three are passed to the same
`src/pipeline/generic_visual_scene_ir.py::validate_fixture` path. The generic
core contains no fixture-name branch and was not edited after adding another
fixture.

Run the read-only check:

```powershell
uv run python -m src.pipeline.generic_visual_scene_ir --check
```

Regenerate only the deterministic readback and secondary HTML board:

```powershell
uv run python -m src.pipeline.generic_visual_scene_ir
```

`conformance_readback.json` must remain `evidence_level=C2`,
`runtime_capability_proven=false`, and `cross_topic_proven=false`. Route A's
motion gaps are expected and have explicit static/narration fallbacks. Do not
turn this lab into a final project or render request.
