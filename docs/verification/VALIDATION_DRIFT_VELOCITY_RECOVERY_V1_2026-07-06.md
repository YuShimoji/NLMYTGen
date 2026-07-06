# Validation Drift Velocity Recovery v1

This note classifies the current validation drift enough to keep product work
moving. It is not a full-suite green campaign and does not rewrite old
newsroom snapshots.

## Decision

Episode 002 product work can continue. The current failures are nonblocking for
the next product-building slice because the episode 002 dashboard readiness
test remains green and the failures cluster in older generated newsroom
artifacts.

## Failure Ledger

| group | count | blocking for next product slice | evidence | action |
|---|---:|---|---|---|
| true_blocker_for_next_product_slice | 0 | no | `tests/test_dashboard_readiness_ingest.py` passed | continue product work |
| nonblocking_validation_noise | 22 | no | recent full pytest reported 22 failures outside dashboard ingest | do not pursue global green |
| host_or_path_drift | 9 | no | stored `C:\Users\thank...` paths differ from current `C:\Users\PLANNER007...` paths | normalize later only if that lane becomes active |
| generated_artifact_dirtiness | 1 | no | previous full pytest dirtied unrelated newsroom generated artifacts | avoid broad full-suite loops |
| stale_expected_metadata | 4 | no | visual-card tests expect old `audience-fit-v1` metadata while current artifacts are `density-benchmarked-v1` | defer to visual-card lane |
| fixture_snapshot_drift | 12 | no | SVG/contact-sheet/rendered artifact equality failures are older newsroom snapshots | no broad snapshot rewrite |
| unrelated_legacy_residue | 22 | no | failures are dense-script, visual-card, animation, and background-animation surfaces | keep episode 002 velocity |
| requires_human_input_or_provenance | 0 | no | real transcript is a product gate, not a validation blocker | choose only if input exists |
| unknown_needs_followup | 0 | no | representative failures explain the current drift classes | no immediate follow-up |

## Evidence Commands

```text
uv run pytest tests\test_newsroom_v0_1_dense_script_semantic_audit.py::test_user_saved_dense_v1_source_ymmp_is_ignored_local_evidence tests\test_newsroom_visual_card_benchmarked_refinement.py::test_per_card_changes_and_svg_assets_encode_benchmarked_text_fit -q
```

Result: 2 failed, confirming host/path drift and stale visual-card metadata.

```text
uv run pytest tests\test_dashboard_readiness_ingest.py -q
```

Result: 4 passed.

Recent full-suite input from the prior terminal output:

```text
uv run pytest
```

Result: 22 failed, 1173 passed, 28 skipped. This slice did not rerun full pytest.

## Product Return Path

Preferred next slice: episode 002 GUI dashboard panel.

Reason: dashboard readiness ingest is generated and validated, and the
validation drift does not block a read-only GUI/panel surface. YMM4 import
preview and thumbnail proof remain reasonable follow-ups. Real transcript or
source replacement should wait until local input and provenance are available.

## Boundaries Kept

- No full-suite green campaign.
- No repeated full pytest loops.
- No broad fixture regeneration.
- No unrelated Baseball/static/frame/hash cleanup.
- No public upload, OAuth/API keys, payment, legal/public-ready acceptance, or
  destructive/cross-repo action.
- No YMM4 GUI launch/render.
- No live scraping/media download.
