# Review Console Visual Self-Review

- Gaze: header identity -> main review target -> inspector next operation -> evidence drawer only when detail is needed
- Priority: primary recommendation and blocker are above secondary records
- Operation flow: review surface, choose operation, inspect raw records only on demand
- Text density: 50.1% reduction (359 -> 179 words)
- Evidence handling: evidence_visible_outside_drawer=True; drawer role=secondary_raw_records_and_source_paths
- Safety surface: gate_text_bounded=True; closed gates are compact badges, not the main content.
- Hold handling: safe_fallback_not_progress and not the primary recommendation.
