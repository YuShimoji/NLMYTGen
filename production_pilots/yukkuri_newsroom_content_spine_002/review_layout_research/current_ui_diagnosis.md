# Current UI Diagnosis

Evaluated prototype: `production_pilots/yukkuri_newsroom_content_spine_002/review_cockpit_compact/review_cockpit.html`

Verdict: weak_pass_evaluated_prototype.

## User Feedback Mapping

- Prior-project knowledge burden: internal names such as GUI dashboard panel, import preview pack, and thumbnail visual proof pack are primary labels.
- Search burden: the user must infer whether real input, YMM4 observation, or hold is the right path.
- Tool-centric framing: the surface lists known artifacts and gates before it explains the user's situation.
- Text density: each action card carries use/effect/requires text and competes with the surface status row.
- Durability issue: a cockpit built around episode-specific artifact names will not scale to repeated review surfaces.

## Design Requirement

The replacement direction should open with a plain-language situation check, produce one recommended next action, and keep source records and gates secondary but available.
