# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-three-run-operator-repeatability-validated-v1
State-Revision: 2026-07-26.1
Updated: 2026-07-26 JST
Product-State: two-topic-factory-with-clean-gui-zero-intervention-repeatability
Product-Gate: third-topic-variation-validation
Recommended-Next: run-third-real-topic-with-new-cue-scene-speaker-time-shape
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-three-run-operator-repeatability-v1
Handoff-PR: none
Required-Base: da88ad52d9157da9be3d40a56567d80a1b9f025b
Implementation-Checkpoint: 2d5c4f34c8b88070075a2678a08d9a72fafa9f31
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; ignored/private runs preserved

## Current Slice

- REINS factory canaryを同一clean checkpointから通常Electron 43 GUI経路で
  3回連続実行した。3回ともdoctor code/review/render/regenerate 4/4 ready、
  protected inputs 9/9 exact、write-free dry-run、実YMM4 render、media validation、
  result readbackをpassした。
- final seriesは`real_estate_reins_repeatability_v3_01`、`v3_02`、`v3_03`。
  `readiness_bypass=false`、`render_test_double=false`、tracked clean dispatch、
  manual intervention / Computer Use / SendKeys / keyboard-mouse injectionは各0。
- post-runのElectron、Python、YMM4、Win32Service、render driver、ffmpeg residueは
  各run 0。playbackとsystem-volume operationも0。
- content identity
  `15375b3a9265269776e0c35e5f3104025fa5857155f4888ab75e9e43b3d45c06`、
  normalized project
  `6211ca91e0db06d54ef15d1f40cc53a18722aafd457385c253483d2a790dd3cf`、
  MP4
  `4c99feed4e487743e5243074c3eca6aad51a7b16392f7f405ce158f038cb5c75`、
  asset semantic
  `c5165a0f615189a1a870a667a768560fc691d6a740ef0e87744f4f522386a8f9`、
  cue semantic
  `bb5fa4b7c5c408965b92794ee88e80fdc43fb85dfab1926c2f6290eccd92a196`
  は3回一致した。
- raw project SHAはrun-local pathで異なる。各run-id 8か所を同一placeholderへ
  置換した全文SHAは3本とも
  `d7aeee07b07f06b797b618c9b2b0e18981533f58ef7963cf51cd788f3dad10cf`。
  item content、timing、effects、asset、structure差は0。
- stage totalは137.568453 / 163.916620 / 226.260147秒、
  median 163.916620秒。差分は主にYMM4 render時間で、artifact identityへ影響なし。
- final run 03のcompleted-run resumeを実GUIとCLIで実行した。GUI job 1.4881秒、
  CLI observation 1.067912秒、`verified_noop`、`validation_only=true`、
  `outputs_rewritten=false`、`yymm4_launched=false`。26 canonical filesの
  SHA / size / mtime mismatchは0。
- isolated fixtureでrender settingを変更し、`resume_artifact_drift`を確認した。
  completed output破損もfocused testでfail-closed。real/private outputは未変更。
- timeout authorityはmanifestの1200秒へ統合した。pipeline 1260秒、GUI observer
  1290秒をcleanup / observer grace付きで導出し、Windows Job Objectでowned
  descendantをcontainする。synthetic child/grandchild timeout testはresidue 0、
  unrelated process不変。
- ユーザー観測の「filename欄にaddressを入れて停止」は、Save dialog内
  `保存したゲーム`TreeItemをSave buttonと誤認したことが原因だった。filename editと
  Save buttonをAutomationId + ControlTypeで特定する修正をcheckpointへ含めた。
- attempt 1の`repeatability_01` / `02`とv2 failureを全てignored evidenceとして保持。
  failed seriesとfinal v3 seriesはaggregate receiptで分離した。
- accepted new-banknote source/project/MP4/human receiptとprior REINS
  source/project/MP4/GUI receiptは作業後のlive hashがauthorityと一致した。
- REINS packageは`internal_factory_canary_not_human_accepted`。creative acceptance、
  rights、production、publication、external uploadはfalse。

## Product Position

new-banknoteとREINSという異なる2実トピックを一つのfactory contractで処理でき、
REINSではclean GUIからの3回連続zero-intervention operationとcompleted-run no-op
resumeまで実証した。single success、operator repeatability、recovery identityを
機械的に区別できる状態である。

現在の主要な未証明は第3の入力形状である。次sliceは新しいcue / scene / speaker /
time shapeを通し、topic-specific hard-codeの残存を検出する。

## Exact Next Action

第3実トピックを選び、official source、claim registry、canonical script、derived CSV、
real-media provenance、source YMMP、episode manifestを新しいidentityで用意する。

成功条件:

- 7/9 cues、3/4 scenes、4/3・3/6 speaker、45/73秒と異なるshape
- normal GUI doctor 4/4 → dry-run → real render → receipt
- manual intervention 0、owned process residue 0、silent policy維持
- existing new-banknote / REINS / v3 repeatability identity exact
- private media非追跡
- creative / rights / production / publication gate維持

## Evidence and Access

- Aggregate machine receipt:
  `production_pilots/factory_canaries/real_estate_reins_transparency_001/three_run_repeatability_receipt.json`
- Detailed supervisor report:
  `docs/verification/THREE_RUN_OPERATOR_REPEATABILITY_2026-07-26.md`
- Final ignored run receipts:
  `production_pilots/factory_canaries/real_estate_reins_transparency_001/auto_video_runs/real_estate_reins_repeatability_v3_0{1,2,3}/`
- GUI probes:
  corresponding `_gui_probe/receipt.json` sibling directories
- Resume GUI observation:
  `real_estate_reins_repeatability_v3_03_resume_gui_probe/receipt.json`
- Pipeline:
  `src/pipeline/episode_video.py`
- UIA driver:
  `tools/Ymm4RenderAutomation/Program.cs`
- GUI smoke:
  `gui/three_run_operator_repeatability_smoke.js`

## Cross-Terminal Re-entry

- Fetch and track
  `origin/codex/nlmytgen-three-run-operator-repeatability-v1`; require
  `HEAD...@{upstream}=0/0` and tracked clean.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Restore dependencies with `uv sync --extra dev --locked` and
  `npm --prefix gui ci`; require Electron 43.2.0.
- Private source media/YMMP/MP4 remain outside Git. Use declared locators and
  hash verification before real render.
- Focused portable checks:
  `uv run pytest -q tests/test_episode_video_pipeline.py tests/test_standard_production_loop_gui.py tests/test_runtime_doctor.py`,
  `npm --prefix gui run test:standard-production-loop`, and Release .NET build.

## Active Boundaries

- 3-run result is technical internal-review evidence.
- accepted new-banknote bytes and human decision receipt remain immutable.
- REINS official captures have unresolved reuse rights.
- Third topic, human review, rights approval, production, publication, upload,
  release, PR, merge, master mutation, deployment, access change are unperformed.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
