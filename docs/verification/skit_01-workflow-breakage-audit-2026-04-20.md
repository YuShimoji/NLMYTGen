# skit_01 workflow breakage audit (2026-04-20)

## Why this exists

`skit_01` was being treated as the next G-24 proof gate, but the repo-local handoff chain drifted:

- `docs/runtime-state.md` referenced `_tmp/skit_ManualSample_01.ymmp` as a manual reference master, but that file is not present in the repo worktree.
- `docs/verification/skit_01_delivery_dispute_v1_2026-04-19.md` and the continuation prompt pointed at `_tmp/skit_01_v2.ymmp`, while the surviving repo artifact is `_tmp/skit_01_v2_verify.ymmp`.
- `samples/registry_template/skit_group_registry.template.json` describes the G-24 target state, but the registry is still shared metadata only and is not consumed by CLI resolution yet.

This is not just `skit_01 NG`; it is a repo-side sync / handoff failure.

## Trusted repo-local artifacts

- source ymmp: `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp`
- proof ymmp: `_tmp/skit_01_v2_verify.ymmp`
- IR: `samples/_probe/skit_01/skit_01_ir.json`
- registry: `samples/registry_template/skit_group_registry.template.json`
- audit command: `python3 samples/_probe/skit_01/audit_skit_01_proof.py`

These are enough to classify what the current proof candidate does mechanically, without asking the user to rebuild a missing manual sample.

## Failure classes fixed as canonical for now

- `REFERENCE_MASTER_MISSING`
  - `_tmp/skit_ManualSample_01.ymmp` is absent. It must not be used as an active gate or comparison baseline.
- `PROOF_OUTPUT_PATH_DRIFT`
  - `_tmp/skit_01_v2.ymmp` is a stale path in docs/prompt. The surviving repo artifact is `_tmp/skit_01_v2_verify.ymmp`.
- `CANONICAL_GROUP_REMARK_MISSING`
  - **old-corpus-only breakage**. The old source/proof ymmp pair does not contain registry canonical remark `haitatsuin_delivery_main`, so that corpus still does not establish a canonical template anchor. This no longer applies to `samples/canonical.ymmp`, which is tracked separately in [G24-canonical-anchor-adoption-2026-04-20.md](G24-canonical-anchor-adoption-2026-04-20.md).
- `TEMPLATE_RESOLUTION_UNPROVEN`
  - current `skit_01` evidence shows motion-labeled GroupItem segments only. It does not prove exact / fallback / manual-note template resolution for G-24.

## What the current proof is still good for

`_tmp/skit_01_v2_verify.ymmp` is still useful as a mechanical regression artifact for:

- GroupItem segment split timing
- `motion:<label> utt:<index>` remark continuity
- `enter_from_left` / `surprise_oneshot` / `deny_oneshot` / `exit_left` / `nod` motion labeling against `skit_01_ir.json`

That makes it a valid assistant-owned comparison target, but only as a motion proof, not as workflow completion for G-24.

## Safer route from here

1. Keep `skit_01` on a repo-local audit route: source ymmp + proof ymmp + IR + registry.
2. Do not ask the user to recreate `_tmp/skit_ManualSample_01.ymmp`.
3. Do not treat `_tmp/skit_01_v2_verify.ymmp` as G-24 complete proof.
4. Resume G-24 only through artifacts that are actually present in the repo. `samples/canonical.ymmp` now covers canonical anchor existence, but `skit_01` old corpus remains a mechanical motion proof until derived native template assets exist.

## Next official entrypoint

Use `python -m src.cli.main audit-skit-group <ymmp> <ir.json> --skit-group-registry <json>` as the regular preflight entrypoint.

- `status=ok` means canonical anchor + exact/fallback/manual_note resolution is mechanically classifiable for the current repo-local corpus. This is now true for `samples/canonical.ymmp`.
- `status=error` means the workflow is still blocked on repo-side evidence, not on a new user-created ManualSample.
