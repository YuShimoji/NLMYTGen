# Project Lanes

This compact lane map keeps review and maintenance loops from blocking product
progress. It is a navigation artifact, not a production gate or roadmap
expansion. Current state is mirrored in `docs/PROJECT_COCKPIT.md`.

| Lane | Purpose | Effect | Requirement | Current state | Owner | Next move |
|---|---|---|---|---|---|---|
| Output / Video Layer | Move toward an observed Episode 002 project and later video deliverables. | Keeps product proof independent from status/UI polish. | Five-point YMM4 import observation, then verified local input. | Observation package is ready; actual import/render has not happened. | Human operator for YMM4 signal, then NLMYTGen adapter. | Return the five observations; fix the adapter only if evidence requires it. |
| Input / API Hub | Receive verified source/transcript material without taking over upstream selection. | Enables replacement of the explicit sample fixture. | Source or transcript, provenance/rights note, stable identity, and cue alignment. | Required contract exists; candidate count is zero. | Upstream/source-intake lane, then NLMYTGen intake adapter. | Build a validated local receipt after material is supplied. |
| GUI / IA / i18n | Improve visible surfaces without restarting a long prototype chain. | Makes layout, language, color/type, and motion choices cheap to correct. | A new visible slice or explicit rejection of an accepted direction. | Prior Japanese console is a source record, not the current development slice. | NLMYTGen review UI lane. | Run a 2–3 direction low-fi check before the next high-fidelity build. |
| Integrity / Triage | Isolate full pytest drift, fixture drift, generated artifact policy, and heavy constraints. | Prevents validation cleanup from swallowing product slices. | Explicit integrity task or a failing narrow gate. | Full-suite drift is nonblocking for this slice. | Integrity/triage lane. | Use targeted checks only here. |
| Editing / YMM4 Feature Design | Observe import behavior and correct deterministic editing routes. | Separates actual GUI evidence from speculative adapter work. | Human performs the bounded import observation. | Five-point observation is ready; all five results remain unobserved. | Human observation + assistant readback/fix. | Use the observation sheet; do not broaden to render/publication. |
| Deep Research | Study app form, UI model, Docker capabilities, video trends, and production-process reverse engineering. | Feeds later product strategy without delaying current output. | Explicit research lane and bounded question. | Deferred. | Research lane. | Do not run deep external research in this slice. |

## Content Production A-E Mapping (`content-production-lanes/v1`)

This project-local mapping applies the shared content-production lane semantics
without replacing the operational lanes above. It is `CONTROL_ONLY`: it does
not change `docs/runtime-state.md`, `docs/PROJECT_COCKPIT.md`, the recommended
next action, candidate adoption, or product state. Each lane is an independent
requirement vector. Requirements are evaluated in the listed order and the
first failed requirement controls that lane's re-entry. Do not collapse the
vectors into a scalar percentage. Descriptive or flavor prose is not authority,
and a requirement unavailable because another requirement failed is
`BLOCKED_BY_DEPENDENCY`. Use `N/A` only when a responsibility genuinely does
not exist for NLMYTGen, and record both the reason and downstream-dependency
effect when that occurs.

The current mapping preserves the prepared YMMP identity recorded by SHA-256
`576b2e911b5ab0d3ee213fa6fe886994b5cd89e26589a561df15d583689e3105`,
the separate prior-proof identity, the observed 47.25-second native timing for
`cue_001..cue_006`, the six absent hash-bound assets, and
`candidateAdopted=false`. It does not revive another NLM family, adopt the
uncommitted challenge draft, or treat the provisional 140% / 33.75-second
estimate as native evidence.

| Shared lane | NLMYTGen responsibility and real records | Ordered requirements | First failed requirement | Re-entry predicate |
|---|---|---|---|---|
| A — Replaceable assets / generation inputs / metadata | Carries replaceable visual bytes, CSV/IR/registry/template-patch inputs, carrier metadata, and non-overwriting output identities. Current records include `samples/palette.ymmp`, the tracked unadopted excerpt-input candidate, and the protected uncommitted challenge draft. The six registered visual identities are exact but their bytes are present `0/6`. | A1 stable input and output identities are explicit — **met**. A2 all six exact hash-bound asset bytes are physically available through an authorized path — **failed**. A3 machine-local path resolution and template-ready input map — **BLOCKED_BY_DEPENDENCY**, because A2 is false and no substitute path is permitted. | `A-ASSET-BYTES-AVAILABLE`: six exact registered bytes are absent. | Restore all six bytes through an authorized path and verify every registered SHA-256 without aliasing, regeneration, hash relaxation, or substitution. Rights approval remains a separate E-lane requirement. |
| B — Evidence / source / facts / profiles / provenance | Owns the canonical nine-cue source and approval locks, claim/provenance records, real-media provenance, and tracked YMM4 native timing observation. These records establish the 4,415-frame full script and the 2,835-frame / 47.25-second shortest unchanged six-cue window. They may inform C and D but never select or rewrite authored content. | B1 canonical source and human-approval identities are locked — **met**. B2 source/provenance and exact asset identities are recorded — **met**. B3 tracked native YMM4 timing is sufficient to evaluate the current duration claim — **met**. B4 evidence remains non-authoring — **met**. | **None — all current B requirements satisfied.** B cannot turn those findings into a C-lane content decision. | Re-open B only when an underlying source, claim, provenance record, asset identity, or actual YMM4 observation changes and needs a new attributable receipt. More summaries of unchanged evidence are busywork. |
| C — Authored content / narrative intent / structure / selected beats | Owns the approved nine-cue authored script and any human-approved short premise, beat selection, condensation, or structural change. The current `cue_001..cue_006` excerpt is noncanonical and unadopted; topic, canon, selected beats, source rewriting, and major voice intent remain human-owned. | C1 the full nine-cue script and its approval identity are preserved — **met**. C2 one authority-compatible 20–35-second authored premise or allowed transformation is selected and adopted for the challenge — **failed**. C3 its exact wording/order/beat change class is approved and serialized — **BLOCKED_BY_DEPENDENCY**, because C2 has no decision. | `C-AUTHORED-SHORT-PREMISE-ADOPTED`: no human-authorized short premise or transformation currently makes a new candidate permissible. | Resolve `DEC-NLMYTGEN-NATIVE-20-35-PREMISE-20260814-001` with an exact allowed source/selection/major-voice change or an explicit unchanged-content instruction. The decision remains pending/backlog, not the current human action. |
| D — Presentation / realization | Owns YMM4-native timing, speaker-distinct readable subtitles, content-linked visual placement, template application, and render realization. Tracked native evidence exhaustively places every contiguous 6–9 cue window outside the inclusive 1,200–2,100-frame contract; the shortest is 2,835 frames. No current YMMP/MP4/review candidate is attached to this challenge. | D1 an authority-compatible tracked YMM4-native observation for an applicable contiguous 6–9 cue candidate is inclusively 1,200–2,100 frames at 60 fps — **failed**. D2 template application and actual VoiceItem/subtitle/visual readback — **BLOCKED_BY_DEPENDENCY**, because D1 is false and A2 is also false. D3 non-overwriting render and silent technical verification — **BLOCKED_BY_DEPENDENCY**, because no template-ready candidate exists. | `D-NATIVE-TIMING-IN-RANGE`: eligible native windows are `0/10`; a calculated speed estimate is not an observation. | Supply a genuinely new tracked YMM4-native observation for an unchanged contiguous 6–9 cue span at inclusive 1,200–2,100 frames, or first satisfy the C-lane decision and then record actual native VoiceItem timing for its successor. Do not open YMM4 or apply a template merely to repeat the unchanged failed route. |
| E — Integration / final experience / rights / release / acceptance | Owns cross-lane integration, rights, an actually reviewable artifact, creative acceptance, production/release, and publication. Current state has no MP4 or review packet; the six asset rights flags remain false; creative, production, publication, and release acceptance remain open. | E1 the intended visual assets have an explicit rights decision — **failed**. E2 an integrated artifact exists from eligible A/C/D inputs — **BLOCKED_BY_DEPENDENCY**, because A2, C2, and D1 are false. E3 human experience/creative acceptance — **BLOCKED_BY_DEPENDENCY**, because no reviewable artifact exists. E4 production/release/publication acceptance — **BLOCKED_BY_DEPENDENCY**, because E2 and E3 are unresolved. | `E-ASSET-RIGHTS-DECISION`: exact asset identity does not imply permission to use it. | Obtain the separate rights decision for the six exact assets. After A, C, and D independently satisfy their first-failed requirements, create a non-overwriting artifact and route only that real artifact to human experience/creative acceptance. |

### Portable Evidence Locators

The formal records below use these repo-relative locators. Fragment names are
typed observations, not new authority or inferred acceptance.

| Evidence ID | Portable locator and typed observation |
|---|---|
| `EV-A1` | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/development_challenge_excerpt_inputs/nlmyt-a203cf3-adoption-eligibility-excerpt-inputs-v1/manifest.json#files,source_locks,boundaries` — stable input locks and non-overwriting/input-only boundaries are recorded. |
| `EV-A2` | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/development_challenge_excerpt_inputs/nlmyt-a203cf3-adoption-eligibility-excerpt-inputs-v1/input_registry.json#assets,gates` — typed absence: `all_required_assets_present=false`, exact bytes present `0/6`. |
| `EV-B1` | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/canonical_script.json` and `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/human_script_approval_receipt.json` — canonical nine-cue source and approval identities. |
| `EV-B2` | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_pipeline/new_banknote_real_media_provenance.json` and `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/development_challenge_excerpt_inputs/nlmyt-a203cf3-adoption-eligibility-excerpt-inputs-v1/input_registry.json#source_registry,source_visual_mapping` — provenance and exact asset identities. |
| `EV-B3-D1` | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/existing_yymm4_evidence_revalidation_receipt.json` SHA-256 `4b6d3e781f98a585778c8b1c05da7f7646566a2b881aeaf694b68c982c30a5f0` and `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/existing_yymm4_evidence_revalidation_readback.json` SHA-256 `8075efa1d9c49afe0282af550520bb28cf6c197392c3f450bf44d22ab034e44c` — tracked native observation: nine VoiceItems, 4,415 frames at 60 fps; shortest unchanged six-cue window 2,835 frames, eligible windows `0/10`. |
| `EV-B4` | `docs/INVARIANTS.md` and `docs/CONTENT_TRANSFORMATION_PROVENANCE.md` — evidence/provenance may inform authored content but cannot silently control or change it. |
| `EV-C1-C2` | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/development_challenge_excerpt_inputs/nlmyt-a203cf3-adoption-eligibility-excerpt-inputs-v1/manifest.json#base_identity,scope,duration_gate` — typed absence: `candidate_adopted=false`; excerpt is noncanonical and duration gate is failed closed. |
| `EV-D2-E2` | `docs/DEVELOPMENT_GENERATED_VIDEO_CHALLENGE.md` — no current challenge YMMP, rendered MP4, or review candidate; the protected uncommitted input draft is not adoption. |
| `EV-E1` | `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/development_challenge_excerpt_inputs/nlmyt-a203cf3-adoption-eligibility-excerpt-inputs-v1/input_registry.json#gates,assets` — typed absence: `rights_approved=false` for the six exact registered assets. |

### Formal Active Requirement Records

`order` is a stable, globally unique integer used only for deterministic
first-failed selection. File order, table row order, and requirement labels are
non-authoritative. Only `depends_on` creates a dependency; a lower order in one
lane never makes an independent higher-order lane depend on it. Active records
use only `SATISFIED`, `UNSATISFIED`, or `BLOCKED_BY_DEPENDENCY`. There is no
current `N/A`. If a future responsibility genuinely does not exist, its record
must add both `na_reason` and `na_dependency_effect` and be excluded from the
active first-failed calculation.

| requirement_id | lane | order | unit | required | observed | owner | depends_on | evidence | authority_effect | status |
|---|---:|---:|---|---|---|---|---|---|---|---|
| `A1` | `A_REPLACEABLE_ASSETS_AND_METADATA` | 100 | identity contract | Stable input/output identities and non-overwriting boundaries. | Exact locks and input-only boundaries recorded. | `agent_owned` | `[]` | `EV-A1` | Makes inputs attributable; does not adopt content or authorize rendering. | `SATISFIED` |
| `A2` | `A_REPLACEABLE_ASSETS_AND_METADATA` | 110 | exact asset bytes | Six registered bytes available through an authorized path with exact SHA-256. | Typed absence `0/6`; no substitute is permitted. | `external_evidence_owned` | `[A1]` | `EV-A2` | Passing unlocks A3 only; it does not decide rights, authored content, timing, or acceptance. | `UNSATISFIED` |
| `A3` | `A_REPLACEABLE_ASSETS_AND_METADATA` | 120 | runtime input map | Machine-local resolution and template-ready input map. | Not materialized because exact bytes are absent. | `agent_owned` | `[A2]` | `EV-A1`, `EV-A2` | Passing can make inputs template-addressable; it cannot adopt or render a candidate. | `BLOCKED_BY_DEPENDENCY` |
| `B1` | `B_EVIDENCE_AND_REFERENCE` | 200 | source lock | Canonical source and human-approval identities are locked. | Nine-cue source and approval receipt present. | `agent_owned` | `[]` | `EV-B1` | Establishes source identity only; it does not choose a short premise. | `SATISFIED` |
| `B2` | `B_EVIDENCE_AND_REFERENCE` | 210 | provenance registry | Claim/provenance and exact asset identities are recorded. | Portable provenance and registry records present. | `agent_owned` | `[B1]` | `EV-B2` | Allows attribution and asset identity checks; it does not grant rights. | `SATISFIED` |
| `B3` | `B_EVIDENCE_AND_REFERENCE` | 220 | native timing observation | Attributable tracked YMM4-native timing sufficient to evaluate the current duration claim. | Nine VoiceItems and all current native frame boundaries recorded. | `external_evidence_owned` | `[B1]` | `EV-B3-D1` | May inform D1; it cannot select, shorten, or rewrite C. | `SATISFIED` |
| `B4` | `B_EVIDENCE_AND_REFERENCE` | 230 | authority boundary | Evidence remains informative and non-authoring. | Boundary is explicit in project invariants and lineage contract. | `human_owned` | `[]` | `EV-B4` | Prevents B facts or flavor prose from controlling authored content. | `SATISFIED` |
| `C1` | `C_AUTHORED_CONTENT_AND_STRUCTURE` | 300 | canonical authored script | Approved canonical nine-cue script remains preserved. | Exact source and approval identity remain unchanged. | `human_owned` | `[B1]` | `EV-B1` | Preserves canon; it does not adopt a challenge excerpt. | `SATISFIED` |
| `C2` | `C_AUTHORED_CONTENT_AND_STRUCTURE` | 310 | short-premise decision | Human-authorized 20–35-second premise or allowed authored transformation selected and adopted. | Typed absence: `candidate_adopted=false`; current six-cue excerpt is noncanonical. | `human_owned` | `[C1]` | `EV-C1-C2` | Passing authorizes a specific authored candidate only; it does not prove native timing or rights. | `UNSATISFIED` |
| `C3` | `C_AUTHORED_CONTENT_AND_STRUCTURE` | 320 | serialized change class | Approved wording/order/beat change class serialized with exact identity. | No authorized C2 decision exists to serialize. | `agent_owned` | `[C2]` | `EV-C1-C2` | Passing makes an authored change attributable; it does not authorize template application or release. | `BLOCKED_BY_DEPENDENCY` |
| `D1` | `D_PRESENTATION_AND_REALIZATION` | 400 | native frames at 60 fps | Applicable contiguous 6–9 cue candidate has actual tracked timing inclusively 1,200–2,100 frames. | Shortest is 2,835 frames; eligible windows `0/10`; 140% estimate excluded. | `external_evidence_owned` | `[B3]` | `EV-B3-D1` | Passing unlocks D2 timing-wise; it does not satisfy A, C, E, or creative acceptance. | `UNSATISFIED` |
| `D2` | `D_PRESENTATION_AND_REALIZATION` | 410 | template and readback | Template application plus actual VoiceItem, subtitle, and visual readback. | No template-ready eligible candidate exists. | `agent_owned` | `[A2,D1]` | `EV-A2`, `EV-D2-E2` | Passing enables D3 technical realization only; it is not creative acceptance. | `BLOCKED_BY_DEPENDENCY` |
| `D3` | `D_PRESENTATION_AND_REALIZATION` | 420 | render verification | Non-overwriting render plus silent technical verification. | No eligible template-applied project exists. | `agent_owned` | `[D2]` | `EV-D2-E2` | Produces a technical artifact eligible for E integration; it does not accept it. | `BLOCKED_BY_DEPENDENCY` |
| `E1` | `E_INTEGRATION_EXPERIENCE_AND_RELEASE` | 500 | rights decision | Explicit rights decision for the six exact intended assets. | Typed absence: `rights_approved=false`. | `external_evidence_owned` | `[B2]` | `EV-E1` | Passing permits the specified use only; it does not restore bytes, prove timing, or accept experience. | `UNSATISFIED` |
| `E2` | `E_INTEGRATION_EXPERIENCE_AND_RELEASE` | 510 | integrated artifact | One integrated non-overwriting artifact exists from eligible A/C/D inputs. | No current challenge YMMP, MP4, or review candidate exists. | `agent_owned` | `[A2,C2,D1,E1]` | `EV-A2`, `EV-C1-C2`, `EV-B3-D1`, `EV-D2-E2`, `EV-E1` | Passing creates a reviewable object; it does not imply human acceptance or release. | `BLOCKED_BY_DEPENDENCY` |
| `E3` | `E_INTEGRATION_EXPERIENCE_AND_RELEASE` | 520 | creative experience acceptance | Human reviews and accepts the exact integrated artifact's experience. | No artifact exists to review. | `human_owned` | `[E2]` | `EV-D2-E2` | Closes creative experience only for the exact artifact reviewed. | `BLOCKED_BY_DEPENDENCY` |
| `E4` | `E_INTEGRATION_EXPERIENCE_AND_RELEASE` | 530 | production and release acceptance | Explicit production, release, and publication decision for the accepted artifact. | No integrated and creatively accepted artifact exists. | `human_owned` | `[E2,E3]` | `EV-D2-E2` | Closes only the explicitly decided production/release/publication scope. | `BLOCKED_BY_DEPENDENCY` |

### Mechanical First-Failed Derivation

For any scope, take records in that scope whose `status` is `UNSATISFIED` and
whose complete `depends_on` set is `SATISFIED`, then select the smallest
explicit integer `order`. `BLOCKED_BY_DEPENDENCY` records are not eligible.

| Scope | Mechanically derived first-failed | Meaning |
|---|---|---|
| Overall project audit cursor | `A2` at order `110` | This is the smallest eligible global order, not a dependency or precedence claim over independent C, D, or E gates. |
| Lane A | `A2` | Exact asset bytes are absent. |
| Lane B | None | All active B requirements are satisfied. |
| Lane C | `C2` | No human-authorized short premise or allowed transformation is adopted. |
| Lane D | `D1` | No applicable native observation is within inclusive 1,200–2,100 frames. |
| Lane E | `E1` | No explicit rights decision exists for the six exact assets. |

The overall cursor and lane-local first-failed records therefore differ by
design. A2 does not block C2, D1, or E1 because those records do not declare A2
in `depends_on`. Independent gates remain independently actionable whenever
their own re-entry predicate changes.

The abstraction unlocks no new NLMYTGen product action in the current state.
Additional mapping prose, repeated asset searches, repeated timing arithmetic,
or tests over unchanged evidence would be `CONTROL_ONLY` or busywork. Agent work
reopens only after at least one lane's stated predicate changes; success in one
lane must not be extrapolated to another.

## Stop Rule

Maintenance work returns to the product lane after its focused checks pass. A
new visible product direction gets one low-cost comparison before high-fidelity
work; an accepted direction is not reopened by ordinary polish.
