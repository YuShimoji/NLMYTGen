# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-factory-contract-v2-validated-v1
State-Revision: 2026-07-26.3
Updated: 2026-07-26 JST
Product-State: three-topic-evidence-extracted-into-versioned-executable-factory-contract
Product-Gate: fourth-topic-out-of-sample-validation
Recommended-Next: run-fourth-topic-through-factory-contract-v2-with-unobserved-input-axis
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-factory-contract-v2-v1
Handoff-PR: none
Required-Base: aad0043d1218cdfae8027160cd57651b04fec2ef
Implementation-Checkpoint: aad0043d1218cdfae8027160cd57651b04fec2ef
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- 観測済みnew-banknote、REINS、AI monitoringの3 packageから
  `nlmytgen.factory_package.v2`を抽出した。
- JSON Schemaと50-field inventoryをversion化した。分類はrequired 19、
  variable 10、optional 5、forbidden 7、topic-extension 2、run-local 3、
  evidence-only 4。
- source intake、claim support、canonical content、shape、media provenance、
  episode execution、source/generated project、render validation、content /
  resume identity、human decision、rights / production / publication / upload
  authority、extensionsを別sectionと別clockへ分けた。
- 3 packageに`factory_package_v2.json`を追加した。既存v1 manifest、claims、
  canonical、provenance、project、receiptをexact SHAで参照し、既存bytesは変更しない。
- generic descriptor-driven read-only adapterを実装した。shared validator内の
  known topic IDは0、unknown field / private path / hash drift / authority overclaimは
  field-level errorでfail closedする。
- CLIに`validate-factory-package`と
  `build-episode-video --factory-package ... --dry-run`を追加した。後者は既存
  v1 `run_episode_video`だけを使い、render / resume / force / explicit run-idは拒否する。
- live profileは3 packages、9 identity artifactsが9/9
  `live_file_hash_exact`。before / afterのSHA / size / mtime mismatchは0。
- Git metadataと`node_modules`を持たないtracked-only隔離copyでも3/3 pass。
  private/ignored実体の無い9 identityは`receipt_only_no_live_file`として明示した。
- 3件のpipeline dry-runはcontent identity 3/3 exact、render request / stage 0、
  YMM4 / Electron launch 0、playback / network 0、v1 tracked mutation 0。
- descriptor validationを各2回実行し、descriptor / normalized / content identityは
  3/3 repeat exact。
- focused Python 51/51、standard-loop Node contract 7/7 pass。Factory Contract
  固有24 testsがmissing section、binding gap、private path、authority inheritance、
  live drift、unobserved-axis overclaimなどを拒否する。
- new-banknoteだけが既存accepted exact artifactに結合する。REINSとAI monitoringは
  `internal_factory_canary_not_human_accepted`、rights / production /
  publication / upload / releaseはfalseのまま。

## Product Position

3件の異なる実トピック証拠を、versioned schemaとexecutable validatorで共通表現し、
既存v1 pipelineへread-only接続できる状態になった。tracked contractはprivate
artifactのlive availabilityに依存せず検証でき、live profileではexact hashを
別途確認できる。

これはobserved three-topic compatibilityである。universal arbitrary-topic
compatibility、第4トピック、全packageのhuman acceptance、rights、production、
publication、releaseは未証明または未承認である。

## Exact Next Action

既存3件に無い入力軸を最低1つ持つ第4トピックを選び、Factory Contract v2へ
out-of-sample入力として通す。

開始条件:

- source / claim / media / rights境界を先に記録する
- v2 descriptorを作成し、field-level validatorを通す
- tracked-only profileとlive availability profileを分離する
- pipeline dry-runで既存v1経路とcontent identityを確認する
- ownerが許可した場合だけnormal production loopへ進む
- 結果は観測した新軸だけに限定し、universal claimへ拡張しない

## Evidence and Access

- Contract schema:
  `schemas/factory_contract_v2/factory_package_v2.schema.json`
- Field inventory:
  `schemas/factory_contract_v2/field_inventory.json`
- Validator:
  `src/pipeline/factory_contract_v2.py`
- Package descriptors:
  各topic packageの`factory_package_v2.json`
- Machine-readable receipt:
  `docs/verification/FACTORY_CONTRACT_V2_VALIDATION_2026-07-26.json`
- Detailed supervisor report:
  `docs/verification/FACTORY_CONTRACT_V2_VALIDATION_2026-07-26.md`

## Cross-Terminal Re-entry

- Fetch and track `origin/codex/nlmytgen-factory-contract-v2-v1`; require
  `HEAD...@{upstream}=0/0` and tracked clean.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Restore with `uv sync --extra dev --locked`; this slice itself does not require
  Electron, YMM4, private artifacts, or media playback.
- Validate one descriptor with
  `uv run python -m src.cli.main validate-factory-package --package <path> --check-live`.
- Dry-run through the existing pipeline with
  `uv run python -m src.cli.main build-episode-video --factory-package <path> --dry-run`.
- Focused regression:
  `uv run pytest -q tests/test_factory_contract_v2.py tests/test_episode_video_pipeline.py tests/test_third_real_topic_factory_canary.py tests/test_standard_production_loop_gui.py`
  and `node --test gui/standard_production_loop.test.js`.

## Active Boundaries

- Accepted new-banknote bytes and exact human decision receipt remain immutable.
- REINS and AI-monitoring human creative acceptance and media rights remain open.
- A receipt proves past identity; it does not claim current live availability.
- Technical validation cannot change rights, production, publication, upload,
  release, or public authority clocks.
- GUI, YMM4, render, playback, private transfer, fourth-topic execution, PR,
  merge, master mutation, deployment, publication, upload, release, access
  change, and public exposure were not performed in this slice.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
