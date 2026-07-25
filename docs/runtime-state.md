# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-second-real-topic-gui-render-validated-v1
State-Revision: 2026-07-25.5
Updated: 2026-07-25 JST
Product-State: two-distinct-real-topics-through-one-gui-and-video-pipeline
Product-Gate: third-topic-variation-or-three-run-operator-repeatability
Recommended-Next: run-third-topic-with-new-input-shape-or-measure-three-consecutive-operator-runs
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-second-real-topic-factory-v1
Handoff-PR: none
Required-Base: 02e5464c0f7d0ce90a198e788a336cb201682e9b
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; ignored/private runs preserved

## Current Slice

- 第2実トピック`REINSと不動産情報流通の仕組み`を、7 cues / 4 scenes /
  Reimu 4・Marisa 3 / 2725 frames / 45.416秒のfactory canaryとして固定した。
  new-banknoteの9 cues / 3 scenes / 3・6分布 / 4415 framesとは入力形状が異なる。
- raw scriptとG-27 packetは発見・変換入力に限定した。発話事実は東日本
  レインズ3 surfaceと国土交通省1 PDFの計4 official sourcesへ結合し、
  factual cue 6件はすべてclaim/source edgeを持つ。unsupported spoken
  factual unitは0。
- tracked canary packageはcanonical script、canonical/derived CSV、source
  claim registry、support edges、transformation ledger、real-media provenance、
  episode manifest、technical receiptを持つ。source media、source YMMP、
  render run、GUI probeは`auto_video_runs/`配下のignored local evidenceである。
- YMM4 source projectは実YMM4のGUI行追加で生成した7 VoiceItemsを保持する。
  bounded Windows UI Automation driverはspeaker combo、row add、output settings、
  character-settings dialogをUIA patternだけで操作し、keyboard/mouse injectionを
  使用しない。端末の現在キャラクター設定を保持する分岐を選び、rooted Tachie
  pathだけをportable basenameへ変換する。
- Electron 43.2.0の実main/renderer/preloadでaccepted manifest読込、deep doctor、
  write-free dry-run、real YMM4 render、result readbackまで完走した。実装中の
  tracked dirty状態ではdoctorはreviewのみready、codeは`git_tracked_worktree`、
  render/regenerateはdependency chainでunavailableだったため、probe専用の狭い
  real-render bridgeを使った。通常GUIのfail-closed条件は変えていない。
- final local runはgenerated project SHA-256
  `ea4bc001068cf0f398d428072b2b94a6b3b1f4beed5ba0efb2b04f0d040e4da8`、
  review MP4 SHA-256
  `4c99feed4e487743e5243074c3eca6aad51a7b16392f7f405ce158f038cb5c75`。
  MP4はH.264/AAC、1920x1080、60fps、45.416秒、57,508,191 bytesで、
  ISO-BMFF、ffprobe、full decode、project/media bindingがpassした。
- project readbackはVoiceItem 7、ImageItem 7、speaker 4/3、2725 frames、
  exact text/order、absolute path leak 0、SVG 0。7 cue frameはすべて別SHAで、
  目視でも公式surface、字幕、話者labelを確認した。
- fresh real runを2回実施し、generated project、final MP4、local media manifest、
  cue readbackが全て同一SHAになった。既存runの無断上書き拒否とresume drift検出も
  観測した。3連続operator-runの証明はまだ行っていない。
- accepted new-banknote source、generated project、MP4、human receiptはそれぞれ
  `beee7e...aa54`、`244c05...2611`、`423553...a476`、
  `cd0b4f...f4b8`のままexactであり、既存の人間受理identityを変更していない。
- packageとrenderは`internal_factory_canary_not_human_accepted`である。visual
  readback上の既存keyword emphasisを含め、人のcreative acceptance、rights、
  production、publication、external uploadは未承認。

## Product Position

new-banknoteとREINSという異なる2トピックが、同じmanifest/preflight/project
generation/YMM4 render/media validation/Electron result契約を通過した。これにより
標準制作ループは単一デモ専用ではなく、少なくとも2つの実入力形状を処理できる。
残る主要な製品証明は、第三の入力形状へ広げるvariation proofか、同一operator
手順を3回連続で成功させるrepeatability proofである。

## Exact Next Action

既定は、現行2本を変更せず第三トピックを選び、source package、claim registry、
canonical script、derived CSV、real-media provenance、source YMMP、episode manifestを
新しいrun IDで用意する。成功条件は、現在と異なるcue/scene/speaker/time shapeで
GUI doctor → dry-run → real render → receiptがpassし、既存2本のidentityが不変であること。

operator安定性が先に必要なら、同じREINS packageを毎回新しいrun IDへ3回連続実行し、
手動介入0、project-owned process残留0、artifact SHA一致、各GUI receipt passを測る。
どちらの経路もhuman creative acceptanceとrightsを自動昇格しない。

## Evidence and Access

- Factory package:
  `production_pilots/factory_canaries/real_estate_reins_transparency_001/`
- Machine receipt:
  `production_pilots/factory_canaries/real_estate_reins_transparency_001/technical_validation_receipt.json`
- Detailed supervisor report:
  `docs/verification/SECOND_REAL_TOPIC_FACTORY_VALIDATION_2026-07-25.md`
- GUI probe:
  `gui/second_real_topic_production_loop_smoke.js`
- Pipeline:
  `src/pipeline/episode_video.py`
- UIA driver:
  `tools/Ymm4RenderAutomation/Program.cs`

## Cross-Terminal Re-entry

- Fetch and track `origin/codex/nlmytgen-second-real-topic-factory-v1`; require
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Run `uv sync --extra dev --locked`, `npm --prefix gui ci`, then
  `npm --prefix gui ls --depth=0`; require Electron 43.2.0.
- Private local source media/YMMP/MP4 are intentionally absent from Git. Restore only
  through declared local paths and verify hashes before a real run.
- Focused portable checks are
  `uv run pytest -q tests/test_second_real_topic_factory_canary.py tests/test_episode_video_pipeline.py tests/test_standard_production_loop_gui.py`,
  `npm --prefix gui run test:standard-production-loop`, and the Release .NET build.

## Active Boundaries

- The new result is technical internal-review evidence, not a human-approved cut.
- Accepted new-banknote bytes and decision receipt remain immutable.
- Official-page captures have unresolved reuse rights and remain ignored/local.
- No PR, merge, master integration, release, deployment, public upload, or access
  change is authorized by this state.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
