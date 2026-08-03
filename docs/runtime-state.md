# Runtime State — NLMYTGen

Project-State-ID: yukkuri-six-channel-reverse-benchmark-v1
State-Revision: 2026-08-03.1
Updated: 2026-08-03 JST
Product-State: six-benchmarks-configured-reproduction-evidence-pending
Product-Gate: six-complete-reference-evidence-sets
Recommended-Next: prepare-b05-authorized-static-evidence-intake
External-State: local-feature-branch
Development-Audio-Policy: static_only_and_silent
Handoff-Branch: codex/yukkuri-six-benchmark-reverse-engineering-v1
Handoff-PR: none
Required-Base: 543b46ee5f9dd1ced48ed48b912c23449652fa3f
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: resolve from Git at handoff; do not infer from this capsule
Tracked-Worktree: verify clean after the current static slice is committed

## Current Slice

- G-28 is now the approved Six-channel Reverse Benchmark Pack. Six real
  Yukkuri-explainer channels and one fixed public video per channel are registered
  with unique channel, video, and editing-archetype identities.
- The controlled registry defines twelve completion dimensions: identity, script,
  full timeline, composition, subtitles, characters, assets, motion, audio,
  YMM4 mapping, rights, and final render comparison.
- `build-yukkuri-benchmark-pack` validates the registry and emits six static
  reproduction blueprints, static HTML review cards, a gap matrix, a quick-win
  execution queue, a machine readback, and a hash manifest.
- Quick-win priority starts with B05 `compact_question_overview`, then B02, B03,
  B01, B04, and B06. This order reduces initial layout and timing complexity; it
  does not authorize automatic media inspection or production.
- Existing repository evidence for B01–B05 is linked by exact registry and bounded
  observation locators. B06 currently has public metadata identity only.
- Current readback passes all structural checks: 6 targets, 6 channels, 6 videos,
  6 archetypes, 12 required dimensions, exact quick-win priorities, silent policy,
  no foreground media, no automatic download, no embedded media/iframe, and no
  false readiness claims.
- All six targets remain `blocked_by_missing_evidence`; none is represented as a
  complete reproduction. The generated pack is an executable intake and gating
  contract, not six finished videos.
- No public player, YMM4 window, rendered video, media download, audio path, Python
  video renderer, `.ymmp` zero-generation, production action, or publication path
  was used in this slice.

## Product Position

NLMYTGen now has a reverse-engineering-first control plane for comparing and
promoting six distinct Yukkuri production profiles. It replaces skill-driven
appearance guessing with source identity, measured-evidence status, explicit
gaps, deterministic static review artifacts, and a fail-closed readiness gate.
It does not yet contain the full authorized dialogue, state-by-state timelines,
rights-cleared replacement assets, operator-saved YMM4 carriers, or final render
comparisons needed to produce and accept six complete replicas.

## Exact Next Action

Prepare the B05 authorized static evidence intake without launching media. Supply
or approve a complete dialogue transcript, speaker map, full timeline/state map,
subtitle and composition measurements, rights-cleared replacement asset manifest,
and an operator-saved YMM4 template source. After those inputs exist, map B05 to
the existing IR / registry / template-first YMM4 route, perform static readback,
and leave audio/render comparison for a separately authorized guarded session.

## Evidence and Access

- Six-target source registry:
  `production_pilots/yukkuri_benchmark_six_v1/benchmark_registry.json`
- Generated machine readback:
  `production_pilots/yukkuri_benchmark_six_v1/reproduction_pack/readback.json`
- Quick-win execution queue:
  `production_pilots/yukkuri_benchmark_six_v1/reproduction_pack/execution_queue.json`
- Cross-target gap matrix:
  `production_pilots/yukkuri_benchmark_six_v1/reproduction_pack/gap_matrix.json`
- Static review hub:
  `production_pilots/yukkuri_benchmark_six_v1/reproduction_pack/index.html`
- Builder and validator:
  `src/pipeline/yukkuri_benchmark_reproduction.py`
- Focused tests:
  `tests/test_yukkuri_benchmark_reproduction.py`

## Cross-Terminal Re-entry

- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Check out `codex/yukkuri-six-benchmark-reverse-engineering-v1` and verify its
  upstream parity after the current slice is published.
- Rebuild with
  `python -m src.cli.main build-yukkuri-benchmark-pack --format json`.
- Run
  `python -m pytest tests/test_yukkuri_benchmark_reproduction.py -q`.
- Do not open the static HTML automatically; inspect JSON/readback first. Do not
  launch any public player, YMM4 preview, rendered video, or audio path.

## Active Boundaries

- Complete reproduction: pending for B01–B06.
- Rights clearance and approved replacement assets: pending for B01–B06.
- Full transcript/timeline/motion/audio measurement: pending for B01–B06.
- YMM4 mapping/readback and final render comparison: pending for B01–B06.
- Human creative acceptance: pending for B01–B06.
- Existing accepted new-banknote internal cut and dependency-lock authority:
  preserved and unchanged.
- Electron 35.7.5 security remediation: still a separate pending major-version
  compatibility decision; not changed by this slice.
- Publication, upload, release, PR, merge, and main integration: not performed.

## Maintenance Note

Keep this capsule within 160 lines. Do not convert static benchmark readiness into
a media-playback permission. Resolve the outcome commit and remote parity only
after the current implementation is committed and pushed.
