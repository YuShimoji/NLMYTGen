# New-banknote Successor Branch Integration Audit

> **READ-FIRST AUDIT — NO SOURCE BRANCH INTEGRATION — NO VISUAL SELECTION**

## Recommendation

- class: `selective_integration_ready`
- state: `new-banknote-successor-integration-audited-selective-ready-v1`
- primary: `origin/codex/new-banknote-existing-yymm4-evidence-revalidation-v1` @ `5e50ff707806724e67a5e0cec215bdd3b604ce32`
- candidate: `origin/codex/new-banknote-authoritative-source-script-v1` @ `833717f63713db9555f563a2a26285fa2f621e3d`
- baseline: `b05eb3867caabda496fb9a0070d230a4e81aea01`
- divergence: primary-only `7` / candidate-only `13`
- content change authorized or performed: `false`
- visual route selected: `false`

The two branches must not be normally merged. A selective path construction is ready:
keep the primary approval, T00–T07 lineage, current YMM4 revalidation, and
Operator Batch byte-exact; add only the candidate historical observation,
editorial deep-audit core, and A/B/C proposal paths; then regenerate the
candidate-current provenance surfaces and all current-state prose.

## Coverage

| measure | result |
| --- | ---: |
| primary-only commits | 7 |
| candidate-only commits | 13 |
| audited commits | 20 |
| primary side paths | 33 |
| candidate side paths | 51 |
| audited side-path entries | 84 |
| union paths | 77 |
| overlapping paths | 7 |
| unclassified commits / paths | 0 / 0 |

## Approved-content identity

- primary approved hashes: `8 / 8` exact
- candidate approved hashes: `7 / 8` exact
- candidate drift: `README_CANONICAL_SCRIPT_REVIEW.md` metadata link only;
  it is excluded because its hash is approval-conflicting
- canonical script JSON object, TXT, canonical CSV, derived CSV, cue trace,
  and source manifest: exact across branches
- content contract: 9 cues, S1/S2/S3 `2/4/3`, Reimu/Marisa `3/6`, 15 adopted
  claims, 20 factual units, 21 evidence edges, unsupported spoken claims `0`
- authority: primary explicit human approval receipt and all eight primary
  hashes remain sole current authority

## Authority result

| family | current role after later integration | candidate treatment |
| --- | --- | --- |
| Approved content | primary human receipt + eight hashes | exclude the modified approved README variant |
| Content lineage | primary T00–T07 package | no replacement |
| Editorial provenance | primary lineage remains current; D00–D10 is secondary deep audit | integrate stable core; regenerate README/lock/readback |
| YMM4 evidence | primary current-lineage revalidation | retain candidate observation as historical predecessor |
| Operator Batch | primary five-action approval/lineage-aware family | exclude candidate four-action executable family |
| Visual A/B/C | proposal-only review surface | integrate with Route A `recommended_not_selected` |
| Current state | one successor state | regenerate; never merge branch prose |

## Conflict and merge mechanics

`git merge-tree` found 7 conflicts and did not mutate the index,
worktree, or refs:

- `docs/PROJECT_COCKPIT.md`
- `docs/PROJECT_PIPELINE.mmd`
- `docs/THREAD_REGISTRY.md`
- `docs/project-context.md`
- `docs/runtime-state.md`
- `src/pipeline/new_banknote_yymm4_import_operator_batch.py`
- `tests/test_new_banknote_yymm4_import_operator_batch.py`

The five state documents require regeneration. The two Operator Batch code/test
paths are add/add conflicts where primary wins. A normal merge or whole-commit
cherry-pick is rejected because candidate commits mix compatible additions with
state, approved-README, generator, and Operator Batch changes.

## Candidate contribution

- tracked predecessor YMM4 observation: same project/result hashes, 9
  VoiceItems, 3/6, exact text/order, 60 fps, 4415 frames, 73.583333 seconds
- editorial deep audit: D00–D10, 9/9 cue coverage, 38/38 attributed substantive
  units, bounded prior-user-script result
  `not_proven_from_available_repo_evidence`
- visual review: three routes; Route A recommended but not selected; S1/S2/S3
  map to 2/4/3 cues; implementation and rights approval remain false

Candidate detached focused validation passed 30 tests and failed one
cross-check because three committed provenance surfaces encode the original
same-machine local-evidence disposition. That failure is the evidence for
`regenerate_successor`, not authority to repair the candidate branch.

## Exact later integration contract

- owner: `new-banknote-successor-selective-integration-v1`
- successor branch: `codex/new-banknote-successor-selective-integration-v1`
- base: `5e50ff707806724e67a5e0cec215bdd3b604ce32`
- candidate source: `833717f63713db9555f563a2a26285fa2f621e3d`
- mechanism: `selective_path_materialization_from_exact_candidate_ref_onto_exact_primary_base`
- candidate paths to integrate: 27
- candidate paths retained as historical: 2
- candidate paths regenerated: 8
- candidate paths excluded: 14

Order:

1. create the successor branch from the exact primary base
2. materialize only accepted candidate paths from the exact candidate revision
3. retain historical candidate receipts/reports with explicit secondary status
4. keep all primary approved, lineage, revalidation, and Operator Batch bytes
5. rebind editorial provenance implementation to primary approval/T00-T07/revalidation authority
6. regenerate the three provenance authority surfaces and all compact current-state surfaces
7. run targeted primary, editorial-provenance, visual, observation, privacy, and state validation

The full exact path lists, exclusions, authority roles, and validation plan are
in `new_banknote_successor_integration_audit.json` and the path inventory.

## Gates that remain open

- pronunciation / rhythm / clipping: unknown
- exact S04/S05 historical identity: unresolved
- token-level authorship: unavailable
- human A/B/C selection: pending
- actual integration, diagnostic YMM4 project, render, production, rights,
  publication, and master integration: not performed

## Operations not performed

No source branch was merged, rebased, cherry-picked, or modified. No approved
content, candidate package, ignored evidence, YMM4 project, media, or master ref
was changed by this audit.
