# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-third-real-topic-gui-render-validated-v1
State-Revision: 2026-07-26.2
Updated: 2026-07-26 JST
Product-State: three-distinct-real-topics-through-one-clean-gui-and-video-pipeline
Product-Gate: factory-contract-v2-extraction
Recommended-Next: derive-factory-contract-v2-from-three-observed-topics
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-third-real-topic-factory-v1
Handoff-PR: none
Required-Base: fe6672686625d401a7d2dd77fa9d9935e6036e0a
Implementation-Checkpoint: fe6672686625d401a7d2dd77fa9d9935e6036e0a
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- 第3実トピック「AIによる職場モニタリングと働く人への影響」を、5 cues、
  2 scenes、れいむ2 / まりさ3、1606 frames、26.766667秒という新しいshapeで
  同一standard production loopへ通した。
- official primary sourceはOECD、EU-OSHA、ILOの3 surface。spoken factual
  unitsは4、unsupportedは0。login、credentials、source playbackは0。
- 5 cuesすべてに別のofficial PDF raster captureを割り当てた。real-media
  provenanceは5/5、unique source SHAは5、SVGとAI-generated visualは0。
  source cache、extract、runはpackage-local ignored rootに保持する。
- source YMMPは既存のgeneric arbitrary-row `import-script`経路で自動生成した。
  actual YMM4 4.54.0.1、Windows UIA、5/5 rows、VoiceItem 5、2 scenes、
  1920x1080、60fps。manual YMM edit、Computer Use、SendKeys、input injectionは0。
- actual Electron 43.2.0 main / renderer / preloadからdeep doctor 4/4、
  protected 10/10 exact、write-free dry-run、normal enabled primary action、
  real YMM4 render、media validation、result readbackをpassした。
  `readiness_bypass=false`、`render_test_double=false`、tracked clean dispatch。
- generated projectはVoiceItem 5 / ImageItem 5 / scenes 2 / speakers 2:3、
  exact text/order、1606 frames、SVG 0。run directory外のabsolute path leakは0。
- MP4はSHA
  `f39297c9888fb59e0260676c1810430f06145949d99a8c3b46dea5d606d80e8d`、
  33,762,259 bytes、ISO-BMFF、H.264 Main / AAC-LC、1920x1080、60fps、
  26.766016秒。full decode pass、5 cue framesをvisual inspectionした。
- visual inspectionでは各official pageと字幕を識別できた。既存YMM4 character
  settingsによる大きい赤/黄keyword emphasisが一部字幕へ重なるため、
  technical passとhuman aesthetic acceptanceを分離している。
- completed runへCLI `--render --resume`を1回実行した。0.269496秒、
  `verified_noop`、YMM4 / driver launch 0、outputs rewrite 0、22 filesの
  SHA / size / mtime mismatch 0。
- isolated copyでvideo bitrateだけを変え、`resume_artifact_drift`を確認した。
  canonical runは不変。
- accepted new-banknote、prior REINS、REINS repeatability v3三本について
  20/20 live identity exact。5 dry-run recheckは全pass、prior renderは0。
- 第3topic packageは`internal_factory_canary_not_human_accepted`。rights、
  production、publication、external upload、releaseはfalse。

## Product Position

new-banknote、REINS、AI職場モニタリングという3実トピックが、異なるcue / scene /
speaker / duration / media countで同じclean standard GUI and video pipelineを
通過した。これは観測した3件に対するvariation evidenceである。

universal arbitrary-topic compatibility、production readiness、rights approval、
REINS / AI職場モニタリングのhuman creative acceptanceは未証明である。次sliceは
4件目を増やす前に、3 packageの共通部と変動部をFactory Contract v2として抽出する。

## Exact Next Action

3 packageのmanifest、provenance、claim edge、source project、generated project、
receiptsをread-only比較し、observed common contractとtopic-variable fieldsを
versioned schemaへ固定する。

成功条件:

- v2 contractがrequired / variable / optional / forbiddenを明示する
- 3 packageをmigrationまたはadapterでv2 validatorへ通す
- accepted/new and prior outputsをrerenderせずidentity exactで再検証する
- source intake、claim support、media provenance、resume identityを別contractとして保つ
- fourth-topic testはv2 extractionとfixture revalidation後のout-of-sample gateにする
- creative / rights / production / publication authorityを技術contractへ混ぜない

## Evidence and Access

- Third-topic package:
  `production_pilots/factory_canaries/ai_monitoring_labor_001/`
- Technical receipt:
  `production_pilots/factory_canaries/ai_monitoring_labor_001/technical_validation_receipt.json`
- Three-topic bounded receipt:
  `production_pilots/factory_canaries/ai_monitoring_labor_001/three_topic_variation_receipt.json`
- Detailed supervisor report:
  `docs/verification/THIRD_REAL_TOPIC_FACTORY_VALIDATION_2026-07-26.md`
- Actual ignored run:
  `production_pilots/factory_canaries/ai_monitoring_labor_001/auto_video_runs/ai_monitoring_labor_internal_review_v1/`
- Actual GUI receipt:
  sibling `ai_monitoring_labor_internal_review_v1_gui_probe/receipt.json`
- Generic source-project path:
  `tools/Ymm4RenderAutomation/` `import-script`
- GUI smoke:
  `gui/third_real_topic_production_loop_smoke.js`

## Cross-Terminal Re-entry

- Fetch and track `origin/codex/nlmytgen-third-real-topic-factory-v1`; require
  `HEAD...@{upstream}=0/0` and tracked clean.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Restore with `uv sync --extra dev --locked` and `npm --prefix gui ci`;
  Electron 43.2.0 and actual YMM4 remain runtime prerequisites for a new render.
- Factory Contract v2 extraction is read-only over existing outputs. Do not require
  private run availability to inspect tracked schemas, and do not rerender accepted/prior cuts.
- Focused regression:
  `uv run pytest -q tests/test_third_real_topic_factory_canary.py tests/test_episode_video_pipeline.py tests/test_standard_production_loop_gui.py`
  and `node --test gui/standard_production_loop.test.js`.

## Active Boundaries

- The three-topic conclusion is bounded observation, not a universal factory claim.
- Accepted new-banknote bytes and human decision receipt remain immutable.
- REINS and AI-monitoring official captures have unresolved reuse rights.
- AI-monitoring human aesthetic review remains open.
- PR, merge, master mutation, deployment, publication, upload, release, access
  change, and public exposure are unperformed.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
