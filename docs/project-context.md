# Project Context — NLMYTGen

## 現在の別端末再開ハンドオフ（2026-07-19 JST・Route A dual-surface proof / human review ready）

この節だけが現在の再開地点である。下にある日付付きhandoffは判断履歴であり、
現在の指示として読まない。

- **取得先**: `origin/codex/new-banknote-route-a-concrete-visual-proof-v1`。
  remoteは`https://github.com/YuShimoji/NLMYTGen.git`に設定済みで、新規repository作成は不要。
  `git fetch --prune origin`後、同branchをcheckoutしてfast-forward限定pullする。
  exact content-authority baseは`d38075b97efabc99d1a23e8e0afafd5d44f1e2de`、presentation
  revision baseは`f611aacd0e6d238bce76df7bdc6f55b86695b842`。outcome commitは
  current remote branch tipから解決し、push後のremote parity `0/0`とclean tracked worktreeを確認する。
  source successor、master、approved content、ignored evidenceは変更しない。
- **最小読取順**: `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
  `docs/runtime-state.md` → この節 → pilotの
  `route_a_visual_proof/README_ROUTE_A_VISUAL_PROOF.md` → primary proof HTML。
  旧Web thread、元A/B/C proposal、下のhandoffを現在の指示として使わない。
- **現在の状態**: Project-State-IDは
  `new-banknote-route-a-dual-surface-visual-proof-human-review-ready-v1`、State-Revisionは
  `2026-07-19.5`。Route Aはconcrete proof生成の方向として明示的に選択済みだが、
  final visual acceptanceとimplementation authorizationはfalse。
- **H0 dual-surface proof**: S1、cue_003–cue_006、S3の六つのclean viewer frameと
  六つのannotation frameを分離した。HTMLはviewerを既定表示とし、annotation overlayは
  動画graphicではないことを明記する。approved subtitles付き9/9 cue contact sheet、
  全cueのstart/emphasis/settled storyboard、visible schematic disclaimerを保持する。
- **protected authority**: 8 approved hashes、9 cue text/order、2/4/3 scene、3/6 speaker、
  claims/edges、canonical/derived CSV、lineage、current/historical YMM4 evidence、
  five-action Operator Batch、元A/B/C proposalはsource baseとbyte-exact。
- **inspection / validation**: all SVG/HTML/JSONをparseし、local Chromeでviewer 6、
  annotation 6、contact sheet、storyboard、primary HTMLを1920×1080表示した。句読点単独、
  既知語中分割、説明活用分割、motion label省略を修復し、四行annotation字幕のbaselineも
  一回repairした。approved text、visual semantics、motion budgetは変更していない。
- **exact next action**: `route_a_visual_proof.html`と四問review sheetを見て、
  `accept`またはscene/cue-specific revisionを返す。A/B/Cは選び直さない。
- **未完了境界**: human visual acceptance、Shot/Motion、Asset/Proxy/Rights、YMM4 feasibility、
  pronunciation/rhythm/clipping、render、production/publication、PR、master integration、
  remote CI/policy、full suite。untracked supervision artifactとignored evidenceは保持する。

## 直前の別端末再開ハンドオフ（2026-07-13 JST・default branch integration・履歴）

この節はdefault branch integration時点の判断履歴であり、現在の再開指示として読まない。

- **取得先**: `origin/master`。
- **再開前確認**: `git fetch --prune origin`、`git switch master`、
  `git pull --ff-only`、`git status --short --branch`、
  `git rev-list --left-right --count "HEAD...@{u}"`の順でclean / `0 0`を確認する。
- **最小読取順**: `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
  `docs/runtime-state.md` → この節。integration再監査時だけ
  `docs/verification/EPISODE_002_DEFAULT_BRANCH_INTEGRATION_2026-07-12.md`と
  `docs/verification/episode_002_default_branch_integration_receipt.json`を追加で読む。
- **現在の状態**: `Project-State-ID`は
  `episode-002-milestone-integrated-default-branch-v1`、revisionは`2026-07-13.1`。
  Product-Stateは`episode-002-milestone-integrated-on-default-branch`、Product-Gateは
  `verified-external-editorial-input-selection`、Recommended-Nextは
  `select-or-provide-verified-editorial-source`、External-Stateは
  `public-repo-default-branch`。
- **統合provenance**: fixed subject `d8e959c54b8c8f28c31cc2b586bbdd8c79f69f97`、
  audit tail `a8b81e43616281691b73520a045dfa6ff44d2054`、integration branchを
  rewrite/deleteせず維持した。integration commit SHAはtracked contentへself-embedせず、
  Git refとAGENT_REPORTで解決する。
- **metadata rebind**: final runtime-stateへ依存するsource bundle、input readback、
  internal review manifestだけをdeterministicにrebindした。canonical script、claim semantics、
  canonical/derived CSV、source receipts、render/project/media identity、audit artifactsは不変。
- **local evidence**: MP4、proxy、`.local.ymmp`、operator result、`local_outputs`は
  ignored/untrackedのまま維持した。YMM4、Computer Use、media再生成は行っていない。
- **exact next action**: source、provenance/rights context、stable identity、cue alignmentを
  備えたverified external editorial sourceを1件選定または提供する。
- **未完了境界**: external editorial adoption、human visual/editorial acceptance、
  YMM4/profile portability、production `.ymmp`、creative polish、rights/legal/final-thumbnail
  approval、upload/publication、full-suite Integrity campaign。

## 直前の別端末再開ハンドオフ（2026-07-12 JST・operator-batch-ready・履歴）

この節はoperator-batch-ready時点の判断履歴であり、現在の再開指示として読まない。

- **取得先**: `origin/codex/episode-002-verified-local-evidence-render-v1` のbranch先端。
- **再開前確認**: `git fetch --prune origin`、同branchへのswitch、
  `git pull --ff-only`、`git status --short --branch`、
  `git rev-list --left-right --count "HEAD...@{u}"`の順でclean / `0 0`を確認する。
- **最小読取順**: `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
  `docs/runtime-state.md` → この節 →
  `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/operator_batch/README_OPERATOR_BATCH.md`。
  source/claimの再監査時だけ同pilotの`source_bundle_manifest.json`、
  `source_claim_ledger.json`、`input_validation_readback.json`を追加で読む。
- **現在の状態**: `Project-State-ID`は
  `episode-002-verified-local-evidence-operator-batch-ready-v1`、revisionは
  `2026-07-12.1`。Product-Stateは
  `episode-002-verified-local-evidence-render-operator-batch-ready`、Product-Gateは
  `manual-yymm4-render-batch`、Recommended-Nextは
  `run-one-yymm4-operator-batch`。
- **復旧結果**: target branchは期待source HEAD
  `a4eed8fe76085d7a59d483ffbafec0867b64812d`から作成。canonical historical CSVの
  delayed YMM4 alias projectionだけをapplication-generated contaminationとして一点復旧し、
  accepted SHA-256
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`
  を確認した。unrelated/uncertain user workはなかった。
- **tracked source/script成果**: 6 authorized/related sourcesをhash/schema/statusで拘束し、
  9 cuesすべてをclaim ledgerのJSON pointerへ接続した。unsupported claimは0、scene配分は
  S1=2 / S2=2 / S3=5、canonical speakerは`れいむ` 3 / `まりさ` 6。
- **CSV成果**: 新`canonical_yymm4.csv`と`derived_yymm4_import.csv`はheaderless 2列・
  9行でtext/order同一、explicit environment-specific profileによりspeaker列だけ
  `ゆっくり霊夢` 3 / `ゆっくり魔理沙` 6へ射影する。historical sample CSV/receiptsは変更していない。
- **project境界**: 旧local import baseはtracked manifestとhash一致し、1 timeline / 9 VoiceItems
  の構造は健全だが旧dry-run本文なので新CSVには再利用しない。generatorはoperatorが保存する
  new baseをexact row matchで検証し、VoiceItem objectsを不変保持してS1/S2/S3へ各1 ImageItem
  と各1 independent TextItemだけを追加する。labelsは`INTERNAL REVIEW / NOT FINAL /
  LOCAL EVIDENCE PILOT`。
- **Operator Batch**: `run_yymm4_operator_batch.ps1`がprimary surface。manual actionsは5、
  returnは最大3項目、stop/prohibited conditionsを内蔵する。PowerShell syntaxと
  operator directory起点の`-PreflightOnly`がpassedし、local_outputs未作成・YMM4未起動を確認した。
  installed YMM4はprofile観測版と異なる場合があるため、mapping dialog、character mismatch、
  update requirement、parse/open errorでは必ず停止する。
- **focused checks**: new pilot tests 7 passed、reused diagnostic/profile tests 14 passed、
  modified Python compile、source/claim/CSV/project/operator validator、deterministic regeneration、
  state sync、`git diff --check`を使用。full pytestは実行していない。
- **exact next action**: unrelated/unsaved YMM4 workを先に解消したうえで、operator batch directoryから
  `powershell -NoProfile -ExecutionPolicy Bypass -File .\run_yymm4_operator_batch.ps1`
  を一度だけ実行する。ユーザーだけがGUIを操作し、指定CSV import、new base save、generated
  project open、exact MP4 render、safe close、result collectionを一括で行う。
- **未完了境界**: actual YMM4 import/project reopen/render、MP4 validation、production `.ymmp`、
  external editorial/real-media input、creative polish、rights/legal/final-thumbnail approval、
  upload/publication、default-branch integration、full-suite Integrity campaign。

## 直前の別端末再開ハンドオフ（2026-07-11 JST・diagnostic proof observed・履歴）

この節はdiagnostic-proof-observed時点の履歴であり、現在の再開指示として読まない。

- **取得先**: `origin/codex/episode-002-ymm4-five-point-observation-v1` のbranch先端。
- **再開前確認**: `git fetch --prune origin`、同branchへのswitch、
  `git pull --ff-only`、`git status --short --branch`、
  `git rev-list --left-right --count "HEAD...@{u}"`の順でclean / `0 0`を確認する。
- **最小読取順**: `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
  `docs/runtime-state.md` → この節 → `docs/PROJECT_COCKPIT.md` →
  `docs/THREAD_REGISTRY.md`。証拠の再確認時だけ
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_csv_gate_observation_receipt_2026-07-11.json`、
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_diagnostic_placeholder_proof/diagnostic_project_manifest.json`、
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_diagnostic_placeholder_proof/diagnostic_project_readback.json`、
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_diagnostic_placeholder_proof/diagnostic_project_receipt.json`を追加で読む。
- **現在の状態**: `Project-State-ID`は
  `episode-002-ymm4-diagnostic-placeholder-proof-observed-v1`、revisionは
  `2026-07-11.2`。Product-Stateは
  `episode-002-ymm4-diagnostic-placeholder-proof-observed`、Product-Gateは
  `supervisor-next-slice-decision`。
- **CSV gate実観測**: 許可対象だったrecovered unsaved projectを破棄し、clean projectで
  derived CSVだけをYMM4 `4.53.0.9`へimportした。mapping dialogは出ず、9 VoiceItems、
  `ゆっくり霊夢` 3件 / `ゆっくり魔理沙` 6件、linked subtitle text/orderを確認した。
  timing orderは維持され、60 fps・2790 frames・46.50秒だった。receipt v2は`passed`。
- **diagnostic project実観測**: 別認可のdiagnostic-only projectを生成してYMM4で再openし、
  error/unexpected dialogなし、元の9 VoiceItemsとlinked subtitles維持、3 ImageItems、
  3 independent TextItems、明示的にnon-finalなS1 / S2 / S3 labelを確認した。
  render/exportは行わず、applicationは保存済みdiagnostic projectを開いた状態にある。
- **portable evidence**: local `episode_002_imported_base.local.ymmp`と
  `episode_002_diagnostic_placeholder.local.ymmp`はmachine-local referenceを持ち、後者は
  絶対asset referenceを含むためignoreし、commitしない。tracked対象はdeterministic generator、placeholder PNG、
  manifest、machine readback、GUI receipt、READMEである。
- **不変証拠**: canonical CSV SHA-256は
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`、
  derived CSVは`5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC`、
  historical 2026-07-10 receiptは
  `DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5`のまま。
- **検証境界**: receipt/readbackはCSV gateとdiagnostic GUI gateを分離して記録する。
  screenshotは未取得だが必須gateではない。full pytestは実行せず、focused validationと
  target state ID付きstate syncをcloseout gateにする。
- **次の入口**: supervisorが`Advance`（verified real input）または`Integrate`
  （feature/default diff review）を選ぶ。どちらもこの成功から自動開始しない。
- **閉じたままのgate**: production `.ymmp`、render/export、real-input replacement、
  rights/public/final-thumbnail approval、upload/publication、default-branch integration。

## 直前の別端末再開ハンドオフ（2026-07-11 JST・alias reobservation blocker・履歴）

この節は、Case A成功前のblocker判断を残す履歴であり、現在の指示として読まない。

- **取得先**: `origin/codex/episode-002-ymm4-five-point-observation-v1` のbranch先端。
- **再開前確認**: `git fetch --prune origin`、同branchへのswitch、
  `git pull --ff-only`、`git status --short --branch`、
  `git rev-list --left-right --count "HEAD...@{u}"`の順でclean / `0 0`を確認する。
- **最小読取順**: `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
  `docs/runtime-state.md` → この節 → `docs/PROJECT_COCKPIT.md` →
  `docs/THREAD_REGISTRY.md`。GUI再観測時だけ
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/manual_ymm4_observation_readback.md`
  を追加で読む。
- **現在の状態**: `Project-State-ID`は
  `episode-002-ymm4-speaker-alias-ready-for-reobservation-v1`。
  Product-Stateは`episode-002-ymm4-speaker-alias-ready-for-reobservation`、
  Product-Gateは`bounded-yymm4-alias-reobservation`。
- **実装済み**: canonical speaker identityは`れいむ` / `まりさ`のまま、
  explicit profile `ymm4_4_53_0_9_yukkuri_characters_ja_v1`で
  `ゆっくり霊夢` / `ゆっくり魔理沙`へstrictに射影する。generic `build-csv`の
  source-label mapping既定動作は変更していない。
- **derived CSV**:
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/derived_yymm4_import.csv`。
  9行、text/order同一、speaker列だけ変換。SHA-256は
  `5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC`。
  canonical CSVは元のSHA-256
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`
  のまま。
- **責務契約**: CSV import gateは`VoiceItem + linked subtitle`だけを期待する。
  `ImageItem + independent TextItem placeholders`は別のdiagnostic projectで、
  `not_authorized / not_attempted`。CSV importに出ないことはfailureではない。
- **旧証拠**: `ymm4_observation_receipt_2026-07-10.json`はbyte不変で、
  SHA-256 `DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5`。
  旧mixed contract下のhistorical `partial` evidenceとして残す。
- **GUI blocker**: YMM4 `4.53.0.9`を開いたところ、以前の9-item / 2790-frame
  projectがunsaved `無題*`として復元された。clean project開始には既存stateの
  discardまたは退避が必要なため、無断破棄せず停止した。derived CSV import、new
  project、save、render、exportは未実施で、YMM4はstate保全のため開いたまま。
- **次の入口**: まずuserが既存unsaved projectをsave elsewhereするかdiscardするかを
  決める。その後だけclean untitled projectへderived CSVを一度importし、mapping dialog、
  9 VoiceItems、character counts、linked text/order、timing order、CSV responsibility
  boundaryを記録して、新しい観測projectを保存せず閉じる。
- **禁止された自動遷移**: CSV gate成功からdiagnostic `.ymmp`、real input、render、
  publication、default-branch integrationへ自動で進めない。
- **詳細証跡**:
  `docs/verification/NEWSROOM_EPISODE_002_YMM4_ALIAS_CSV_CONTRACT_2026-07-11.md`。

## その前の別端末再開ハンドオフ（2026-07-10 JST・履歴）

この節は判断履歴であり、現在の指示として読まない。下部に残る旧端末の絶対pathは
当時の履歴であり、現在の実行pathとして再利用しない。

- **取得先**: `origin/codex/episode-002-ymm4-five-point-observation-v1` のbranch先端。
- **再開前確認**: `git fetch --prune origin`、`git switch
  codex/episode-002-ymm4-five-point-observation-v1`、`git pull --ff-only origin
  codex/episode-002-ymm4-five-point-observation-v1` の順に実行し、`git status
  --short --branch` と `git rev-list --left-right --count "HEAD...@{u}"` が
  clean / `0 0` であることを確認する。
- **最小読取順**: `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` →
  `docs/runtime-state.md` → この節 → `docs/PROJECT_COCKPIT.md` →
  `docs/THREAD_REGISTRY.md`。YMM4観測を扱うときだけ
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/manual_ymm4_observation_readback.md`
  を追加で開く。
- **現在の状態**: `Project-State-ID` は
  `supervisor-only-control-boundary-restored-v1`、revisionは`2026-07-10.5`。
  Product-Stateは`episode-002-ymm4-observation-completed-with-adapter-gap`、
  Product-Gateは`evidence-backed-adapter-correction`。
- **実観測の事実**: tracked 9-row CSVをYMM4 `4.53.0.9`へ読み込み、9/9 VoiceItems、
  csv_row_1 -> csv_row_9、cue map対応のS1 -> S2 -> S3、linked subtitle text、
  timing orderを確認した。YMM4はprojectを保存せず閉じた。
- **五点結果**: cue順=OK、VoiceItem件数/欠落/重複/順序=OK、字幕本文=手動話者mapping後OK、
  timing順=OK（60fps・2790 frames・46.50秒へ再計算）、placeholder境界=NG。
  CSV importではVoiceItem/subtitleのみ生成され、期待されたImageItem/TextItem placeholder
  scene laneは現れなかった。`まりさ`は誤った初期mappingから`ゆっくり魔理沙`へ手動補正した。
- **証跡**: input receiptは
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_receipt_2026-07-10.json`、
  machine readbackは同packageの`ymm4_observation_readback_pack/observation_readback.json`。
  generator/CLIは`--observation-receipt`を明示したactual modeと、未指定時の従来operator-only
  modeを両方保持する。
- **次の入口**: 推奨は`Correct`。automatic speaker bindingとImageItem/TextItem placeholder
  laneの二つだけを実測証拠に基づいて補正し、同じbounded observationを再実行する。
  `Advance`はverified source/transcript受領後、`Integrate`はfeature/default差分再計測後。
- **確認済み**: observation/import/local-edit/real-inputのfocused regressionは24 passed。
  full pytestは既知のfixture side effectを持つため実行していない。render/export、production
  `.ymmp`、実素材置換、rights/public/final thumbnail/uploadは未実施のまま閉じている。

## PROJECT CONTEXT
- Episode 002 actual YMM4 five-point observation (2026-07-10 JST):
  `regenerated_draft_yymm4.csv` was imported in YMM4 `4.53.0.9` and produced
  nine ordered VoiceItems with matching linked subtitle text after manual
  character mapping. Cue order remained `csv_row_1` through `csv_row_9`, mapped
  to S1 -> S2 -> S3. YMM4 recalculated provisional four-second durations to
  2790 frames / 46.50 seconds at 60 fps while preserving order. The result is
  `partial`, not a production pass: expected ImageItem/TextItem placeholder
  scene lanes were absent, and `れいむ`/`まりさ` required manual binding (with
  `まりさ` initially defaulting to the wrong character). The application was
  closed without saving; no render/export, production `.ymmp`, real-input
  replacement, rights/public/final-thumbnail approval, or upload occurred.
  The tracked actual-observation receipt drives regenerated JSON/HTML/Markdown
  readback, while omitting the receipt preserves the prior operator-only mode.
  The next product gate is evidence-backed correction of those two adapter
  gaps, followed by the same bounded observation.
- Control-boundary correction (2026-07-10 JST):
  `supervisor-only-control-boundary-restored-v1` removes the repository-side
  Supervisor Prompt source, generic Worker authority, response-quality lint,
  and Stop-hook state gate introduced by `workflow-velocity-and-current-state-v1`.
  A self-contained prompt supplied through the Web supervisor remains the
  session execution authority. The repository retains only product-specific
  review guidance plus compact runtime/cockpit navigation and an explicitly
  invoked state-alignment checker. `docs/PROJECT_COCKPIT.md`,
  `docs/THREAD_REGISTRY.md`, and `docs/PROJECT_PIPELINE.mmd` persist current
  routing without governing Worker behavior. The repository is public; the
  tracked Markdown cockpit is therefore readable without GitHub Pages, while
  Pages remains an optional publication choice. The product frontier returns
  to the Episode 002 five-point YMM4 observation.
- Superseded workflow decision (2026-07-10 JST; historical record only):
  `workflow-velocity-and-current-state-v1` changes the supervisor-to-developer
  default from prompt-per-step to one outcome-sized slice. Reversible repo-local
  implementation, related fixes, proportional validation, current-state sync,
  and Git follow-through continue without a checkpoint. A Direction Check is
  used only for a new high-cost visible direction; destructive work, dependency
  addition, DB/auth/API contract changes, external publication/rights/payment,
  specification conflict, and an approved-direction change remain hard stops.
  Stop-hook content quality findings are advisory by default and strict only
  when `NLMYTGEN_GUARDRAILS_STRICT` is explicitly enabled. Current state is no
  longer append-only: `docs/runtime-state.md` is a <=160-line capsule and
  `docs/PROJECT_COCKPIT.md` is its GitHub-readable mirror, coupled by
  `Project-State-ID` and `scripts/check_project_state_sync.py`. The historical
  common-foundation HTML/JSON dashboard is explicitly a 2026-06-22 snapshot.
  GitHub Pages/Wiki publication remains a separate decision because repository
  visibility, sanitization, and branch-promotion policy are not yet confirmed.
- Current handoff (2026-07-09 JST):
  `episode-002-ymm4-observation-readback-v1` is complete on branch
  `codex/episode-002-ymm4-observation-readback-v1`; the artifact/package
  commit before this docs-only remote seal is `506ec9e`, the branch was
  pushed to origin, and upstream parity was `0 0` with a clean worktree. The
  active artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/`.
  Primary human review is `observation_preview.html`; operator readback sheet
  is `manual_ymm4_observation_readback.md`; primary machine readback is
  `observation_readback.json`; detailed restart handoff is
  `docs/verification/NEWSROOM_EPISODE_002_YMM4_OBSERVATION_READBACK_2026-07-09.md`.
  Current open command:
  `Invoke-Item -LiteralPath "C:\Users\PLANNER007\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\ymm4_observation_readback_pack\observation_preview.html"`.
  This slice resolves the queued A lane honestly: YMM4 is installed locally
  (`C:\Users\PLANNER007\Downloads\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe`)
  and the import CSV candidates exist, but actual GUI import observation was
  not attempted because the worker has no safe manual/GUI visual readback
  channel for importing and inspecting the YMM4 result. The package is
  therefore an operator-instruction hold, not a pass claim:
  `status=blocked`, `validation_status=passed`,
  `observation_mode=operator_instruction_only`,
  `actual_ymm4_import_attempted=false`, `actual_ymm4_imported=false`,
  `cue_count_expected=9`, `cue_count_observed=0`, and voice/subtitle/timing/
  placeholder observations remain `not_observed`. It preserves closed gates:
  no render/export, no production `.ymmp` write, no real input replacement, no
  rights/public approval, no final thumbnail approval, no upload, no live
  fetch, and no external media download. The Japanese-first HTML uses a
  pipeline runway plus observation/status tables rather than a primary
  card-grid dashboard. Regeneration command:
  `python -m src.cli.main build-ymm4-observation-readback-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_ymm4_observation_readback_pack_v1`.
  Targeted validation passed with
  `uv run pytest tests/test_ymm4_observation_readback_pack.py tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_real_input_replacement_readiness_pack.py -q`
  -> 16 passed; full pytest was not run by repo policy and slice scope.
  Another terminal should fetch, switch to
  `codex/episode-002-ymm4-observation-readback-v1`, run
  `git pull --ff-only origin codex/episode-002-ymm4-observation-readback-v1`,
  confirm `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then
  read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry, the detailed handoff file, and the package
  `observation_readback.json`. Next meaningful move is for a human/operator to
  open YMM4, import
  `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`,
  and return the five observations listed in
  `manual_ymm4_observation_readback.md`. Do not resume render/export,
  production `.ymmp` write, real input replacement, rights/legal/public-ready
  acceptance, final thumbnail approval, YouTube upload/publication, live
  fetch/scraping, external media download, OAuth/API/payment work, ClipPipeGen
  edits, destructive git, or full pytest loops from this handoff.

- Current handoff (2026-07-09 JST):
  `episode-002-verified-real-input-prep-v1` is complete on branch
  `codex/episode-002-verified-real-input-prep-v1`. The active artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/real_input_replacement_readiness_pack/`.
  Primary human review is `real_input_replacement_preview.html`; operator
  contract is `real_input_replacement_contract.md`; primary machine readback
  is `validation_readback.json`; placeholder input folder note is
  `input_dropzone/README.md`; detailed restart handoff is
  `docs/verification/NEWSROOM_EPISODE_002_VERIFIED_REAL_INPUT_PREP_HANDOFF_2026-07-09.md`.
  Current open command:
  `Invoke-Item -LiteralPath "C:\Users\PLANNER007\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\real_input_replacement_readiness_pack\real_input_replacement_preview.html"`.
  This slice advances the verified real-input gate without replacing content:
  it uses the accepted YMM4 import-ready pack and prior real-input intake
  contract as read-only sources, then states the exact local material needed
  before sample/diagnostic Episode 002 content can be replaced. Required inputs
  are source audio/video/document path, transcript path or transcript
  generation receipt, provenance/rights note, hash or stable identity, and
  Episode 002 cue-map alignment. The operator-facing HTML is Japanese-first and
  built as a pipeline runway plus matrix/status tables, not a primary card-grid
  dashboard. Validation readback reports `status=passed`,
  `required_local_input_count=5`, `candidate_input_count=0`,
  `actual_real_input_replaced=false`, `live_fetch_performed=false`,
  `external_media_downloaded=false`, `actual_ymm4_imported=false`,
  `rendered_video_created=false`, `ymmp_file_created=false`,
  `rights_approved=false`, `public_ready=false`, no external dependencies, no
  forbidden production/public/YMM4 true claims, and no temporary-copy markers.
  Generated files are JSON/HTML/MD only; no media/render/`.ymmp` file was
  created. Regeneration command:
  `python -m src.cli.main build-real-input-replacement-readiness-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_verified_real_input_replacement_readiness_pack_v1`.
  Targeted validation passed with
  `uv run pytest tests/test_real_input_replacement_readiness_pack.py tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q`
  -> 24 passed. Full pytest was not run by repo policy and slice scope.
  Another terminal should fetch, switch to
  `codex/episode-002-verified-real-input-prep-v1`, run
  `git pull --ff-only origin codex/episode-002-verified-real-input-prep-v1`,
  confirm `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then
  read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry, the detailed handoff file, and the package
  `validation_readback.json`. Next meaningful move is to provide verified
  local source/transcript material and build a validated local input receipt;
  YMM4 observation remains second_launch. Do not resume actual real input
  replacement, actual YMM4 GUI import/render/export, production `.ymmp` write,
  rights/legal/public-ready acceptance, final thumbnail approval, YouTube
  upload/publication, live fetch/scraping, external media download,
  OAuth/API/payment work, ClipPipeGen edits, destructive git, or full pytest
  loops from this handoff.

- Current handoff (2026-07-09 JST):
  `episode-002-ymm4-import-ready-ja-review-v1` is complete on branch
  `codex/episode-002-ymm4-import-ready-ja-review-v1`; the artifact completion
  commit before this docs-only handoff note is `1cc52b6`. The active artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/`.
  Primary human review is `ymm4_import_ready_preview.html`, now Japanese-first;
  manual future operator sheet is `manual_ymm4_import_observation_sheet.md`,
  now Episode 002-specific and Japanese-first; primary machine readback is
  `validation_readback.json`; detailed remote restart handoff is
  `docs/verification/NEWSROOM_EPISODE_002_YMM4_IMPORT_READY_JA_REVIEW_REMOTE_HANDOFF_2026-07-09.md`.
  Current open command:
  `Invoke-Item -LiteralPath "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\ymm4_import_ready_pack\ymm4_import_ready_preview.html"`.
  This slice localized the review surface without changing JSON identity or
  machine contracts: schema keys, artifact ID, cue IDs, state enum values, and
  gate flags remain stable while Japanese display labels explain cue order,
  provisional timing, VoiceItem/subtitle, visual/overlay,
  placeholder/diagnostic boundary, import risk, and false gate meanings. The
  manual sheet is a temporary Episode 002 checkpoint with purpose, scope,
  out-of-scope boundaries, the next expected artifact
  `YMM4 observation readback`, and 5 natural-language checks. The package still
  records 7 queue operations, 3 scenes, 9 cues, 5 manual observation checks,
  `ymm4_import_state=ready_for_manual_import_observation`, and
  `ymmp_file_created=false`. Actual YMM4 import, render/export, production
  `.ymmp` write, real input replacement, rights approval, public readiness,
  final thumbnail approval, live fetch, external media download, OAuth/API use,
  and YouTube upload remain closed. Validation readback reports `status=passed`,
  all generated JSON parses, no external dependencies, no forbidden
  production/public/YMM4 true claims, and no temporary-copy markers. Generated
  files are JSON/HTML/MD only; no media/render/`.ymmp` file was created.
  Another terminal should fetch, switch to
  `codex/episode-002-ymm4-import-ready-ja-review-v1`, run
  `git pull --ff-only origin codex/episode-002-ymm4-import-ready-ja-review-v1`,
  confirm `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then
  read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry, the detailed remote handoff file, and the package
  `validation_readback.json`. Regeneration command:
  `python -m src.cli.main build-ymm4-import-ready-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id nlm-e002-ymm4-import-ready-edit-package-v1-001`.
  Targeted validation passed with
  `uv run pytest tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q`
  -> 20 passed; `git diff --check` and `git diff --cached --check` passed for
  the artifact commit. Full pytest was not run by policy. Next meaningful move
  is a future explicit YMM4 import observation readback using this Japanese
  surface, or a verified real-input replacement gate before changing placeholder
  content. Do not resume actual YMM4 GUI import/render/export, production
  `.ymmp` write, real input replacement without verified input,
  rights/legal/public-ready acceptance, final thumbnail approval, YouTube
  upload/publication, live fetch/scraping, external media download,
  OAuth/API keys/payment, destructive git, ClipPipeGen work, or full pytest
  loops from this handoff.

- Current handoff (2026-07-08 JST):
  `episode-002-ymm4-import-ready-edit-package-v1` is complete on branch
  `codex/episode-002-ymm4-import-ready-edit-package-v1`; the artifact
  completion commit before this docs-only handoff note is `a39ce95`. The
  active artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/`.
  Primary human review is `ymm4_import_ready_preview.html`; manual future
  operator sheet is `manual_ymm4_import_observation_sheet.md`; primary machine
  readback is `validation_readback.json`; detailed remote restart handoff is
  `docs/verification/NEWSROOM_EPISODE_002_YMM4_IMPORT_READY_REMOTE_HANDOFF_2026-07-08.md`.
  Current open command:
  `Invoke-Item -LiteralPath "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\ymm4_import_ready_pack\ymm4_import_ready_preview.html"`.
  The package converts the local edit-slice queue into YMM4-facing
  import/observation concepts without performing actual YMM4 work. It records
  7 queue operations, 3 scenes, 9 cues, 5 manual observation checks,
  `ymm4_import_state=ready_for_manual_import_observation`, and an adapter plan
  with `ymmp_file_created=false`. Cue map rows include provisional timing,
  voice/subtitle action, visual placeholder action, citation/thumbnail
  placeholder action, expected VoiceItem/subtitle plus ImageItem/TextItem
  lanes, required asset state, import risk, and a manual observation question.
  It keeps actual YMM4 import, render, production `.ymmp` write, real input
  replacement, rights approval, public readiness, final thumbnail approval,
  live fetch, external media download, OAuth/API use, and YouTube upload
  closed. Validation readback reports `status=passed`, all generated JSON
  parses, no external dependencies, no forbidden production/public/YMM4 true
  claims, and no temporary-copy markers. Generated files are JSON/HTML/MD only;
  no media/render/`.ymmp` file was created. Another terminal should fetch,
  switch to `codex/episode-002-ymm4-import-ready-edit-package-v1`, run
  `git pull --ff-only origin codex/episode-002-ymm4-import-ready-edit-package-v1`,
  confirm `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then
  read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry, the detailed remote handoff file, and the package
  `validation_readback.json`. Regeneration command:
  `python -m src.cli.main build-ymm4-import-ready-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id nlm-e002-ymm4-import-ready-edit-package-v1-001`.
  Targeted validation passed with
  `uv run pytest tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q`
  -> 20 passed; `git diff --check` and `git diff --cached --check` passed for
  the artifact commit. Full pytest was not run by policy. Next meaningful move
  is a future explicit YMM4 import observation using the manual sheet, or a
  verified real-input replacement gate before changing placeholder content. Do
  not resume actual YMM4 GUI import/render/export, production `.ymmp` write,
  real input replacement without verified input, rights/legal/public-ready
  acceptance, final thumbnail approval, YouTube upload/publication, live
  fetch/scraping, external media download, OAuth/API keys/payment, destructive
  git, ClipPipeGen work, or full pytest loops from this handoff.

- Current handoff (2026-07-08 JST):
  `episode-002-local-edit-slice-execution-v1` is complete on branch
  `codex/episode-002-local-edit-slice-execution-v1`; the artifact completion
  commit before this docs-only handoff note is `697cb7e`. The active artifact
  is
  `production_pilots/yukkuri_newsroom_content_spine_002/local_edit_slice_execution_pack/`.
  Primary human review is `local_edit_execution_preview.html`; primary machine
  readback is `validation_readback.json`; detailed remote restart handoff is
  `docs/verification/NEWSROOM_EPISODE_002_LOCAL_EDIT_SLICE_EXECUTION_REMOTE_HANDOFF_2026-07-08.md`.
  Current open command:
  `Invoke-Item -LiteralPath "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\local_edit_slice_execution_pack\local_edit_execution_preview.html"`.
  The package turns the completed Editing Operations readiness contracts into a
  local-only execution queue: 7 queued operations across 3 scenes, with 3
  blocked gate operations recorded but not queued. Queued operations are
  provisional scene duration, voice/subtitle alignment, subtitle wrap intent,
  visual scene template assignment, citation overlay reservation, thumbnail
  motif transfer, and package validation. It keeps actual YMM4 import, render,
  production `.ymmp` write, real input replacement, rights acceptance, public
  readiness, final thumbnail approval, live fetch, external media download,
  OAuth/API use, and YouTube upload closed. Validation readback reports
  `status=passed`, no external dependencies, no forbidden
  production/public/YMM4 true claims, no temporary-copy markers, protected
  context touch lists empty, and `blocked_gate_operations_not_queued=true`.
  Another terminal should fetch, switch to
  `codex/episode-002-local-edit-slice-execution-v1`, run
  `git pull --ff-only origin codex/episode-002-local-edit-slice-execution-v1`,
  confirm `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then
  read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry, the detailed remote handoff file, and the package
  `validation_readback.json`. Regeneration command:
  `python -m src.cli.main build-local-edit-slice-execution-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_local_edit_slice_execution_pack_v1`.
  Targeted validation passed with
  `uv run pytest tests/test_local_edit_slice_execution_pack.py tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q`
  -> 16 passed; `git diff --check` and `git diff --cached --check` passed for
  the artifact commit. Full pytest was not run by policy. Next meaningful move
  is to use the queue for one future local draft edit artifact, or explicitly
  open real-input/YMM4 gates before replacement or observation work. Do not
  resume YMM4 GUI launch/import/render, production `.ymmp`, real input
  replacement without verified input, rights/legal/public-ready acceptance,
  final thumbnail approval, YouTube upload/publication, live fetch/scraping,
  external media download, OAuth/API keys/payment, destructive git, cross-repo
  edits, or full pytest loops from this handoff.

- Current handoff (2026-07-08 JST):
  `episode-002-editing-operations-readiness-v1` is complete on branch
  `codex/episode-002-editing-operations-readiness-v1`; the artifact
  completion commit before this docs-only handoff note is `b5ac43d`. The
  branch was pushed to
  `origin/codex/episode-002-editing-operations-readiness-v1`, the worktree was
  clean before this docs-only handoff, and `HEAD...@{u}` was `0 0`. The active
  artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/editing_operations_readiness_pack/`.
  Primary human review is `editing_operations_preview.html`; primary machine
  readback is `validation_readback.json`; detailed remote restart handoff is
  `docs/verification/NEWSROOM_EPISODE_002_EDITING_OPERATIONS_REMOTE_HANDOFF_2026-07-08.md`.
  Current open command:
  `Invoke-Item -LiteralPath "C:\Users\PLANNER007\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\editing_operations_readiness_pack\editing_operations_preview.html"`.
  The package turns Episode 002 output-template and real-input-intake context
  into concrete editing operation contracts across timing, voice/subtitle,
  visual scene slots, citation overlays, thumbnail transfer, and future manual
  YMM4 observation readback. It records 10 operations, covers 3 scenes, maps 9
  voice/subtitle rows and 3 visual slot rows, and keeps actual YMM4 import,
  render, real input replacement, public readiness, rights acceptance, and
  final thumbnail approval closed. Operation gaps are grouped as 7 buildable
  locally, 4 blocked by real input, 4 blocked by explicit YMM4 gate, and 3
  blocked by public/rights gate. Validation readback reports `status=passed`,
  no external dependencies, no forbidden production/public/YMM4 true claims,
  no GUI lane files touched, no output-template files touched, and no
  input-intake files touched. Another terminal should fetch, switch to
  `codex/episode-002-editing-operations-readiness-v1`, run
  `git pull --ff-only origin codex/episode-002-editing-operations-readiness-v1`,
  confirm `git rev-list --left-right --count HEAD...'@{u}'` is `0 0`, then
  read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry, the detailed remote handoff file, and the package
  `validation_readback.json`. Regeneration command:
  `python -m src.cli.main build-editing-operations-readiness-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_editing_operations_readiness_pack_v1`.
  Targeted validation passed with
  `uv run pytest tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q`
  -> 12 passed; `git diff --check` and `git diff --cached --check` passed
  before the artifact commit. Full pytest was not run by policy. Next
  meaningful move is to review the operation matrix, then choose verified real
  local source/transcript, explicit YMM4 observation readback, citation or
  thumbnail gate audit, or a local edit-slice execution. Do not resume YMM4
  GUI launch/import/render, production `.ymmp`, real input replacement without
  verified input, rights/legal/public-ready acceptance, final thumbnail
  approval, YouTube upload/publication, live fetch/scraping, external media
  download, OAuth/API keys/payment, destructive git, cross-repo edits, or full
  pytest loops from this handoff.

- Current handoff (2026-07-08 JST):
  `episode-002-output-video-layer-proof-v1` is complete on branch
  `codex/episode-002-output-video-layer-proof-v1`; the artifact completion
  commit before this docs-only handoff note is `ed7bc04`. The branch was
  fetched from `origin`, the worktree was clean before this handoff note, and
  `HEAD...@{u}` was `0 0`. The active artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/output_video_layer_proof/`.
  Primary human review is `episode_002_storyboard_preview.html`; primary
  machine readback is `validation_readback.json`; the timeline is
  `scene_timeline.json`; the YMM4 boundary readback is
  `yymm4_handoff_readiness.json`; output/editing gaps are
  `output_gap_ledger.json` and `missing_editing_features.md`; source/context
  provenance is `source_artifact_index.json`. Current open command:
  `Invoke-Item -LiteralPath "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\output_video_layer_proof\episode_002_storyboard_preview.html"`.
  The package turns existing dry-run Episode 002 artifacts into a local static
  storyboard/timeline proof for the parallel Output / Video Layer lane. It
  records 3 scenes, uses
  `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`,
  keeps real input blocked, keeps YMM4 not imported, and names 13 remaining
  output/editing features: 5 buildable locally, 2 blocked by real input, 3 by
  the YMM4 gate, and 3 by public-rights gates. Validation readback reports
  `status=passed`, all required package files present, no external
  dependencies, no forbidden production/public/YMM4 true claims, no GUI lane
  files touched, and no shared docs touched by the artifact generation step.
  This handoff note is the explicit exception that records the context in the
  shared project docs for cross-terminal restart. Another terminal should
  fetch, switch to `codex/episode-002-output-video-layer-proof-v1`, run
  `git pull --ff-only origin codex/episode-002-output-video-layer-proof-v1`,
  confirm `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then
  read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry, and
  `production_pilots/yukkuri_newsroom_content_spine_002/output_video_layer_proof/validation_readback.json`.
  Regeneration command:
  `python -m src.cli.main build-output-video-layer-proof --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_output_video_layer_proof_v1`.
  Targeted validation passed with
  `uv run pytest tests/test_output_video_layer_proof.py tests/test_japanese_graphic_review_console.py -q`
  -> 8 passed; `git diff --check` and `git diff --cached --check` passed
  before the artifact commit. Full pytest was not run by policy. Next
  meaningful move is to review the storyboard and gap ledger, then choose
  verified local source/transcript input, more local output-template proof, or
  an explicit YMM4 observation gate. Do not resume GUI/i18n lane modification,
  production video/render claims, YMM4 GUI launch/import/render, production
  `.ymmp`, final thumbnail approval, real transcript/source replacement
  without verified input, live fetch/scraping, external media download,
  OAuth/API keys/payment, rights/legal/public-ready acceptance, YouTube
  upload/publication, destructive git, cross-repo edits, or repeated
  full-suite pytest loops.

- Current handoff (2026-07-07 JST):
  `episode-002-split-view-decision-evidence-prototype-v1` is complete on
  branch `codex/episode-002-surface-alignment-repair-and-reviewer-packet-v1`;
  the artifact completion commit before this docs-only handoff note is
  `e86cd8f`. The branch was fetched from `origin`, the worktree was clean
  before this handoff note, and `HEAD...@{u}` was `0 0`. The active artifact
  is
  `production_pilots/yukkuri_newsroom_content_spine_002/split_view_decision_evidence_prototype/`.
  Primary human review is `split_view_decision_evidence.html`; primary
  machine readback is `validation_readback.json`; recommendation readback is
  `recommendation_readback.json`; evidence pane readback is
  `evidence_pane_readback.json`; source records are secondary in
  `source_record_index.json`; layout readback is `layout_metrics.json`.
  Current host open command:
  `start "" "C:\Users\PLANNER007\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\split_view_decision_evidence_prototype\split_view_decision_evidence.html"`.
  The split-view prototype materializes the selected
  `candidate_a_split_view_decision_evidence_pane` direction from
  `review_layout_second_pass/`: left decision rail for user situation,
  active decision, current recommendation, and next product-enabling action;
  right evidence pane for evidence preview, source readiness, rationale,
  bounded gate context, and raw source records. Evidence is visible without a
  drawer-only mechanism. Internal artifact IDs and raw paths are absent from
  the left-pane primary copy. The current checked recommendation is
  `prepare_verified_local_source_transcript`; `hold_review_later` is only
  `safe_fallback_not_progress`; YMM4 import observation is an explicit-gate
  alternative only. Another terminal should fetch, switch to
  `codex/episode-002-surface-alignment-repair-and-reviewer-packet-v1`, confirm
  `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then read
  `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry,
  `production_pilots/yukkuri_newsroom_content_spine_002/split_view_decision_evidence_prototype/validation_readback.json`,
  and
  `production_pilots/yukkuri_newsroom_content_spine_002/split_view_decision_evidence_prototype/recommendation_readback.json`.
  Regeneration command:
  `python -m src.cli.main build-split-view-decision-evidence-prototype --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_split_view_decision_evidence_prototype_v1`.
  Targeted validation passed with
  `uv run pytest tests/test_split_view_decision_evidence_prototype.py tests/test_review_layout_second_pass.py tests/test_guided_decision_flow_prototype.py -q`
  -> 12 passed; generated readback reports
  `evidence_visible_without_drawer=true`,
  `source_records_secondary=true`, `gate_text_bounded=true`,
  `internal_artifact_ids_in_left_primary_copy=[]`, and
  `card_grid_as_primary_structure=false`; `git diff --check` and
  `git diff --cached --check` passed before commit. Full pytest was not run by
  policy. Next meaningful product slice after human visual acceptance is
  preparing or providing verified local source/transcript material so Episode
  002 can leave sample-only review. Do not resume production UI promotion,
  YMM4 GUI launch/import/render, production `.ymmp`, final thumbnail approval,
  real transcript/source replacement before verified input exists, live
  fetch/scraping, external media download, OAuth/API keys/payment,
  rights/legal/public-ready acceptance, YouTube upload, destructive git,
  cross-repo edits, or repeated full pytest loops.

- Current handoff (2026-07-07 JST):
  `episode-002-review-layout-research-and-pattern-benchmark-v1` is complete on
  branch `codex/episode-002-surface-alignment-repair-and-reviewer-packet-v1`;
  the artifact completion commit before this docs-only handoff note is
  `7d9427a`. The branch was fetched from `origin`, the worktree was clean
  before this handoff note, and `HEAD...@{u}` was `0 0`. The active
  artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/review_layout_research/`.
  Primary human review is `layout_research_report.md`; low-fidelity dark-mode
  wireframes are `candidate_wireframes.html`; primary machine readback is
  `validation_readback.json`; final recommendation is
  `final_layout_recommendation.md`; decision matrix is
  `layout_decision_matrix.json`. Current host open command:
  `start "" "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\review_layout_research\candidate_wireframes.html"`.
  The compact cockpit at
  `production_pilots/yukkuri_newsroom_content_spine_002/review_cockpit_compact/review_cockpit.html`
  is now a weak-pass evaluated prototype, not the next UI direction. The
  research packet compares dashboard/status board, start page/service entry,
  task list/checklist, command center/cockpit, wizard/step-by-step decision
  flow, and card-board/kanban-like review patterns, then selects exactly one
  next implementation target: `candidate_b_guided_decision_flow`. Another
  terminal should fetch, switch to
  `codex/episode-002-surface-alignment-repair-and-reviewer-packet-v1`, confirm
  `git rev-list --left-right --count "HEAD...@{u}"` is `0 0`, then read
  `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, this
  handoff entry,
  `production_pilots/yukkuri_newsroom_content_spine_002/review_layout_research/validation_readback.json`,
  and
  `production_pilots/yukkuri_newsroom_content_spine_002/review_layout_research/final_layout_recommendation.md`.
  Regeneration command:
  `python -m src.cli.main build-review-layout-research --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_review_layout_research_and_pattern_benchmark_v1`.
  Targeted validation passed with
  `uv run pytest tests\test_review_layout_research.py tests\test_review_cockpit_compact.py -q`
  -> 8 passed; generated JSON loaded; candidate wireframes had no external
  CSS/JS/font/image/media dependencies; forbidden production/public/YMM4 true
  claims were absent; `git diff --check` and `git diff --cached --check`
  passed before commit. Full pytest was not run by policy. Next meaningful
  product slice is a guided start-to-decision prototype using Candidate B.
  Real input replacement and actual YMM4 import observation remain later
  human/product decisions after the better review surface exists. Do not
  resume production review-cockpit replacement from this handoff, YMM4
  GUI launch/import/render, production `.ymmp`, final thumbnail approval,
  real transcript rerun without verified input, live fetch/scraping, external
  media download, OAuth/API keys/payment, rights/legal/public-ready acceptance,
  YouTube upload, destructive git, cross-repo edits, broad fixture
  regeneration, or repeated full pytest loops.

- Current handoff (2026-07-06 JST):
  `episode-002-surface-alignment-repair-and-reviewer-packet-v1` is complete on
  branch `codex/episode-002-surface-alignment-repair-and-reviewer-packet-v1`
  at commit `2d602de` before the handoff-sync note. The active artifact is
  `production_pilots/yukkuri_newsroom_content_spine_002/surface_alignment_review_packet/`.
  Primary human review is `aligned_review_story.md`; primary machine readback
  is `validation_readback.json`; primary repair summary is
  `alignment_repair_summary.json`; drift detail is
  `remaining_mismatch_ledger.json`. The packet consumes the accepted
  `surface_alignment_pack/`, leaves GUI/import/thumbnail source surfaces and
  creative assets unchanged, and classifies the prior 8 drift rows as 5
  `resolved` plus 3 `accepted_nonblocking`, with still-open reviewer drift 0.
  GUI panel, YMM4 import preview, and thumbnail proof remain local/offline
  review surfaces only. Another terminal should fetch, switch to
  `codex/episode-002-surface-alignment-repair-and-reviewer-packet-v1`, confirm
  upstream parity, then read `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`,
  `docs/runtime-state.md`, this handoff entry, and
  `production_pilots/yukkuri_newsroom_content_spine_002/surface_alignment_review_packet/validation_readback.json`.
  Regeneration command:
  `python -m src.cli.main build-surface-reviewer-packet --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_surface_alignment_repair_and_reviewer_packet_v1`.
  Targeted validation passed with
  `uv run pytest tests\test_surface_alignment_reviewer_packet.py tests\test_surface_alignment_pack.py tests\test_gui_dashboard_panel.py tests\test_yymm4_import_preview_pack.py tests\test_thumbnail_visual_proof_pack.py -q`
  -> 20 passed; packet JSON/static scans and diff hygiene passed; full pytest
  was not run by policy. Next recommended product slice is verified local real
  topic/source/transcript replacement; actual YMM4 import observation without
  render/public claims is an alternate later lane only if explicitly selected.
  Do not resume YMM4 GUI launch/import/render, production `.ymmp`, final
  thumbnail approval, real transcript rerun without verified input, live
  fetch/scraping, external media download, OAuth/API keys/payment,
  rights/legal/public-ready acceptance, YouTube upload, destructive git,
  cross-repo edits, broad fixture regeneration, or repeated full pytest loops.

- Current handoff (2026-07-02 JST):
  NLMYTGen is synced on `master` for the episode-production restart lane. The
  active artifact is
  `production_pilots/notebooklm_ymm4_episode_package_001/`, an internal package
  for preparing the user's own video posting candidate from a NotebookLM-style
  transcript. The package is intake-ready, not real-episode generated:
  `real_input/episode_001_transcript.txt` is absent, and current generated
  outputs remain dry-run sample outputs only. The package now includes
  `real_input/README_REAL_INPUT.md`, `real_input/.gitkeep`, and
  `YMM4_IMPORT_RUNBOOK.md`; manifest file checks and the sample rebuild route
  (`validate`, `build-csv`, `build-cue-packet`, `build-diagram-packet`) passed
  before this handoff. Another terminal should fetch/pull `master`, confirm
  `HEAD...origin/master = 0 0`, then read `AGENTS.md`,
  `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, the package README,
  `MANIFEST.json`, `real_input/README_REAL_INPUT.md`, and
  `YMM4_IMPORT_RUNBOOK.md`. Next action: add a user-approved real NotebookLM
  transcript at `real_input/episode_001_transcript.txt`, update the speaker
  map if needed, regenerate `outputs/episode_001_ymm4.csv`,
  `outputs/episode_001_cue_packet.md`, and
  `outputs/episode_001_diagram_packet.md`, then have a human manually check
  YMM4 import. Do not resume live RSS, scraping, OAuth, payment, upload,
  render, rights/legal acceptance, cross-repo edits, or common-foundation /
  status-producer work from this handoff.
- Current newsroom slice (2026-07-01 JST):
  `newsroom-live-rss-operator-authorization-sheet-v1` is complete. The route
  remains authorization-template-only: no live RSS/news fetch, no network
  access, no active feed target, no fetch adapter, no article scraping, no
  actual user authorization request, and no production or publication claim.
  The sheet defines purpose, operator-fill fields, required yes/no
  confirmations, forbidden actions, abort conditions, and expected future
  result artifacts. The machine packet template keeps authorization
  `not_requested`, feed URL as a placeholder, max entries at zero, and all
  network/article/media/render/audio/production/public flags false. The
  selected next axis is `newsroom-rss-source-manifest-schema-v1`.
- Current newsroom slice (2026-07-01 JST):
  `newsroom-live-rss-preflight-contract-v1` is complete. The route remains
  preflight-contract-only: no live RSS/news fetch, no network source access,
  no active feed target, no fetch adapter, no article scraping, no actual
  user authorization request, and no production or publication claim. The
  contract defines the preflight packet schema, authorization states, future
  local/ignored output policy, future artifact schemas, abort conditions,
  post-fetch gates, and readiness classification. Current defaults keep
  authorization not requested and every network/article/media/render/audio/
  production/public flag false. The selected next axis is
  `newsroom-live-rss-operator-authorization-sheet-v1`.
- Current newsroom slice (2026-07-01 JST):
  `newsroom-live-rss-boundary-plan-v1` is complete. The route remains
  planning-only: no live RSS/news fetch, no network source access, no active
  feed target, no fetch adapter, no article scraping, and no production or
  publication claim. The plan defines the state machine through
  `live_boundary_planned`, future local/ignored artifact requirements, the
  normalized live RSS topic schema, live/source/capsule/publication gates,
  responsibility split, and risk register. Decision readback sets
  `live_fetch_implementation_allowed_now=false`,
  `live_boundary_plan_ready=true`, and selects
  `newsroom-live-rss-preflight-contract-v1` as the next axis.
- Current newsroom slice (2026-07-01 JST):
  `newsroom-source-boundary-adversarial-fixtures-v1` is complete. The offline
  adversarial suite covers the diagnostic control and ten failure classes for
  missing required fields, unmarked placeholders, invalid URL/timestamp,
  unknown rights, stale freshness, absent excluded claims, excluded-claim
  misuse, unknown source boundary, false production readiness with
  placeholders, and live-fetch-attempt flags. Validation found zero
  unexpected passes/fails and kept `production_script_ready=false` plus
  `live_boundary_plan_ready=false` for every case. Capsule hardening blocked
  clean capsule generation where required and detected the injected
  excluded-claim misuse. The selected next axis is
  `newsroom-live-rss-boundary-plan-v1`, limited to planning; live fetch
  implementation remains out of scope.
- Previous newsroom slice (2026-07-01 JST):
  `newsroom-rss-topic-fixture-route-hardening-v1` is complete. The offline
  RSS-like fixture v2 route now has deterministic field validation,
  placeholder classification, route boundary states, production blocker
  reporting, and capsule readiness classification. The fixture is reusable for
  offline diagnostics, not blocked for offline validation, and still blocked
  from live/production use because source URL, published timestamp, freshness,
  attribution, and rights remain explicit placeholders. The selected next axis
  is `newsroom-episode-capsule-route-hardening-v1`.
- Current newsroom slice (2026-07-01 JST):
  `newsroom-episode-capsule-route-hardening-v1` is complete. The five-beat
  capsule now carries validated fixture boundaries at capsule and beat level:
  rights/freshness/attribution status, production status, can-use flags,
  production-claim denial, excluded-claim propagation, and a mandatory
  source-boundary warning beat. The route remains diagnostic-only and reusable
  offline, not live-boundary-ready, and not production-script-ready. The
  selected next axis is `newsroom-source-boundary-adversarial-fixtures-v1`.
- Current remote handoff (2026-07-01 JST):
  `newsroom-terminal-resume-remote-sync-handoff-v4` records the latest
  PLANNER007 restart context after
  `28940f8 newsroom: harden episode capsule boundaries`. Another terminal
  should fetch/pull `master`, confirm `HEAD...origin/master = 0 0`, then
  resume from `docs/runtime-state.md` and
  `docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V4_2026-07-01.md`.
- Previous newsroom slice (2026-06-30 JST):
  `newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1`
  is complete. The current handoff is no longer visual preview or animation
  polish; it is an offline RSS-like topic fixture route that is stronger than
  v1, generates a five-beat diagnostic capsule, and still needs fixture
  hardening because URL, freshness, and rights remain placeholders.
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現在地の正本: 通常再開では `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → `docs/runtime-state.md` で止める。本ファイル冒頭は状態スナップショットではなく、航海日誌への短い入口。
- 現フェーズ: `docs/runtime-state.md` が最新の current slice を所有する。2026-06-30 時点の実行入口は readable mini episode preview pass 後の offline RSS-like topic fixture route audit と fixture v2 強化。G-27 Real Estate DX の production carrier 待ちは active blocker から外し、case-specific evidence として保持する。G-28 Reference-Driven Generic Screen Carrier は既存 diagnostic / prototype evidence からの refinement lane として残るが、今回の mainline handoff では進めない。
- 古い roadmap / prompt / verification packet は現行判断に使わない。必要な履歴は DECISION LOG と HANDOFF SNAPSHOT の該当行だけ読む。
- Python のスコープは「テキスト変換 + IR/registry + ymmp 限定後段適用」。動画レンダリング・画像生成・YMM4 GUI 操作は Python の責務ではない。

---

## ACTIVE ARTIFACT
- Previous newsroom artifact: offline RSS-like topic fixture v2 plus a
  route-hardening validation layer. The hardening output validates all 13
  required fields, detects five explicit placeholder-capable fields with zero
  unmarked placeholders, classifies the route as diagnostic-only and reusable
  offline, and keeps live RSS planning plus production script generation
  closed until real source, freshness, attribution, reliability, and rights
  review replace the placeholders.
- Current newsroom artifact: hardened offline RSS-like topic fixture v2
  episode capsule route. The new hardened capsule/readback keeps the original
  v2 capsule artifact unchanged, then adds capsule-level boundary summary and
  beat-level propagation for source, rights, freshness, attribution,
  production status, excluded claims, and readiness flags. Production and live
  boundary readiness remain false while placeholders and source approval gaps
  remain.
- Previous newsroom artifact: offline RSS-like topic fixture v2 plus a
  diagnostic five-beat mini episode capsule. The v2 fixture explicitly carries
  required source, placeholder URL, placeholder published time, summary, key
  claim, why-it-matters, boundary, rights, intended angle, excluded claims, and
  diagnostic production status fields. The route is `current_partial`, not
  blocked, and selected next axis is
  `newsroom-rss-topic-fixture-route-hardening-v1`.
- Active Artifact: NLM transcript → YMM4 CSV → Writer IR → Template Registry → YMM4 Adapter → 動画制作ワークフロー効率化
- Artifact Surface: CLI artifact → CSV / registry / patched ymmp → YMM4 読込・確認・レンダリング
- 現在のスライス: PLANNER007 上では episode capsule route hardening が完了し、YMM4 visual gate は `closed_for_now` のまま。次の主摩擦は visual/card/animation ではなく、source-boundary の adversarial cases を validator と capsule route の両方へ通すこと。
- 成功状態: 現行 capsule route が diagnostic-only reusable offline capsule として境界を保持し、live/production blockers を残したまま、次の adversarial fixture axis を明確にすること。

---

## CURRENT LANE
- Current sync state: product work has advanced through
  `newsroom-live-rss-operator-authorization-sheet-v1`. The next bottleneck is
  a source/feed manifest schema that can describe future feed targets without
  activating a real feed or asking for authorization prematurely. This does
  not approve live fetch, network access, real feed use, article scraping,
  YMM4 preview, render, `.ymmp`, media, audio/TTS, animation, card,
  production, publication, or audience-acceptance work.
- Current sync state: product work has advanced through
  `newsroom-live-rss-preflight-contract-v1`. The next bottleneck is a
  human-facing operator authorization sheet that can be filled later without
  silently turning into a fetch request. This does not approve live fetch,
  network access, real feed use, article scraping, YMM4 preview, render,
  `.ymmp`, media, audio/TTS, animation, card, production, publication, or
  audience-acceptance work.
- Current sync state: product work has advanced through
  `newsroom-live-rss-boundary-plan-v1`. The next bottleneck is a stricter
  live RSS preflight contract: prove the authorization sheet, local ignored
  output shape, receipt schema, manifest schema, and no-production readback
  before any diagnostic live fetch can be authorized. This does not approve
  live fetch implementation, real feed use, article scraping, YMM4 preview,
  render, `.ymmp`, media, audio/TTS, animation, card, production,
  publication, or audience-acceptance work.
- Current sync state: product work has advanced through
  `newsroom-source-boundary-adversarial-fixtures-v1`. The next bottleneck is
  a live RSS boundary plan that specifies source, freshness, rights,
  attribution, excluded-claim, and no-network-test gates before any live fetch
  implementation. This does not reopen YMM4 preview, render, `.ymmp`, media,
  audio/TTS, animation, card, production, publication, or audience-acceptance
  work.
- Current sync state: product work has advanced into
  `newsroom-episode-capsule-route-hardening-v1`. The next bottleneck is
  adversarial source-boundary fixtures for missing, invalid, and unmarked
  placeholder cases across validator and capsule route, not live RSS fetch,
  YMM4 preview, render, animation, cards, audio/TTS, or publication.
- Previous sync state: local context is being mirrored to `origin/master` through
  terminal resume handoff v3. Product work should resume at
  `newsroom-rss-topic-fixture-route-hardening-v1`; handoff work itself must not
  reopen YMM4 preview, render, `.ymmp`, media/audio/TTS, live RSS/news,
  animation tuning, or card polish loops.
- Current lane reason: the readable YMM4 gate is already closed for now, so
  the bottleneck moved upstream to fixture/schema quality. This slice did not
  create or modify `.ymmp`, did not launch YMM4, did not render, did not fetch
  live RSS/news, and did not tune animation or cards.
- 主レーン: Downstream adapter / YMM4 diagnostic handoff（newsroom-produced handoff material）。現行の優先は [runtime-state.md](runtime-state.md) の top entry。
- 今このレーンを優先する理由: readable v2 preview で five visible human-readable TextItems が確認され、animation accent も blocking と報告されていない。これ以上の YMM4 visual preview / animation tuning / card work は現在の bottleneck ではなく、次は offline topic/RSS-like fixture を robust にして episode capsule 生成へ戻ることにある。

---

## ROADMAP UPDATE (2026-04-27 post-cleanup prep)

This section narrows the next roadmap after the legacy-document cleanup. It does not approve new implementation scope. The gate-shaped author/export pass is now closed for the v1 planned set; the current value path is production-use validation with existing templates.

### 現行ロードマップの主軸

1. **G-24 `delivery_nod_v1` cautious gate を閉じる（完了）**
   - actor: user + assistant
   - owner artifact: YMM4 native template asset + `skit_group` registry / Capability Atlas state
   - bottleneck: `audit-skit-group` readiness と standalone native template export proof の分離
   - done condition: `delivery_nod_v1` が GroupItem + body/face の 2 `ImageItem` children + no `TachieItem` で export され、manual acceptance (`nod amplitude`, `does not dominate scene`) を PASS する
2. **`deny_oneshot -> exit_left` を同じ gate で処理する（完了）**
   - actor: shared
   - owner artifact: `skit_group.intent.*` の support level
   - bottleneck: starter 2 件の成功を remaining intent 群へ安全に横展開すること
   - done condition: `deny_oneshot` / `exit_left` が `direct_proven` after export proof になること
   - result: user completed both samples; repo inspection found ImageItem body/face + no `TachieItem`; both intents are now `direct_proven`
3. **P02 production adoption を template 解決の実戦運用へ寄せる（現行）**
   - actor: assistant + user
   - owner artifact: production adoption proof / template resolution notes
   - bottleneck: 小演出 authoring 自体を progress と誤認せず、作った template が実制作の選択負荷を減らすかへ接続すること
   - done condition: exact / fallback / manual note が、実制作の S-6（背景・演出設定）でどの手作業を減らすかまで記録される
   - loop stop: `exit_left` 後は追加 motion 作成へ進まず、実制作 IR の template 解決結果を見て production gap が出た時だけ新テンプレートを再起票する
   - role split: user は少数の reusable native template を作り、assistant は組み合わせ・registry・fallback note で production-like sample / 解決結果を作る。user は全サンプル作成ではなく確認に集中する
4. **メンテ層は on-demand に保つ**
   - actor: operator / assistant
   - owner artifact: B-18 台本診断、B-17 改行残差、H-01/H-02 packaging / thumbnail briefs
   - bottleneck: G-24 の主軸を、done 件数稼ぎや古い spec/proof 整備で薄めないこと
   - done condition: 新台本・新サムネ・drift 発生時だけ起動し、通常の次 frontier にはしない

### formal plan の分岐条件

- **通常**: 次プランは existing v1 template set を使った production-like sample / 解決結果作成から始める。assistant が exact / fallback / manual_note を整理し、user は YMM4 上で結果確認に集中する。
- **十分**: exact coverage が制作負荷を減らすなら production-use hardening を続ける。追加 motion authoring はしない。
- **不足**: `fallback` / `manual_note` / missing-template / body-face drift / `TachieItem` 混入 / repo bug を failure class として分け、追加テンプレート起票か修正かを選ぶ。FAIL を代替成功にしない。
- **新規制作案件が先に来た場合**: G-24 の主軸は維持し、メンテ層は B-18 → H-01/H-02 on demand → B-17 drift-only の順で必要分だけ起動する。

### プラン作成前に揃えるもの

- [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) は G-24 production-use validation を現行アンカーとして更新済み。
- `runtime-state.md` と `verification/P02-production-adoption-proof.md` は、v1 template completion と production-use validation を分離する現行参照先として更新済み。
- 削除済みレガシードキュメント名への repo-local 参照は `git grep` で残存なし。
- `formal plan の分岐条件` は本節に固定済み。次プランはこの分岐のどれに入ったかを冒頭で宣言してから書く。
- 次の formal plan は **production-like sample / 解決結果作成** から始める。追加 motion authoring は production gap が具体化した時だけ起票する。

### 今回やらないこと

- 新しい FEATURE を増やさない。
- `motion_target` / `group_motion` を `nod` の代替成功として扱わない。
- 背景アニメ/S6 の古い証跡を、現行判断に混ぜない。
- `audit-skit-group` の `exact` を standalone export proof と読み替えない。

## DECISION LOG

Latest Episode 002 Output / Video Layer handoff decision (2026-07-08 JST):
`episode_002_output_video_layer_proof_v1` is the current cross-terminal
restart focus on branch `codex/episode-002-output-video-layer-proof-v1`. The
user explicitly requested that all current context be held in the project and
that local state be reflected to remote, so the otherwise lane-local Output /
Video proof context was recorded in `docs/runtime-state.md` and this
`project-context.md` handoff/decision entry. This does not promote shared-doc
churn as the default for parallel lanes; it is the handoff exception for this
request. The proof remains local/static and non-production: real
transcript/source input is blocked, YMM4 import/render is closed, public
rights/upload gates are closed, and GUI/IA/i18n review packages are not the
active edit target. The next decision is whether to review the storyboard/gap
ledger only, supply verified local source/transcript material, continue local
output-template proofing, or explicitly open a YMM4 observation gate.

Latest newsroom live RSS operator authorization sheet decision (2026-07-01 JST):
`newsroom_live_rss_operator_authorization_sheet_v1_2026_06_30` creates the
human-facing authorization sheet template and machine-readable authorization
packet template for a future one-time diagnostic live RSS fetch. The tracked
artifacts are
`samples/_probe/newsroom_handoff/live_rss_operator_authorization_sheet_v1.json`,
`samples/_probe/newsroom_handoff/live_rss_authorization_packet_template_v1.json`,
and
`docs/verification/NEWSROOM_LIVE_RSS_OPERATOR_AUTHORIZATION_SHEET_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_live_rss_operator_authorization_sheet.py` /
`tests/test_newsroom_live_rss_operator_authorization_sheet.py`.

The sheet is template-only and does not request actual authorization. Operator
fill fields include feed title, feed URL, source name, rationale, max entries,
fetch mode, output root, expiry, and notes. Required confirmations explicitly
separate a future one-time RSS feed fetch from article scraping, media
download, render/export, audio/TTS, production/public claims, raw-output
policy, source-boundary validation, rights/freshness/attribution readback,
excluded-claims readback, and diagnostic-only capsule candidacy. The packet
template defaults to `authorization_status=not_requested`,
`network_access_allowed=false`, `article_page_fetch_allowed=false`,
`media_download_allowed=false`, `render_allowed=false`,
`audio_tts_allowed=false`, `production_claim_allowed=false`,
`publication_allowed=false`, `feed_url=placeholder:future_feed_url_not_set`,
and `max_entries=0`. Safety classification sets
`authorization_sheet_ready=true`, `actual_authorization_requested_now=false`,
`fetch_implementation_allowed_now=false`, `network_access_allowed_now=false`,
`operator_action_required_now=false`, and
`next_allowed_state=authorization_request_or_source_manifest_schema`. The
selected next axis is `newsroom-rss-source-manifest-schema-v1`. No Agent-side
network/live RSS/news fetch, actual authorization request, active feed source,
fetch adapter implementation, article scraping, YMM4 launch, render, `.ymmp`
creation/modification/stage/commit, media/audio/TTS generation, card redesign,
animation tuning, production/public readiness claim, or audience/order
acceptance claim occurred.

Latest newsroom live RSS preflight contract decision (2026-07-01 JST):
`newsroom_live_rss_preflight_contract_v1_2026_06_30` defines the preflight
packet and authorization model for a future diagnostic live RSS smoke after
the live boundary plan completed. The tracked artifacts are
`samples/_probe/newsroom_handoff/live_rss_preflight_contract_v1.json`,
`samples/_probe/newsroom_handoff/live_rss_preflight_packet_template_v1.json`,
and
`docs/verification/NEWSROOM_LIVE_RSS_PREFLIGHT_CONTRACT_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_live_rss_preflight_contract.py` /
`tests/test_newsroom_live_rss_preflight_contract.py`.

The packet template defaults to `authorization_status=not_requested`,
`network_access_allowed=false`, `article_page_fetch_allowed=false`,
`media_download_allowed=false`, `render_allowed=false`,
`audio_tts_allowed=false`, `production_claim_allowed=false`, and
`publication_allowed=false`. Future output policy keeps raw live fetch
materials local/ignored and allows only summarized readbacks to become
tracked after redaction/summarization. Abort conditions cover missing or
malformed feed URL, missing output root, unauthorized network access, article
page fetch, media download, render/audio/publication requests, too many
entries, unclear rights/terms, unexpected redirect/non-RSS response,
scraping requirement, and production/public claims. Post-fetch gates are
defined but not executed: `FETCH_RECEIPT_GATE`, `NORMALIZED_TOPIC_GATE`,
`SOURCE_BOUNDARY_GATE`, and `CAPSULE_INPUT_GATE`. Readiness classification
sets `preflight_contract_ready=true`, `authorization_sheet_ready=true`,
`fetch_implementation_allowed_now=false`, `network_access_allowed_now=false`,
`operator_action_required_now=false`, and
`next_allowed_state=authorization_request_preparation`. The selected next
axis is `newsroom-live-rss-operator-authorization-sheet-v1`. No Agent-side
network/live RSS/news fetch, active feed source, fetch adapter implementation,
article scraping, actual user authorization request, YMM4 launch, render,
`.ymmp` creation/modification/stage/commit, media/audio/TTS generation, card
redesign, animation tuning, production/public readiness claim, or
audience/order acceptance claim occurred.

Latest newsroom live RSS boundary plan decision (2026-07-01 JST):
`newsroom_live_rss_boundary_plan_v1_2026_06_30` defines the planning boundary
for future live RSS/topic introduction after adversarial source-boundary
fixtures passed. The tracked artifacts are
`samples/_probe/newsroom_handoff/live_rss_boundary_plan_v1.json`,
`samples/_probe/newsroom_handoff/live_rss_boundary_contract_v1.json`, and
`docs/verification/NEWSROOM_LIVE_RSS_BOUNDARY_PLAN_V1_2026-06-30.md`, with
implementation/tests in `src/pipeline/newsroom_live_rss_boundary_plan.py` /
`tests/test_newsroom_live_rss_boundary_plan.py`.

The state machine stops at `live_boundary_planned`; future states for live
fetch authorization, result capture, live source boundary validation,
diagnostic capsule readiness, and production readiness are not set. The
future diagnostic smoke contract requires nine local/ignored artifacts:
`fetch_receipt`, `feed_source_manifest`, `raw_entry_snapshot`,
`normalized_topic_candidate`, `source_boundary_validation`,
`rights_attribution_freshness_readback`, `excluded_claims_readback`,
`capsule_input_candidate`, and `operator_action_log`. Gate definitions cover
`LIVE_FETCH_GATE`, `SOURCE_BOUNDARY_GATE`, `CAPSULE_GENERATION_GATE`, and
`PUBLICATION_GATE`. The decision readback sets
`live_fetch_implementation_allowed_now=false`,
`live_boundary_plan_ready=true`, and selects
`newsroom-live-rss-preflight-contract-v1`. No Agent-side network/live RSS/news
fetch, active feed source, fetch adapter implementation, article scraping,
YMM4 launch, render, `.ymmp` creation/modification/stage/commit,
media/audio/TTS generation, card redesign, animation tuning,
production/public readiness claim, or audience/order acceptance claim
occurred.

Latest newsroom source boundary adversarial fixtures decision (2026-07-01 JST):
`newsroom_source_boundary_adversarial_fixtures_v1_2026_06_30` validates the
offline RSS-like topic fixture route against 11 adversarial source-boundary
cases before live boundary planning. The tracked artifacts are
`samples/_probe/newsroom_handoff/source_boundary_adversarial_fixtures_v1.json`,
`samples/_probe/newsroom_handoff/source_boundary_adversarial_fixture_validation_v1.json`,
`samples/_probe/newsroom_handoff/source_boundary_adversarial_capsule_hardening_v1.json`,
and
`docs/verification/NEWSROOM_SOURCE_BOUNDARY_ADVERSARIAL_FIXTURES_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_source_boundary_adversarial_fixtures.py` /
`tests/test_newsroom_source_boundary_adversarial_fixtures.py`.

Readback confirms `total_cases=11`, `expected_pass_count=1`,
`expected_block_count=10`, `unexpected_pass_count=0`,
`unexpected_fail_count=0`, and `production_ready_false_count=11`.
Capsule hardening reports five diagnostic-only capsule generations, six
blocked clean-generation cases, one excluded-claim positive-claim misuse
detected, and zero production/live readiness true counts. The selected next
axis is `newsroom-live-rss-boundary-plan-v1`; live fetch implementation is not
approved. No Agent-side YMM4 launch, render, `.ymmp`
creation/modification/stage/commit, media/audio/TTS generation, live
RSS/news fetch, card redesign, animation tuning, production/public readiness
claim, or audience/order acceptance claim occurred.

Latest newsroom terminal resume remote sync handoff v4 decision (2026-07-01 JST):
`newsroom_terminal_resume_remote_sync_handoff_v4_2026_07_01` persists the
latest PLANNER007 restart context after
`28940f8 newsroom: harden episode capsule boundaries`. The tracked handoff
artifacts are
`samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v4.json`
and
`docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V4_2026-07-01.md`,
with this runtime/context update. Another terminal should run `git fetch
origin`, `git checkout master`, `git pull --ff-only origin master`, then confirm
`git status --short --branch` is clean and
`git rev-list --left-right --count HEAD...origin/master` returns `0 0`.

The latest product slice remains
`newsroom-episode-capsule-route-hardening-v1`, whose selected next axis is
`newsroom-source-boundary-adversarial-fixtures-v1`. Relevant ignored local
probes on PLANNER007 include
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp`
and
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp`;
both resolve through `.gitignore:37:_tmp/` and must remain local-only. This
handoff did not launch YMM4, render, create/modify/stage/commit `.ymmp`,
generate media/audio/TTS, fetch live RSS/news, redesign cards, tune animation,
claim production/public readiness, or claim audience/order acceptance.

Latest newsroom episode capsule route hardening decision (2026-07-01 JST):
`newsroom_episode_capsule_route_hardening_v1_2026_06_30` hardens the five-beat
capsule route after fixture validation confirmed required fields and explicit
placeholders. The tracked artifacts are
`samples/_probe/newsroom_handoff/episode_capsule_route_hardening_v1.json`,
`samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_hardened_episode_capsule_v1.json`,
and
`docs/verification/NEWSROOM_EPISODE_CAPSULE_ROUTE_HARDENING_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_episode_capsule_route_hardening.py` /
`tests/test_newsroom_episode_capsule_route_hardening.py`.

The original v2 capsule artifact is unchanged; the new hardened capsule
propagates fixture validation boundaries into capsule-level summary and each
beat. Every beat carries excluded claims, rights/freshness/attribution status,
diagnostic production status, can-use flags, not-accepted scope, and
`production_claim_allowed=false`. The source-boundary warning beat explicitly
mentions the offline fixture, placeholder source URL/timestamp, rights,
freshness, and attribution not being production-approved, and excluded claims
not being assertable. Readback confirms excluded claims are present, not used
as positive claims, production blockers and placeholder counts are propagated,
the source-warning beat is present, and both `production_script_ready` and
`live_boundary_plan_ready` are false. No Agent-side YMM4 launch, render,
`.ymmp` creation/modification/stage/commit, media/audio/TTS generation, live
RSS/news fetch, card redesign, animation tuning, production/public readiness
claim, or audience/order acceptance claim occurred. The selected next axis is
`newsroom-source-boundary-adversarial-fixtures-v1`.

Latest newsroom RSS topic fixture route hardening decision (2026-07-01 JST):
`newsroom_rss_topic_fixture_route_hardening_v1_2026_06_30` validates the
offline RSS-like topic fixture v2 route before any live RSS/news source
ingestion. The tracked artifacts are
`samples/_probe/newsroom_handoff/rss_topic_fixture_route_hardening_v1.json`,
`samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_validation_v1.json`,
and
`docs/verification/NEWSROOM_RSS_TOPIC_FIXTURE_ROUTE_HARDENING_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_rss_topic_fixture_route_hardening.py` /
`tests/test_newsroom_rss_topic_fixture_route_hardening.py`.

The hardening layer confirms that all 13 required fields are present, that
`source_url_or_placeholder`, `published_at_or_placeholder`, `rights_status`,
`freshness_status`, and `attribution_note` are explicit placeholders, and that
there are zero unmarked placeholders and zero missing required fields. The
route remains diagnostic-only and reusable as an offline fixture; it is not
blocked for offline validation, but it is still synthetic and production
blocked because source URL, published timestamp, freshness, attribution,
source reliability, and rights are not real reviewed source facts. Capsule
readiness is true for diagnostic capsule and reusable offline fixture, false
for live boundary planning and production script generation. No Agent-side
YMM4 launch, render, `.ymmp` creation/modification/stage/commit,
media/audio/TTS generation, live RSS/news fetch, card redesign, animation
tuning, production/public readiness claim, or audience/order acceptance claim
occurred. The selected next axis is
`newsroom-episode-capsule-route-hardening-v1`.

Latest newsroom terminal resume remote sync handoff v3 decision (2026-06-30 JST):
`newsroom_terminal_resume_remote_sync_handoff_v3_2026_06_30` persists the
latest PLANNER007 restart context after
`84f4406 docs: add offline rss fixture v2 capsule`. The tracked handoff
artifacts are
`samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v3.json`
and
`docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V3_2026-06-30.md`,
with this runtime/context update. Another terminal should run `git fetch
origin`, `git checkout master`, `git pull --ff-only origin master`, then confirm
`git status --short --branch` is clean and
`git rev-list --left-right --count HEAD...origin/master` returns `0 0`.

The latest product slice remains
`newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1`, whose
selected next axis is `newsroom-rss-topic-fixture-route-hardening-v1`. Relevant
ignored local probes on PLANNER007 include
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp`
and
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp`;
both resolve through `.gitignore:37:_tmp/` and must remain local-only. This
handoff did not launch YMM4, render, create/modify/stage/commit `.ymmp`,
generate media/audio/TTS, fetch live RSS/news, redesign cards, tune animation,
claim production/public readiness, or claim audience/order acceptance.

Latest newsroom offline RSS-like topic fixture v2 to mini episode capsule decision (2026-06-30 JST):
`newsroom_offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1_2026_06_30`
strengthens the previous offline topic/RSS-like input route after
`rss_topic_fixture_route_audit_v1` found v1 diagnostic-only and reusable but
too synthetic for safer episode generation. The tracked artifacts are
`samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json`,
`samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_schema_contract_v1.json`,
`samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json`,
and
`docs/verification/NEWSROOM_OFFLINE_RSS_LIKE_TOPIC_FIXTURE_V2_TO_MINI_EPISODE_CAPSULE_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_offline_rss_like_topic_fixture_v2.py` /
`tests/test_newsroom_offline_rss_like_topic_fixture_v2.py`.

The v2 fixture fills the required source, placeholder URL, placeholder
published time, summary, key claim, why-it-matters, boundary, rights, intended
angle, excluded claims, and diagnostic production status fields. The
transformation generates five diagnostic beats: hook / issue framing, key claim
/ explanation, source-boundary warning, implication / why it matters, and close
/ next action. Each beat carries source fields used, excluded claims applied,
plain TextItem/overlay roles for later materialization, and optional frozen
animation assignment metadata only. The route classification is
`current_partial`: diagnostic-only, reusable fixture candidate, stronger than
v1, not blocked, but still synthetic because source URL, freshness, and rights
remain explicit placeholders. This decision did not launch YMM4, render,
create/modify/stage/commit `.ymmp`, generate media/audio/TTS, fetch live
RSS/news, redesign cards, tune animation, claim production/public readiness, or
claim audience/order acceptance. The selected next axis is
`newsroom-rss-topic-fixture-route-hardening-v1`.

Latest newsroom offline topic readable preview readback and RSS topic fixture route audit decision (2026-06-30 JST):
`newsroom_offline_topic_readable_preview_readback_and_rss_topic_fixture_route_audit_v1_2026_06_30`
records the user-side preview observation for
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp`.
The readable v2 preview is accepted with boundary: YMM4 opened, five TextItems
were visible, the five screen-facing lines were human-readable hook / key claim
/ warning / implication / close beats, debug labels were not primary screen
text, and animation was not reported as blocking. This closes the current
YMM4 visual gate for now and requests no further preview in this slice.

The tracked artifacts are
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_readable_preview_observation_v1.json`,
`docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_READABLE_PREVIEW_OBSERVATION_V1_2026-06-30.md`,
`samples/_probe/newsroom_handoff/rss_topic_fixture_route_audit_v1.json`, and
`docs/verification/NEWSROOM_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_rss_topic_fixture_route_audit.py` /
`tests/test_newsroom_rss_topic_fixture_route_audit.py`. The route audit
classifies the current offline RSS-like topic route as diagnostic-only and a
reusable fixture candidate, but too synthetic for safer episode generation.
Current available fields are `topic_id`, `title`, `source_kind`,
`key_fact_or_claim`, `explanation_angle`, and `boundary_note`; missing or
placeholder-required fields include `source_name`,
`source_url_or_placeholder`, `published_at_or_placeholder`, `summary`,
`rights_status`, and `excluded_claims`. Route confidence is `medium` and the
route is not blocked. The recommended minimal v2 fixture schema requires
`topic_id`, `title`, `source_name`, `source_url_or_placeholder`,
`published_at_or_placeholder`, `summary`, `key_claim`, `why_it_matters`,
`uncertainty_or_boundary`, `rights_status`, `intended_episode_angle`,
`excluded_claims`, and `production_status`. This decision did not launch YMM4
from the Agent, render, create/stage/commit `.ymmp`, generate media/audio/TTS,
fetch live RSS/news, redesign cards, tune animation, claim production/public
readiness, or claim audience/order acceptance. The selected next axis is
`newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1`.

Latest newsroom offline topic mini episode readable text materialization decision (2026-06-30 JST):
`newsroom_offline_topic_mini_episode_readable_text_materialization_v1_2026_06_30`
records the user-side preview observation for
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp`.
The v1 preview is a bounded pass for route/materialization structure:
five TextItems appeared sequentially, and the character animation accent was
present in the same scene/timing without being disruptive. It is not a pass
for human-readable mini episode text because the user observed screen-facing
debug labels like
`offline_topic_mini_episode:text:offline_topic_mini_ep_beat_01_hook`.

The tracked artifacts are
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_preview_observation_v1.json`,
`docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_PREVIEW_OBSERVATION_V1_2026-06-30.md`,
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_readable_text_materialization_v1.json`,
and
`docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_READABLE_TEXT_MATERIALIZATION_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_offline_topic_mini_episode_readable_text_materialization.py`
/ `tests/test_newsroom_offline_topic_mini_episode_readable_text_materialization.py`.
The local ignored v2 project exists at
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp`;
it is verified ignored by `.gitignore` `_tmp/` and must remain
untracked/uncommitted. It preserves the v1 route, timing, and frozen animation
accent policy while replacing the five screen-facing `TextItem` `Text` and
`Remark` values with short English explanation lines. English is used because
the Japanese examples in the supplied prompt were mojibake and the current
capsule route already uses ASCII English safely. Readback passes with a
60 fps / 1800-frame timeline, 5 beats, 5 `TextItem`s, 8 `GroupItem`s,
8 `ImageItem`s, 16 animation items, `debug_label_visible_count=0`, and
`human_readable_text_item_count=5`. This decision did not launch YMM4 from the
Agent, render, stage/commit `.ymmp`, generate media/audio/TTS, fetch live
RSS/news, redesign cards, tune animation, claim production/public readiness,
or claim audience/order acceptance. The selected next axis is
`newsroom-offline-topic-mini-episode-readable-preview-operator-instruction-v1`.

Latest newsroom offline topic mini episode capsule materialization decision (2026-06-30 JST):
`newsroom_offline_topic_mini_episode_capsule_materialization_v1_2026_06_30`
connects the current offline-topic 5-beat capsule to a non-speculative local
YMM4 diagnostic materialization route on PLANNER007. The route classification
is `current_supported`: it uses the current
`offline_topic_mini_episode_capsule_with_animation_accent_v1` capsule and
contract, the prior bridge, `rss_dry_run_topic_to_animated_explanation_beat_v1`,
the frozen background animation policy, and tracked `samples/nod_head.ymmp`.
The older `episode_production_capsule_v1` remains historical
`stale_fake_packet_only` evidence and is not used as the current route.

The tracked artifacts are
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_materialization_route_v1.json`,
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_materialization_v1.json`,
and
`docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_MATERIALIZATION_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_offline_topic_mini_episode_materialization.py` /
`tests/test_newsroom_offline_topic_mini_episode_materialization.py`. The local
ignored project exists at
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp`;
it is verified ignored by `.gitignore` `_tmp/` and must remain
untracked/uncommitted. Readback passes with a 60 fps / 1800-frame timeline,
5 beats, 5 `TextItem`s, 8 `GroupItem`s, 8 `ImageItem`s, 16 animation items,
one plain diagnostic text role per beat, no card/shape/audio/video items,
fixed parent X `-96.0` for all animation accents, and no animation on the close
beat. This decision did not launch YMM4 from the Agent, render, stage/commit
`.ymmp`, generate media/audio/TTS, fetch live RSS/news, redesign cards, tune
animation, claim production/public readiness, or claim audience/order
acceptance. The selected next axis is
`newsroom-offline-topic-mini-episode-preview-operator-instruction-v1`.

Latest newsroom offline topic mini episode capsule with animation accent decision (2026-06-30 JST):
`newsroom_offline_topic_mini_episode_capsule_with_animation_accent_v1_2026_06_30`
advances the previous bridge into a diagnostic 5-beat mini episode capsule
contract from the offline RSS-like topic fixture. The tracked artifacts are
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_with_animation_accent_v1.json`,
`docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_WITH_ANIMATION_ACCENT_V1_2026-06-30.md`,
and
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_contract_v1.json`,
with implementation/tests in
`src/pipeline/newsroom_offline_topic_mini_episode_capsule.py` /
`tests/test_newsroom_offline_topic_mini_episode_capsule.py`.

The capsule has five beats: hook / issue framing, explanation / key claim,
source-boundary warning, implication / why it matters, and close / next action.
Each beat carries `beat_id`, `source_topic_id`, `beat_function`,
`explanation_line`, `narration_intent`, `subtitle_or_text_role`,
`minimal_overlay_role`, `background_animation_accent_role`,
`source_boundary_role`, `materialization_role`, and `review_status`. The
frozen MVP animation policy remains optional and subordinate: assignments are
`stable_pose_only`, `expression_event`, `expression_plus_short_nod`,
`short_nod_reaction`, and `none`. Disabled remain body forward/back movement,
repeated nodding, mechanical expression cycling, speech balloons, full chaban
scenes, animation-only probe loops, and tempo-only loops.

Existing `episode_production_capsule_v1` is treated as an older fake-packet
structural precedent, not as the current offline-topic YMM4 route. No local
`.ymmp` was created because a safe non-speculative PLANNER007 multi-beat YMM4
materialization route is not yet verified; the planned ignored path
`_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp`
is verified ignored and recorded as `not_created_deferred`. This decision did
not launch YMM4 from the Agent, render, stage/commit `.ymmp`, generate
media/audio/TTS, fetch live RSS/news, redesign cards, tune animation, claim
production/public readiness, or claim audience/order acceptance. The selected
next axis is
`newsroom-offline-topic-mini-episode-capsule-materialization-v1`.

Latest newsroom RSS dry-run animated beat preview readback and mini episode capsule bridge decision (2026-06-30 JST):
`newsroom_rss_dry_run_animated_beat_preview_readback_and_mini_episode_capsule_bridge_v1_2026_06_30`
records the user-side preview observation for the ignored local RSS dry-run
animated beat at
`_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp`.
The preview showed the plain topic-derived `TextItem`
`Offline fixture: verify source boundary before production.` and the character
animation accent at the same timing in the same scene. No card-like designed
overlay was visible. This closes the one-beat visual integration gate as
`content_flow_visual_status=pass_with_boundary`, while production subtitle
design, production card design, render quality, public readiness, and
audience/order acceptance remain false.

The tracked artifacts are
`samples/_probe/newsroom_handoff/rss_dry_run_animated_beat_preview_observation_v1.json`,
`docs/verification/NEWSROOM_RSS_DRY_RUN_ANIMATED_BEAT_PREVIEW_OBSERVATION_V1_2026-06-30.md`,
`samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_bridge_v1.json`,
and
`docs/verification/NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_BRIDGE_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_offline_topic_mini_episode_capsule_bridge.py` /
`tests/test_newsroom_offline_topic_mini_episode_capsule_bridge.py`. The bridge
keeps the existing one-beat route as a candidate and creates a 5-beat
diagnostic capsule contract: hook / issue framing, explanation / key claim,
source-boundary warning, implication / why it matters, and close / next action.
The selected next axis is
`newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1`.

The current `C:\Users\PLANNER007\NLMYTGen` workspace does not contain the
ignored local `.ymmp` opened on the earlier `C:\Users\thank\...` host path; the
path remains ignored by `.gitignore` `_tmp/` and was not recreated in this
slice. This decision did not launch YMM4 from the Agent, render, create or
stage/commit `.ymmp`, generate media/audio/TTS, fetch live RSS/news, redesign
cards, tune animation, claim production/public readiness, or claim
audience/order acceptance.

Latest terminal resume remote sync handoff decision (2026-06-30 JST):
`newsroom_terminal_resume_remote_sync_handoff_v2_2026_06_30` preserves the
current restart context after
`3e81daa docs: add rss dry-run animated beat proof`. Before this handoff, the
mainline-slot worktree was fetched, clean, on `master`, and aligned with
`origin/master` (`HEAD...origin/master = 0 0`). The tracked context added by
this handoff is
`samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v2.json`
and
`docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V2_2026-06-30.md`,
plus this decision-log entry and the top runtime-state entry.

The current restart surface is the RSS dry-run animated explanation beat proof:
`samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json`,
`samples/_probe/newsroom_handoff/rss_dry_run_animated_explanation_beat_contract_v1.json`,
and
`docs/verification/NEWSROOM_RSS_DRY_RUN_TO_ANIMATED_EXPLANATION_BEAT_V1_2026-06-30.md`.
The current ignored local review targets are
`_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp`
and
`_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v2_visible_integration.ymmp`;
both exist on this host and are ignored through `.gitignore` `_tmp/`, so they
must remain untracked/uncommitted. The next default axis remains
`newsroom-rss-dry-run-animated-explanation-beat-preview-operator-instruction-v1`.
This handoff did not launch YMM4, render, stage/commit `.ymmp`, generate
media/audio/TTS, fetch live RSS/news, redesign cards, tune animation, claim
production/public readiness, or claim audience/order acceptance.

Latest newsroom RSS dry-run to animated explanation beat decision (2026-06-30 JST):
`newsroom_rss_dry_run_topic_to_animated_explanation_beat_v1_2026_06_30`
records the user-side v2 visible-integration observation for
`_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v2_visible_integration.ymmp`.
The file opened in YMM4 and showed one visible plain explanation `TextItem`,
the character, and the minimal animation accent in the same scene. No
card-like designed overlay was visible. This is a bounded integration pass, not
production subtitle/card design acceptance.

The slice returns to content-flow proof by creating one offline
RSS-like diagnostic topic fixture and transforming it into one animated
explanation beat. The tracked artifacts are
`samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json`,
`docs/verification/NEWSROOM_RSS_DRY_RUN_TO_ANIMATED_EXPLANATION_BEAT_V1_2026-06-30.md`,
and
`samples/_probe/newsroom_handoff/rss_dry_run_animated_explanation_beat_contract_v1.json`,
with implementation/tests in
`src/pipeline/newsroom_rss_dry_run_to_animated_explanation_beat.py` /
`tests/test_newsroom_rss_dry_run_to_animated_explanation_beat.py`. The ignored
local probe exists at
`_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp`;
it is verified present on this host, verified ignored by `.gitignore` `_tmp/`,
and must remain untracked/uncommitted. It copies the v2 visible-integration
YMM4 structure, keeps `GroupItem=8` and `ImageItem=8` animation items
unchanged, and replaces the single visible `TextItem` with
`Offline fixture: verify source boundary before production.` Readback passes
with `TextItem=1`, visible text/overlay item count `1`, and animation item
count `16`. This decision did not fetch live RSS/news or network content, did
not create an animation-only probe, did not tune nod/expression/primitive
motion, did not redesign cards or create production subtitle/card design, did
not launch YMM4 from the Agent, did not render, did not stage/commit `.ymmp`,
did not generate media/audio/TTS, and did not claim production/public readiness
or audience/order acceptance. The selected next axis is
`newsroom-rss-dry-run-animated-explanation-beat-preview-operator-instruction-v1`.

Latest newsroom minimal animated explanation beat visual integration gap fix decision (2026-06-30 JST):
`newsroom_minimal_animated_explanation_beat_preview_gap_v1_2026_06_29`
records the user-side v1 preview observation for
`_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v1.ymmp`.
The file opened and the character nod animation was visible, but no card-like,
overlay-like, subtitle, or explanation text element was visible. The actual
structure audit confirms `GroupItem=8` and `ImageItem=8` only; there is no
`TextItem` or `ShapeItem` in v1. This means the previous integrated beat
contract was not fully materialized in the YMM4-visible scene. The primary root
cause is `contract_only_not_materialized`; the contributing factor is
`overlay_role_readback_only`.

The tracked artifacts are
`samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_preview_gap_v1.json`,
`docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_PREVIEW_GAP_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_visual_integration_gap_fix_v1.json`,
and
`docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_VISUAL_INTEGRATION_GAP_FIX_V1_2026-06-29.md`,
with implementation/tests in
`src/pipeline/newsroom_minimal_animated_explanation_beat_visual_gap_fix.py` /
`tests/test_newsroom_minimal_animated_explanation_beat_visual_gap_fix.py`.
The ignored local v2 probe exists at
`_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v2_visible_integration.ymmp`;
it is verified present on this host, verified ignored by `.gitignore` `_tmp/`,
and must remain untracked/uncommitted. V2 copies the v1 animation items
unchanged and adds one full-duration plain `TextItem` diagnostic explanation
overlay. Readback passes with `TextItem=1`, `GroupItem=8`, `ImageItem=8`,
visible text/overlay item count `1`, and animation item count `16`. This
decision did not tune nod speed, expression timing, or primitive motion; did
not create an animation-only probe; did not launch YMM4 from the Agent; did not
render, stage/commit `.ymmp`, generate media/audio/TTS, fetch real RSS/news or
external media, redesign cards, create polished visual cards, continue dense
script work, claim production/public readiness, or claim audience/order
acceptance. The selected next axis is
`newsroom-minimal-animated-explanation-beat-v2-preview-operator-instruction-v1`.

Latest newsroom minimal animated explanation beat mainline proof decision (2026-06-30 JST):
`newsroom_minimal_animated_explanation_beat_mainline_v1_2026_06_29`
returns the background animation work to a mainline explanation beat instead of
continuing primitive or animation-only tuning. The proof binds one review-only
diagnostic line to narration intent, subtitle/readback role, existing minimal
label/readback overlay semantics, source-boundary role, and the frozen MVP
background animation accent policy. The animation remains subordinate to the
explanation: stable pose, one expression event tied to the key phrase, one
short nod/reaction, and return to stable pose.

The tracked artifacts are
`samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_mainline_v1.json`,
`docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_MAINLINE_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_contract_v1.json`,
and
`docs/verification/NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_V1_2026-06-29.md`,
with implementation/tests in
`src/pipeline/newsroom_minimal_animated_explanation_beat.py` /
`tests/test_newsroom_minimal_animated_explanation_beat.py`. The ignored local
YMM4 representation candidate exists at
`_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v1.ymmp`;
it is derived from the known minimal integrated scene route, verified present
on this host, verified ignored by `.gitignore` `_tmp/`, and must remain
untracked/uncommitted. Structural readback passes with a 720-frame /
12.0-second timeline, `GroupItem=8`, `ImageItem=8`, no unexpected item types,
and semantic checks confirming narration/subtitle/readback binding, minimal
overlay role, frozen animation policy, source-boundary preservation, and no
render/audio dependency. This decision did not launch YMM4 from the Agent,
render, stage/commit `.ymmp`, create media/audio/TTS, fetch real RSS/news or
external media, redesign cards, continue dense script work, claim production or
public readiness, or claim audience/order acceptance. The selected next axis is
`newsroom-minimal-animated-explanation-beat-preview-operator-instruction-v1`:
prepare one bounded preview instruction for the verified integrated local
target; if another preview is not needed, return to
`newsroom-rss-dry-run-to-animated-explanation-beat-v1`.

Latest newsroom background animation MVP accent freeze and mainline return decision (2026-06-30 JST):
`newsroom_background_animation_mvp_freeze_v1_2026_06_29` records the user-side
preview readback for the existing ignored local minimal integrated scene probe
at
`_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp`.
The user opened the file successfully, saw an expression change, and then saw a
nod-like motion. That is sufficient for MVP accent-layer acceptance with
boundary: the animation layer is accepted as a small support accent, not as
production animation quality, render proof, public readiness, or audience/order
acceptance.

The tracked artifacts are
`samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_preview_observation_v1.json`,
`docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json`, and
`docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MVP_FREEZE_V1_2026-06-29.md`,
with implementation/tests in
`src/pipeline/newsroom_background_animation_mvp_freeze.py` /
`tests/test_newsroom_background_animation_mvp_freeze.py`. The frozen policy
allows stable pose, one expression event tied to a scene beat, one short
nod/reaction after that event, and return to stable pose. It disables body
forward/back movement, repeated nodding, mechanical expression cycling, speech
balloons, full chaban scenes, animation-only probe loops, and tempo-only probe
loops by default. This decision did not create another `.ymmp`, launch YMM4
from the Agent, render, stage/commit `.ymmp`, create media/audio/TTS, modify
card assets, continue dense script work, fetch real RSS/news or external
reference video, or claim production/public/order/audience acceptance. The
selected next axis is
`newsroom-minimal-animated-explanation-beat-in-mainline-pipeline-v1`: attach
the frozen MVP accent policy to a real explanation beat / YMM4 scene route in
the mainline pipeline instead of reopening primitive-only animation work.

Latest newsroom background animation minimal integrated scene operator-surface decision (2026-06-30 JST):
`newsroom_background_animation_minimal_integrated_scene_contract_v1_2026_06_29`
implements the next slice after the stop-loss policy by creating one integrated
review-only explanation beat. The local ignored probe exists at
`_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp`;
it is generated from the known `samples/nod_head.ymmp` route, verified present
on this host, verified ignored by `.gitignore` `_tmp/`, and must remain
untracked/uncommitted. The scene is 720 frames / 12.0 seconds at 60 fps: stable
start pose, one expression event tied to the key phrase, one short
nod/reaction, and stable end pose. It deliberately omits lateral emphasis,
speech balloons, card redesign, full chaban acting, and body forward/back
movement.

The tracked artifacts are
`samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_contract_v1.json`,
`docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_CONTRACT_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_probe_v1.json`,
and
`docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_PROBE_V1_2026-06-29.md`,
plus the operator surface
`samples/_probe/newsroom_handoff/background_animation_minimal_integrated_scene_operator_instruction_v1.json`
and
`docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_OPERATOR_INSTRUCTION_V1_2026-06-30.md`,
with implementation/tests in
`src/pipeline/newsroom_background_animation_minimal_integrated_scene.py` /
`tests/test_newsroom_background_animation_minimal_integrated_scene.py`.
Structural readback passes with `GroupItem=8`, `ImageItem=8`, four segments,
one expression event, one nod/reaction, all parent X routes fixed at `-96.0`,
no unexpected item types, and semantic checks pass. This is integrated-scene
structure proof only: visual quality is pending a single freeform user preview,
and no production/public/order/audience acceptance is claimed. This decision
did not launch YMM4 from the Agent, render, stage/commit `.ymmp`, create
media/audio/TTS, modify card assets, continue dense script work, fetch real
RSS/news or external reference video, or reopen primitive-only tempo/angle/
expression tuning. The previous scene choreography probe is classified as
`insufficient_too_abstract` for another preview because it has already served
as primitive-feasibility evidence and the active surface is now the integrated
explanation beat. No duplicate `.ymmp` was created for the operator surface.
The selected next axis is one freeform operator preview of the verified local
minimal integrated scene target; the operator instruction asks only three
look-for questions and requests no render, screenshot, production/public
judgment, Git operation, `.ymmp` commit, audio/TTS, RSS/news fetch, or card
redesign.

Latest newsroom background animation stop-loss and minimal integrated scene plan decision (2026-06-29 JST):
`newsroom_background_animation_mvp_policy_v1_2026_06_29` records the latest
user-side scene choreography preview observation and converts it into an MVP
stop-loss policy. The user observation is preserved as: YMM4 opened the scene
choreography probe, the scene is partially coherent rather than fully
incoherent, expression changes and nodding are visible, earlier forward/back
movement is mostly gone, unstable movement remains near the angry expression,
final animation quality is not accepted, and the primitive tuning loop risk is
high. This decision stops further primitive-only tempo, angle, or expression
iteration unless an integrated scene later proves a specific primitive is
blocking.

The tracked readback, policy, and plan artifacts are
`samples/_probe/newsroom_handoff/yukkuri_animation_scene_preview_observation_v1.json`,
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_SCENE_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/background_animation_mvp_policy_v1.json`,
`docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MVP_POLICY_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/background_animation_integration_plan_v1.json`,
and
`docs/verification/NEWSROOM_BACKGROUND_ANIMATION_INTEGRATION_PLAN_V1_2026-06-29.md`,
with implementation/tests in
`src/pipeline/newsroom_background_animation_mvp_policy.py` /
`tests/test_newsroom_background_animation_mvp_policy.py`. The MVP default
allows stable pose, one expression event, one short nod/reaction, and optional
small lateral emphasis only when justified. It disables repeated nodding,
mechanical expression cycling, body forward/back motion, complex speech
balloons, and full chaban scenes by default. The selected next axis is
`newsroom-background-animation-minimal-integrated-scene-probe-v1`: a later
10-20 second integrated scene with one actual explanation beat, minimal
existing card/overlay, one expression event, one nod/reaction, no default body
forward/back movement, and one freeform preview only. This decision did not
launch YMM4 from the Agent, render, create or stage `.ymmp`, create
media/audio/TTS, modify cards, continue dense-script work, fetch real RSS/news
or external reference video, or claim production/public/order/audience
acceptance. If that integrated scene still feels bad, the default is to freeze
animation as minimal accent and return to RSS/story integration.

Latest newsroom yukkuri v4 tempo default policy and scene-beat route decision (2026-06-29 JST):
`newsroom_yukkuri_animation_scene_choreography_contract_v1_2026_06_29`
records the latest user-side v4 tempo sweep observation and exits the
primitive-only fast/slow loop. The preserved observation is that `0.75s` looks
the most natural, the best duration depends on the scene, `1.0s` is within
acceptable range, `0.5s` is within acceptable range, and no production/public/
render approval was given. The active tempo default policy is `0.75s` /
45 frames at 60 fps for default light reenactment beats. `0.5s` / 30 frames is
kept for quick reaction, punch, or short emphasis; `1.0s` / 60 frames is kept
for slower explanatory or readability-heavy moments; and `1.5s` / 90 frames is
only an upper comparison or special slow-scene case. Render/export remains
unnecessary because the current decision is tempo policy and scene-beat
integration, not render mechanics.

The tracked readback and contract artifacts are
`samples/_probe/newsroom_handoff/yukkuri_animation_v4_tempo_sweep_observation_v1.json`,
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_V4_TEMPO_SWEEP_OBSERVATION_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/yukkuri_animation_scene_choreography_contract_v1.json`,
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_SCENE_CHOREOGRAPHY_CONTRACT_V1_2026-06-29.md`,
and
`samples/_probe/newsroom_handoff/yukkuri_animation_scene_choreography_probe_v1.json`,
with implementation/tests in
`src/pipeline/newsroom_yukkuri_animation_scene_choreography.py` /
`tests/test_newsroom_yukkuri_animation_scene_choreography.py`. The ignored
local scene probe exists at
`_tmp/newsroom_manual_probe/yukkuri_animation_scene_choreography_probe_v1.ymmp`
and must remain untracked/uncommitted. It is a 1080-frame / 18-second coherent
mini-scene, not a tempo comparison: neutral listening pose, question/reaction
cue, one short acknowledgement nod, reasoned caution expression, one small
intentional nudge, and return to stable explanation pose. Structural readback
passes with `GroupItem=16`, `ImageItem=16`, one meaningful nod, one small
intentional move, reasoned expression changes, and stable `X=-96` anchor
continuity. This decision did not launch YMM4 from the Agent, render,
stage/commit `.ymmp`, create media/audio/TTS, modify cards, continue
dense-script work, fetch real RSS/news or external reference video, or claim
production/public/order/audience acceptance. The next default axis is
`newsroom-yukkuri-animation-scene-beat-integration-v1`: apply the tempo policy
inside an actual short scene/beat structure rather than running another raw
primitive tempo sweep by default.

Latest newsroom yukkuri v3 observation and v4 tempo sweep probe decision (2026-06-29 JST):
`newsroom_yukkuri_animation_tempo_sweep_contract_v1_2026_06_29` records the
user-side v3 preview observation and replaces single-value tempo tweaking with
one ignored local comparison probe. The normalized observation is that the v3
probe is shorter but still floaty and slow; the user suggested starting around
1 second, so continuing one fast/slow value at a time is now the wrong
bottleneck. Render/export remains unnecessary because the current decision is
tempo band selection, not render mechanics.

The tracked readback and contract artifacts are
`samples/_probe/newsroom_handoff/yukkuri_animation_v3_preview_observation_v1.json`,
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_V3_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/yukkuri_animation_tempo_sweep_contract_v1.json`,
and
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_TEMPO_SWEEP_CONTRACT_V1_2026-06-29.md`,
with implementation/tests in
`src/pipeline/newsroom_yukkuri_animation_tempo_sweep.py` /
`tests/test_newsroom_yukkuri_animation_tempo_sweep.py`. The ignored local v4
probe exists at
`_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp`
and must remain untracked/uncommitted. It compares 30, 45, 60, and 90 frame
bands at 60 fps (0.5, 0.75, 1.0, and 1.5 seconds), preserves the v2/v3
`X=-96` anchor policy, covers `head_nod`, `small_position_move`,
`character_entrance_exit`, and `expression_swap` in every band, and has
structural readback pass. The expected default candidate is 60 frames / 1.0
second. This decision did not launch YMM4 from the Agent, render, stage/commit
`.ymmp`, create media/audio/TTS, modify cards, continue dense-script work,
fetch real RSS/news or external reference video, or claim production/public/
order/audience acceptance. The next default axis is
`newsroom-yukkuri-animation-tempo-sweep-preview-operator-instruction-v1`.

Latest terminal resume remote sync handoff decision (2026-06-29 JST):
`newsroom_terminal_resume_remote_sync_handoff_v1_2026_06_29` persists the
current cross-terminal restart context before reflecting local state to
`origin/master`. The repo was clean and aligned with `origin/master` at
`6b66f03` before this handoff. The new tracked context is
`samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v1.json`
and
`docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V1_2026-06-29.md`,
with pointers in `docs/runtime-state.md` and this decision log. This slice does
not alter product code or executable contracts.

The active production context remains the yukkuri v3 tempo-fix preview gate:
v2 improved motion connection and shared-anchor continuity, the remaining
actionable issue is slow tempo, and v3 shortens each beat to 180 frames / 3
seconds for a 900-frame / 15-second ignored local probe. The host-local probe at
`_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp`
exists on the authoring machine and is ignored through `.gitignore` `_tmp/`, so
it must remain untracked and uncommitted. No Agent-side YMM4 launch,
render/export pass, `.ymmp` stage/commit, media/audio/TTS generation, real
RSS/news fetch, external reference-video fetch, production/public readiness
claim, or audience/order acceptance claim occurred. The next default axis is
`newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1`.

Latest newsroom yukkuri v2 preview readback and v3 tempo-fix decision (2026-06-29 JST):
`newsroom_yukkuri_animation_tempo_contract_v1_2026_06_29` records the user-side
preview observation of the v2 motion-fix probe and converts it into a tempo
contract. V2 improved anchor continuity and segment connection; no new X jump
or major visual breakage was reported. The remaining actionable issue is
tempo: motion still feels very slow. Render/export remains unnecessary for this
stage because the bottleneck is preview tempo calibration, not render mechanics.

The tracked readback and tempo artifacts are
`samples/_probe/newsroom_handoff/yukkuri_animation_v2_preview_observation_v1.json`,
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_V2_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/yukkuri_animation_tempo_contract_v1.json`, and
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_TEMPO_CONTRACT_V1_2026-06-29.md`,
with implementation/tests in
`src/pipeline/newsroom_yukkuri_animation_tempo_contract.py` /
`tests/test_newsroom_yukkuri_animation_tempo_contract.py`. The ignored local v3
probe exists at
`_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp`
and must remain untracked/uncommitted. It preserves v2 anchor/facing fixes,
keeps the GroupItem/ImageItem structure, halves beat length from 360 frames /
6 seconds to 180 frames / 3 seconds, shortens total probe length to 15 seconds,
and keeps head neutral return and `X=-96` nudge anchors. This decision did not
launch YMM4 from the Agent, render, stage/commit `.ymmp`, create media/audio/TTS,
modify cards, continue dense-script work, fetch real RSS/news or external
reference video, or claim production/public/order/audience acceptance. The next
default axis is
`newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1`.

Latest newsroom yukkuri primitive preview observation and v2 motion-fix decision (2026-06-29 JST):
`newsroom_yukkuri_animation_motion_contract_v1_2026_06_29` records the first
user-side preview observation of the ignored local primitive probe and converts
it into a motion-quality contract. The v1 probe opened in YMM4, the character
was visible, head/body attachment had no major breakage, expressions switched,
and animation was visible. The actionable warnings are motion speed, broad
centerward X travel that reads as backward movement, underspecified
facing/orientation, X anchor discontinuity between primitive segments, and a
head nod that is too slow. Render/export was not checked and is not required at
this point because the bottleneck is preview-level motion behavior, not render
mechanics.

The tracked readback and contract artifacts are
`samples/_probe/newsroom_handoff/yukkuri_animation_primitive_preview_observation_v1.json`,
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PREVIEW_OBSERVATION_V1_2026-06-29.md`,
`samples/_probe/newsroom_handoff/yukkuri_animation_motion_contract_v1.json`, and
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_MOTION_CONTRACT_V1_2026-06-29.md`,
with implementation/tests in
`src/pipeline/newsroom_yukkuri_animation_motion_contract.py` /
`tests/test_newsroom_yukkuri_animation_motion_contract.py`. The ignored local
v2 probe exists at
`_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp`
and must remain untracked/uncommitted. It is derived from tracked
`samples/nod_head.ymmp`, keeps the GroupItem/ImageItem structure, shortens the
timeline to 30 seconds, uses bounded neutral side entry/exit, carries `X=-96`
as the shared anchor across adjacent beats, and makes head nods return to
neutral through `0 -> negative -> 0` rotation routes. This decision did not
launch YMM4 from the Agent, render, stage/commit `.ymmp`, create media/audio/TTS,
modify cards, continue dense-script work, fetch real RSS/news or external
reference video, or claim production/public/order/audience acceptance. The next
default axis is
`newsroom-yukkuri-animation-primitive-v2-preview-operator-instruction-v1`.

Latest newsroom yukkuri animation primitive probe materialization decision (2026-06-28 artifact date; recorded 2026-06-29 JST):
`newsroom_yukkuri_animation_primitive_probe_materialization_v1_2026_06_28`
creates the previously reserved ignored local probe target at
`_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp`. The
tracked readback is
`samples/_probe/newsroom_handoff/yukkuri_animation_primitive_probe_materialization_v1.json`,
with the human readback in
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PROBE_MATERIALIZATION_V1_2026-06-28.md`
and implementation/tests in
`src/pipeline/newsroom_yukkuri_animation_primitive_probe_materialization.py` /
`tests/test_newsroom_yukkuri_animation_primitive_probe_materialization.py`.

The materialized local `.ymmp` is derived from tracked `samples/nod_head.ymmp`
proof items, not from a zero-start YMM4 project. The builder clones the
GroupItem/ImageItem structure and applies only bounded Frame/Length,
current-host FilePath, expression image, parent X-position, and head Rotation
changes. Structural readback passes with a 60 fps / 3600-frame timeline,
20 items, `GroupItem=10`, `ImageItem=10`, and no unexpected item types. The
probe covers the four previously pass-status primitives: `head_nod`,
`expression_swap`, `character_entrance_exit`, and `small_position_move`.
`speech_balloon` remains omitted/partial because the repo has ShapeItem/TextItem
routes but no dedicated speech-balloon template or visual pass. The local probe
exists on the current host and `git check-ignore -v` resolves it through
`.gitignore` `_tmp/`, so it must remain untracked and uncommitted. The prior
primitive-proof builder is kept slice-static so the later local probe existence
does not mutate that historical readback. No YMM4 launch, render, `.ymmp`
stage/commit, audio/TTS, card modification, real RSS/news fetch, external
reference-video fetch, production/public readiness claim, or audience/order
acceptance claim occurred. The next default axis is
`newsroom-yukkuri-animation-primitive-render-smoke-v1`, but only after an
operator instruction sheet is created for opening/rendering the ignored local
probe.

Latest newsroom yukkuri animation primitive proof decision (2026-06-28 artifact date; recorded 2026-06-29 JST):
`newsroom_yukkuri_animation_primitive_proof_v1_2026_06_28` converts the
background animation format direction into a no-render structural proof for
the first primitive set. The new proof artifacts are
`samples/_probe/newsroom_handoff/yukkuri_animation_primitive_proof_v1.json` and
`samples/_probe/newsroom_handoff/yukkuri_animation_scene_beat_probe_v1.json`,
with human readbacks in
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PROOF_V1_2026-06-28.md`
and
`docs/verification/NEWSROOM_YUKKURI_ANIMATION_SCENE_BEAT_PROBE_V1_2026-06-28.md`,
plus implementation/tests in
`src/pipeline/newsroom_yukkuri_animation_primitive_proof.py` /
`tests/test_newsroom_yukkuri_animation_primitive_proof.py`.

The proof selects `head_nod`, `expression_swap`, `character_entrance_exit`,
`small_position_move`, and `speech_balloon`. The first four are structurally
provable from tracked repo evidence: `samples/nod_head.ymmp`, expression PNGs
plus face-map/body assets, skit-group templates/registry, and
`samples/group_motion_map.example.json`. `speech_balloon` remains `partial`
because ShapeItem/TextItem routes are documented but no dedicated balloon
template or visual pass exists. The scene beat probe maps five narration roles
to primitives without creating a dense script rewrite. This slice intentionally
did not create the optional ignored probe `.ymmp`; the path
`_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp` is
recorded as ignored/missing for the next gate. No YMM4 launch, render,
`.ymmp` stage/commit, audio/TTS, card modification, real RSS/news fetch,
external reference-video fetch, production/public readiness claim, or actual
audience/order acceptance claim occurred. Because four primitives pass
structurally, the next default axis is
`newsroom-yukkuri-animation-primitive-render-smoke-v1`; that next slice must
first create or verify an ignored local primitive probe target and keep render
behind an explicit gate.

Latest newsroom yukkuri background animation format spec decision (2026-06-28 artifact date; recorded 2026-06-29 JST):
`newsroom_yukkuri_background_animation_format_spec_v1_2026_06_28` records the
user correction that the main format is still `yukkuri_explainer`; the missing
core is a supportive background reenactment/light animation PV layer, not
dialogue-only chaban, not more text density, and not card-only polish. The new
spec, inventory, and recovery audit artifacts are
`samples/_probe/newsroom_handoff/yukkuri_background_animation_format_spec_v1.json`,
`samples/_probe/newsroom_handoff/yukkuri_animation_primitive_inventory_v1.json`,
`samples/_probe/newsroom_handoff/prior_animation_asset_recovery_audit_v1.json`,
with human readbacks under `docs/verification/` and implementation/tests in
`src/pipeline/newsroom_yukkuri_background_animation_format_spec.py` /
`tests/test_newsroom_yukkuri_background_animation_format_spec.py`.

The audit found enough tracked repo-local evidence to avoid a recovery-only
slice first: expression PNGs, a body source, face-map bundles, `nod_head.ymmp`,
skit-group templates/registry, group-motion map, G-24 blueprint/readback
artifacts, and validator/placement/motion code/docs. The first animation proof
set should cover `head_nod`, `expression_swap`, `character_entrance_exit`,
`small_position_move`, and `speech_balloon`; the balloon route remains
unproven but can be tested as ShapeItem/TextItem without external media. This
slice intentionally did not launch YMM4, render, edit or commit `.ymmp`,
generate audio/TTS, regenerate cards, fetch real RSS/news, fetch/copy external
reference videos, stage media outputs, or claim production/public/order/audience
acceptance. The next default slice is
`newsroom-yukkuri-animation-primitive-proof-v1`.

Latest newsroom v0.1 dense script semantic audit and v2 rewrite decision (2026-06-26):
`newsroom_v0_1_dense_script_semantic_audit_v1_2026_06_26` records the latest
freeform user warning after YMM4 dense CSV import/save: the mechanics signal is
positive, but the v1 13-line script still feels like "just 13 text lines." The
decision treats that as a semantic script-quality gap, not as a render, YMM4,
or card-generation problem. The v1 dense source project exists as ignored
local evidence at
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp`
and remains outside git. The new audit artifact is
`samples/_probe/newsroom_handoff/v0_1_dense_script_semantic_audit_v1.json`,
with human readback in
`docs/verification/NEWSROOM_V0_1_DENSE_SCRIPT_SEMANTIC_AUDIT_V1_2026-06-26.md`
and implementation/tests in
`src/pipeline/newsroom_v0_1_dense_script_semantic_audit.py` /
`tests/test_newsroom_v0_1_dense_script_semantic_audit.py`.

The audit result is `semantic_delta_from_4_line_baseline=partial`; v1 improves
mechanics and proof inventory but remains weak on problem clarity, offer
clarity, viewer value, next-action clarity, line-role distinctness, and padding.
Therefore the same slice created `newsroom_v0_1_dense_script_package_v2_2026_06_26`,
`newsroom_v0_1_dense_caption_timing_plan_v2_2026_06_26`, and the force-added
UTF-8 BOM CSV at
`samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v2.csv`. V2 keeps
the diagnostic/fake/private boundary and 13-line / 68 second plan, but rewrites
around a requester problem, reviewable video draft offer, proof confidence
chain, unaccepted source/rights/narration limits, and a purpose-clarity next
action. This slice intentionally did not launch YMM4, render, edit or commit
`.ymmp`, regenerate cards, generate audio/TTS, fetch real RSS/news, use real
brands/URLs/screenshots, request a fixed review form, or claim production,
public, order, or audience acceptance. The next default slice is
`newsroom-v0.1-dense-v2-source-ymmp-operator-instruction-v1`: import the v2 CSV
in YMM4 and save
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v0_1_dense_source_v2.ymmp`
as ignored local source evidence before any v2 render proof.

Latest newsroom v0.1 dense script package decision (2026-06-26):
`newsroom_v0_1_dense_script_package_v1_2026_06_26` and
`newsroom_v0_1_dense_caption_timing_plan_v1_2026_06_26` implement the prior
script-density plan as a review-only 13-line source package. The new artifacts
are `samples/_probe/newsroom_handoff/v0_1_dense_script_package_v1.json`,
`samples/_probe/newsroom_handoff/v0_1_dense_caption_timing_plan_v1.json`,
`samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv`,
`docs/verification/NEWSROOM_V0_1_DENSE_SCRIPT_PACKAGE_V1_2026-06-26.md`, and
`docs/verification/NEWSROOM_V0_1_DENSE_SOURCE_YMMP_IMPORT_V1_2026-06-26.md`,
with implementation in `src/pipeline/newsroom_v0_1_dense_script_package.py`
and focused tests in `tests/test_newsroom_v0_1_dense_script_package.py`. The
package keeps the surface fake/review-only and maps the 68 second plan across
opening, mechanism, proof, boundary, and next-action segments. It improves the
local explanation gates from partial to pass for problem, offer, and next
action, and records `access_clear=pass` for the dense CSV current-host access
route, while keeping audience-fit proxy partial because no real viewer/order
acceptance was measured. This slice intentionally did not launch YMM4, render,
edit `.ymmp`, regenerate cards, generate audio/TTS, fetch real RSS/news, stage
media, request a structured answer, or claim production/public readiness. The
next default slice is
`newsroom-v0.1-dense-source-ymmp-operator-instruction-v1`: import the dense CSV
in YMM4 and save the ignored local dense source project before any dense render
proof or RSS dry-run planning.

Latest newsroom v0.1 explanation readiness and script density decision (2026-06-26):
`newsroom_v0_1_explanation_readiness_v1_2026_06_26` and
`newsroom_v0_1_script_density_plan_v1_2026_06_26` move the active bottleneck
from visual polish and render mechanics to explanation/adoption usefulness.
The current diagnostic mp4 exists locally and the pipeline has demonstrated
YMM4 script import, speaker binding, native yukkuri audio, diagnostic English
loanword handling, source `.ymmp` recreation from CSV, 68 second timing, card
PNG generation, YMM4 ImageItem placement, render output, benchmark-driven
visual refinement, and local artifact recovery. The new artifacts are
`samples/_probe/newsroom_handoff/v0_1_explanation_readiness_v1.json`,
`samples/_probe/newsroom_handoff/v0_1_script_density_plan_v1.json`,
`docs/verification/NEWSROOM_V0_1_EXPLANATION_READINESS_V1_2026-06-26.md`, and
`docs/verification/NEWSROOM_V0_1_SCRIPT_DENSITY_PLAN_V1_2026-06-26.md`, with
implementation in `src/pipeline/newsroom_v0_1_explanation_readiness.py` and
focused tests in `tests/test_newsroom_v0_1_explanation_readiness.py`. The
decision records explanation readiness as mixed: proof and boundary are clear,
but problem, offer, next action, and audience-fit proxy are only partial. The
current four dialogue lines over about 68 seconds are enough to prove mechanics
but too sparse to explain the value path; the plan targets 60-75 seconds, five
narration segments, and roughly 10-14 short lines. This slice intentionally did
not launch YMM4, render video, edit `.ymmp`, regenerate cards, create
audio/TTS, fetch real RSS/news, stage media, request a fixed form, claim
audience/order acceptance, or claim production/public readiness. The next
default slice is `newsroom-v0.1-script-density-implementation-plan-v1`; do not
prioritize full render automation before explanation/script density unless the
supervisor explicitly changes that axis.

Latest newsroom post-density refinement render smoke result readback decision (2026-06-26):
`newsroom_post_density_refinement_render_smoke_result_readback_v1_2026_06_26`
consumes the latest user freeform YMM4 observation after density-benchmarked
card refinement and records it as a diagnostic render-smoke pass. The new
readback artifacts are
`samples/_probe/newsroom_handoff/post_density_refinement_render_smoke_result_readback_v1.json`
and
`docs/verification/NEWSROOM_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-26.md`,
with implementation in
`src/pipeline/newsroom_post_density_refinement_render_smoke_result_readback.py`
and focused tests in
`tests/test_newsroom_post_density_refinement_render_smoke_result_readback.py`.
The normalized observation records that the card-placement YMM4 project was
opened, rendering completed, duration remains approximately 68 seconds, four
density-simplified cards are visible, information density is reduced at
diagnostic observation level, dialogue items and native audio are preserved,
and no timing/audio regression was reported. The decision does not reopen card
design, mechanics proof, or asset generation: no Agent YMM4 launch, Agent
render, `.ymmp` edit, SVG/PNG regeneration, audio/TTS generation, external
fetch, media staging, fixed review form, production/public readiness claim, or
actual audience acceptance claim occurred. Video readiness remains `6/7`;
visual density readiness is diagnostic pass. The next default slice is
`newsroom-internal-review-v0.1-reevaluation-card-v1`, because mechanics,
timing, audio, placement, and density-refinement render observation now pass at
diagnostic level and the next value is internal review against the simplified
surface.

Latest newsroom visual card density benchmarked refinement decision (2026-06-26):
`newsroom_visual_card_density_benchmarked_refinement_v1_2026_06_26` consumes
the density simplification spec and regenerates the current four diagnostic
card SVG/PNG assets under the existing stable `visual_cards_v1` paths. The new
readback artifacts are
`samples/_probe/newsroom_handoff/visual_card_density_benchmarked_refinement_v1.json`
and
`docs/verification/NEWSROOM_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_V1_2026-06-26.md`,
with implementation in
`src/pipeline/newsroom_visual_card_density_benchmarked_refinement.py` and
focused tests in
`tests/test_newsroom_visual_card_density_benchmarked_refinement.py`. The
applied decision is density-linked only: remove nonessential microcopy, merge
repeated labels, demote source/debug metadata, replace dense details with one
simple support marker where useful, increase whitespace around essential text,
and preserve role variation plus the review-only boundary without adding more
boxes or shrinking text. The local proxy recheck is
`proxy_status=materially_improved` with `fail_count=0`, `warning_count=0`, and
stable paths preserved; PNG export completed for all four cards. This slice did
not launch YMM4, render video, edit `.ymmp`, create audio/TTS/voice cache,
fetch external media, import real content, add a fixed review form, claim
production/public readiness, or claim actual audience acceptance. The next
default slice is
`newsroom-card-placement-post-density-refinement-render-smoke-v1`.

Latest newsroom visual density simplification spec decision (2026-06-26):
`newsroom_visual_density_simplification_spec_v1_2026_06_26` converts the prior
post-benchmarked density gate into explicit criteria for the next card change.
The new spec artifacts are
`samples/_probe/newsroom_handoff/visual_density_simplification_spec_v1.json`
and
`docs/verification/NEWSROOM_VISUAL_DENSITY_SIMPLIFICATION_SPEC_V1_2026-06-26.md`,
with implementation in
`src/pipeline/newsroom_visual_density_simplification_spec.py` and focused tests
in `tests/test_newsroom_visual_density_simplification_spec.py`. The spec
defines a per-card density budget: one dominant message, no more than one
headline, one primary sentence, one supporting note or diagram, two to three
meaningful labels, no essential meaning in tiny metadata, demoted/hidden
debug or source text, and a non-competing subtitle reserve. Future visual work
must use remove, merge, demote, visual-marker replacement, and whitespace
operations before changing style, and must not shrink text, add explanatory
boxes for existing boxes, introduce real brands/URLs/news visuals, convert
cards into complex YMM4 object graphs, or claim production/audience acceptance.
The next default slice is
`newsroom-visual-card-density-benchmarked-refinement-v1`. Use
`newsroom-visual-information-density-benchmark-v1` only if this spec is
insufficient as criteria, and use
`newsroom-visual-card-source-band-simplification-v1` only if the source/
subtitle band is the dominant actionable issue. This slice did not launch YMM4,
render video, edit `.ymmp`, regenerate SVG/PNG assets, generate audio/TTS,
fetch external material, request a fixed review form, or claim production/
public/audience acceptance.

Latest newsroom post-benchmarked visual observation density gate decision (2026-06-26):
`newsroom_post_benchmarked_visual_observation_density_gate_v1_2026_06_26`
records the post-benchmarked user observation as
`visual_density_issue_confirmed`, not as another local text-fit repair. The
new readback artifacts are
`samples/_probe/newsroom_handoff/post_benchmarked_visual_observation_density_gate_v1.json`
and
`docs/verification/NEWSROOM_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_V1_2026-06-26.md`,
with implementation in
`src/pipeline/newsroom_post_benchmarked_visual_observation_density_gate.py` and
focused tests in
`tests/test_newsroom_post_benchmarked_visual_observation_density_gate.py`.
Mechanics remain pass for the current diagnostic observation: four cards are
visible, native YMM4/yukkuri audio remains, dialogue item count is preserved,
and no timing/duration regression was reported. The visual finding is that the
post-benchmarked surface still has high information density and cognitive load:
unexpected rendered line count, tight text fit, small/source text tightness,
and format attention competing with content are now the relevant gate. This
slice did not launch YMM4, render video, edit `.ymmp`, regenerate SVG/PNG card
assets, generate audio/TTS, fetch external assets, request a fixed review form,
or claim production/public/audience acceptance. The next default axis is
`newsroom-visual-density-simplification-spec-v1`; use
`newsroom-visual-information-density-benchmark-v1` only if the existing
benchmark lacks enough density criteria. A later
`newsroom-visual-card-density-benchmarked-refinement-v1` is valid only after a
density spec or sufficient density criteria exist.

Latest newsroom source .ymmp recreation import pack decision (2026-06-26):
`newsroom_source_ymmp_recreation_import_pack_v1_2026_06_26` converts the
current local artifact gap into a user-executable YMM4 script-import recovery
step without fabricating `.ymmp` internals. The source project
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp` is an
ignored local artifact and is absent from this checkout, so later timing-patch
and card-placement regeneration cannot proceed from tracked repo state alone.
The new tracked package consists of
`samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv`,
`samples/_probe/newsroom_handoff/source_ymmp_recreation_import_pack_v1.json`,
`docs/verification/NEWSROOM_SOURCE_YMMP_RECREATION_IMPORT_PACK_V1_2026-06-26.md`,
`src/pipeline/newsroom_source_ymmp_recreation_import_pack.py`, and
`tests/test_newsroom_source_ymmp_recreation_import_pack.py`. The CSV is UTF-8
BOM, headerless, two-column `speaker,text`, and uses canonical source evidence:
speaker `ゆっくり霊夢` and the four diagnostic fake/review-only lines recorded
in `diagnostic_ymmp_structure_readback_v1.json`,
`diagnostic_ymmp_probe_packet_v1.json`, and the existing bound-speaker CSV.
This slice intentionally did not launch YMM4, render, generate/edit `.ymmp`,
generate audio/TTS, import media, fetch sources, change card assets/timing
strategy, request a structured user template, or claim production/public readiness. The
next action is user-side YMM4 `台本読込` and local save to
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`; after that
Codex can retry local timing-patch and card-placement `.ymmp` regeneration
while keeping `_tmp/` outputs ignored and unstaged.

Latest newsroom visual card benchmarked refinement decision (2026-06-26):
`newsroom_visual_card_benchmarked_refinement_v1_2026_06_26` consumes the prior
audience-fit benchmark evaluation failure and performs the allowed material
card refinement without changing the four-card mapping or stable asset paths.
The new readback artifacts are
`samples/_probe/newsroom_handoff/visual_card_benchmarked_refinement_v1.json`
and
`docs/verification/NEWSROOM_VISUAL_CARD_BENCHMARKED_REFINEMENT_V1_2026-06-26.md`,
with implementation in
`src/pipeline/newsroom_visual_card_benchmarked_refinement.py` and focused tests
in `tests/test_newsroom_visual_card_benchmarked_refinement.py`. The existing
audience-fit card generator now uses benchmarked wrap/clamp constraints:
headline max 2 lines, body max 3 lines, left-panel safe text width 702 px,
minimum meaningful font floor still 34 px, and short `SRC N/4` source labels
separated from the subtitle-safe reserve. The stable SVG/PNG assets and contact
sheet under `samples/_probe/newsroom_handoff/visual_cards_v1/` were
regenerated in place. The local proxy recheck is
`improved_no_material_static_failures` with `fail_count=0`; the only remaining
warnings are reference-unproven familiar grammar and 68 sec playback pacing,
which require later evidence and were not claimed here. This slice did not
launch YMM4, render video, edit or commit `.ymmp`, create audio/TTS/voice
cache, fetch external media/live YouTube, import real content, add a fixed
review form, claim production/public readiness, or claim actual audience
acceptance. The next default slice is
`newsroom-card-placement-post-benchmarked-refinement-render-smoke-v1`.

Latest newsroom audience-fit benchmark evaluation decision (2026-06-26):
`newsroom_audience_fit_benchmark_evaluation_v1_2026_06_26` applies the
benchmark from `visual_audience_fit_benchmark_v1.json` to the current four
diagnostic cards. The result artifacts are
`samples/_probe/newsroom_handoff/audience_fit_benchmark_evaluation_v1.json`
and
`docs/verification/NEWSROOM_AUDIENCE_FIT_BENCHMARK_EVALUATION_V1_2026-06-26.md`.
The evaluation records one material failure:
`text_clipping_or_wrapping`. Cards 3 and 4 visibly clip meaningful left-panel
text, while cards 1 and 2 crowd the same boundary. It also carries warnings
for glance readability, unproven reference familiarity, source/subtitle reserve
crowding, and 68 sec pacing density. Passing proxies are minimum meaningful
font size, one dominant message per card, role variation, diagnostic boundary
visibility, and no real brand/URL/public claim. This slice did not launch YMM4,
render video, edit `.ymmp`, regenerate SVG/PNG cards, generate audio/TTS,
fetch external material, import real media, stage media, claim production or
public readiness, or claim actual audience acceptance. The next default slice
is `newsroom-visual-card-benchmarked-refinement-v1`, limited to left-panel text
wrapping/fit and bottom source/subtitle reserve separation.

Latest newsroom visual audience-fit benchmark decision (2026-06-26):
`newsroom_visual_audience_fit_benchmark_v1_2026_06_26` turns the latest
audience-fit correction into a measurable proxy benchmark before any further
visual redesign. The benchmark artifacts are
`samples/_probe/newsroom_handoff/visual_audience_fit_benchmark_v1.json` and
`docs/verification/NEWSROOM_VISUAL_AUDIENCE_FIT_BENCHMARK_V1_2026-06-26.md`,
with the builder in
`src/pipeline/newsroom_visual_audience_fit_benchmark.py` and focused tests in
`tests/test_newsroom_visual_audience_fit_benchmark.py`. The decision preserves
the current state as improved but not audience-fit accepted: evidence remains
L1 user freeform direction plus local diagnostic screenshots/render
observations, while target viewer comprehension, retention/CTR, production
visual quality, and actual audience preference are unknown. The benchmark
defines proxy metrics for glance readability, clipping/wrapping, meaningful
font size, one dominant message per card, familiar explainer/TV/YouTube
grammar, no tiny metadata dependency, role variation, 68 sec pacing/density,
diagnostic boundary visibility, and absence of real brand/URL/public claims.
This slice did not launch YMM4, render video, edit `.ymmp`, regenerate card
assets, generate audio/TTS, fetch external material, import real media, stage
media, claim production/public readiness, or claim actual audience acceptance.
The next default slice is `newsroom-audience-fit-benchmark-evaluation-v1`.
Further visual refinement is allowed only after that evaluation identifies
concrete benchmark failures.

Latest newsroom visual card audience-fit remote handoff decision (2026-06-26):
`newsroom_visual_card_audience_fit_remote_handoff_2026_06_26` preserves the
restart context after
`93ebf62 feat: refine newsroom visual cards for audience fit`. Before writing
the handoff, `master` was aligned with `origin/master`
(`HEAD...origin/master = 0 0`) and the tracked worktree was clean. The
canonical handoff file is
`docs/verification/NEWSROOM_VISUAL_CARD_AUDIENCE_FIT_REMOTE_HANDOFF_2026-06-26.md`.
The preserved state is: latest review normalized to
`needs_audience_fit_refinement`, audience-fit SVG/PNG cards regenerated at
stable paths, bundled Python Pillow fallback used for PNG export, no YMM4
launch/render/`.ymmp` edit/audio/TTS/external fetch/media staging performed,
and production/public readiness still closed. Ignored local diagnostic
artifacts may exist under `_tmp/newsroom_manual_probe/` but are not repo
artifacts. The next default milestone is
`newsroom-card-placement-post-audience-fit-render-smoke-v1`; placement refresh
is only a fallback if stable PNG paths are not reusable.

Latest newsroom visual card audience-fit refinement decision (2026-06-26):
`newsroom_visual_card_audience_fit_refinement_v1_2026_06_25` consumes the
latest freeform visual review after the post-refinement package: the cards are
cleaner and modern, but still retain small text and read too much like a
polished SaaS/dashboard UI for a mainstream YouTube audience. The selected
correction axis is audience-fit visual language, not mechanics, timing, audio,
placement, real content, or production approval. New canonical readbacks are
`visual_card_audience_fit_review_readback_v1.json` and
`visual_card_audience_fit_refinement_v1.json`, with human docs in
`docs/verification/`. The four stable SVG/PNG paths under
`samples/_probe/newsroom_handoff/visual_cards_v1/` were regenerated in place
as diagnostic-only fake cards using larger plain labels, large-number/process/
check/status motifs, minimum visible text of `34` px, and a declared `132` px
display-number allowance. The contact sheet now previews the same
audience-fit surface. PNG export used the bundled Python Pillow fallback
because the `uv` runtime did not provide Pillow. This does not launch YMM4,
render video, edit `.ymmp`, generate audio/TTS, fetch external sources, import
real media, change dashboard/governance/freshness work, stage media, approve
production, or claim public readiness. Production visual quality, final design
system, post-audience-fit render proof, placement proof after this refinement,
real newsroom visuals, real content readiness, and production approval remain
outside accepted scope. The next default slice is
`newsroom-card-placement-post-audience-fit-render-smoke-v1`; use
`newsroom-yym4-card-asset-placement-refresh-v1` only if the ignored placement
project cannot reuse the stable PNG paths.

Latest newsroom card placement post-refinement render smoke package decision (2026-06-26):
`newsroom_card_placement_post_refinement_render_smoke_v1_2026_06_26`
converts the completed visual-card refinement into the next milestone-gated
observation package. The package confirms that the refined SVG/PNG cards are
present at stable paths and that the existing ignored placement project
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp`
still references all four regenerated PNG paths, so a placement refresh is not
the default next move. The package records the separate suggested output path
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_post_refinement_v1.mp4`
but does not create or retain render output. It defines an agent-owned
freeform result normalizer and classifier for the later observation, covering
project-open failure, render failure, duration mismatch, refined-card
visibility regression, readability/clipping regression, dialogue preservation,
native audio, and operator uncertainty. This does not launch YMM4, render,
edit `.ymmp`, generate audio/TTS, import real media, fetch external sources,
stage media, approve production, or claim public readiness. The next default
slice is
`newsroom-card-placement-post-refinement-render-smoke-result-readback-v1`
after a future observation; use
`newsroom-yym4-card-asset-placement-refresh-v1` only if the ignored placement
project no longer reuses the stable refined PNG paths.

Latest newsroom visual card design refinement remote handoff decision (2026-06-25):
`newsroom_visual_card_design_refinement_remote_handoff_2026_06_25` preserves
the current mainline restart context after
`92b7c92 feat: refine newsroom visual card design`. Before this handoff,
`master` was aligned with `origin/master` (`HEAD...origin/master = 0 0`) and
the tracked worktree was clean. The canonical handoff file is
`docs/verification/NEWSROOM_VISUAL_CARD_DESIGN_REFINEMENT_REMOTE_HANDOFF_2026-06-25.md`.
The preserved state is: internal review normalized to visual refinement needed,
mechanics/timing/native audio/render/card placement still diagnostic pass,
refined SVG/PNG card assets present at stable paths, and production/public
readiness still closed. Ignored local `.ymmp` and mp4 diagnostic artifacts may
exist under `_tmp/newsroom_manual_probe/` but are not repo artifacts. The next
default milestone remains
`newsroom-card-placement-post-refinement-render-smoke-v1`; placement refresh is
only a fallback if stable PNG paths are not reusable.

Latest newsroom visual card design refinement decision (2026-06-25):
`newsroom_visual_card_design_refinement_v1_2026_06_25` consumes the freeform
internal review result that accepted diagnostic mechanics but rejected the
visual readability baseline. Timing, native YMM4 audio, render, and card
placement remain diagnostic pass; the selected correction axis is external
visual card refinement. The bridge generator now produces four refined
fake/review-only `1920x1080` SVG cards with wrapped/clamped text, bounded
`28` to `54` px type, deliberate subtitle-safe reserve, removed debug-footer
clutter, and distinct role motifs for intro/summary, handoff/process,
claim/check, and source/status. The four committed PNGs were regenerated at
the same stable paths under
`samples/_probe/newsroom_handoff/visual_cards_v1/`, and the contact sheet was
updated. New canonical readbacks are
`internal_review_v0_1_result_readback_v1.json` and
`visual_card_design_refinement_v1.json`, with human docs in
`docs/verification/`. This does not launch YMM4, render, edit `.ymmp`,
generate audio/TTS, fetch external sources, import real media, approve
production, or claim public readiness. Production visual quality, final design
system, YMM4 placement proof after refinement, post-refinement render proof,
real newsroom visuals, real content readiness, production approval, and media
retention remain outside accepted scope. Video readiness remains `6/7`; visual
readiness is `7/7` diagnostic-refined; production readiness remains
low/diagnostic-only. The next default slice is
`newsroom-card-placement-post-refinement-render-smoke-v1`; use
`newsroom-yym4-card-asset-placement-refresh-v1` only if the stable PNG paths do
not hold in the ignored local placement project.

Latest newsroom internal review v0.1 prep decision (2026-06-25):
`newsroom_internal_review_v0_1_prep_v1_2026_06_25` packages the current
diagnostic 68 sec YMM4 video as an internal review v0.1 candidate without
launching YMM4, rendering, editing `.ymmp`, generating audio/TTS, importing
media, fetching external sources, or approving production/public use. The
package cites the established evidence chain: script/caption import, speaker
binding, native YMM4/yukkuri audio, 68 sec timing patch, external PNG card
assets, `ImageItem` card placement, card-placement render smoke, approximate
30 sec render time, and the closed production/public scope. The candidate is
`diagnostic_bound_speaker_probe_card_placement_v1.mp4`, duration `68` sec,
fake/review-only diagnostic content, four visual cards, four dialogue items,
and `YMM4_native_yukkuri_japanese` voice path. The review questions are
compact and freeform-friendly, focused on pacing, card comprehensibility,
subtitle/card safe area, v0.1 viability, and the single highest-value
improvement before real packet integration. This does not accept production
pacing, final visual design, final narration/script density, real newsroom
content, RSS/live ingest, rights/publication boundary, production export
settings, final artifact packaging, public readiness, or production approval.
Video readiness remains `6/7` until review is completed; visual readiness
remains `7/7` diagnostic; production readiness remains low/diagnostic-only.
The next default slice is `newsroom-internal-review-v0.1-operator-review-card`.
Further renders stay milestone-gated to material surface changes, explicit
internal review need, or a later real-packet dry run.

Latest newsroom card placement render smoke result decision (2026-06-25):
`newsroom_card_placement_render_smoke_result_readback_v1_2026_06_25` records
the user freeform card-placement render observation, with screenshot support,
as canonical diagnostic evidence. The ignored local card-placement project
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp`
opened in YMM4 `4.53.0.6` and rendered to
`diagnostic_bound_speaker_probe_card_placement_v1.mp4` at approximately
`00:01:08` / `68` sec, with a reported render time of about `30` sec. Four
dialogue/subtitle items remained visible, four cards (`Card 1/4` through
`Card 4/4`) were visible as external PNG card assets, and the preview surface
showed title/chips/source-caption/subtitle-safe-reserve elements with no
reported visible element breakage. No native audio, timing, subtitle/dialogue,
or card placement regression was reported. This closes the visual placement
render-smoke uncertainty at diagnostic level while preserving the boundary
that production visual quality, final design system, final narration/script
density, public video readiness, real newsroom visuals, real content readiness,
production approval, final export packaging, and publication readiness remain
not accepted. Video readiness remains `6/7` until internal review; visual
readiness advances to `7/7`; production readiness remains low/diagnostic-only.
The current render observation is consumed once. The next default slice is
`newsroom-internal-review-v0.1-prep`; additional renders should be
milestone-gated to internal review v0.1 or a material visual/timing/audio
surface change, not docs/readback changes.

Latest newsroom YMM4 card asset placement decision (2026-06-25):
`newsroom_yym4_card_asset_placement_probe_v1_2026_06_25` advances the
diagnostic visual lane from external asset bridge to structural YMM4 placement
proof without launching YMM4 or rendering. The four fake/review-only SVG cards
were deterministically rasterized to PNGs under
`samples/_probe/newsroom_handoff/visual_cards_v1/` using the local Pillow
SVG-subset renderer, then placed as `ImageItem` entries in the ignored local
copy
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp`.
The source and output `.ymmp` files remain under `_tmp/` ignore policy and are
not repo artifacts. The structural result is `pass`: total duration stays
`4080` frames / `68` sec, the four dialogue/native voice items and voice cache
fields are preserved, and card image items map to the existing caption rows at
`0-12s`, `12-24s`, `24-46s`, and `46-68s`. This preserves the prior native
YMM4 audio and timing evidence while continuing to reject direct YMM4 card
object graph construction, YMM4 text/shape reconstruction, external TTS,
production visual-quality claims, public video readiness, real newsroom
visuals, real content readiness, and production approval. Video readiness
remains `6/7`; visual readiness advances to `6/7`. The next default milestone
is `newsroom-card-placement-render-smoke-v1`, because the video surface has now
changed enough to justify one milestone-gated render smoke. Internal review
v0.1 prep remains later, after post-placement render observation is read back.

Latest newsroom visual card asset bridge decision (2026-06-25):
`newsroom_visual_card_asset_bridge_v1_2026_06_25` creates the first
diagnostic external card-asset bridge after the 68 sec timing/audio render
smoke passed. The bridge generates four fake/review-only `1920x1080` SVG cards
and a local HTML contact sheet under
`samples/_probe/newsroom_handoff/visual_cards_v1/`, mapped one-to-one to the
existing neutral caption/dialogue rows at `0-12s`, `12-24s`, `24-46s`, and
`46-68s`. This decision deliberately avoids rebuilding card layouts as complex
direct YMM4 object graphs: the placement contract is future image-asset import,
with `direct_yym4_card_object_graph=false` and
`yym4_text_shape_reconstruction=false`. Native YMM4 audio and the existing
timing strategy stay preserved. Accepted scope is limited to external
diagnostic card assets, the contact sheet, caption-row mapping, fake-content
safety, and suitability for a later bounded YMM4 placement probe. Not accepted:
production visual quality, final design system, YMM4 placement proof,
post-card render proof, public video readiness, real newsroom visuals, real
content readiness, or production approval. No YMM4 launch, render, `.ymmp`
edit, media import, audio/TTS generation, real source fetch, or media staging
was performed. Video readiness remains `6/7`; visual readiness is `4/7`; the
next default slice is `newsroom-yym4-card-asset-placement-probe-v1`, followed
by `newsroom-card-placement-render-smoke-v1` only after placement changes the
video surface enough to justify a milestone render.

Latest newsroom timing patch render smoke result decision (2026-06-25):
`newsroom_ymmp_timing_patch_render_smoke_result_readback_v1_2026_06_25`
records the user freeform post-patch render observation, with screenshot
support, as canonical diagnostic repo evidence. The patched ignored diagnostic
copy
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`
opened in YMM4 and rendered to
`diagnostic_bound_speaker_probe_timing_patch_v1.mp4` at `00:01:08` / `68` sec,
`1920x1080`, `60` fps, with an audio stream at `48kHz`. Four dialogue/subtitle
items remained visible, preview text included `Fake topic, review only.`, and
native YMM4/Yukkuri speech was present. The observed majority silence and
post-speech/timeline extension are accepted only as expected diagnostic sparse
timeline behavior, not as production pacing. This closes the 8 sec versus 68
sec uncertainty at diagnostic render-smoke level and advances video readiness
to `6/7`. Production readiness remains low/diagnostic-only: production pacing,
final narration pacing, final script density, visual layout quality, public
video readiness, production render readiness, real content readiness,
production approval, and external TTS adoption remain not accepted. The current
render observation is consumed once; no new render is needed for docs/readback
changes. The next default slice is `newsroom-visual-card-asset-bridge-v1`, using
external visual card assets generated from HTML/SVG/Canvas rather than complex
direct YMM4 object graph construction. The ignored `.ymmp` and mp4 stay under
`_tmp/` and must not be staged or committed.

Latest newsroom timing patch remote handoff decision (2026-06-24):
`newsroom_ymmp_timing_patch_remote_handoff_2026_06_24` preserves the
supervisor-accepted state after `a0a3485 feat: probe newsroom YMM4 timing patch`
and makes another-terminal restart unambiguous. The structural patch proof is
accepted: the ignored diagnostic copy
`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp`
now carries a `4080` frame / `68` sec surface at `60` fps, with dialogue frames
`0 / 720 / 1440 / 2760` and lengths `720 / 720 / 1320 / 1320`; native YMM4
speaker/text/voice fields remain preserved. The active gate is not more repo
implementation. It is one manual YMM4 milestone render smoke of that ignored
patched copy, followed by an agent readback slice
`newsroom-ymmp-timing-patch-render-smoke-result-readback-v1`. Before this
handoff docs update, `master` was fetched and confirmed at parity with
`origin/master` (`HEAD...origin/master = 0 0`). The handoff does not claim
post-patch render success, production render readiness, public video readiness,
visual layout readiness, production narration quality, real content readiness,
production approval, or permission to stage/commit `.ymmp` or media output.

Latest newsroom audio/TTS boundary handoff decision (2026-06-24):
`remote_handoff_after_newsroom_audio_tts_boundary_resume_2026_06_24`
preserves the post-`newsroom-audio-tts-boundary-v1` continuation context in
repo-local docs before handing off to another terminal. The active mainline
checkout is
`C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage`
on `master`; the sibling `NLMYTGen` checkout is on
`codex/baseball-bn08-script-beat-linkage` and was not used for this mainline
handoff. Before writing this handoff, `master` was fetched and confirmed at
`16dcadc docs: define newsroom audio tts boundary` with
`HEAD...origin/master = 0 0` and a clean tracked worktree. The resume check
confirmed all expected active artifacts for the audio/TTS boundary, tiny render
smoke result, timing strategy, and diagnostic `.ymmp` structure readback exist.
The carry-forward decision is to recommend
`newsroom-yym4-native-audio-path-proof-v1` as the next entry. The reason is that
tiny render smoke already passed, external TTS is closed for now, the saved
diagnostic `.ymmp` contains YMM4 voice fields / VoiceCache, and neutral `68` sec
timing patch work should not be mixed with unresolved audio/TTS responsibility.
The handoff does not claim audio presence, audio quality, TTS readiness,
production render readiness, public video readiness, visual layout readiness,
or production approval. It also did not launch YMM4, render, generate TTS/audio,
import media, edit/stage/commit `.ymmp` or media, or touch
dashboard/governance/freshness work.

Latest newsroom/YMM4 manual-result decision (2026-06-23):
`newsroom_yym4_manual_import_result_readback_v1_2026_06_23` records the
user/operator YMM4 manual import observation for the committed tiny script CSV
as a diagnostic-only repo readback. The result is `pass_with_warnings`, not a
production pass: YMM4 showed `4/4` dialogue rows and all text was visible after
manual speaker/character selection, using existing `ゆっくり霊夢`, with no
reported encoding/text/header/column issue and no reported error. Screenshot
evidence is referenced only as `provided_in_supervisor_thread`; no screenshot
file is introduced into the repo. The warning classification is
`manual_speaker_binding_required` with next axis `speaker_binding_policy`; TTS
remains non-ready because the operator did not explicitly perform a separate
TTS generation (`operator_did_not_explicitly_generate_tts`). Accepted scope is
only tiny `speaker,text` CSV import visibility, row text visibility, and manual
speaker binding observation. Not accepted: automatic speaker binding, TTS
readiness, render readiness, `.ymmp` readiness, production readiness, or public
video readiness. This decision introduces
`samples/_probe/newsroom_handoff/yym4_manual_import_result_readback_v1.json`,
`docs/verification/NEWSROOM_YYM4_MANUAL_IMPORT_RESULT_READBACK_V1_2026-06-23.md`,
`src/pipeline/newsroom_yym4_manual_import_result.py`, and focused coverage in
`tests/test_newsroom_yym4_manual_import_result.py`. The agent did not launch
YMM4, create/edit `.ymmp`, render, generate TTS/audio, import real media, fetch
external sources, or modify dashboard/governance/freshness work. Next
non-redundant axes are `newsroom-speaker-binding-policy-v1`,
`newsroom-yym4-import-readiness-after-manual-result-v1`, and
`newsroom-minimal-ymmp-boundary-decision-v1`.

Latest newsroom/YMM4 manual-check decision (2026-06-22):
`newsroom_yym4_manual_import_check_packet_v1_2026_06_22` closes the next
diagnostic handoff step after the tiny importable proof without launching YMM4
or claiming any operator result. Commit
`3dfafd2 docs: define newsroom YMM4 manual import check packet` is on
`origin/master` and records the manual check packet in
`samples/_probe/newsroom_handoff/yym4_manual_import_check_packet_v1.json`, the
blank operator result template in
`samples/_probe/newsroom_handoff/yym4_manual_import_result_template_v1.json`,
the human readback in
`docs/verification/NEWSROOM_YYM4_MANUAL_IMPORT_CHECK_PACKET_V1_2026-06-22.md`,
the builder in `src/pipeline/newsroom_yym4_manual_import_check_packet.py`, and
focused coverage in `tests/test_newsroom_yym4_manual_import_check_packet.py`.
The target remains the committed tiny CSV
`samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv`: UTF-8
BOM, no header, two columns (`speaker,text`), and four synthetic diagnostic
rows. `manual_check_status` remains `not_run`; no `.ymmp`, carrier, render,
TTS/audio, real media, real newsroom ingest, external fetch, production
approval, or public video readiness was created. The safe next move is human
operator evidence only: manually open YMM4, use the repo-known script import /
台本読み込み route only far enough to observe whether four rows/texts appear,
then fill the result template with `pass`, `pass_with_warnings`, `fail`, or
`blocked_by_operator_uncertainty`. If the operator cannot locate the import
route or YMM4 would require crossing into TTS/render/project-save work, record
operator uncertainty and improve the instructions instead of expanding the
pipeline.

Latest newsroom/video-readiness decision (2026-06-22):
`newsroom_episode_production_capsule_v1_2026_06_22` closes the pivot from
dashboard/governance maintenance back toward video-readiness without opening
real ingest or YMM4 transfer. Commit
`bbe5528 feat: define newsroom episode production capsule` is on
`origin/master` and records the diagnostic capsule in
`samples/_probe/newsroom_handoff/episode_production_capsule_v1.json`, the human
readback in
`docs/verification/NEWSROOM_EPISODE_PRODUCTION_CAPSULE_V1_2026-06-22.md`, the
builder in `src/pipeline/newsroom_episode_production_capsule.py`, and focused
coverage in `tests/test_newsroom_episode_production_capsule.py`. The adapted
packet is the episode identity; older slot/transfer readbacks were inspected
only as earlier chain evidence. The current recomputed state is validator
`passed`, G-28 slot-linkage `passed_with_warnings`, transfer planning
`blocked`, transfer status `blocked`, blocker count `13`, and unlock
requirement count `13`. This decision does not continue dashboard freshness or
status producer work, does not accept a real packet, fetch sources, open
RSS/Inoreader, access real URLs, download media, edit or generate `.ymmp`,
generate YMM4 carriers, render media, generate TTS/audio, approve rights,
approve production, or publish/upload output. Next safe action is supervisor
capsule review or a separate read-only Review Console episode preview slice.

Latest common-foundation cockpit remote decision (2026-06-18):
`common_foundation_cockpit_remote_verified_2026_06_18` closes the repeated
network-blocked retry loop. Live `ls-remote` now confirms
`origin/codex/common-foundation-hold-state-audit` at
`1b1cc8e4f6d0f43dd4662d9efd64887653862b5c`
(`docs(common-foundation): add cockpit dashboard review surface`). No
feature-branch push was needed because the remote already contained the
expected commit. The remote-review identity/access split is: dashboard
`docs/dashboard/index.html` via `scripts/operator/open_dashboard.ps1`; status
JSON `docs/dashboard/project-status.json` linked from the dashboard; screenshot
`docs/review/common-foundation-dashboard-2026-06-17.png` linked from the
dashboard/docs index; report template
`docs/_templates/operation-cockpit-report.md` as repo-relative reference. User
Git work remains none; later dashboard review, if requested, should be
freeform review only. This decision does not authorize real `codex exec`,
subprocess runner, stdin piping, runtime loop, external notification,
repo-root `.agent` runtime artifacts, `.agent/needs_human.json`, G-28, G-27,
GUI, YMM4, render, rights, production, publishing, ClipPipeGen, Newsroom, RSS,
OPML, Inoreader, NotebookLM, or `.ymmp` work.

Latest local-residue decision (2026-06-18):
`local_residue_quarantine_2026_06_18` keeps post-push local state out of
source history while preserving the re-entry context in tracked docs.
`edbdc45 fix: clarify pre-execution preview packet` is already on
`origin/master` (`HEAD...origin/master=0 0`). The local checkout now hides the
known residue in `.git/info/exclude`: `.claude/worktrees/` (local agent
worktree area), `.codex/hooks.json` and `.codex/hooks/` (local Codex hook
mirror; guardrails match tracked `.claude/hooks`), the stale
`docs/verification/COMMON-FOUNDATION-REVIEW-INDEX-2026-06-15.md` (later
refresh/discard candidate; current common-foundation branch head observed as
`1b1cc8e`), and `samples/2026-05-16.ymmp` (partial YMM4 sample with external
absolute paths, not a production carrier). None of these files should be
committed by `git add .`; none were deleted. If a future terminal needs one of
them, open a separate explicit lane first: common-foundation review refresh,
Codex hook policy, Claude worktree cleanup, or YMM4 artifact review.

Latest remote-sync decision (2026-06-17):
`remote_sync_handoff_2026_06_17` preserves the local continuation context in
tracked project files before publishing `master` for resume from another
terminal. The committed context includes the G-28 object catalog and review
protocol, Freeform Review / Long-Run Autonomy rules, docs cockpit cleanup,
`docs/LANE_REGISTRY.md`, `docs/LANE_ALIGNMENT_PROMPTS.md`, the local MkDocs
browser entry pages, and this handoff record. The root `CLAUDE.md` standalone
entry is removed; Claude Code now uses `.claude/CLAUDE.md` as a thin pointer
back to `docs/REPO_LOCAL_RULES.md`, while `AGENTS.md` remains the repo entry
pointer. The local MkDocs files are browsing aids only: `_local/` outputs stay
ignored and are not canonical source. The remaining `stash@{0}` is a local
duplicate of residue already applied into tracked files, so a different
terminal should not need it after pulling `master`. This decision does not
authorize `.ymmp` edits, renders, media / TTS, publishing, rights approval,
external asset intake, DB/auth/API contract changes, or real-runner execution.
Next safe restart is `git fetch --prune origin`, `git checkout master`,
`git pull --ff-only origin master`, then `AGENTS.md` ->
`docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`.

Latest G-28 decision (2026-06-12):
`g28_reference_layout_object_preset_revise_once_001` expands the reference
layout prototype pack from static screen mock review toward reusable layout
presets, object presets, and content slots. The new verification owner is
`docs/verification/G28-LAYOUT-PRESET-OBJECT-CATALOG-2026-06-11.md`. The review
hub `samples/_probe/g28/reference_layout_prototypes/index.html` now links to
`object_catalog.html` plus six content-first prototypes:
`image_annotation_simple`, `screenshot_callout`, `two_image_compare`,
`article_quote_card`, `asset_plus_caption`, and
`source_footage_annotated`. The object catalog records visual presets for
`image_slot`, `screenshot_slot`, `footage_slot`, `highlight_box`, `arrow`,
`leader_line`, `label_chip`, `callout_box`, `lower_third_telop`,
`source_note`, `quote_card`, `comparison_panel`, `table_row`,
`host_placeholder`, and `caption_reserve`, including allowed layout families,
parameters, YMM4 transfer cautions, and misuse risks. The additions are
self-contained HTML/CSS/SVG with explicit theme tokens, fixed `1920x1080`
canvases, visible subtitle reserve, local navigation, and no external images,
URLs, raw reference files, real screenshots, real map / satellite / company /
character / footage assets, audio, or TTS. `mechanism_diagram` remains
`causal_diagram_grammar_debt` and was not revised. This is not YMM4 transfer:
no `.ymmp`, builder, existing game-mechanics carrier, existing map-evidence
carrier, generated YMM4 artifact, render, production candidate, rights
approval, creative final acceptance, Newsroom, common foundation, G-27,
ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, external asset intake, or real
runner path was opened. Next safe action is human browser review from
`index.html`, then `object_catalog.html` if the chat-first digest is sufficient
to judge the preset system.

Latest G-28 decision (2026-06-12):
`g28_chat_first_visual_review_protocol_001` records the human review result for
the G-28 reference layout prototype pack and changes future visual review
reporting to a chat-first / accumulated review model. The HTML/SVG
visual-authoring-first route remains useful, but future G-28 visual artifact
reports must include a digest before asking the human to open HTML, YMM4, or
screenshot evidence. The digest must state artifact id, visible summary,
primary focus, layout grammar, object slots, fulfilled specs, known weak
points, open-file trigger, accumulated review tags, and next decision options.
The durable protocol is
`docs/verification/G28-CHAT-FIRST-VISUAL-REVIEW-PROTOCOL-2026-06-11.md`, and
the existing prototype pack record now points to it. Review levels are Level 1
chat-first digest, Level 2 optional visual check, and Level 3 accumulated rich
review grouped by tags / issue families after multiple artifacts accumulate.
`mechanism_diagram` is recorded as `causal_diagram_grammar_debt`: it is a
reviewable prototype, but not a YMM4 transfer candidate without later revision
or explicit accepted caveat because arrows, boxes, and causal payload are not
semantically coupled enough. This decision is docs-only: it does not edit HTML,
create or modify `.ymmp`, build YMM4 tooling, touch existing game-mechanics or
map-evidence carriers, render, approve production / rights / creative final
acceptance, process Newsroom, touch common foundation, reopen G-27, touch
ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, import external assets, or run a
real runner. Next safe action is to use the chat-first digest contract for the
next G-28 visual artifact report, or open accumulated rich review later by tags
such as `causal_diagram_grammar_debt`, `layout_system_debt`, `density_debt`,
`content_slot_gap`, `subtitle_reserve_risk`, and `transfer_candidate`.

Latest G-28 decision (2026-06-12):
`g28_reference_layout_prototype_path_checkout_audit_001` resolves the reported
missing `reference_layout_prototypes` folder as a local checkout / path sync
issue, not an artifact absence in the current repository state. In
`C:\Users\PLANNER007\NLMYTGen`, `git fetch --prune origin` advanced
`origin/master` from `1ab3903` to `c6f17b5`, and
`git pull --ff-only origin master` fast-forwarded `master` to
`c6f17b5 feat: add G-28 reference layout prototypes`. After the pull, branch
`master`, `HEAD=c6f17b5`, and `HEAD...@{u}=0 0`; `git status --porcelain=v1`,
`git status --porcelain=v1 -uno`, `git diff --name-only`, and
`git diff --cached --name-only` are empty. `git ls-tree` and `Get-ChildItem`
both show the eight expected files under
`samples/_probe/g28/reference_layout_prototypes/`: `index.html`,
`lecture_list.html`, `mechanism_diagram.html`, `map_evidence.html`,
`cluster_map.html`, `evidence_table.html`, `conversation_board.html`, and
`source_footage_frame.html`. The wrong `samples_probe` path is absent. The
old `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen` checkout path
was not present in this environment. The correct local review hub is
`C:\Users\PLANNER007\NLMYTGen\samples\_probe\g28\reference_layout_prototypes\index.html`.
Existing proof images should still be treated as earlier pipeline /
storyboard / GUI proof, not as the reference layout prototype pack. This audit
did not regenerate prototypes, edit HTML, create `.ymmp`, build a YMM4
builder, touch existing carriers, render, approve production / rights /
creative final acceptance, or touch Newsroom, common foundation, G-27,
ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, or real runner paths. Next safe
action is human browser review of the HTML pack.

Latest G-28 decision (2026-06-11):
`g28_reference_layout_prototype_pack_created_001` implements the safe
HTML/SVG visual-prototype-first route after the YMM4 coordinate-generation
method blocker. The created review hub is
`samples/_probe/g28/reference_layout_prototypes/index.html`, with seven fixed
1920x1080 self-contained prototypes: `lecture_list`, `mechanism_diagram`,
`map_evidence`, `cluster_map`, `evidence_table`, `conversation_board`, and
`source_footage_frame`. The packet owner is
`docs/verification/G28-REFERENCE-LAYOUT-PROTOTYPE-PACK-2026-06-11.md`.
The prototypes abstract layout grammar only; they do not include external
links, image paths, raw reference images, logos, third-party character
reproduction, real map or satellite imagery, source footage, audio, or TTS.
The route remains pre-YMM4-transfer and diagnostic: no `.ymmp` generation,
builder creation, existing carrier regeneration, render, production candidate,
rights approval, creative final acceptance, Newsroom, common foundation, G-27,
ClipPipeGen, RSS / OPML / Inoreader / NotebookLM, or real runner work is
approved by this decision. Next safe action is human browser review of the
HTML pack and a decision of `accept`, `accept_with_caveats`, `revise_once`,
`reject`, or `redesign_required`.

Latest G-28 decision (2026-06-11):
`g28_ymmp_coordinate_generation_method_blocker_001` records the human YMM4
review result for
`samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp`.
The decision is `redesign_required_generation_method_blocker`: the Map /
Evidence carrier is not accepted as a diagnostic candidate, and `revise_once`
is not appropriate. The issue is not a single carrier's local spacing defect.
It is a visual-authoring method blocker: direct script-coordinate `.ymmp`
construction can pass structural readback while still producing a weak review
surface. The tracked builder, `.ymmp`, readback, and report remain as negative
evidence / failed sample, but they must not be regenerated, micro-tuned, or used
as proof that this generation method is good enough for more G-28 carriers.
Readback pass is now explicitly limited to boundary / structure confirmation,
not visual-quality assurance. Stop the same coordinate-only YMM4 carrier
generation route as a visual authoring source. Safe future entries are a
human-authored YMM4 seed carrier, an HTML/SVG visual prototype approved before
YMM4 transfer, or a later bounded cross-screen layout-normalization review.
This is docs-only and does not change `.ymmp`, builders, samples, render,
production candidate state, rights, creative final acceptance, Newsroom, common
foundation, G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, real runner,
GUI, or `src`.

Latest G-28 decision (2026-06-11):
`g28_map_evidence_ymmp_diagnostic_carrier_created_001` advances the next
reviewable artifact after the game-mechanics `layout_system_debt` decision.
The game-mechanics YMM4 carrier is not tuned again. Instead,
`scripts/build_g28_map_evidence_ymmp_probe.js` converts the existing passed Map
/ Evidence skeleton into a self-contained ShapeItem/TextItem-only YMM4
diagnostic carrier candidate at
`samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp`, with
readback and report siblings. The readback passes as
`classification=pass_map_evidence_ymmp_diagnostic_carrier_created`,
`diagnostic_only=true`, `production_candidate=false`, caption reserve clear,
evidence surface in main canvas, three annotation slots, bounded source note,
non-focal hosts, external image / URL / source-footage / audio / TTS counts
zero, `render_output=false`, production / creative / rights approvals false,
and failures empty. The verification record is
`docs/verification/G28-MAP-EVIDENCE-YMMP-DIAGNOSTIC-CARRIER-PROBE-2026-06-11.md`.
This does not modify the game-mechanics carrier, create a production candidate,
render, approve rights, claim creative final acceptance, process Newsroom,
resume common foundation, revive G-27, touch ClipPipeGen, RSS, OPML, Inoreader,
NotebookLM, real runner / `codex exec`, GUI, or `src`. Next safe action is human
YMM4 review intake for the new Map / Evidence carrier.

Latest G-28 decision (2026-06-11):
`g28_game_mechanics_ymmp_batch_review_layout_system_debt_001` records the human
batch review result for
`samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`
as `layout_system_debt`. The current screen remains reviewable as a diagnostic
artifact, but the dominant issue is not single-label fitting. The issue is
layout-system debt: element centering, spacing regularity, and split-layout
generalizability are not stable enough to keep solving with same-screen
micro-tuning. The chosen direction is speed-first: stop further tuning on this
screen, produce more reviewable G-28 artifacts, and revisit the issue later in
a bounded cross-screen batch review or layout-normalization slice. Safe next
entries are Advance to another G-28 artifact / reviewable screen, Audit later
for layout normalization across screens, or Hold this screen as known
`layout_system_debt`. This is docs-only and does not modify `.ymmp`, builder,
samples, production candidate state, render, rights, creative final acceptance,
Newsroom, common foundation, G-27, ClipPipeGen, RSS, OPML, Inoreader,
NotebookLM, real runner / `codex exec`, GUI, or `src`.

Latest G-28 decision (2026-06-11):
`g28_game_mechanics_ymmp_batch_visual_review_protocol_001` switches the next
review of
`samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`
from individual label checking to a full-screen batch visual review protocol.
The durable packet is
`docs/verification/G28-GAME-MECHANICS-YMMP-BATCH-VISUAL-REVIEW-PACKET-2026-06-11.md`.
It preserves `27b4736 fix: align G-28 game mechanics YMM4 labels` as the
current known state: `画面上の結果` uses font size 38 with the inherited
rightward nudge removed; lower callouts use a common centered rule at font size
28; readback remains
`classification=pass_game_mechanics_ymmp_label_layout_fixed`,
`one_pass_targeted_fix=true`, and
`no_further_micro_tuning_recommended=true`. Those facts are no longer the whole
review request; they are checklist rows inside a batch decision surface covering
overall composition, focal-chain meaning, central priority, label fit,
callouts, readability, spacing, density, host role, caption reserve, eye flow,
generic transferability, YMM4 maintainability, and diagnostic usefulness. Human
return decisions are `accept`, `accept_with_caveats`, `revise_once`,
`layout_system_debt`, or `redesign_required`; only `must_fix` items can justify
one consolidated follow-up fix. This is docs-only and does not modify `.ymmp`,
builder, samples, render, production, rights, creative final acceptance,
Newsroom, common foundation, real-estate work, G-27, GUI, ClipPipeGen, RSS,
OPML, Inoreader, NotebookLM, `.claude/worktrees/`,
`samples/2026-05-16.ymmp`, or real runner / `codex exec` paths.

Latest G-28 decision (2026-06-11):
`g28_game_mechanics_ymmp_label_layout_fix_001` applies exactly one targeted
layout fix to the existing YMM4 diagnostic carrier candidate after human visual
review. The carrier path remains
`samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`.
The fix preserves the same carrier, variant, meaning structure, focal chain,
callouts, host role, and bottom caption reserve. It only removes the right
focal label's inherited rightward nudge, reduces that label to font size 38,
and applies one common centered callout label rule at font size 28. The
regenerated readback classifies the result as
`pass_game_mechanics_ymmp_label_layout_fixed`, records
`one_pass_targeted_fix=true`,
`no_further_micro_tuning_recommended=true`, and sets the next decision gate to
`accept_with_layout_caveat`. This remains diagnostic-only:
`production_candidate=false`, no render, no rights approval, no creative final
acceptance, and no external image / URL / source footage / audio / TTS. A later
batch visual review protocol supersedes the old two-target check and treats
those labels as part of the whole-screen checklist; do not keep tuning the same
screen.

Latest G-28 decision (2026-06-10): `g28_game_mechanics_ymmp_diagnostic_carrier_created`
creates a self-contained YMM4 diagnostic carrier candidate for the accepted
`game_mechanics_explanation` Lecture Diagram review surface. The generated
candidate lives at
`samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`
with readback/report siblings and verification record
`docs/verification/G28-GAME-MECHANICS-YMMP-DIAGNOSTIC-CARRIER-PROBE-2026-06-10.md`.
The readback passed as diagnostic-only / production-candidate false, ShapeItem
and TextItem only, with focal chain `入力操作` -> `内部ルール / 判定` -> `画面上の結果`,
callouts `操作感`, `判定 / 当たり判定`, `リスクとリターン`, non-focal hosts, bottom
caption reserve clear, external image / URL / source-footage / audio / TTS
counts all zero, and no render or production approval. This does not reopen
real-estate evidence, process Newsroom handoff material, revive G-27, advance
common foundation, or approve production / rights / creative final acceptance.
Next safe action is human YMM4 review intake only: carrier path, preview
screenshot, timeline screenshot, item/layer confirmation, bottom caption
safe-area evidence, and `accept` / `revise` / `reject`.

Latest common foundation decision (2026-06-15):
`common_foundation_status_input_audit_design_001` records a docs-only
repo-status input audit design on top of the earlier live status producer
contract. The design lives in
`docs/verification/COMMON-FOUNDATION-STATUS-INPUT-AUDIT-DESIGN-2026-06-15.md`
and defines the audit-facing common status object fields for branch, HEAD,
upstream, remote parity, tracked-only porcelain status, full porcelain status,
known-untracked allowlist matching, dirty state, staged diff, unstaged tracked
diff, runtime artifact state, needs-human state, checked authority docs,
execution policy snapshot, adapter id, observed timestamp, observer mode,
source/command provenance, and fail-closed reasons. It also records the
repo-adapter boundary: common core owns schema, normalization, provenance,
redaction, timestamp/staleness handling, fail-closed reason vocabulary, and the
rule that status input is not execution authority; NLMYTGen adapter policy owns
authority docs, known untracked residue, runtime artifact paths, execution
policy source, forbidden domains, and local artifact vocabulary. Live pre-edit
readback found `master`, upstream parity `0 0`, no tracked or staged diff,
known untracked residue limited to `.claude/worktrees/` and
`samples/2026-05-16.ymmp`, `.agent/reports/` and `.agent/logs/` containing only
`.gitkeep`, and no `.agent/needs_human.json`; the old `66be70d` HEAD assumption
was stale because this checkout was already at
`4746d81 docs: design live repo status producer`. This slice remains docs-only:
no real `codex exec`, `subprocess.run`, stdin piping, runtime worker loop,
external notification, runtime artifact creation, G-28 / G-27 / Newsroom /
ClipPipeGen / RSS / OPML / Inoreader / NotebookLM / `.ymmp` / render / rights /
production / publishing work was opened. Next safe action is Hold, or a
separately authorized stdout-only producer implementation proof that creates no
runtime artifacts and still cannot grant real-runner permission.

Latest common foundation decision (2026-06-13):
`live_repo_status_json_producer_design_001` records a docs-only contract for a
future machine-collected live repo status JSON producer. The design lives in
`docs/verification/LIVE-REPO-STATUS-JSON-PRODUCER-DESIGN-2026-06-13.md` and
defines fields for repo root, branch, HEAD, upstream parity, tracked/staged
dirty state, untracked entries, known-untracked allowlist match, runtime
artifact state, `.agent/needs_human.json` presence, inspected paths, command
provenance, timestamp, source provenance, adapter id, confidence/trust boundary,
and fail-closed status. This narrows the older `--repo-status-clean` operator
assertion by requiring future machine-collected evidence before a status object
is treated as preflight input. The producer remains only an observer/serializer:
it cannot grant execution permission, cannot set `safe_to_start_real_runner=true`,
cannot start real `codex exec`, cannot add `subprocess.run`, cannot pipe stdin,
cannot create a runtime worker loop, cannot send external notification, and
cannot write `.agent/reports`, `.agent/logs`, or `.agent/needs_human.json`.
Unknown, missing, parse-error, command-failure, dirty, staged,
unknown-untracked, unexpected runtime artifact, or needs-human-present state
must surface as `needs_human` or `blocked`, not pass. Common core keeps schema,
fail-closed semantics, redaction, provenance, timestamp, and operator readback;
repo adapter keeps authority docs, known untracked allowlist, allowed/blocked
paths, runtime artifact paths, repo-specific vocabulary, and forbidden domains.
NLMYTGen-specific YMM4 / `.ymmp` / G-28 / production vocabulary stays out of the
common core. This slice did not implement Python, runner behavior, runtime
artifact generation, G-28 / G-27 / Newsroom / ClipPipeGen / RSS / OPML /
Inoreader / NotebookLM / `.ymmp` / render / rights / production / publishing
work. Next safe action is Hold or a separately authorized stdout-only producer
implementation proof.

Latest common foundation decision (2026-06-10):
`pre_execution_dry_run_preview_hold_001` accepts the wording-refined preview as
holdable for cross-terminal restart. The check ran
`uv run python scripts/agent_orchestrator.py --worker audit --pre-execution-dry-run --timestamp hold-check --repo-status-clean`
after `8006349 fix: clarify dry-run preview wording` and found the stdout
review surface sufficient without opening files: repo-status source is labeled
as an operator-provided assertion not checked by the CLI, the report path is
planned only and not written, the outer plan-level preview and embedded raw
preflight card are distinct, and preflight allowed / `safe_to_start_real_runner`
remain review / eligibility signals rather than execution permission. Runtime
artifact state remains clean with only `.agent/reports/.gitkeep` and
`.agent/logs/.gitkeep`; `.agent/needs_human.json` is absent. This does not
implement real `codex exec`, `subprocess.run`, stdin piping, runtime worker
loop, external notification, worker report validation from a real run, `.agent`
runtime artifact creation, GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML,
Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing, or
release automation. Default next action is Hold; future work should enter
through a repo-status input audit, a narrow wording/readback correction if drift
appears, or a separately authorized docs-only real-runner consumption design.

Latest common foundation decision (2026-06-10):
`pre_execution_dry_run_preview_wording_refine_001` keeps the preview-only CLI
contract but tightens stdout wording so a human can review it without opening
supporting docs. The repo-status section now says an input is an
operator-provided assertion after external git checks and is not checked by this
CLI. The selected-plan section states that the report path is planned only and
is not written by the preview. The outer preview is described as a plan-level
review of the would-be worker run, while the embedded card is labeled as the raw
preflight result. The standalone raw preflight card now phrases `allowed` as
preflight-review-only and `safe_to_start_real_runner` as eligibility-only, not
execution permission. Redaction remains in place. This does not implement real
`codex exec`, `subprocess.run`, stdin piping, runtime worker loop, external
notification, worker report validation from a real run, `.agent` runtime
artifact creation, GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader,
NotebookLM, `.ymmp`, render, rights, production, publishing, or release
automation. Next safe action is human acceptance of the wording or a separate
repo-status input handling audit; real runner work still requires explicit
authorization.

Latest common foundation decision (2026-06-10):
`pre_execution_dry_run_preview_surface_and_repo_status_audit_001` verified the
preview-only dry-run surface and repo-status input handling after
`cf5df6c feat: add pre-execution dry-run preview`. The audit confirmed the
surface shows the selected worker, prompt source, schema, planned report path,
working directory, timeout, shell-free argv, repo-status summary, authority
summary, preflight pass/block state, reasons, inspected paths, embedded
preflight preview card, explicit boundary, and human next action, and that it
stops at stdout without writing runtime artifacts. It also confirmed dirty,
staged, and unknown-untracked status can be rendered as blocked reasons,
simultaneous repo-status inputs are rejected, and repo-external status JSON
paths fail closed. The audit tightened one safety gap: the outer Markdown
renderer now redacts credential-like values from operator-controlled display
fields such as timestamp-derived report paths and repo-status paths, matching
the raw preflight card's redaction posture. This does not implement real
`codex exec`, `subprocess.run`, stdin piping, runtime worker loop, external
notification, worker report validation from a real run, `.agent` runtime
artifact creation, GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader,
NotebookLM, `.ymmp`, render, rights, production, publishing, or release
automation. A later wording pass makes the operator-provided repo-status source,
planned-only report path, preview/card role split, and review-only preflight
allowance explicit in stdout.

Latest common foundation decision (2026-06-10):
`pre_execution_dry_run_preview_mvp_001` implements the preview-only CLI allowed
by the prior design review. `scripts/agent_orchestrator.py --pre-execution-dry-run`
now builds the existing shell-free execution plan, runs
`build_execution_preflight` in `dry_run_preview` mode, embeds the existing raw
preflight preview card, and prints one Markdown review surface to stdout. The
surface shows worker, prompt source, schema, planned report path, working
directory, timeout, argv preview, repo status summary, authority summary,
preflight pass/block state, `safe_to_start_real_runner`, reasons, inspected
paths, human next action, and the explicit boundary. The CLI may accept
`--repo-status-clean` as an operator-provided clean assertion after external git
checks, or `--repo-status-json` for a repo-local status object; it does not spawn
Git itself. This does not implement real `codex exec`, `subprocess.run`, stdin
piping, runtime worker loop, external notification, worker report validation
from a real run, `.agent` runtime artifact creation, GUI, G-28, Newsroom, G-27,
ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, `.ymmp`, render, rights,
production, publishing, or release automation. Tests now cover the allowed
preview, blocked repo-status reasons, CLI Markdown output, and preservation of
the no-real-execution sentinel. Next safe action is human review of the preview
surface or a focused audit of repo-status input handling; real runner work still
requires a separate explicit authorization.

Latest common foundation decision (2026-06-10):
`pre_execution_dry_run_flow_design_001_docs_only` adds
`docs/verification/PRE-EXECUTION-DRY-RUN-FLOW-DESIGN-2026-06-10.md` as the
human-visible design for a future pre-execution dry-run flow after the parked
preflight / operator-surface state. The design shows what a human must see
before any real runner exists or starts: selected worker, prompt source,
schema, planned report path, shell-free argv preview, working directory,
timeout, repo state, authority summary, `build_execution_preflight` result, raw
preflight preview card, inspected files, stop conditions, and decision options.
It explicitly keeps `safe_to_start_real_runner=true` as eligibility for a
separately authorized future runner slice, not execution permission. This
decision does not implement real `codex exec`, `subprocess.run`, stdin piping,
runtime worker loops, external notification, `.agent` runtime artifacts,
Python/test changes, GUI, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML,
Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing, or
release automation. Next safe action is human review of this design; any
preview-only implementation remains a separate explicitly authorized slice.

Latest common foundation decision (2026-06-09):
`remote_handoff_sealed_after_preflight_operator_surface_parking_001` records
the repo-local handoff for the parked common foundation state. The restart entry
was legacy `docs/USER_COPYPASTE_BLOCKS.md` SECTION 22 (removed from the active
prompt file on 2026-07-10; recover only with
`git show 99477a0:docs/USER_COPYPASTE_BLOCKS.md`), and it pointed the next terminal
back to `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`,
`docs/project-context.md`, `docs/AGENT_ORCHESTRATION.md`, and
`docs/AGENT_OPERATOR_SURFACE.md`. This handoff preserves the human-confirmed
review-surface state after `cde00ca feat: add preflight preview card` and the
parking note after `f7d4733 docs: park preflight operator surface`, while
keeping real execution closed. It does not authorize real `codex exec`,
`subprocess.run`, stdin piping, runtime worker loops, external notification,
`.agent` runtime artifacts, `.ymmp`, render, rights, production, publishing,
release automation, G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, or
NotebookLM work.

Latest common foundation decision (2026-06-09):
`preflight_operator_surface_parking_001` records human acceptance of
`cde00ca feat: add preflight preview card` as sufficient for the current
review-surface need. The common foundation is parked with two read-only
Operator Review Surface faces: the existing flow-result card and the standalone
raw preflight preview card. This means a human can inspect preflight status,
`safe_to_start_real_runner`, reasons, inspected paths, authority summary,
execution boundary, and next action before any runner is considered. The parking
decision deliberately does not move to real execution: `safe_to_start_real_runner=true`
is only an eligibility signal for a separately authorized future runner slice,
not execution permission. Real `codex exec`, `subprocess.run`, stdin piping,
runtime worker loop, external notification, worker report validation from a
real run, and `.agent` runtime artifact creation remain unimplemented. If common
foundation work resumes, the next allowed entry is a separately authorized
runner consumption design or pre-execution dry-run flow; do not jump straight to
real runner implementation or mix this with G-28, Newsroom, G-27, ClipPipeGen,
RSS, OPML, Inoreader, NotebookLM, `.ymmp`, render, rights, production,
publishing, or release automation.

Latest common foundation decision (2026-06-09):
`standalone_preflight_preview_adapter_mvp_001` implements the read-only adapter
that converts a raw preflight result into a Markdown preview card. The new
`render_preflight_preview_card(preflight_result)` and `--preflight-example`
surface preflight status, mode / worker, allowed, `safe_to_start_real_runner`,
reasons, inspected paths, authority summary, execution boundary, and human next
action without wrapping the result into a runner flow. Tests cover blocked raw
preflight, allowed dry-run preview, authorized real-runner preflight preview,
the deterministic CLI example, existing flow-card compatibility, and
credential-like value redaction. This does not implement real `codex exec`,
`subprocess.run`, stdin piping, runtime worker loop, external notification,
worker report validation, `.agent` runtime artifact creation, or permission to
start a real runner. It also does not resume G-28, Newsroom, G-27, ClipPipeGen,
RSS, OPML, Inoreader, NotebookLM, `.ymmp`, render, rights, production,
publishing, or release automation.

Latest common foundation decision (2026-06-09):
`disabled_real_runner_preflight_audit_001` reviewed the implemented preflight
boundary without opening any real runner path. The audit found the mode split,
execution boundary, fail-closed path checks, and result shape suitable for the
current pre-run gate, then tightened one coverage gap: supplied credential-like
metadata now has an explicit regression test that blocks preflight and does not
echo the secret-like value in the returned result. `docs/AGENT_ORCHESTRATION.md`
also records that the current operator card reads preflight only when embedded
in a complete flow result; a standalone dry-run / real-runner preflight preview
still needs a future adapter that wraps raw preflight with runner/gate placeholder
state and surfaces `safe_to_start_real_runner` plus `authority_summary`. This
audit does not implement real `codex exec`, `subprocess.run`, stdin piping,
runtime worker loop, external notification, or `.agent` runtime artifact
creation, and it does not resume G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML,
Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing, or
release automation.

Latest common foundation decision (2026-06-09):
`disabled_by_default_real_runner_preflight_001_test_first` implements the
preflight helper only. `scripts/agent_orchestrator.py` now distinguishes
`real_runner`, `dry_run_preview`, and `fake_runner_helper` modes and returns a
JSON-serializable result with allow/block reasons, inspected paths,
`safe_to_start_real_runner`, and authority summary while keeping
`codex_execution_started=false` and `real_subprocess_started=false` inside
preflight. `tests/test_agent_orchestration.py` fixes fail-closed cases for
missing authority, disabled policy, dirty/staged state, unsafe paths, existing
report overwrite, shell command shape, missing timeout, invalid worker, missing
schema, prompt ambiguity, notification ambiguity, dry-run preview allow,
fake-helper allow, and the narrow authorized future real-runner allow case.
`docs/AGENT_ORCHESTRATION.md` records the updated contract. This does not
implement real `codex exec`, `subprocess.run`, stdin piping, runtime worker
loop, external notification, or `.agent` runtime artifact creation. It also
does not resume G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader,
NotebookLM, `.ymmp`, render, rights, production, publishing, or release
automation. Any real runner remains a separate future slice after review.

Latest common foundation decision (2026-06-09):
`real_runner_preflight_implementation_plan_001_docs_only` accepts
`docs/verification/REAL-RUNNER-BOUNDARY-DESIGN-2026-06-09.md` as sufficient for
the next design step and adds
`docs/verification/REAL-RUNNER-PREFLIGHT-IMPLEMENTATION-PLAN-2026-06-09.md` as
the active pre-implementation plan. The plan defines what a future
disabled-by-default preflight must inspect, refuse, allow, and return before any
real runner can start. It keeps real `codex exec`, `subprocess.run`, stdin
piping, runtime worker loop, external notification, and `.agent` runtime
artifact creation unimplemented. The next common-foundation move is human
review of the plan; code/test implementation must remain a separate slice and
must not mix with G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader,
NotebookLM, `.ymmp`, render, rights, production, publishing, or release
automation.

Latest common foundation decision (2026-06-09): `real_runner_boundary_design_001_docs_only`
records that `docs/verification/REAL-RUNNER-BOUNDARY-DESIGN-2026-06-09.md`
defines the boundary required before any real runner implementation. The
Operator Review Surface MVP is treated as sufficient to proceed to boundary
design, but not as execution authority. The sealed state remains fake runner
scaffold plus test/helper-only single fake execution flow plus read-only
operator card, with `codex_execution_started=false` and
`real_subprocess_started=false`. This decision does not implement real
`codex exec`, `subprocess.run`, stdin piping, runtime worker loop, cancellation
code, external notification, or `.agent` runtime artifact generation. Future
work must first review the documented opt-in authority, subprocess, stdin,
timeout/cancellation, report containment, gate/notify sequence, operator-card
integration, runtime artifact hygiene, implementation checklist, and stop
conditions. Do not mix this common-foundation path with G-28, Newsroom, G-27,
ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, `.ymmp`, render, rights,
production, publishing, or release automation.

Latest supervision gate (2026-06-09): `newsroom_handoff_request_authority_no_op_wait`
records the refreshed cross-repo review of the supplied `newsroom-yt-pipeline`
handoff. The handoff is candidate downstream input, not active NLMYTGen
authority yet. NLMYTGen remains on the G-28 `game_mechanics_explanation`
diagnostic lane. This refresh did verify the Newsroom repo and export read-only:
`C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline` was on
`main` / `1296b8e` with `HEAD...origin/main=0 0`, and
`C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853`
contained `export_manifest.json`, `script.csv`, `script_ir.json`,
`visual_ir.json`, `visual_plan.md`, `source_list.md`, `quote_manifest.yml`,
`asset_manifest.yml`, and `ymm4_notes.md`. The selected decision still remains
`request_authority / no-op_wait` because no human decision has authorized
copy-in versus read-only reference, no human decision has paused or superseded
the current G-28 game_mechanics lane, and the inspected Newsroom export is not
NLMYTGen production proof. Do not couple to Newsroom by subprocess/path/pip
dependency, copy runtime export files into tracked artifacts, start
implementation, Review Console changes, context visual plugin work, `.ymmp`
generation, render, production timing, rights approval, creative final
acceptance, G-27 revival, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, common
foundation, or real `codex exec` work from this gate. If the user wants
Newsroom downstream intake, first collect explicit authority for copy-in versus
read-only reference and explicit authority to pause/supersede the current G-28
game_mechanics lane. Detailed gate evidence is in
`docs/verification/NEWSROOM-HANDOFF-SUPERVISION-GATE-2026-06-09.md`.
Reporting format scar: for ChatGPT handoff blocks, wrap the whole copy block in
one outer Markdown code fence, keep `BEGIN_COPY_BLOCK_FOR_CHATGPT` and
`END_COPY_BLOCK_FOR_CHATGPT` inside it, and do not use nested code fences in the
`next prompt` field.

Latest common foundation decision (2026-06-09): `single_fake_execution_flow_committed_audited`
records that `post_commit_audit_single_fake_execution_flow_001` passed for
`e509863 feat: update orchestration scaffold`, with the commit pushed to
`master` and upstream parity verified as `HEAD...@{u}=0 0`. This retires
stale staged-work prompts for the slice: `stage_single_fake_execution_flow_001`,
`single_fake_execution_flow_staged_diff_review_001`, and any fake runner
scaffold stage/commit prompt. The active common foundation state is committed
and audited: fake runner scaffold exists, the single fake execution flow helper
exists, the helper is test/helper-only, and normal CLI/runtime behavior does
not expose the fake flow. There is no `--single-fake-flow` flag. Valid fake
reports go through `agent_gate.evaluate_report`; the local notify stub is only
after `gate_result.needs_human=true`; pass writes no notify artifact; invalid
JSON, missing report, nonzero exit, and timeout fail closed. Real `codex exec`
remains disabled/unimplemented: `codex_execution_started=false`,
`real_subprocess_started=false`, no `subprocess.run`, no stdin piping, no
runtime worker loop, and no external notification service. The next common
foundation work is not immediate real execution. If explicitly authorized
later, use design-only `real_runner_boundary_design_001`, covering explicit
opt-in execution policy, subprocess boundary, stdin piping boundary,
timeout/cancellation, report path containment, gate authority, notify boundary,
runtime artifact hygiene, and no external notification without separate
authorization.

G-28 real-estate diagnostic review surface acceptance (2026-06-08):
Record `overall_decision=accept_as_diagnostic_review_surface_with_title_metric_caveat`
for the YMM4 diagnostic probe and stop the individual pixel-tuning loop for
this artifact. The accepted scope is diagnostic review surface use only:
openability, focal chain, connector treatment, X=313.0 lower-right callout
alignment, caption reserve, diagnostic host placeholders, and diagnostic
boundary pass, while title metric debt and layout-system debt remain. Do not
continue title-Y / callout / right-node micro-offset fixes; any future visual
centering problem should become a text/layout system redesign slice. This does
not approve Review Console implementation changes, production render,
production carrier approval, creative final acceptance, rights automation,
source footage, G-27 authority reuse, common foundation work, or ClipPipeGen
access.

G-28 real-estate evidence note (2026-06-08):
`pass_dom_evidence_needs_manual_screenshot` is recorded in
`docs/verification/G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-EVIDENCE-2026-06-07.md`
for the earlier `real_estate_information_gap` read-only Review Console panel.
Existing Electron DOM smoke confirmed `#g28-review-console-ingest`, artifact
inventory, diagnostic badges, readback summary, human GUI summary, caveats,
allowed diagnostic decisions, and absence of production approval labels. No
Review Console implementation files, generated probe artifacts, builders,
readback/report files, render, production approval, creative final acceptance,
rights automation, G-27 authority, ClipPipeGen, RSS / NotebookLM, or common
foundation work changed. A manual screenshot or separately authorized
G-28-specific capture slice remains optional if visual screenshot evidence is
still required.

Latest G-28 decision (2026-06-08): `remote_handoff_sealed_after_g28_game_mechanics_inspector_accept`
keeps the accepted `game_mechanics_explanation` inspector-first diagnostic
review surface context in-project for another terminal. The restart owner is
`AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md` plus
legacy `docs/USER_COPYPASTE_BLOCKS.md` SECTION 20 (removed from the active
prompt file on 2026-07-10; recover only with
`git show 99477a0:docs/USER_COPYPASTE_BLOCKS.md`). The accepted contract remains
`review_surface=inspector_first`, `in_frame_review_overlay=false`,
`clean_frame_available=true`, `semantic_labels_human_visible=true`,
`diagnostic_only=true`, and `production_candidate=false`. This handoff does not
authorize Source-Footage, `.ymmp` generation, render, production timing,
creative final acceptance, G-27 revival, RSS / OPML / Inoreader / NotebookLM,
common foundation, ClipPipeGen, generated artifact rewrites, or generator
changes. The next safe input is human-supplied evidence for the already scoped
YMM4-saved carrier review conditions, or a decision to stay with the accepted
HTML/readback diagnostic precedent.

Latest G-28 decision (2026-06-08): `g28_game_mechanics_ymmp_saved_carrier_review_conditions`
adds the scoped condition checklist for moving the accepted
`game_mechanics_explanation` Lecture Diagram review surface toward a later
YMM4-saved carrier review. The required inputs are explicit human selection of
that review mode, a carrier path, preview screenshot, timeline screenshot,
item/layer confirmation, and bottom caption safe-area evidence. This is
conditions-only documentation: no `.ymmp` generation, render, production timing,
creative final acceptance, Source-Footage intake, gameplay screenshot intake,
image path/URL/raw reference intake, G-27 revival, RSS, NotebookLM, generated
artifact rewrite, or generator change is approved.

Latest G-28 decision (2026-06-08): `g28_game_mechanics_review_surface_accept`
records human `decision: accept` for the repaired `game_mechanics_explanation`
Lecture Diagram review surface. The accepted scope is reviewability only:
the clean 16:9 frame and lower Review Inspector are separated, the frame no
longer has double-box review overlays, semantic labels remain visible through
the inspector, host remains non-focal, and caption reserve / density are
acceptable for this diagnostic surface. This does not approve production:
`diagnostic_only=true`, `production_candidate=false`, no Source-Footage, no
`.ymmp` generation, no render, no production timing, and no creative final
acceptance. Next safe work, only if needed, is scoped condition planning for a
YMM4-saved carrier review.

Latest G-28 decision (2026-06-08): `g28_game_mechanics_review_surface_inspector_first`
is implemented for the existing `game_mechanics_explanation` Lecture Diagram
diagnostic artifact after human `decision: further revise`. The previous
review-only labels were visible but appeared as in-frame boxed overlays, making
the left/right nodes, callouts, and center focal look double-boxed. The artifact
is repaired in place: default HTML keeps the 16:9 frame clean, moves semantic
labels into the lower review inspector, and records
`in_frame_review_overlay=false`, `review_overlay_default=false`, and
`clean_frame_available=true` in readback. This remains diagnostic-only:
`production_candidate=false`, no new theme variant, no Source-Footage generator,
no `.ymmp`, no render, no production timing, and no creative final acceptance.

Latest common foundation decision (2026-06-08): `fake_runner_scaffold_committed`
adds a tests-only fake runner scaffold in `da254ff feat: add fake runner
scaffold`. The helper writes synthetic reports to `ExecutionPlan.report_path`,
keeps valid report authority in `agent_gate.evaluate_report`, invokes the local
notify stub only after `gate_result.needs_human=true`, and fails closed for
invalid JSON, missing report, nonzero exit, and timeout. This does not enable
real `codex exec`, stdin piping, subprocess runner behavior, runtime worker
loop, external notification service, ClipPipeGen support, publish/release,
rights automation, or `production_candidate` handling. It also does not resume
G-28 mainline work. The next common-foundation slice should keep the same
boundary unless real runner support is explicitly authorized.

Latest G-28 decision (2026-06-08): `remote_handoff_sealed_after_review_console_ingest`
keeps the latest context in-project for another terminal. The durable restart
packet is now `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`
plus legacy `docs/USER_COPYPASTE_BLOCKS.md` SECTION 18 (removed from the active
prompt file on 2026-07-10; recover only with
`git show 99477a0:docs/USER_COPYPASTE_BLOCKS.md`). The next safe work was only
screenshot / Electron smoke evidence or human GUI confirmation of the read-only
G-28 Review Console panel; this does not reopen `.ymmp` generation, builders,
readback/report artifacts, production carrier approval, creative final
acceptance, render, rights/public-use automation, slot-fill, G-27 authority,
ClipPipeGen, RSS, NotebookLM, or common foundation work. Local residue remains
explicitly outside this handoff scope.

Latest G-28 decision (2026-06-08): `pass_review_console_ingest_implemented`
is recorded for the calibrated real-estate YMM4 diagnostic probe. The Review
Console now has a read-only G-28 panel that references the existing `.ymmp`,
readback JSON, report MD, human review record, and ingest plan in place, checks
repo-relative artifact existence, shows diagnostic boundary badges, summarizes
readback/human GUI results, exposes caveats for X=313, title readback debt, host
placeholders, and glyph optical-center limits, and limits visible decisions to
diagnostic review-surface outcomes. DOM smoke verifies the panel and the absence
of production approval labels. This does not change `.ymmp`, builder,
readback/report artifacts, render, production carrier approval, creative final
acceptance, rights/public-use automation, slot-fill, G-27 authority, common
foundation, ClipPipeGen, RSS, or NotebookLM work. Next safe action is screenshot
/ Electron smoke evidence or human GUI confirmation of the read-only panel.

Latest G-28 decision (2026-06-08): `G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-PLAN-2026-06-07`
is added as the docs-only plan for read-only Review Console ingest of the
accepted real-estate YMM4 diagnostic probe. The plan defines the input artifact
inventory, diagnostic status badges, readback summary, human GUI result summary,
title readback follow-up requirements, host placeholder boundary,
human-calibrated callout caveat, diagnostic-only decision schema, future GUI
implementation surfaces, error states, and next-slice acceptance criteria. It
does not implement GUI ingest, modify GUI files, regenerate `.ymmp`, change the
builder, rewrite readback/report artifacts, approve production, approve render,
approve rights/public use, slot-fill, revive G-27, access ClipPipeGen, restart
RSS / NotebookLM work, or implement common foundation / Codex Worker
Orchestration. Next safe action is an explicitly authorized read-only Review
Console ingest implementation slice based on this plan.

Latest G-28 decision (2026-06-08): `accept_for_review_console_ingest_candidate_with_layout_metric_caveat`
is recorded for the calibrated real-estate YMM4 diagnostic probe. Human GUI
recheck accepted the X=313.0 lower-right callout label `仲介インセンティブ`:
openability, focal-chain readability, connector treatment, caption reserve,
diagnostic boundary, and major side-effect checks pass. This authorizes only a
Review Console ingest candidate record / ingest plan. It does not authorize
actual Review Console ingest implementation, production render, production
carrier approval, creative final acceptance, rights automation, slot-fill,
external material intake, G-27 revival, ClipPipeGen, RSS / NotebookLM, or common
foundation / Codex Worker Orchestration work. Layout metric debt remains part of
the candidate: current readback does not directly measure YMM4 glyph optical
center, title y=`-474.5` is visually acceptable but should become a future title
anchor/text-center/safe-area readback check, host placeholders are
diagnostic-only and not production character/visual assets, and X=313 remains a
human-calibrated override rather than reusable formula proof.

Latest G-28 decision (2026-06-08): `g28_real_estate_information_gap_callout_label_human_calibration_v1`
is implemented after human GUI recheck found the lower-right callout label
`仲介インセンティブ` still visually left-shifted after the bounded alignment fix.
The previous computed/polished YMM4 TextItem X was `289`; the human-measured
correct X is `313.0`, so the builder now applies a one-time
`human_calibrated_x=313` and records `calibration_delta_x=24`. This decision
does not claim formula success. It records callout text layout system debt:
`text_center_error_px` remains registered-placement proof only, and a remaining
visual mismatch after this slice should move to callout text layout system
redesign rather than another individual pixel/offset adjustment. Readback passes
as `pass_callout_label_human_calibrated` while the boundary remains
`diagnostic_only=true` / `production_candidate=false`; Review Console ingest,
production render, production approval, creative final acceptance, rights
automation, slot-fill, external materials, G-27 revival, ClipPipeGen, RSS /
NotebookLM, and common foundation / Codex Worker Orchestration remain
unapproved.

Latest G-28 decision (2026-06-07): `g28_real_estate_information_gap_callout_label_alignment_v1`
is implemented after human GUI correction clarified that the actual remaining
visual target is the lower-right callout label `仲介インセンティブ`, not the
right node `借主判断`. Only `G28_LDC_CalloutSlot_3_Label` changed: its
registered optical offset moved from `{x:0,y:-3}` to `{x:4,y:-3}`. The previous
right-node fix is retained because no adverse side effect was reported. The
shared callout formula, node labels, connectors, hosts, caption reserve, variant
id, and diagnostic boundary are unchanged. Readback passes as
`pass_callout_label_alignment_fixed`. This decision also records the metrics
caveat that `text_center_error_px=0` checks registered placement, not rendered
YMM4 glyph optical center. Next safe move is human YMM4 GUI recheck of this
callout-label-only fix; Review Console ingest and all production/rights/render/
slot-fill work remain unapproved.

Latest G-28 decision (2026-06-07): `g28_real_estate_information_gap_right_node_alignment_v1`
is implemented for the existing real-estate YMM4 diagnostic probe after human
GUI recheck returned `revise_probe_again_narrow_right_node_text_alignment`.
Only `G28_LDC_Node_Right_Label` changed: its registered optical offset moved
from `{x:0,y:-4}` to `{x:4,y:-4}`. The shared text-centering formula,
connectors, callouts, hosts, caption reserve, variant id, and diagnostic
boundary are unchanged. Readback passes as `pass_right_node_alignment_fixed`.
This decision also records the metrics caveat that `text_center_error_px=0`
checks registered placement, not rendered YMM4 glyph optical center. Next safe
move is human YMM4 GUI recheck of this right-node-only fix; Review Console
ingest and all production/rights/render/slot-fill work remain unapproved.

Latest G-28 decision (2026-06-07): `g28_real_estate_information_gap_layout_contract_v1`
is implemented for the existing real-estate YMM4 diagnostic probe. The builder
now records derived connector geometry, manual text offset registry, a bounded
2-3 callout formula with four-callout risk, and tolerance readback. Verification
passed as `pass_probe_polished` with
`layout_contract_metrics_present=true` and
`layout_contract_tolerances_pass=true`. This remains diagnostic-only
(`production_candidate=false`); the next safe move is human YMM4 GUI recheck
before any Review Console ingest decision. No production render, production
approval, creative final acceptance, rights automation, slot-fill, external
image/URL/raw reference, source footage/audio/TTS, G-27 revival, ClipPipeGen,
RSS / NotebookLM, or common foundation / Codex Worker Orchestration work is
approved by this decision.

| 日付 | 決定事項 | 選択肢 | 決定理由 |
|------|----------|--------|----------|
| 2026-06-07 | **G-28 real-estate polished YMM4 diagnostic probe の layout contract audit は `needs_layout_contract_implementation` を推奨する。** | Review Console ingestへ即進む / さらに目分量polishを続ける / probe pathを延期する / layout contractを1回だけbounded revisionする | `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-LAYOUT-CONTRACT-AUDIT-2026-06-07.md` により、現在probeは diagnostic GUI surface としては accept 済みだが、再利用可能なlayout systemとしては未実装部分が残ると判断した。TextItemはtop-left formulaで説明できるがmanual optical offsetに依存し、connectorはedge-to-edge barとして説明できるがhard-coded override、callout rowは3件専用で4件以上の破綻リスクがある。次は追加polishではなく、derived connector geometry、explicit offset registry、2-3 callout formula、tolerance readbackを入れる bounded layout-system revision が妥当。今回 `.ymmp`、builder/generator、readback/report、render、production approval、creative final acceptance、rights automation、source footage/audio/TTS、外部画像/URL/raw reference、G-27、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 real-estate polished YMM4 diagnostic probe の GUI re-review は `accept_as_diagnostic_gui_probe_with_layout_contract_followup` として受け、次工程を layout contract audit に限定する。** | production approvalへ進む / さらに目分量polishを続ける / Review Console ingestへ即進む / re-review結果を記録し layout contract audit へ進む | 人間reviewでは YMM4 openability、focal chain、caption reserve、callout readability、host role、実在サービス/物件感、diagnostic boundary は pass/clear。yellow connector treatment と rectangle text alignment は見た目として改善したが `pass_partial` であり、残課題は数pxの再polishではなく、text centering formula、connector positioning formula、callout slot rule、manual offset registry、tolerance readback を明示する layout contract 問題として扱う。今回 `.ymmp`、builder/generator、readback/report再生成、render、production carrier approval、creative final acceptance、rights automation、source footage/audio/TTS、外部画像/URL/raw reference、G-27、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 real-estate YMM4 diagnostic probe bounded polish revision は `pass_probe_polished` として通過した。** | `revise_probe` を未処理に残す / production promotion に進む / 新variantに逃がす / 同一diagnostic probeを最小更新する | Human GUI review の `revise_probe` に対して、`scripts/build_g28_real_estate_ymmp_probe.js` は yellow connector alignment、callout slot spacing、TextItem visual offset の bounded polish だけを行うようになった。`samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.{ymmp,readback.json,report.md}` を同一pathに再生成し、readback は `diagnostic_only=true` / `production_candidate=false` / 1920x1080 / bottom 20% caption reserve clear / focal chain 3 / callout count 3 / non-focal hosts / bounded text budget / external image・URL・source footage・audio・TTS・token-like counts 0 を満たす。今回も diagnostic polish only であり、production render、creative final acceptance、production carrier approval、rights automation、real material slot-fill、G-27復帰、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 real-estate YMM4 diagnostic probe の human GUI review は `revise_probe` として受け、次は bounded polish revision に限定する。** | production 承認へ進む / probe を完了扱いにする / 新variantへ逃がす / human review result を記録し、同一probeのpolish revisionへ限定する | ユーザー確認では YMM4 openability、focal chain、caption reserve、host role、実在サービス/物件感、diagnostic boundary は pass/clear だが、callout readability は `pass_partial`、alignment/polish は `partial` であり、黄色い線の処理・矩形内テキスト整列・微妙な視覚ズレが認知摩擦として残ったため。`docs/verification/G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md` に記録し、次の許可範囲は同じ `variant_id=g28_ldc_real_estate_information_gap` / diagnostic-only / production-candidate-false 境界を保つ polish revision のみ。production render、creative final acceptance、production carrier approval、rights automation、real material slot-fill、外部画像/URL/raw reference、G-27復帰、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 `real_estate_information_gap` accepted diagnostic variant を self-contained YMM4-compatible probe へ進める。** | plan のまま待つ / production carrier approval へ進む / new G-28 variant を作る / accepted済み variant から shapes/text only の `.ymmp` diagnostic probe を作る | `g28_lecture_diagram_carrier_real_estate_information_gap_v1` は human decision が `accept_as_diagnostic_direction`、readback が `passed` であり、直前 plan が YMM4-compatible probe を次 slice として許可しているため。今回の成果は `scripts/build_g28_real_estate_ymmp_probe.js` と `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.{ymmp,readback.json,report.md}` に限定し、classification `pass_ymmp_probe_created` まで確認する。これは diagnostic GUI review surface であり、production render、creative final acceptance、production carrier approval、rights automation、real material slot-fill、external image/URL/raw reference、G-27復帰、common foundation、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 `real_estate_information_gap` を最初の YMM4-compatible diagnostic probe 候補として計画する。** | すぐ `.ymmp` を作る / production carrier approvalへ進む / deferred carrierを先にprobe化する / accepted済み Lecture Diagram variant の probe plan だけ作る | `g28_lecture_diagram_carrier_real_estate_information_gap_v1` は `accept_as_diagnostic_direction` 済みで、readback も `diagnostic_only=true` / `production_candidate=false` / caption reserve clear / 3-node focal chain / 3 callouts を満たしているため、最初の YMM4-compatible probe 候補として最も摩擦が少ない。一方で今回の目的は plan 作成のみなので、`docs/verification/G28-REAL-ESTATE-YMM4-COMPATIBLE-PROBE-PLAN-2026-06-07.md` に item/group mapping、layer order、readback requirements、human GUI checklist、next slice options を固定し、`.ymmp`、render、production approval、creative final acceptance、rights automation、new variant、generator変更、G-27復帰、common foundation、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 game-mechanics の `revise` は、まず diagnostic semantics clarification で閉じる。** | すぐ generator / JSON を変更する / 新variantを作る / YMM4 probeへ進む / 既存 semantics note で `判定 / 当たり判定` 中心の因果構造を明確化する | `g28_lecture_diagram_carrier_game_mechanics_explanation_v1` の人間decisionは `revise` だが、求められている修正は production 昇格ではなく「何を説明する carrier か」の明確化であるため。既存 3-node chain は維持し、`入力操作` -> `内部ルール / 判定` -> `画面上の結果` の middle node を first-review では `判定 / 当たり判定` として読む。`操作感` / `リスクとリターン` は補助 callout に留め、caption reserve、non-focal host、dense table回避、indexed whiteboard回避を維持する。今回 generator、new variant、JSON/readback/report rewrite、`.ymmp`、render、production carrier approval、creative final acceptance、G-27復帰、common foundation、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 diagnostic artifacts 6件の human decision を記録し、production には進めない。** | 全件accept扱いにする / reviseからgenerator変更へ進む / deferをproduction probe扱いにする / supplied human decisions だけを decision record に記録する | 人間decision が明示されたため、`docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md` にそのまま記録する。generic Lecture Diagram skeleton と `real_estate_information_gap` は `accept_as_diagnostic_direction`、`game_mechanics_explanation` は `revise`、Map / Evidence・Source-Footage definition-only・Conversation / Buffer definition-only は `defer_to_ymmp_carrier_probe`。accept は diagnostic direction の承認のみであり、production carrier approval、creative final acceptance、`.ymmp`、render、G-27復帰、common foundation実装、RSS / NotebookLM には進まない。 |
| 2026-06-07 | **G-28 human decision record は、判断を捏造せず pending intake surface として作る。** | accept / revise / reject / defer をAgent判断で埋める / 新variantやgenerator変更へ進む / pending_human_decision の decision record を作る | 今回の prompt では人間側の accept / revise / reject / defer 判断がまだ明示されていないため。既存 diagnostic artifacts は readback-passed / diagnostic_only=true / production_candidate=false なので、次の成果物は `docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md` に human input fields と allowed decisions を固定することに限定する。production carrier approval、creative final acceptance、`.ymmp`、render、G-27 revival、common foundation 実装、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 は追加 variant 量産ではなく、既存 diagnostic artifact を人間が判定する review packet に進める。** | さらに Lecture Diagram variant を追加する / production carrier や `.ymmp` probe へ飛ぶ / common foundation 実装へ戻る / 汎用 diagnostic human review packet を作る | 現存する Lecture Diagram generic skeleton、`real_estate_information_gap`、`game_mechanics_explanation`、Map / Evidence skeleton は readback-passed diagnostic-only であり、次の摩擦は生成不足ではなく人間が `accept_as_diagnostic_direction` / `revise` / `reject` / `defer_to_ymmp_carrier_probe` を返す decision surface の不足にあるため。今回の artifact は `docs/verification/G28-DIAGNOSTIC-HUMAN-REVIEW-PACKET-2026-06-07.md` に限定し、新しい JSON/HTML/readback/generator、production carrier approval、creative final acceptance、`.ymmp`、render、G-27 revival、RSS / NotebookLM、Codex Worker Orchestration 実装には進めない。 |
| 2026-06-05 | **G-28 game-mechanics human review は `revise` として受け、Lecture Diagram Carrier の diagram semantics note に落とす。** | acceptとして次へ進む / Source-Footageへ切り替える / 新variantを生成する / 既存carrierのsemantics noteに限定する | ユーザーが「入力操作 -> 内部ルール / 判定 -> 画面上の結果」は正しいが、`内部ルール` が抽象的なので `判定 / 当たり判定`、`無敵時間`、`硬直` のような具体内部処理例を1つ選べる余地を残したい、と返したため。最初のreview主軸は `判定 / 当たり判定`、`操作感` と `リスクとリターン` は補助扱いにする。host は non-focal、medium caption 前提、画面内textは短く保つ。新variant、Source-Footage、`.ymmp`、render、production timing、creative final acceptance には進めない。 |
| 2026-06-05 | **G-28 game-mechanics review packet までの文脈を repo-local handoff として保持し、別端末再開用 prompt を更新する。** | チャット報告だけで止める / AGENTS.md に長文追記 / runtime-state・decision log・USER_COPYPASTE_BLOCKS に最小追記して push | ユーザーが「全コンテキストをプロジェクトに保持しつつ、ローカルをリモートに反映」「別端末からすぐ再開」を明示したため。最新の実体は `docs/verification/G28-GAME-MECHANICS-HUMAN-REVIEW-PACKET-2026-06-05.md` までで、G-28 は diagnostic-only、Source-Footage は future-only backup、次は human `accept` / `revise` / `reject` 記録または design-only checklist に限る。AGENTS.md と既存 generated artifact は触らず、`.ymmp`、render、production timing、creative final acceptance、G-27、RSS / NotebookLM へは進めない。 |
| 2026-06-05 | **G-28 toolbox を、次の1 shot の carrier selection worksheet に落とす。** | 実際の shot が来るまで待つ / 新しい skeleton や theme variant を増やす / 既存 generated artifact を変更する / 空テンプレートと判定規則だけを verification artifact にする | 次の制作時の摩擦は「Lecture / Map / Source-Footage / Conversation のどれを選ぶか」なので、現存 toolbox に基づき shot purpose、source material、visual evidence type、claim type、required viewer action、caption density を埋めれば carrier を選べる worksheet を作るのが最小で有効。Source-Footage と Conversation / Buffer は未着手のまま進む条件だけを明示し、source intake、image path/URL、`.ymmp`、render、production timing、creative final acceptance、G-27 復帰、RSS / NotebookLM には進めない。 |
| 2026-06-05 | **G-28 archetype 群は、追加サンプルではなく画面設計の道具箱として整理する。** | 新しい theme variant を増やす / 新しい carrier skeleton を増やす / 既存 artifact を変更する / 4 archetype の目的・適用範囲・readback 状態・production 前判断を1つの verification artifact にまとめる | G-28 の次の詰まりは標本数ではなく、次の shot でどの carrier を選ぶかの判断摩擦に移ったため。Lecture Diagram と Map / Evidence は readback-passed の diagnostic-only、Source-Footage と Conversation / Buffer は definition-only と明示し、source intake、image path、URL、`.ymmp`、render、production timing、creative final acceptance、G-27 復帰、RSS / NotebookLM には進まない境界を維持する。 |
| 2026-06-05 | **G-28 Map / Evidence Carrier 完了後の全コンテキストを repo-local handoff として保持し、`origin/master` に反映する。** | チャット報告だけで止める / AGENTS.md に長文追記 / runtime-state・decision log・USER_COPYPASTE_BLOCKS に最小追記して push | ユーザーが「上記までで全コンテキストをプロジェクトに反映してプッシュ」を明示したため。通常再開入口を肥大化させないため `AGENTS.md` は触らず、現在位置は `docs/runtime-state.md`、判断履歴は本 decision log、ChatGPT へ貼る最新再開 prompt は `docs/USER_COPYPASTE_BLOCKS.md` に分離する。Map / Evidence は diagnostic skeleton であり、production carrier approval、`.ymmp`、render、creative final acceptance、G-27 promotion、RSS / NotebookLM へは進めない。 |
| 2026-06-05 | **G-28 Map / Evidence Carrier は、Lecture Diagram Carrier の追加 theme variant ではなく、別 archetype の diagnostic skeleton として生成する。** | Lecture Diagram variant を量産する / 実地図や衛星画像を取り込む / 新しいSCS typeを増やす / 既存SCSの `center-focal` に写像した Map-Evidence skeletonを追加 | ユーザーが地図・統計・産業立地・企業分布・人口・市場・地域差・出典付き論証を「飾りではなく論証装置」として扱う carrier archetype を1つだけ作るよう指定したため。今回の skeleton は `G28_MEC_EvidenceSurface` を focal anchor、3つの annotation slot、bounded source note、non-focal hosts を持つが、real map / satellite image / image path / URL / raw reference / `.ymmp` / render / production timing / creative final acceptance / source footage / gameplay screenshot intake には進まない。SCS mapping は `center-focal` で、新しい composition type は増やさない。 |
| 2026-06-05 | **G-28 `game_mechanics_explanation` は、Source-Footage Carrier へ進まず、Lecture Diagram Carrier の2つ目の theme-specific diagnostic variant として生成する。** | 不動産variantだけで止める / gameplay screenshot や source footage を取り込む / Lecture Diagram上の `center-focal` diagnostic variantを追加 | ユーザーが G-28 generic capability の確認として、ゲームレビュー / ゲームメカニクス解説へ転用できるかを1variantだけ検証するよう指定したため。今回のvariantは `入力操作` -> `内部ルール` -> `画面上の結果` の focal-chain semantics と、`操作感` / `判定 / 当たり判定` / `リスクとリターン` の callout semantics を持つが、source footage carrier ではなく、画像・URL・raw reference・production render・creative final acceptance・`.ymmp` 生成には進まない。 |
| 2026-06-05 | **G-28 `real_estate_information_gap` variant 完了後の全コンテキストを repo-local handoff として保持し、`origin/master` に反映する。** | チャット報告だけで止める / AGENTS.md に長文追記 / `runtime-state.md` と decision log に最小追記して push | ユーザーが「全コンテキストをプロジェクトに保持しつつ、ローカルをリモートに反映」を明示したため。通常再開入口を肥大化させないため `AGENTS.md` は触らず、現在位置は `runtime-state.md`、判断履歴は本 decision log に限定して保存する。既知未追跡 `.claude/worktrees/` と `samples/2026-05-16.ymmp` は local residue のまま触らない。 |
| 2026-06-05 | **G-28 `real_estate_information_gap` は、G-27 復帰や production carrier 昇格ではなく、既存 Lecture Diagram skeleton の theme-specific diagnostic variant として生成する。** | 汎用 skeleton のまま停止 / G-27 carrier path へ戻る / `.ymmp` production carrier へ飛ぶ / `--variant real_estate_information_gap` で JSON/HTML/readback/MD を生成 | ユーザーが theme を `real_estate_information_gap`、readback variant id を `g28_ldc_real_estate_information_gap` に固定し、approved carrier 不在で止めないこと、production / render / creative acceptance / source footage / image path / URL / RSS / NotebookLM に進まないことを明示したため。variant は `center-focal` の Lecture Diagram 上で `元付情報` -> `ポータル掲載` -> `借主判断` の3ノード focal-chain semantics と、`情報遅延` / `掲載粒度の欠落` / `仲介インセンティブ` の3 callout semantics を持つが、slot-fill済み production text ではない。根拠: user prompt + G28 Lecture Diagram spec + generated readback `status=passed` |
| 2026-06-05 | **G-28 Lecture Diagram Carrier は、production approval 待ちで停止せず、Agent-owned diagnostic skeleton / readback artifact まで進める。** | 人間がcarrierを作るまで停止 / `.ymmp` zero-generationへ飛ぶ / JSON/HTML/readback skeletonで実体化 | ユーザーが Human Authority 化 / carrier 官僚制の再発防止を明示したため、creative final acceptance と diagnostic skeleton generation を分離する。現行 G-28 v0.1 は `.ymmp` zero-generation を非目的に置くので、このスライスでは `docs/verification/G28-LECTURE-DIAGRAM-CARRIER-SPEC-2026-06-05.md` と `samples/_probe/g28/lecture_diagram_carrier_skeleton_*` の machine-readable artifact で frame contract / layer order / caption reserve / focal area / host role / callout count を閉じる。根拠: user prompt + REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md + SCENE_COMPOSITION_SCHEMA.md |
| 2026-06-05 | **G-28 の初回参照画像入力を受領済みとして扱い、画像丸コピーではなく reference style brief へ抽出する。** | input-wait 継続 / 画像を素材化 / G-27 carrier 待ちへ戻す / G-28 style brief に抽出 | ユーザーが 7 枚の参照画像と extraction 方針を渡したため、G-28 の parked 状態を解除し、`docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md` と SCS に沿って per-image extraction、共通画面文法、generic carrier archetype、YMM4 item/group 構成案へ変換するのが最小前進。根拠: runtime-state 2026-06-05 handoff + docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md + SCENE_COMPOSITION_SCHEMA.md |
| 2026-06-04 | **G-28 を parked / input-wait として保持し、詳細 handoff と ChatGPT 貼付用 block を repo 内に保存する。** | runtime-state の短文だけに留める / AGENTS.md に長文手順を追加 / verification handoff + USER_COPYPASTE_BLOCKS に分離 | ユーザーは全コンテキストを project に保持したうえで remote 反映を求めている。一方で通常再開入口を重くすると drift するため、現状態は `runtime-state.md`、詳細な G-28 parking context は `docs/verification/G28-REFERENCE-INPUT-WAIT-HANDOFF-2026-06-04.md`、ユーザーが ChatGPT へ貼る reusable block は `docs/USER_COPYPASTE_BLOCKS.md` に分離する。 |
| 2026-06-04 | **G-27 を active production carrier blocker から外し、case-specific legacy / reference evidence として保持する。後継として G-28 Reference-Driven Generic Screen Carrier を proposed 登録する。** | G-27 carrier 待ちを継続 / diagnostic carrier を production 昇格 / G-27 を削除 / 汎用 screen carrier issue へ再生成 | G-27 の diagnostic carrier、review console、SCS lessons は有用だが、不動産DX固有の carrier 未受領を active next action として延命すると制作摩擦が増える。画像丸コピーではなく、参照画像から構図・密度・余白・色階層・視線誘導・UI感を抽出して SCS / YMM4 carrier handoff へ変換する汎用能力に再定義する方が、NLMYTGen の downstream adapter / YMM4 接着層の責務に合う。根拠: INVARIANTS §Responsibility Boundaries + FEATURE_REGISTRY G-27/G-28 + docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md |
| 2026-06-04 | **Codex 側の作業完了・停止・確認報告は、ChatGPT へ一発コピーできる単一コードブロックを最後に含める。** 正本の通常再開は引き続き `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md` で、詳細テンプレは `docs/USER_COPYPASTE_BLOCKS.md`、対話上の report contract は `docs/INTERACTION_NOTES.md` に置く。 | チャットだけで運用 / AGENTS.md に長いテンプレを追加 / interaction note + reusable copypaste block に分ける | ユーザーは Codex の報告を ChatGPT 側へ毎回貼り付けて監修するため、ドラッグ選択なしでコピーできる唯一の正本が必要。一方で `AGENTS.md` を運用マニュアル化すると再開入口が重くなるため、入口・現状態・対話契約・ユーザー用テンプレを分離する。 |
| 2026-06-03 | **ChatGPT / Codex 間で再利用する長文 Prompt / PowerShell / 停止文 / 報告文を、Agent再開マニュアルではなくユーザー用コピペ資産として保存する。** 正本は `docs/USER_COPYPASTE_BLOCKS.md`。通常再開で読む3点は増やさず、active next action や runtime-state の代替にも使わない。 | 次Agentへのキックスタートとして扱う / repoに残さない / ユーザー用保存版として残す | ユーザーの目的は次Agentへ作業を実行させることではなく、毎回長文を手で組み立てる摩擦を減らすことだったため。RSS / OPML / NotebookLM source-pack selection は NLMYTGen では旧水路であり、保存版内でも downstream adapter 境界と G-27 分離を保つ必要がある。 |
| 2026-06-03 | **RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection を NLMYTGen の active lane から外し、`newsroom-yt-pipeline` 側の上流編集責務として扱う。** NLMYTGen 側の既存 RSS 実装や過去証跡は削除せず、legacy / reference-only として残す。今後の NLMYTGen は newsroom-produced packet / transcript / ScriptIR / VisualIR / export bundle を受け取ってから、YMM4 CSV、YMM4 adapter、Review Console、proof ingest へ落とす。 | NLMYTGenでOPML復元とsource-pack選定を継続 / RSS実装を削除 / active laneからretireしてnewsroomへ寄せる | newsroom-yt-pipeline が source ingest、article ledger、story clustering、scoring、NotebookLM packet preparation、script workbench interfaces、visual planning interfaces、rights manifests を持つ上流編集repoであり、NLMYTGen の価値経路は downstream adapter と YMM4 production proof にあるため。根拠: INVARIANTS §Responsibility Boundaries + runtime-state 2026-06-03 handoff |
| 2026-06-01 | **G-27 `G27_PublicVsBrokerDB` carrier は production slot-fill へ進む前の境界物として必要。ただし user が明示すれば既存 diagnostic carrier を production carrier に昇格する選択肢もある。** デフォルトは人間が YMM4 で最小 stable carrier を作る。速度優先なら `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` を昇格対象にできるが、runtime-state と readback/boundary 記録を更新してから進む。`samples/2026-05-16.ymmp` は item 3 件のみで不可。 | 新規最小 carrier / diagnostic carrier 明示昇格 / carrier なし diagnostic 継続 | YMM4 が制作基盤で Python/assistant は CSV/IR/registry/post-import `.ymmp` patch の接着層であるため、assistant が diagnostic raw geometry を黙って production layout にしてはいけない。carrier は美麗な完成画面ではなく、固定 `G27PBD_*` item 名、card 数、caption safe area、短 Remark、後段 patch で触らない geometry/color/font/layout を固定する台座であるため。 |
| 2026-05-27 | **A-04 RSS Reader Sync v1.1 は `master` / `origin/master` に fast-forward 統合済み**。統合範囲は `da30ff2..1599cf5` で、OPML source sync、fetch coverage、Inoreader read-only adapter、`rss-smoke` sanitized evidence、live-smoke runbook、RSS tests を含む。PR は個人開発のため省略し、merge 前後に RSS narrow tests `41 passed`、full `uv run pytest` `525 passed, 25 skipped`、CLI help smoke、`git diff --check` を確認した。 | PR 作成 / master へ fast-forward / RSS branch 継続 | branch diff が RSS docs/code/tests + `.gitignore` に閉じ、G-27 / Baseball / Thumbnail / GUI / unrelated path と raw OPML / token / private feed URL / article body / live smoke evidence の混入がなかったため。OPML は v1 source of truth、Inoreader は read-only adapter のままで、DB・OAuth refresh・既読同期・購読変更・background polling は実装しない。 |
| 2026-05-26 | **A-04 RSS lane は `codex/rss-reader-sync-clean` を remote handoff 正本にする**。OPML sync v1、fetch coverage、Inoreader read-only adapter、`rss-smoke` one-command sanitized evidence、live-smoke runbook までを `origin/codex/rss-reader-sync-clean` に push 済み。別端末では `docs/runtime-state.md` と `docs/verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md` から再開する。 | clean RSS branch を正本化 / G-27 差分混在 branch を継続 / master 直作業 | 既存作業ツリーには G-27 差分が残っているため、RSS PR/再開経路を汚さないには `origin/master` ベースの clean branch が安全。RSSの残作業は実OPMLまたは一時 Inoreader token による live smoke だけで、raw OPML/token/private URL/full body は commit しない。 |
| 2026-05-25 | **A-04 RSS Reader Sync v1 は OPML export を先に共通正本化する**。`fetch-topics` は URL 直接指定を維持しつつ `--opml` で人間側RSSリーダーの購読一覧をそのままAI側取得対象へ使い、`list-feed-sources` でAIが見る一覧を確認できるようにする。Inoreader OAuth / API 直結は後続の read-only adapter 候補として文脈だけ保存し、このスライスでは認証・DB・既読同期を増やさない。 | Inoreader 直結から開始 / OPML 正本化から開始 / 既存URL指定のみ維持 | Inoreader はOAuth app・token保管・利用条件・rate limit を伴うため、先に依存追加なしで「人間一覧とAI取得一覧が一致する」土台を閉じる方が安全。A-04 はL1入力取得であり、NotebookLM代替や制作artifact生成へ広げないため |
| 2026-04-30 | **G-26 目的別演出制作を `build-motion-recipes` pipeline として実装**。brief `samples/recipe_briefs/g26_motion_recipe_brief.v1.json`、effect catalog / concrete samples / motion library / optional composition corpus を読み、`_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp`、readback JSON、manifest MD を生成する。初期 recipe は `nod_*` / `jump_*` / `panic_crash` / `shocked_jump` / `surprised_chromatic` / `anger_outburst` / `shobon_droop` / `lean_curious` の 12 件。 | 都度手作業で試作 / 既存サンプル再配置だけ / intent-first recipe pipeline | ユーザーの負担は「毎回一から演出を作る」ことなので、IR 作業と同じく意図・候補・readback・採否を machine-readable artifact に固定する必要があるため。effect catalog を機械参照し、最終的な動きから逆算する経路を CLI に閉じる。 |
| 2026-04-30 | **G-26 evidence gate の過剰解釈を修正し、目的別 recipe lab を正当な assistant 作業として扱う**。`_tmp/g26/recipe_lab/g26_goal_motion_recipe_lab.ymmp` は既存 YMM4-saved canvas `samples/canonical.ymmp` と既存 template source `samples/templates/skit_group/delivery_v1_templates.ymmp` から作成した、うなずき・ジャンプ・傾き・chain の review artifact。readback は openability pass / recipe GroupItems 12 / ImageItems 24 / POSIX asset paths 0。 | operator-authored source 待ちだけにする / 既存 sample を再配置するだけ / assistant が目的別 review lab を作る | ユーザーの要求は「既存動作の散布」ではなく「うなずき」「ジャンプ」のような目標を設定して試作すること。`compatible_after` / `forbidden_after` の推測禁止は contract 昇格条件であり、既存 YMM4 source をコピーして transform 値を調整する review sample 作成を止める理由ではないため。 |
| 2026-04-30 | **G-26 Evidence Gate は machine pass / visual not recorded / tilt-chain source absent として扱う**。`_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp` は openability pass、inserted GroupItems 3、POSIX asset paths 0。repo-local `.ymmp` 53 本の scan では tilt / chain Remark が見つからないため、`tilt` は contract 外、`compatible_after` / `forbidden_after` は `unknown` 維持。 | 推測で compatibility を埋める / machine pass だけで production 接続 / visual・tilt・chain を別 gate に分離 | 画面表示の真偽は YMM4 visual confirmation なしに判定できず、chain source なしで相性を埋めると G-25 の accidental composition failure を再発させるため。assistant 側で閉じられる machine readback は閉じ、観測不能部分だけを正確に残す。 |
| 2026-04-30 | **G-26 Phase 3 仮 contract と screen review を強進行で作成**。`dominant_channels` は `VFX:<EffectType>` を含め、Rotation 系の `anchor_dependency` を一級フィールドにする。`_tmp/g26/draft_contracts/*.json` と `_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp` を作成し、readback は openability pass / inserted GroupItems 3 / POSIX asset paths 0。 | 追加確認待ち / contract のみ / contract + screen review | ユーザー要望は別レーン報告の妥当性確認だけでなく、推奨対応の自動適用と「画面上でまともにサンプルが見えていない」問題の前進だったため。G-24 production へ接続せず、既存の YMM4-saved seed + skit_group compact review 経路で安全に画面確認 artifact を作るのが最短だった。 |
| 2026-04-30 | **G-25 の creative acceptance を negative として閉じ、G-26 motion primitive grammar / compatibility probe を起票**。G-25 review はYMM4で開けるが、`nudge / scale / rotate / effect_reuse` は動きのvariationとして使えない。 | G-25候補を調整して継続 / productionへ接続 / G-26へ切替 | ユーザー確認で、うなずき・退場・小ジャンプ・傾きの機械的な組み合わせが、反対方向の傾き、傾いたままの退場、傾いた小ジャンプなどの不自然な動きを生むことが分かったため。次は座標差分ではなく、motion primitive の開始姿勢・終了姿勢・方向意味・reset policy・相性を扱う。 |
| 2026-04-30 | **G-25 review `.ymmp` の openability 修復を C案ベースで実施**。`LayerSettings` は array ではなく `{ "Items": [...] }` object をYMM4期待形として扱い、`probe-ymmp-variations -o` は template/stub source を直接 review surface にせず、必要時に `--review-seed` で YMM4 保存済み full project canvas を使う。 | guard反転のみ / full seed化のみ / guard反転 + full seed化 | ユーザー環境のYMM4エラーは `YukkuriMovieMaker.Project.LayerSettings` object 要求を示しており、repo内 `.ymmp` も object 形が主流だったため。JSON可読性とYMM4実読込schemaを混同し、stubをopenable artifactへ昇格させたことが不安定化の本体だった。 |
| 2026-04-29 | **G-25 YMM4 property-based variation probe を実装し、手動演出からの保守的な派生生成を初回検証へ進める**。`probe-ymmp-variations` は `Remark` clip、`X/Y/Zoom/Rotation`、反転 route、`VideoEffects` fingerprint を JSON report にし、`-o` 指定時だけ compact review `.ymmp` を追加生成する。 | さらに計画保留 / G-24 に直結 / 独立 probe として実装 | ユーザーの痛点は「手動演出のタグ・座標・反転・拡縮から variation を自動生成できるかが未試行」だったため。G-24 production placement に混ぜず、`.ymmp` ゼロ生成や Python 画像生成にも戻らない、限定 readback / derivative review として最小検証する。 |
| 2026-04-29 | **汚染パッチ由来の rejected / hold を手段単位に再定義**。B-10 旧 `--emit-meta`、C-02/C-04/C-05 の Python 万能制御、D-01 の Python 画像生成、F-03 の YMM4 表示エミュレーションは `method-rejected`。一方、診断 JSON / IR / manifest / packaging brief、G-24 template source placement、H-02 thumbnail slot patch、H-01/H-02 由来の metadata draft は `goal-allowed` / `successor-lane` として扱う。 | 目的ごと拒否 / 手段単位で拒否 / 一括再有効化なし | 旧拒否理由が「動画品質を上げるためのメタデータ・演出制御・サムネ・YouTube metadata」まで萎縮させるリスクがあったため。禁止対象を危険な生成・エミュレーション手段に限定し、承認済み artifact 経路を邪魔しないため。 |
| 2026-04-27 | **ドキュメント汚染を根絶し、再開時の入口を最小正本へ戻す**。resume 用プロンプト導線を削除し、`verification/` は証跡置き場に降格、`USER_REQUEST_LEDGER.md` は現在有効な要求だけへ圧縮、固定日付風のルール見出しと旧背景アニメ/S6 再採用を廃止する。 | テンプレ維持 / 古い証跡を正本化 / 最小正本へ集約 | 再スタート時の読了過多と「正本っぽい古い文書」による判断汚染が、G-24 `delivery_nod_v1` の作業接続性を落としていたため。 |
| 2026-04-27 | **次期ロードマップは G-24 `delivery_nod_v1` gate-shaped sequence から始める**。formal plan は `delivery_nod_v1` 未報告 / PASS / FAIL / 新規制作案件のどれかを冒頭で宣言し、未報告なら hands-on acceptance、PASS なら `nod` 昇格 + `deny_oneshot`、FAIL なら failure class 分解から開始する。 | 背景アニメ/S6 に戻す / 新 FEATURE を増やす / G-24 gate 分岐で開始 | レガシードキュメント整理後の bottleneck は `audit-skit-group` readiness と user-owned export proof の分離であり、`exact` を export proof と読み替えると status drift が再発するため。根拠: `runtime-state.md` next_action + `verification/P02-production-adoption-proof.md` + `INTERACTION_NOTES.md` TEMPLATE_FORMALISM |
| 2026-04-23 | **Keep the G-24 `nod` cycle at readiness-PASS, but do not promote to `direct_proven` yet**. Assistant rechecked `delivery_nod_v1` on the canonical/proof corpora and confirmed proof-corpus `group_motion_changes=0`. Because the repo still does not track a discrete canonical-project `delivery_nod_v1` copy, Phase 1 is corrected to YMM4 author/export from `samples/haitatsuin_2026-04-12_g24_proof.ymmp` or an equivalent local project, starting from Layer 9 `GroupItem` Remark `haitatsuin_delivery_main`. `skit_group.intent.nod` stays `template_catalog_only` until manual acceptance plus standalone export are confirmed. | Promote now / assume a tracked copy exists / keep the gate but correct the packet | Readiness is already proven, but assuming a nonexistent tracked copy would corrupt handoff. This keeps assistant-owned facts and user-owned export clearly separated while preserving the cautious-gate order. |
| 2026-04-21 | **starter 2 件の standalone native template export を完了扱いにする**。user report により `delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` は名前そのままの GroupItem template として登録済みで、body/face の `ImageItem` 2 点も含めて保存された。これにより starter 2 件は canonical-project copy / production adoption proof / standalone export の 3 点セットを満たしたとみなす。 | export 保留 / starter 2 件だけ export / 5 件一括 export | cautious gate の目的は「急ぎすぎず proof 後に資産化すること」だった。必要最小限の 2 件だけを先に独立資産化したほうが、Atlas 昇格と次の拡張 frontier を明確に切り分けられるため |
| 2026-04-21 | **G-24 cautious gate の Phase 2 を PASS として閉じる**。`samples/haitatsuin_2026-04-12_g24_proof.ymmp` を canonical-anchor + voice-anchored production proof ymmp として採用し、`samples/_probe/skit_01/skit_01_ir.json` に対する `audit-skit-group` と `apply-production --dry-run` を通す。starter 2 件は `exact`、非 starter 3 件も `exact`、`group_motion_changes=0` を確認したため、template-first が production proof 上でも成立したとみなす。 | proof 追加保留 / Phase 2 PASS / すぐ Atlas 昇格 | cautious gate の目的は standalone export 前に content/workflow proof を 1 件閉じることだった。proof ymmp が用意できた以上、そこで止めず repo-local で成立条件を実測し、昇格条件と export 判断を分離したほうが次の判断が明確だから |
| 2026-04-21 | **starter 2 件の manual acceptance を PASS として閉じる**。`delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` の loop・body-face drift は無く、`enter_from_left` に紛れていた退場設定は YMM4 上でカット済みとして扱う。以後の blocker は acceptance ではなく、canonical anchor を持つ voice-anchored production ymmp 不在に切り替える。 | acceptance 継続保留 / PASS 化 / すぐ export | visual acceptance の論点は user 確認で閉じたため。今後は同じ見え方確認を繰り返すより、Phase 2 proof を閉じるための ymmp 条件に集中したほうが bottleneck 直撃だから |
| 2026-04-21 | **G-24 の standalone export を「受入+P02 先行」へ固定**。順番は `manual acceptance` → `1 件の production adoption proof` → `standalone native template export`。proof の内容候補は `skit_01_delivery_dispute_v2` + `samples/_probe/skit_01/skit_01_ir.json` に固定するが、現状 repo には canonical anchor を持つ voice-anchored production ymmp が無いため、Phase 2 は未成立のまま保守的に据え置く。 | 受入後すぐ export / production proof を後回し / 受入+P02 先行 | starter 2 件は repo 内 copy として観測できるが、standalone export を急ぐと content proof と workflow proof が再び混線するため。old corpus の stale gate に戻らず、exact/fallback/manual_note を 1 件で閉じてから昇格させるため |
| 2026-04-21 | **G-24 の初回スターターバッチは 2 件の canonical-project copy として観測済み**。`samples/canonical.ymmp` には frame 306 `delivery_enter_from_left_v1` / frame 658 `delivery_surprise_oneshot_v1` が追加され、assistant は registry / preflight / P02 / handoff をこの project-resident copy に同期した。`delivery_deny_oneshot_v1` / `delivery_exit_left_v1` / `delivery_nod_v1` は registry catalog と canonical-corpus preflight exact を維持するが、starter 完了扱いには含めない。Capability Atlas は `template_catalog_only` を据え置く。 | 5 件一括 / 2 件スターター / canonical のみ | bottleneck は「2 件をまず作って repo 内で観測できる状態にすること」だった。現状の証跡は canonical project 内 copy までなので、過剰に standalone native template library 完了へ昇格させないため |
| 2026-04-20 | **G-24 の正規入口を CLI preflight `audit-skit-group` に固定**。`patch-ymmp` / `apply-production` でも `--skit-group-registry` 指定時は同じ canonical anchor / exact / fallback / manual_note 監査を先に通し、anchor 不在・曖昧・registry 不正なら fail-fast する。 | docs-only 運用継続 / 暫定 script のみ維持 / CLI preflight 化 | `skit_01` を motion proof と template-first proof の間で曖昧にしないため。repo 内 artifact だけで G-24 成立/不成立を assistant-owned に切れる入口が必要で、しかも patch/apply の前に同じ gate を通す必要があるため |
| 2026-04-20 | **ManualSample 非依存の Capability Atlas を operator 正本として追加**。`IR -> registry -> ymmp` の接合点で route を `direct_proven` / `template_catalog_only` / `probe_only` / `unsupported` に分類し、raw effect 名から IR を逆算しない原則を固定する。 | docs 横断のまま運用 / probe packet のみ増やす / Capability Atlas 追加 | ManualSample が無くても『何ができるか』『どこから先が補助か』を repo 内 artifact だけで判断できる必要があるため。G-24 主軸を崩さず、timeline/effect の整理を operator が即利用できる形にするため |
| 2026-04-20 | **`samples/canonical.ymmp` を official canonical anchor artifact として採用**。`haitatsuin_delivery_main` / Layer 9 / ImageItem-only / 左向き基準姿勢を canonical fact とし、`audit-skit-group` success を repo proof に昇格。ただし派生 native template asset 群は未成立のため、intent 側は `template_catalog_only` のまま据え置く。 | canonical を informal sample 扱い / canonical adoption packet 追加 | old corpus の `CANONICAL_GROUP_REMARK_MISSING` を解消しつつ、G-24 completion を過剰宣言しないため。canonical anchor proof と derived asset proof を分離して handoff できるようにするため |
| 2026-04-20 | **`skit_01` の ManualSample gate を workflow breakage として固定し、repo 内 artifact-only audit へ切り替える**。欠落した `_tmp/skit_ManualSample_01.ymmp` を user に再作成させない。正本 [skit_01-workflow-breakage-audit-2026-04-20.md](verification/skit_01-workflow-breakage-audit-2026-04-20.md) / `samples/_probe/skit_01/audit_skit_01_proof.py` | stale handoff を維持 / user に ManualSample 再作成依頼 / repo artifact-only audit | `runtime-state.md` が存在しない ManualSample を参照し、proof docs/prompt が `_tmp/skit_01_v2.ymmp` を指す一方で surviving artifact は `_tmp/skit_01_v2_verify.ymmp`。registry も CLI 未消費のため、現状は G-24 workflow proof ではなく mechanical motion proof と扱うのが正確だから |
| 2026-04-17 | **茶番劇演者の主経路を template-first に固定**。配達員等の外部素材演者は `speaker_tachie` の `motion` と混同せず、**GroupItem canonical template → 小演出テンプレ量産 → production で template 解決 + fallback + manual note** を正本化。[SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) | `motion` 拡張を主軸 / body_map 旧案継続 / template-first | 既存コードの route contract は `TachieItem` / Layer 0 背景 / Group geometry に分かれており、茶番劇演者の量産には直結しない。production bottleneck は direct write 不足より template 資産不足にあるため |
| 2026-04-13 | **茶番劇 E2E 実演 Phase 1/2 PASS**: face 138 + idle_face 16 + slot 10 + motion 6 を IR→apply-production→YMM4 で実証。src/ 変更なし。正本 [CHABANGEKI-E2E-PROOF-2026-04-13.md](verification/CHABANGEKI-E2E-PROOF-2026-04-13.md) | 既存 done 機能のみ / 新規実装 | トラック A（演出 IR 実戦）のサブセットとして、追加コード変更なしで E2E パイプライン動作を実証 |
| 2026-04-13 | **表情指定: テンプレ（プリセット名）のほうが実用的**。パーツ個別指定（face_map の Eyebrow/Eye/Mouth パス）だと YMM4 上で「カスタム」表示になり、運用上不便。将来の face_map 構造見直しの根拠 | パーツ指定維持 / テンプレ指定移行 | オペレータフィードバック。E2E Phase 1/2 で発見 |
| 2026-04-13 | **体テンプレ構想**: 別体素材（配達員等）にゆっくり頭を重ね、テンプレ蓄積→IR で指定する将来像。グループ制御で移動・拡大縮小は破綻なし。左右反転は素材分割が必要。FEATURE 起票は別ブロック。正本 [TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md) §7 / [TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §3.2 | 体テンプレ / パーツ差替（G-19）/ 保留 | オペレータ調査で YMM4 のグループ制御仕様を確認。IR + レジストリで制御する設計は overlay/bg と同型で実現可能 |
| 2026-04-12 | **P0 Block-A タスク再設計クローズ**: [P0-BLOCK-A-AND-PATH-A.md](verification/P0-BLOCK-A-AND-PATH-A.md) を正本化。[runtime-state.md](runtime-state.md) の P0 優先行を「C-09 必須」と読めないよう修正。Block-A＝S-4 読込エラーのみ／NotebookLM 準拠稿は経路 A で可 | 表を据え置き / 正本化 | CSV 手前で台本改善を前提にするとオペレータがブロックするため。機械再スモーク `samples/p0_steering_v14_2026-04-12_*` |
| 2026-04-11 | **正本の表現是正**: 「運用で二系統ある」という断定を撤回。**案件ごと可変**・現状が原文寄りでも本番固定ではない旨を bottleneck #1 と [P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) に反映。C-09 は任意、v14 は repo 検証アンカーと明記（[P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md) 等） | 二系統を正本に残す / 撤回 | ユーザー指摘: 二系統はエンティティ調査ではなく文書整理枠であり、本番方針まで固定しないため |
| 2026-04-11 | **開発正本から壁時計 cadence を除外**: 「2 週間」「週 1 回」「60〜90 分の固定ブロック」等の運用を repo 正本に置かず、**工程到達**（S-4 等）とオペレータセッション単位で記述する。反映: [P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md)、[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)、[LANE-C-operator-prep-2026-04-09.md](verification/LANE-C-operator-prep-2026-04-09.md)、[PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)、`runtime-state.md` の `next_action` | 週次を正本に残す / 到達のみ | 開発リズムをカレンダー週に束縛しないため |
| 2026-04-11 | **P0 縦優先の固定**: 本編主軸＝AI監視 v14（`samples/v14_t3_ymm4.csv`）。Amazon Panopticon の B-11 §2 は **横**（別オペレータセッション）。正本 [P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md)。P01 行 `p0_mainline_v14_steering_2026-04-11_a`（機械再スモーク）。`runtime-state.md` の `next_action` を P0 先頭へ。旧 T1 DOCSAMPLE の `validate-ir` は当時 PASS 済みだが、現行判断には使わない。 | Amazon 縦を先に採る / 本編のみ固定 | 縦スライスが品質横展開に埋もれないよう、YMM4 到達工程を 1 本に束ねるため（週 cadence は正本に置かない） |
| 2026-04-11 | レーン B（ファイル5）再検証: [LANE-B-execution-record-2026-04-09.md](verification/LANE-B-execution-record-2026-04-09.md) §8 を追記。正本コミット `927588e`、`validate-ir` / `apply-production --dry-run` を再実行し PASS。B-1/B-4/B-5 は従来方針継続。Custom GPT Instructions 突合はオペレータ（repo 外） | 再検証スキップ / 証跡のみ更新 | Prompt-B・ファイル2「プロンプト同期」の参照コミットを現 HEAD に更新するため |
| 2026-04-11 | **T0 クローズ（履歴）**: 旧コア計画で **T1-P2-DOCSAMPLE** / **T1-RUNBOOK-GUI** を起票し、開発フェーズを **T1** へ移行した。2026-04-27 の整理で当該計画文書は削除済み。 | 承認前に T1 着手 / T0 で差し替え協議 | 当時のゲート履歴のみ残す。現行の再開判断は `runtime-state.md` と G-24 gate を優先するため |
| 2026-04-10 | レーン B（ファイル5）再検証: [LANE-B-execution-record-2026-04-09.md](verification/LANE-B-execution-record-2026-04-09.md) §7 を追記。正本コミット `fb0659a`、`validate-ir` / `apply-production --dry-run` を再実行し PASS。B-1/B-4/B-5 は 2026-04-09 方針継続。Custom GPT Instructions 突合はオペレータ（repo 外） | 再検証スキップ / 証跡のみ更新 | 当時のプロンプト同期記録要件を満たすため。現行判断には使わない |
| 2026-04-10 | コア本開発の **フェーズ T0〜T3** と並行レーンの相性を旧文書で一時整理した。2026-04-27 の整理で旧設計文書・旧 Prompt ハブは削除済み。 | タスク設計なしで Prompt のみ / 設計ドキュメントを分離 | 履歴のみ残す。現行の作業接続は `runtime-state.md` / `verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md` / `verification/P02-production-adoption-proof.md` を使うため |
| 2026-04-10 | 並行レーン証跡・H-05（`score-thumbnail-s8`）・旧視覚品質パケット文書を master に統合コミットし、当時は次期コア実装をプラン設計・起票から再開するゲートに固定した。 | 実装を続行 / プラン入口で一旦止める | 2026-04-27 の整理後は、旧プラン入口ではなく `runtime-state.md` の G-24 gate から再開するため |
| 2026-04-09 | レーンB実施計画（Custom GPT / 2体分離）を実行し、運用固定を記録: [LANE-B-execution-record-2026-04-09.md](verification/LANE-B-execution-record-2026-04-09.md)。B-4 は「brief を会話ごとに先貼り」。B-5 は後続整理で、H-02厳密時も素案時も S8 を別レーンに分離 | 方針未固定のまま運用 / 連携方式を固定 | Instructions 側のドリフトを避け、案件ごとに迷わず切替できる最小運用を先に確立するため |
| 2026-04-09 | レーン E（サムネ S-8）の **repo 準備サイクルを完了・運用クローズ** とする: [LANE-E-S8-prep-2026-04-09.md](verification/LANE-E-S8-prep-2026-04-09.md) 運用クローズ節、P03 `lane_e_prep_2026-04-09_a`。公開直前の実 1 枚は P3・runbook トラック E で並行。**本開発幹へ復帰**（`runtime-state.md`） | 準備を開発ブロックに残す / クローズしてコアへ | 正本・チェックリスト・既定案件入力は repo 固定済み。YMM4 実書き出しは公開タイミングのオペレーションのためコア開発をブロックしない |
| 2026-04-09 | レーン B（GUI LLM 正本同期）の **repo 側準備を完了** とする: [LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md)、[samples/packaging_brief.template.md](../samples/packaging_brief.template.md)、[gui-llm-setup-guide.md](gui-llm-setup-guide.md) の v4 正本優先化、runbook B-1/B-4/B-5 の整合。以降の主作業は **本開発幹**（`runtime-state.md` のコア・P0・B-11 ゲート等）。Custom GPT 等への実貼り付けはオペレータがチェックリストで実施 | 文書のみ完了扱い / 貼り付け完了までブロック | 正本と手順は repo に固定済み。GUI 同期は人間作業のため開発レーンをブロックしない |
| 2026-04-08 | P2 次サイクルで map 警告解消（`bg_anim_map` + `transition_map`）後に `test_verify_4_bg.ymmp` へ 4 セクション拡張適用を実施。`BG anim writes: 7` を確認 | 警告放置で拡張 / 先に警告ゼロ化 / bg_anim いったん停止 | 原因切り分けを明確化したうえで拡張でき、短サイクルの再現性を高められるため |
| 2026-04-08 | B-11 を最小クローズ（半分確認時点）し、改行 Pass / 辞書 0 をもって Gate B（運用側移行）を仮確定。P2 背景アニメ小規模適用を先行 | Gate A 維持 / Gate B 仮確定 / B-11 完全完了待ち | ループ停止を避けて最短で演出実戦へ入るため。`test_verify_4_bg.ymmp` で route は profile contract pass、`p2_bg_anim_small_scope.ir.json` で `BG anim writes: 2` を確認 |
| 2026-04-08 | B-11 AI監視 proof の取込後記録を集約し、Gate A（改行系支配）を確定。`runtime-state.md` の `next_action` / P0 説明を Gate 根拠付きへ更新 | 保留継続 / Gate 判定を先に固定 | 次プランを感覚で動かさず、4 区分実測（辞書 0 / 手動改行 5 / 再分割 10 / タイミング 0）で優先順位を固定するため |
| 2026-04-08 | 次以降の推奨プランを `runtime-state.md` に正本化（P0 Phase1 本番 1 本・P1 H-01 運用・P2 演出実戦・P3 サムネ・Parking motion ブランチ）。GUI CSV 同梱診断 JSON を Phase 1 導線に明記 | 暗黙の優先 / 文書固定 | 実制作 bottleneck 軽減レーンを再アンカーし、未承認実装を増やさない |
| 2026-04-07 | G-18 SE `AudioItem` 挿入を実装（`samples/AudioItem.ymmp` readback、`_apply_se_items`、テンプレート deepcopy または最小骨格）。旧 SE unsupported failure class を廃止 | ゲート維持 / 実装 | サンプルと骨格で write route を確定し、G-13 の `se` を mechanical scope まで拡張 |
| 2026-04-06 | G-15〜G-17 を実装（Micro `bg` 発話スパン / `overlay` 配列 / `--timeline-profile` + motion・transition・bg_anim マップ）。G-18 は AudioItem ymmp サンプル入手まで保留（verification に明記） | 一括 / ゲート付き | P2C に沿い SE write は corpus 確定後。G-12 `timeline_route_contract.json` と契約検証を先に置く |
| 2026-04-06 | 視覚三スタイル（挿絵コマ / 再現PV / 資料パネル）を IR 既存語彙にマッピングし doc 正本化。延伸は G-15〜G-18 proposed | 一括実装 / 文書→テンプレ→Writer→台帳パケット | patch 制約（単一 overlay・セクション bg のみ・motion 未書込）を隠さず、`VISUAL_STYLE_PRESETS.md` と v4 プロンプトで Writer と運用を揃える |
| 2026-04-06 | G-15〜G-18 のゲートと feat/phase2-motion-segmentation の保留判断を一度文書化。現在の正本は FEATURE_REGISTRY と各 verification 証跡に統合済み | 未承認を approved に昇格 / 文書のみ | プランに沿いゲートを明文化。実装は承認後のみ |
| 2025 | CLI パイプラインとして構築 | CLI / Web UI / Electron | 最小構成で検証可能 |
| 2025 | IP-01 No-Go | Go / No-Go | 要件未充足 |
| 2025 | Web UI / API / YouTube 連携は後回し | 優先 / 後回し | ロバスト性検証が先 |
| 2026-03-29 | B-10 (--emit-meta) を未承認で混入 | — | 未承認。後に rejected → コード除去 |
| 2026-03-30 | FEATURE_REGISTRY + AUTOMATION_BOUNDARY で機能管理 | 台帳管理 / ad-hoc | 未承認機能混入の再発防止 |
| 2026-03-30 | 自動化レイヤーを L1〜L4+GUI の5層で定義 | 5層 / 3層 / フラット | YMM4内部/外部の境界を明確化 |
| 2026-03-30 | Python での生成・レンダリングを手段単位で禁止 | method-rejected / 全面禁止 / 部分許容 | .ymmp ゼロ生成・音声合成・画像生成・YMM4 表示エミュレーションは不可。この教訓は「目的の禁止」ではなく「危険な手段の禁止」として扱う。CSV / IR / registry / manifest / brief 生成と、台本読込後 `.ymmp` への限定 patch は許容する。rejected: B-10, C-02, C-03, C-04, C-05, D-01, F-03 |
| 2026-03-30 | 外部メディア取得は分離設計で OK | L1拡張許容 / L2専念 | 取得機能と受け取り機能を分離すれば NLMYTGen に含めてよい。最終的に自動化する方針 |
| 2026-03-30 | WORKFLOW.md を S-0〜S-9 の全工程に再設計 | 全面改訂 / 部分改訂 | 前作業者がrejectedで隔離しただけでYMM4側の代替ワークフローが欠落していた。S-5(演出)が5行だけだった。rejected工程の代替手段を全てWORKFLOW.mdに記載 |
| 2026-03-30 | E-02 を先に仕様定義する | E-02 / A-04 / F-01 / 全件hold | ユーザーが選択。L2変換レイヤーで Python スコープ内に収まる唯一の候補 |
| 2026-03-30 | E-02 は単体では価値が薄い | 着手 / 先送り / E-01とセット | YouTube Studio へのコピペが CLI テンプレートに変わるだけ。E-01 (API投稿) とセットでないと実質的効率化にならない |
| 2026-03-30 | S-5 (字幕はみ出し) が最優先の痛点 | S-5 / S-6 / S-2 | ユーザーフィードバック。S-5/S-6 が最も時間がかかる工程 |
| 2026-03-30 | S-6 トピック分析は stdlib 制約内では精度不足 | パターンマッチ / 軽量NLP / やらない | パターンマッチ30-50%、NLP 40-60%+当時の root agent doc 違反。LLM アダプター方式に転換予定 |
| 2026-03-30 | B-04 表示幅ベース分割を実装 | 表示幅 / 文字数維持 | 全角=2,半角=1 の display_width で YMM4 字幕はみ出しを事前防止。--display-width, --max-lines, --chars-per-line 追加 |
| 2026-03-30 | S-6 トピック分析を LLM アダプター方式に転換 | LLM / パターンマッチ / やらない | ユーザー指示。コーパス分析ライブラリはレガシー化しており LLM に統一。モデル切替可能なアダプター設計 |
| 2026-03-30 | サムネイルはYMM4テンプレートの文字・画像入れ替え | テンプレート手動 / Python自動生成 / 外部ツールのみ | Python 画像生成は不可。YMM4 テンプレートの手動カスタマイズを基本にし、後続 H-02 の `thumbnail_design` と `thumb.*` slot 限定 patch は successor-lane として許容する。サムネイルは非常に重要 |
| 2026-03-30 | A-04 / D-02 / F-01 / F-02 を quarantined に移す | proposed維持 / hold / quarantined | B-10 混入時の汚染バッチ由来で、個別再審査前に通常 backlog として扱うと再発するため |
| 2026-03-30 | A-04 を done に戻す | quarantined維持 / hold / done | RSS/Atom からタイトル抽出して NotebookLM 検索クエリへ渡す `fetch-topics` は Python のテキスト取得責務に収まり、実装と台帳が一致したため |
| 2026-03-30 | E-02 を hold に移す | proposed維持 / hold / rejected | 価値検証の結果、単体では bottleneck を減らさず、今は進めない方が正確だから |
| 2026-03-30 | C-01 を done ではなく info に整理する | done維持 / info | Python 機能ではなく、確認済みの手動工程だから |
| 2026-03-30 | canonical docs の雛形放置を handoff 不備として扱う | 雛形維持 / 内容補完 | `8a1c710` で docs は追加済みだったが、実内容が薄いままでは resume 時の再アンカー先として機能しない |
| 2026-03-30 | `docs/ai/*.md` を canonical rules として先に読む | helper docs優先 / canonical rules優先 | tool-specific helper docs や prompt より repo 内 canonical rules を先に読む方が再開の一貫性が高い |
| 2026-03-30 | docs-only handoff 用の単一 resume prompt を採用（2026-04-27 に廃止） | promptなし / prompts分散 / 単一resume prompt | 当時は次セッション開始手順を repo 内で完結させるため |
| 2026-03-31 | B-11 S-5 workflow proof を approved frontier にする | S-5 workflow proof / S-6 LLM adapter / hold継続 | ユーザーが S-5 を先に進めると承認。最大 pain に近く、Python の責務境界を壊さずに workflow proof を積めるため |
| 2026-03-31 | B-12 行バランス重視の字幕分割を実装する | proposal packet のみ / `--balance-lines` 実装 | S-5 proof で辞書や timing ではなく改行系 pain が支配的と確認できたため、2行字幕向けの自然改行 heuristics を opt-in で実装 |
| 2026-03-31 | B-13 を次候補として proposal 化する | B-12 継続 / clause-aware split + widow guard | B-12 は手動改行を減らしたが、長文再分割 15 件と 1 文字最終行が残り、次の主 pain が節分割と widow/orphan 回避に絞れたため |
| 2026-03-31 | B-13 節分割 + widow/orphan guard を実装する | proposal のみ / `--balance-lines` 内部改善 | 句読点の少ない長文と 1 文字最終行を減らす最短経路で、既存フラグのまま改善できるため |
| 2026-03-31 | B-14 を次候補として proposal 化する | B-13 継続 / aggressive clause chunking | B-13 で手動改行は 5 まで減ったが、再分割 10 と長い一文 1 字幕問題が残り、より積極的な chunking の要否を切り分ける必要があるため |
| 2026-03-31 | B-14 aggressive clause chunking を実装する | proposal のみ / `--balance-lines` 内部改善 | B-13 のままでは複数文発話の中にある単一長文が展開されず、operator pain の主因が残ったため。先に CLI 側でどこまで崩せるかを確かめる価値があった |
| 2026-03-31 | S-6 LLM 活用は API SDK ではなく GUI LLM (Custom GPT / Claude Project 等) を優先する | API adapter / GUI LLM / やらない | ユーザー希望。API SDK 導入は stdlib 制約緩和 ADR が必要で依存が増える。GUI LLM ならプロンプトテンプレートのみで Python 変更不要 |
| 2026-03-31 | B-15 改行コーパス収集を approved にする | B-14 継続 / corpus 収集 / hold | B-14 で bulk overflow 収束後、残 pain は個別ケース。heuristic 追加より corpus → 傾向化 → ルール化が強い |
| 2026-03-31 | C-07 S-6 演出メモ生成を proposed にする | proposed / hold / skip | GUI LLM でプロンプトテンプレートを作成し、実動画 1 本で workflow proof する方式。Python 変更なし |
| 2026-03-31 | B-15 をコーパス収集からトップダウン改行再設計に拡張する | パッチ (P1/P2) / トップダウン再設計 / hold | 初期コーパスの傾向分析で現行ボトムアップ方式の構造的限界 (2層の噛み合い不良、全体を見ない局所最適) を特定。ユーザー提案のトップダウン方式が実装可能かつ管理可能と判断。パッチ積み増しより根本解決を選択 |
| 2026-03-31 | 以前会話内でリジェクトされたトップダウン型分割アルゴリズム案を再評価・採用する | 再採用 / パッチ維持 / 別方式 | 当時のリジェクト理由は DECISION LOG に未記録。現在のコーパスで構造的問題が実証されたため、たたき台として再検討。仕様を精緻化し `reflow_utterance()` として実装する方針 |
| 2026-03-31 | 視覚系タスク (背景動画・アニメーション・サムネイル) への着手意向を記録 | 記録 / 即着手 / 無視 | ユーザー希望。字幕分割に目処がつけば次のペイン。D-02 quarantined / D-01 rejected のため権利・境界の再整理が前提。当面は字幕分割を優先 |
| 2026-04-01 | B-15 手動検証: 小区切り (漢字→ひらがな、カタカナ→ひらがな) を候補から除去 | 除去 / penalty引上 / 維持 | ユーザーフィードバック。「単/なる」「見間違/った」のような切断が発生する。大区切り (句読点) がない場所では分割しない方針を徹底。文字種境界より行長精度を優先 |
| 2026-04-01 | B-15 手動検証結果: 明らかなバランス偏りは解消、若干の違和感は残存 | 継続改善 / done化 / hold | ユーザー評価。4行またがり解消、漢字/カタカナ途中切断は改善中。次頁区切り(話者行分割)と同一ページ内改行の区別が今後の課題 |
| 2026-04-01 | B-15 を一旦区切り、残課題を B-16 として分離する | 区切り / 続行 | ユーザー判断。ページ間分割は改善されたが、行内折り返し制御には「1行/1ページ最大文字数から逆算する外殻」が必要で別タスク。画像関連が完全停止しているため、プラン再構成を優先 |
| 2026-04-01 | 開発プラン再構成: C-07→視覚系→B-16 の順で進行 | C-07優先 / B-16優先 / 視覚系優先 | C-07 (演出メモ) が最も軽く、視覚系の入口にもなる。C-07 結果を踏まえて D-02 再審査と視覚系の具体策を決定。B-16 は並行進行可能。E-02 は hold 継続 (E-01 とセットでないと価値が出ない判断は変わらず) |
| 2026-04-01 | 視覚系タスクの start gate を C-07 workflow proof 完了後に設定 | C-07後 / 即時 / hold | C-07 の背景キーワード有用性が視覚系の価値経路の入口。成功なら D-02 再審査へ、失敗ならプロンプト改善 or 手動継続 |
| 2026-04-01 | D-02 再審査チェックリストを作成 | 作成 / 後回し | 取得元、権利、取得/受取分離、YMM4受渡、価値経路、既存フローの6項目。C-07 proof 後に実施 |
| 2026-04-01 | C-07 v1 proof 結果: 2/3 OK だが背景候補の方向が違う | 方向転換 / v1維持 | ストック素材検索は価値が低い。実際に必要なのは「茶番劇風アニメーション + 図解アニメーション」の演出指示。4パターン (茶番劇/情報埋め込み/雰囲気演出/黒板型) を基軸にプロンプトを v2 に改善 |
| 2026-04-01 | 視覚系の最大ペインは「何を表示するか」の判断 + 情報不足時の取材 | 判断支援 / 配置自動化 / 素材API | ユーザーフィードバック。配置作業自体よりバランス判断と素材集めが重い。D-02 の方向性を「素材API」から「演出判断支援」に転換 |
| 2026-04-01 | C-07 v3: マクロ演出設計 + 素材調達ガイドを追加 | v2維持 / v3拡張 / 別プロンプト | C-07 v2 はミクロ (発話単位) のみ。ユーザーの最大ペイン (何を表示するか + 素材調達) はマクロ判断。Part 1 (全体設計) + Part 3 (調達ガイド) を追加し二層構造に拡張 |
| 2026-04-01 | D-02 再審査チェックリストを演出判断支援向けに改訂 | 旧チェックリスト維持 / 改訂 | 旧6項目は素材API方向のもの。方向転換により不適合。C-07 v3 統合/スコープ/価値経路/実装形態/ワークフロー位置/proof依存度の6項目に置換 |
| 2026-04-01 | D-02 の演出判断支援は C-07 v3 に暫定統合 | 独立機能 / C-07統合 / 両方 | ミクロ/マクロを流動的に組み替える方針。独立機能にするかは proof 結果で判断 |
| 2026-04-01 | 演出支援を5レイヤー (L-macro/L-micro/L-section/L-research/L-thumbnail) で整理 | レイヤー分離 / フラット | タスク ID に固執せず、機能をレイヤーとして捉え、後から統合・分割しやすい構造にする |
| 2026-04-01 | C-07 v3 proof 完了。D-02 を hold に変更 | hold / proposed / rejected | v3 出力レビューで L-macro + L-research が有用と確認。D-02 は C-07 v3 に吸収完了。独立機能不要 |
| 2026-04-01 | 作業時間実態: 10分動画で約1週間。長尺化で10分あたり約25%減衰 | 記録 | 素材再利用・パターン定着により摩擦が逓減する構造 |
| 2026-04-01 | proof は出力レビューで完了とし、実動画制作を要件としない | 軽量proof / 実動画proof | 実動画制作は重すぎてブロッカーになる。計測より実用を優先 |
| 2026-04-01 | YMM4 自動化の経路: プラグイン API 先行 → ymmp 直接編集を補完 | プラグインのみ / ymmp のみ / 二段階 | プラグイン API (IToolPlugin) が公式経路。タイムライン操作可否は未検証のため spike で確認。不可なら ymmp 編集を主経路に切替 |
| 2026-04-01 | YMM4 以外の動画制作パイプラインは検討対象外 | YMM4専念 / 代替検討 | ユーザー指示。ffmpeg/MoviePy 等での独自レンダリングは除外 |
| 2026-04-01 | アニメーション自動化 (G-01~G-04) を最優先フロンティアに設定 | アニメ自動化 / YT自動化 / 字幕改善 | S-6 が制作時間の70%以上を占める。ユーザーが「重い上にまだ何もできていない」と指摘 |
| 2026-04-01 | NotebookLM 自動化は NLMYTGen 外。台本入手後の工程に専念 | NLMYTGen内 / 別システム | 台本入手は折衷案 (前処理自動化 + NLM は読解/音声化のみ) で、動画制作が回り始めてから別途構築 |
| 2026-04-01 | G-01~G-04 を FEATURE_REGISTRY に proposed として登録 | 登録 / 保留 | 調査完了。実装承認は spike 結果を踏まえて判断 |
| 2026-04-01 | YMovieHelper を発見。CSV→ymmp 生成 (表情+動画切替対応) の既存ツール | 自前構築 / 既存ツール活用 | 自前でゼロから構築するより既存ツールと接続する方が現実的 |
| 2026-04-01 | G-01 (IToolPlugin spike) の優先度を最下位に変更 | 最優先維持 / 最下位 | タイムライン操作 API が非公開。.NET 環境構築の投資対効果が不明。YMovieHelper 連携で不十分な場合の代替経路 |
| 2026-04-01 | G-02 を YMovieHelper 詳細調査に再定義し最優先に | G-01先行 / G-02先行 | YMovieHelper が既に背景/表情/動画切替を実現しているため、入力仕様を把握して NLMYTGen と接続するのが最短経路 |
| 2026-04-01 | G-05 (build-ymh) を新規追加 | 追加 / 不要 | C-07 v3 の演出メモ → YMovieHelper 入力形式に変換する Python サブコマンド。G-02 の結果が前提 |
| 2026-04-01 | ymmp 直接編集は控える。完成品の解析研究のみ | 編集許可 / 研究のみ | 過去にデッドファイルが積み上がった経験。研究に没頭して開発から逸れるリスク |
| 2026-04-01 | テンプレート資産蓄積戦略を採用 | テンプレート / 毎回手動 | 制作者がテンプレートを用意→汎用素材化→リソース積み上げ。C-07 v3 がテンプレート選定を提案、build-ymh が仮組立。NLMYTGen は提案と仮組立まで、素材の完全自動生成には踏み込まない |
| 2026-04-01 | ドリフト防止ルールを INVARIANTS に固定 | 記録 | テスト目的化禁止、proof 軽量化、研究2ブロック制限。INTERACTION_NOTES にも開発ドリフト回避セクション追加 |
| 2026-04-01 | YMovieHelper を主軸から参照実装に格下げ (第三次改訂) | 主軸維持 / 参照実装 / 完全除外 | サービス終了済み Web アプリ (Docker+WSL+Go+TS)。CLI ではない。メンテナンス停止。設計思想の回収のみ。ツール依存は作らない |
| 2026-04-01 | 自動化の中核を「演出 IR + テンプレート資産」に転換 | ツール依存 / IR 中心 | 特定ツールに依存せず、NLMYTGen 独自の演出中間表現を定義。LLM は意味ラベルのみ出力し、座標変換はテンプレート定義側で解決 |
| 2026-04-01 | G カテゴリ再定義: G-02=IR語彙定義, G-05=IR出力プロンプト, G-06=接続方式決定 | 再定義 / 据置 | G-01/G-03 は hold。G-02 を YMovieHelper 調査 → IR 語彙定義に変更。build-ymh (旧G-05) は廃止し、IR 出力プロンプト (新G-05) に置換 |
| 2026-04-01 | YMovieHelper に言及する際のルール: 「使う」「接続する」ではなく「参考にする」「観察する」と書く | 記録 | 今後のドキュメントでの勘違い防止 |
| 2026-04-01 | G-02 演出 IR 語彙定義 v1.0 完了 | 完了 | `docs/PRODUCTION_IR_SPEC.md` 作成。9フィールド (template/face/bg/bg_anim/slot/motion/overlay/se/transition)、Macro+Micro 二層構造、JSON/CSV 二重表現、carry-forward ルール。S-6 の6手動工程を全カバー |
| 2026-04-02 | 正本ドキュメントを演出IR主軸に更新 | 修正 | README/WORKFLOW/AUTOMATION_BOUNDARY/INVARIANTS から「CSV変換専用ツール」旧理解を除去。再開時の旧理解引き戻しを構造的に防止 |
| 2026-04-02 | G-05 C-07 v4 IR 出力プロンプト作成 | 完了 (proof待ち) | `docs/S6-production-memo-prompt.md` v4 セクション。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の Macro+Micro IR JSON を出力するプロンプト。v3 (自然文) との切替可能。proof はユーザーが Custom GPT で実施 |
| 2026-04-02 | ymmp 後処理の実機検証: 表情パーツ差し替えが動作することを確認 | 実証済み | Python で ymmp JSON のパーツパスを書き換え→YMM4で正常に開ける。音声・字幕は台本読込で確保済みのまま維持。二段階方式 (台本読込→ymmp後処理) が実現可能と確定 |
| 2026-04-03 | YMM4 テンプレートは独立ファイルではなく ItemSettings.json 内の Templates 配列に保存 | 実測確定 | テンプレートの Items 構造は ymmp Items と同一。Adapter ロジック再利用可能。エフェクト・VoiceCache もテンプレートに完全保持 |
| 2026-04-03 | Custom GPT v4 proof 完了 | 実証済み | 28 utterances / 5 sections / 全語彙チェック PASS / Macro-Micro 整合OK。carry-forward は全件フル指定 (省略なし) |
| 2026-04-03 | Custom GPT v4 の IR 出力は 2オブジェクト連結形式 (Macro + Micro) | 実測確定 | load_ir() で単一 JSON と連結形式の両方に対応。CLI patch-ymmp で動作確認済み |
| 2026-04-03 | production-slice patch-ymmp proof 完了、ただし full E2E は実制作 ymmp 不在で未閉塞 | 実証済み / 要再確認 | `samples/test - marisaFX.ymmp` に実IR先頭11発話を適用し face 13 / bg 2 変更を確認。`samples/v4_re.ymmp` は current workspace で未確認のため、28発話 full E2E は次ブロックへ持ち越し |
| 2026-04-03 | Template Registry は visual-review 前提。`extract-template` は棚卸し補助であって意味ラベル推定器ではない | 運用確定 | 表情ラベルは YMM4 上で見え方を確認して人間が命名する。現行 `patch-ymmp` のフラット `face_map` は単一キャラ proof 向けで、複数キャラ案件の最終形は character-scoped registry が必要 |
| 2026-04-05 | face_map を character-scoped に、bg_map は flat を維持 | 実装確定 | face は同じラベルでもキャラごとにパーツが異なる。bg は scene/preset 責務で話者固有ではない |
| 2026-04-05 | Remark フィールドを extract-template --labeled のラベル源に採用 | 実装確定 | Serif は発話テキスト用。Remark は VoiceItem / TachieItem / TachieFaceItem / ImageItem の全てに存在する空きメタデータ欄 |
| 2026-04-05 | row_start / row_end で IR 意味単位と VoiceItem 粒度差を吸収 | 実装確定 | IR を 60 発話に崩す案 (A) とテキストマッチング (C) を却下。IR の意味単位を保ったまま複数 VoiceItem に適用する方式 (B) を採用 |
| 2026-04-05 | idle_face: IR フィールド追加 + TachieFaceItem 挿入方式 | 実装確定 | TachieItem の表情制御ではなく、IR に idle_face を追加して adapter が non-speaker 側に TachieFaceItem を挿入。既存 face 適用経路を崩さず拡張 |
| 2026-04-05 | bg section 切替 proof 成功 (2 ラベル) | 実証済み | 5 セクションのうち 2 ラベルで背景切替を確認。残りはユーザーが bg_map を拡張するだけ |
| 2026-04-05 | `.claude` 側に常設ガードを追加 | 実装確定 | 毎回 prompt に重い禁止を書き足さず、repo-local 入口と hooks で repo 外逸脱 / broad question 停止 / repeated visual proof を抑止する |
| 2026-04-05 | face サブクエストの completion criteria を固定 | 継続調整 / failure class 固定 | face を未整理な改善ループではなく completed subsystem として扱うため。mechanical failure は class 名で止め、人間判断は creative quality に限定 |
| 2026-04-05 | apply-production は partial face output を書かない | patch 先行 / fail-fast | row-range 不整合、validation error、fatal face patch warning を書き出し前に止め、ymmp 化→手動確認ループを再発させないため |
| 2026-04-05 | Packaging / marketing レイヤーを独立 frontier として backlog 化 | C-08 個別改善 / E-02 再開 / packaging layer 新設 | 台本→タイトル侵食を止め、タイトル / サムネ / 台本の整合を 1 つの central brief で管理するため |
| 2026-04-05 | H-01 Packaging Orchestrator brief schema v0.1 を定義 | backlog のみ / schema 定義 | H-01 を abstract な気づきで終わらせず、C-07/C-08/E-02/H-04 が参照できる正本フィールドへ落とすため |
| 2026-04-06 | H-01 workflow proof packet を整備 | schema のみ / proof packet まで整備 | H-01 を `approved` のまま放置せず、user が 1 本の実台本で drift を観測できる実行単位まで前進させるため |
| 2026-04-06 | H-02 Thumbnail strategy v2 schema v0.1 を定義 | backlog のみ / schema 定義 | H-02 を感覚的な運用メモではなく、C-08 が参照できる specificity-first / banned pattern / rotation policy の正本へ落とすため |
| 2026-04-06 | H-04 Evidence richness score schema v0.1 を定義 | backlog のみ / schema 定義 | H-04 を曖昧な「内容が強いか」ではなく、promise_payoff と evidence category に分解された repair-oriented gate にするため |
| 2026-04-06 | H-04 manual scoring proof packet を整備 | schema のみ / proof packet まで整備 | H-04 を机上定義で終わらせず、warning を script/packaging repair に変換できる実行単位まで前進させるため |
| 2026-04-06 | H-02 は dry proof を先に通し、strict GUI rerun proof と分離して扱う | strict proof 待ち / dry proof 先行 | 既存 artifact だけでも specificity-first / banned pattern / rotation contract が機能するかを確認でき、GUI rerun 待ちで packaging lane 全体を止める必要がないため |
| 2026-04-06 | H-01 はまず repo-local dry proof を通し、strict な GUI rerun proof と分離して扱う | dry proof なし / strict proof 待ち / dry proof 先行 | 既存 artifact だけでも brief が共有契約として機能するかは確認でき、strict な before/after rerun 待ちで packaging lane 全体を止める必要がないため |
| 2026-04-06 | H-03 を packaging lane の最後の未定義ピースとして先に定義し、strict GUI rerun とは分離して進める | GUI rerun 完了待ち / H-03 先行定義 | visual stagnation risk は repo-local brief/cue/script だけでも warning 化できるため、外部 GUI 実行待ちで spec 定義全体を止める必要がないため |
| 2026-04-06 | H-04 AI監視 sample は `acceptable` と判定し、主要 warning を anecdote continuity と late payoff に集約 | 高評価でそのまま通す / vague score に留める / warning を repair に落とす | H-04 の価値は数値化より repair 指示にあるため、包装 promise と本文根拠のズレを具体修正へ還元できる形で残す必要があるため |
| 2026-04-06 | G-11 slot patch hardening を実装完了 | proposed 維持 / 実装完了 | timeline edit を broad manual retry loop にせず、slot を deterministic patch + fail-fast validation の packet として閉じるため |
| 2026-04-06 | G-12 は patch 前に readback harness と route contract 照合を先行実装 | 先に patch / 先に measurement harness | native route を未確定のまま `motion` / `transition` / `bg_anim` の adapter write に進むと、file-format risk と creative judgement が再混線するため |
| 2026-04-06 | G-12 の current contract は `test - marisaFX.ymmp` で通し、`production.ymmp` の `bg_anim` miss を failure class として扱う | gap を黙殺 / warning 扱い / failure class 化 | timeline quality 問題を visual impression に戻さず、route gap を mechanical failure として扱うため |
| 2026-04-06 | G-12 measurement packet を追加し、current corpus で route narrowing を先に完了 | harness のみ / packet 化して route narrowing | `motion` / `bg_anim` は current corpus で狭め、manual frontier を `transition` probe 1 本へ縮めると、operator の判断負荷を最小化できるため |
| 2026-04-06 | fade-family `transition` route を ymmp_measure で回収可能にし、G-12 contract を更新 | `transition` を route 不在扱い / fade-family route を corpus-derived contract 化 | repo-local corpus に既にある fade key を拾えば、手動 probe を増やさずに `transition` の主要 family を mechanical に確定できるため |
| 2026-04-06 | G-13 overlay / se insertion packet を completed として閉じる | overlay/se を broad manual frontier に残す / packet として閉じる | `overlay` は registry + timing anchor から deterministic な `ImageItem` 挿入まで閉じた。当時 `se` は timing までで write route 不在を旧 unsupported failure class で fail-fast（G-18 で挿入まで実装） |
| 2026-04-06 | Phase 1 として B-18 台本機械診断と C-09 refinement プロンプトを実装完了 | 保留 / 実装 | `diagnose-script`・`script_diagnostics.py`・`S1-script-refinement-prompt.md`・GUI 品質タブ・B18 dry proof まで一括 |
| 2026-04-06 | Next roadmap: P01 運用手順、P2A feat ブランチレビュー（一括マージ不採用）、P2B+G-14 production contract、P2C SE 境界、サムネ 1 枚チェックリスト | 未実施 / 実施 | Phase 2/3 の文書・contract 整備を master に反映 |
| 2026-04-05 | サムネイル戦略は抽象煽りより具体数値・固有名詞優先 + rotation 管理 | 定型煽り / 具体性優先 / 各動画場当たり | 本文根拠とクリック訴求を両立し、固定パターン反復による疲労と硬直を避けるため |
| 2026-04-05 | スコアリングは visual density / evidence richness の2軸から着手 | スコアなし / 単一総合点 / 2軸 | 演出不足と内容不足を別々に診断し、制作改善とマーケ改善の接続点を明確化するため |
| 2026-04-06 | assistant 側の subquest を timeline edit まで拡張するが、packet 単位で進める | timeline を一括実装 / packet 分割 / 維持 | face と同様に mechanical scope を failure class / readback / boundary で切り分けないと、YMM4 手動確認ループへ戻るため。G-11 slot patch → G-12 native-template measurement → G-13 overlay/se insertion の順に進める |

---

## Python のスコープ（確定事項 — 2026-03-30）

**許可:**
- テキストファイルの変換（transcript → CSV）
- テキストメタデータの生成（タイトル・説明・タグ等の文字列）
- 入力テキストの検証・分析
- 外部ソースからのテキスト/メディア取得（L1、取得と受け取りを分離する設計で）

**禁止:**
- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp ゼロ生成・YMM4 台本読込代替（音声ファイル参照・発音情報を外部生成できないため）
- YMM4 native template 資産の Python 生成・YMM4 GUI 万能制御
- YMM4 出力の模倣・Python preview
- 動画レンダリング・音声合成
- 外部 TTS（Voicevox 等）

**根拠:**
YMM4 の .ymmp プロジェクトファイルは音声ファイル（WAV 等）への参照を含む。その音声は YMM4 が台本 CSV を読み込む際に内蔵 TTS で自動合成するもの。NLMYTGen から音声ファイルを生成できないため、完全な .ymmp を外部から作ることは原理的に不可能。ただしこの制約は、台本読込後 `.ymmp` に対する限定 patch、repo-tracked YMM4 template source の placement、thumbnail `thumb.*` slot patch、audit/readback/compact review artifact を禁止しない。

---

## IDEA POOL

FEATURE_REGISTRY.md に統合済み。機能候補は FEATURE_REGISTRY で管理する。

| ID | 旧アイデア | 移行先 |
|----|----------|--------|
| IP-02 | Web UI 化 | docs/INVARIANTS.md / docs/FEATURE_REGISTRY.md の現スコープ外 |
| IP-03 | YouTube 自動アップロード | FEATURE_REGISTRY E-01 (hold) |

---

## HANDOFF SNAPSHOT (2026-06-24 newsroom audio/TTS boundary resume handoff)

- Branch / remote state: continue on `master` in
  `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage`.
  Before this docs handoff, `git fetch --prune origin` and
  `git pull --ff-only origin master` were run, `HEAD` was
  `16dcadc docs: define newsroom audio tts boundary`, and
  `git rev-list --left-right --count "HEAD...origin/master"` returned `0 0`.
  After pulling the handoff commit, expect the tracked tree to be clean and
  parity with `origin/master` to remain `0 0`.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` ->
  `docs/runtime-state.md`. If more detail is needed, inspect only the current
  artifacts:
  `samples/_probe/newsroom_handoff/audio_tts_boundary_v1.json`,
  `docs/verification/NEWSROOM_AUDIO_TTS_BOUNDARY_V1_2026-06-23.md`,
  `samples/_probe/newsroom_handoff/tiny_render_smoke_result_readback_v1.json`,
  `samples/_probe/newsroom_handoff/yym4_timing_gap_strategy_v1.json`, and
  `samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json`.
- Current accepted evidence: tiny render smoke previously passed by user
  freeform observation; four dialogue lines were visible; duration stayed about
  `8` sec on YMM4 natural timing; canonical speaker remains `ゆっくり霊夢`;
  diagnostic `.ymmp` structure readback found four voice items and VoiceCache.
- Current non-accepted scope: audio presence in the render is still `unknown`;
  `audio_quality_accepted=false`; `TTS_ready=false`; neutral `68` sec timing
  patch is not applied; visual layout readiness, production render readiness,
  public video readiness, and production approval remain false.
- Next concrete move: start `newsroom-yym4-native-audio-path-proof-v1`. Its
  purpose is to make the YMM4 native voice/audio path explicit as the next
  diagnostic default without opening external TTS. Use
  `newsroom-tiny-render-audio-observation-card-v1` only if audio presence in the
  existing tiny render becomes the actual bottleneck, and keep any observation
  freeform with at most three look-for points.
- Boundaries not crossed in this handoff: no YMM4 launch, no render, no
  TTS/audio generation, no real media import, no `.ymmp` or media
  staging/commit, no dashboard/governance/freshness work, no production/public
  readiness claim, no G-27/G-28 implementation.
- Local residue note: ignored `_tmp/` and Python `__pycache__/` files may be
  present in this checkout. They are local diagnostics/runtime residue and are
  not part of the pushed handoff.

## HANDOFF SNAPSHOT (2026-06-23 newsroom YMM4 manual import result readback)

- Result readback commit on `origin/master`:
  `b107473 docs: record newsroom YMM4 manual import result`. The expected restart sync is
  `git fetch --all --prune`, `git checkout master`, `git pull --ff-only origin
  master`, then `git rev-list --left-right --count "HEAD...origin/master" = 0
  0`.
- Current repo path for this machine:
  `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage`.
- Restart read path remains intentionally short:
  `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`.
  Read this snapshot only if branch/commit or manual-result routing context is
  needed.
- Current active artifact chain: tiny importable proof -> YMM4 manual import
  check packet -> manual import result readback. The source CSV is
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv`; the
  packet is
  `samples/_probe/newsroom_handoff/yym4_manual_import_check_packet_v1.json`;
  the result readback is
  `samples/_probe/newsroom_handoff/yym4_manual_import_result_readback_v1.json`;
  the human readback is
  `docs/verification/NEWSROOM_YYM4_MANUAL_IMPORT_RESULT_READBACK_V1_2026-06-23.md`.
- Current status: result is `pass_with_warnings`, with `4/4` rows visible and
  all text visible after manual speaker/character selection of existing
  `ゆっくり霊夢`. This is not production approval, render approval, TTS
  readiness, `.ymmp` readiness, automatic speaker binding, or public video
  readiness.
- Validation at handoff: JSON parse passed, `compileall` passed, focused YMM4
  manual result/check/tiny proof tests reported `22 passed`, `git diff --check`
  and `git diff --cached --check` passed, conflict marker and new doc/JSON URL
  scans were clean, and no `.ymmp`, media, render, TTS/audio, `.codex`, or
  `.claude/worktrees` file was staged or pushed.
- Next executable handoff steps are one of three bounded axes:
  `newsroom-speaker-binding-policy-v1`,
  `newsroom-yym4-import-readiness-after-manual-result-v1`, or
  `newsroom-minimal-ymmp-boundary-decision-v1`. Do not ask the user to repeat
  general timing/caption/copy/tiny-proof review for this same manual import
  observation.
- Explicit non-scope: do not launch YMM4 from the agent, do not create/edit or
  commit `.ymmp`, do not create carriers, render, generate TTS/audio, import
  real media, fetch external sources, ingest a real newsroom packet, approve
  production/public video, revive RSS/Inoreader/NotebookLM source selection, or
  expand dashboard/governance/freshness work from this handoff.

---

## HANDOFF SNAPSHOT (2026-06-22 newsroom YMM4 manual import check packet)

- Branch/remote: `master` at
  `3dfafd2 docs: define newsroom YMM4 manual import check packet`; expected
  restart sync is `git fetch --all --prune`, `git checkout master`,
  `git pull --ff-only origin master`, then
  `git rev-list --left-right --count HEAD...origin/master = 0 0`.
- Working tree state at this handoff: clean locally; `HEAD`, `origin/master`,
  and `origin/HEAD` all point to `3dfafd2`.
- Restart read path remains intentionally short:
  `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`.
  Read this snapshot only if branch/commit or operator-result context is
  needed.
- Current active artifact chain: tiny importable proof ->
  YMM4 manual import check packet. The source CSV is
  `samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv`; the
  latest packet is
  `samples/_probe/newsroom_handoff/yym4_manual_import_check_packet_v1.json`;
  the blank result template is
  `samples/_probe/newsroom_handoff/yym4_manual_import_result_template_v1.json`.
- Current status: `manual_check_status=not_run`. The agent has not opened YMM4
  and must not claim pass/fail without operator evidence.
- Next executable handoff step: a human/operator manually checks whether YMM4
  can show the four synthetic rows/texts through the script import /
  台本読み込み route without saving a production project, rendering, generating
  TTS/audio, importing real media, or committing `.ymmp`. The operator then
  records observed line count, speaker behavior, text behavior, error message
  if any, freeform notes, and one result value in the result template.
- Result routing: `pass` can move to result readback and a tiny YMM4
  import-readiness proof; `pass_with_warnings` should classify warnings first;
  `fail` should trigger only bounded CSV shape/encoding adjustment;
  `blocked_by_operator_uncertainty` should improve manual instructions, not the
  pipeline.
- Validation already run before this handoff: focused manual packet tests
  `7 passed`; focused proof chain tests `27 passed`; repo-level `uv run pytest`
  `743 passed, 28 skipped`; JSON parse, compileall, and `git diff --check`
  passed. `ruff` was unavailable in this environment (`program not found`).
- Explicit non-scope: do not launch YMM4 from the agent, do not create or
  commit `.ymmp`, do not create carriers, render, generate TTS/audio, import
  real media, fetch external sources, ingest a real newsroom packet, approve
  production/public video, revive RSS/Inoreader/NotebookLM source selection,
  or expand dashboard/governance/freshness work from this handoff.

---

## HANDOFF SNAPSHOT (2026-06-22 newsroom episode capsule)

- Branch / remote state: `master` at
  `bbe5528 feat: define newsroom episode production capsule`; after pulling,
  expected sync check is
  `git rev-list --left-right --count "HEAD...origin/master" = 0 0`.
- Current repo path for this machine:
  `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage`.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` ->
  `docs/runtime-state.md`; then open the episode capsule readback if the
  next task is newsroom/video-readiness.
- Primary capsule artifact:
  `samples/_probe/newsroom_handoff/episode_production_capsule_v1.json`.
- Human readback:
  `docs/verification/NEWSROOM_EPISODE_PRODUCTION_CAPSULE_V1_2026-06-22.md`.
- Implementation/test anchors:
  `src/pipeline/newsroom_episode_production_capsule.py` and
  `tests/test_newsroom_episode_production_capsule.py`.
- Current capsule facts: adapted fake newsroom packet identity
  `episode_fake_nlmytgen_delta_v1`; 2 script beats; 2 visual units; provisional
  duration 68 seconds; validator `passed`; G-28 slot-linkage
  `passed_with_warnings`; transfer planning `blocked`; blocker count `13`;
  unlock requirement count `13`; audio/voice `not_started`; production status
  `diagnostic_only`.
- Validation already run for this handoff chain: new capsule tests `7 passed`;
  focused newsroom suite `52 passed`; JSON parse pass; `git diff --check`
  pass; `git diff --cached --check` pass before commit; no real URLs in the new
  capsule/readback; forbidden staged path scan pass.
- Boundary: do not continue dashboard freshness/status producer work in this
  lane; do not accept a real packet, fetch sources, open RSS/Inoreader, access
  real URLs, download media, edit or generate `.ymmp`, generate YMM4 carriers,
  render media, generate TTS/audio, approve rights, approve production, or
  publish/upload output.
- Next concrete move: supervisor capsule review. If accepted, create a
  separate read-only Review Console episode preview slice; if rejected, adjust
  only the capsule/readback fields that the review names.

## HANDOFF SNAPSHOT (2026-06-12 G-28 reference layout path sync)

- Branch / remote state: `master` at `c6f17b5 feat: add G-28 reference layout prototypes`; after sync, `HEAD...@{u}=0 0`.
- Working tree state: clean before and after the docs-only context seal; no generated artifacts were created in this handoff.
- Current repo path for this machine: `C:\Users\PLANNER007\NLMYTGen`.
- Correct G-28 prototype hub to open: `C:\Users\PLANNER007\NLMYTGen\samples\_probe\g28\reference_layout_prototypes\index.html`.
- Git tree / working tree artifact state: the eight HTML files are present under `samples/_probe/g28/reference_layout_prototypes/`; the wrong `samples_probe` path is absent.
- Path-confusion finding: `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen` was not present in this environment, so resume from the PLANNER007 checkout unless the human explicitly points to another synced clone.
- Current interpretation: the reported missing folder was caused by checkout freshness / local path confusion before the fast-forward to `c6f17b5`; the artifact now exists in the active checkout.
- Boundary: do not regenerate HTML prototypes, do not make `.ymmp`, do not build YMM4 tooling, do not touch existing game-mechanics / map-evidence carriers, and do not enter render, production, rights, creative final acceptance, Newsroom, common foundation, G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, or real runner paths.
- Next concrete move: perform human browser review of the static HTML pack and return `accept`, `accept_with_caveats`, `revise_once`, `reject`, or `redesign_required` with per-screen notes.

## HANDOFF SNAPSHOT (2026-05-29 RSS cleanup decision)

- Branch/remote: continue on `master` and pull latest `origin/master` before work. This decision builds on cleanup handoff commit `f6db81e`.
- RSS cleanup decision: user accepted deletion for all failed-feed categories from the audit (`http_404`, `parse_or_non_feed`, `ssl_error`, `timeout`, and `http_403`) because RSS feed resources do not need strict completeness and the sample count is sufficient.
- Committed decision record: `docs/verification/RSS-FAILED-FEED-CLEANUP-DECISION-2026-05-29.md`. It contains only counts, categories, and policy; it does not include feed URLs, raw OPML, tokens, article titles, or article bodies.
- Duplicate handling: duplicate feed URL remains `0`; duplicate title remains `1` and stays `manual_review` because no specific duplicate-title action was supplied.
- Post-cleanup validation state: Inoreader-side changed count is unknown, and the local OPML export has not been refreshed after the deletion decision. Do not rerun post-cleanup smoke as proof until a fresh OPML export replaces `_local/rss/feeds.opml.xml`.
- Next safe restart move: ask for or wait for a fresh OPML export at `_local/rss/feeds.opml.xml`, then rerun `list-feed-sources` and `rss-smoke` with sanitized evidence only. Do not use Inoreader API or tokens unless explicitly re-scoped.

## HANDOFF SNAPSHOT (2026-05-28 RSS cleanup handoff)

- Branch/remote: `master` is pushed to `origin/master`; restart with `cd C:\Users\PLANNER007\NLMYTGen && git fetch --all --prune && git checkout master && git pull --ff-only origin master`. The cleanup audit commit immediately before this handoff is `b98afac`; after pulling, use the latest `origin/master` commit and read this snapshot.
- RSS OPML status: RSS UI comparison matched NLMYTGen's OPML view at `147` sources and `7` categories, so the ignored OPML export can be treated as the current operational source of truth until the reader list changes.
- Committed RSS evidence to read first: `docs/verification/RSS-LIVE-SMOKE-EVIDENCE-2026-05-28.md` for the smoke/diagnostic baseline, then `docs/verification/RSS-FAILED-FEED-CLEANUP-SUMMARY-2026-05-28.md` for the cleanup audit summary. `docs/runtime-state.md` has the active top-line state.
- Local-only artifacts: `_local/rss/feeds.opml.xml` is the raw OPML input and must stay uncommitted. `_tmp/rss_failed_feed_cleanup_candidates.md` and `_tmp/rss_failed_feed_cleanup_candidates.json` contain the detailed failed-feed titles/URLs for human Inoreader UI cleanup and must also stay uncommitted.
- Latest local cleanup audit: status counts were `fetched=121`, `empty=0`, `error=26`, `listed=0`; error breakdown was `http_404=2`, `parse_or_non_feed=15`, `ssl_error=2`, `timeout=3`, `http_403=4`. Prior live diagnostics varied around `31/32` errors, so treat exact failure count as live-network variable and use categories for cleanup planning.
- Cleanup order for the human UI pass: review `http_404` first, then `parse_or_non_feed`, `ssl_error`, `timeout`, and `http_403`. Delete/replace/keep decisions happen in Inoreader manually; repo code and OPML files are not mutated by this audit.
- Duplicate handling: duplicate feed URL count is `0`; duplicate title count is `1` and remains `manual_review`. Do not auto-merge or auto-delete the duplicate title.
- Boundaries not crossed: Inoreader API, token use, subscription mutation, DB/background sync, G-27 carrier work, Baseball, Thumbnail, GUI work, NotebookLM API, video generation, and YouTube posting were not run.
- Validation before handoff: CLI help smoke for `rss-smoke`, `list-feed-sources`, and `fetch-topics` passed; `git diff --check` passed; added committed lines had no URL/token/raw OPML marker hits. The ignored local files remain outside git.
- Next safe restart choices: `Verify` the local-only failed-feed list in Inoreader UI and rerun `rss-smoke` after manual cleanup; `Audit` the one duplicate title manually; or `Advance` source category representative selection so categorized entries can appear in the shown sample. Do not start Inoreader live API smoke without an explicit new instruction.

## HANDOFF SNAPSHOT (2026-05-27 update)

- Branch / remote state: `master`. Pull latest `origin/master`; expected sync check is `git rev-list --left-right --count "HEAD...@{u}" = 0 0`. Working tree may still show pre-existing untracked local files `.claude/worktrees/` and `samples/2026-05-16.ymmp`; they are not part of this handoff.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. `runtime-state.md` is the live frontier authority.
- Closed diagnostic slice: `samples/_probe/g24/layout_instruction_proof.ymmp` now has machine readback pass and user-side YMM4 v4.52.0.8 GUI proof pass. The visible issues found in the first GUI pass (bottom-looking title alignment, no title/grid gap, unstable labels) were corrected by `4631f89 fix(g27): stabilize layout instruction proof spacing`.
- Current proof facts: `layout_instruction_proof_readback.json` reports `status=passed`, 17 items, hard_fail=0, violations=[], `title_grid_gap_visible=pass`, and `region_labels_clear_major_items=pass`. Narrow checks run: `node scripts\build_g27_layout_instruction_proof.js --write`, `node scripts\build_g27_layout_instruction_proof.js`, `node scripts\render_g27_layout_instruction_proof_html.js`, and `git diff --check`.
- Boundary: this is a diagnostic layout/slot proof only. It is not a render, creative acceptance, production carrier replacement, slot-fill readiness, or production readiness claim.
- Next frontier: return to the `G27_PublicVsBrokerDB` carrier / slot-fill path. Do not design an anchored slot contract or implement slot-fill before a human-authored carrier exists. After carrier receipt, assistant should read back required `G27PBD_*` item names, short Remarks, fixed card counts, `G27PBD_Arrow` existence, and geometry-free patch feasibility.

---

## HANDOFF SNAPSHOT (2026-05-14 update)

- Branch / remote state: `codex/g24-nod-sync-adoption`; pull the latest branch and expect the active project changes to be committed. Confirm with `git status --short --branch` and `git rev-list --left-right --count HEAD...'@{u}'`.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. The live `next_action` is waiting for a human-authored `G27_PublicVsBrokerDB` YMM4 carrier, not a scene-generation or render slice.
- Current decision: G-27 direct dense `ShapeItem` / `TextItem` scene generation is stopped as a production route. Existing visual proxy v2/v2.1, minimal probe, micro scene, and micro scene visibility outputs are diagnostic-only and must not be promoted into stable carriers.
- New handoff artifact: `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`. It tells the human exactly what to create in YMM4: 16:9 / 1920x1080 carrier, 5% outer safe margin, bottom 10-15% caption safe area, left public panel, right broker/private DB panel, center lock/threshold, fixed 2 public cards, fixed 3 broker cards, optional `G27PBD_Arrow`, short `G27PBD_*` item names, short Remarks, and no provenance in item names/Remarks.
- User should return: carrier `.ymmp` path, preview screenshot, timeline screenshot, representative item property screenshots for `G27PBD_PublicPanel`, `G27PBD_PublicCard1`, `G27PBD_BrokerPanel`, and `G27PBD_Lock`, light/dark stage choice, and a short note that the caption safe area is clear.
- Assistant next after receiving carrier: read back required item names, duplicate/missing items, short Remarks, fixed card counts, `G27PBD_Arrow` existence, and whether text / visibility / timing / sidecar provenance can be patched without touching geometry, anchors, colors, font hierarchy, or layout grid. Only then prepare an anchored slot contract.
- Not done: no `.ymmp` carrier was created, no slot-fill contract was written, no patch script was implemented, no raw geometry was generated, no render, no production timing, no creative acceptance, no G-26, no `sports_news`, no INT-02e, no publishing, no master integration, no new gate, and no broad roadmap.
- Local note: `docs/WritingPage.code-workspace` is an unrelated untracked editor workspace file with sibling-project references; do not commit it as NLMYTGen handoff context.

---

## HANDOFF SNAPSHOT (2026-05-13 update)

- Branch / remote state: `codex/g24-nod-sync-adoption`; pull the latest branch and expect a clean working tree. Confirm with `git status --short --branch` and `git rev-list --left-right --count HEAD...'@{u}'`.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. The live `next_action` is the G-27 primitive visibility calibration GUI readback wait; this snapshot only preserves the executable handoff context.
- Current G-27 artifact: `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe.ymmp`, generated by `scripts/build_g27_primitive_visibility_calibration_probe.js`.
- Companion artifacts: `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_readback.json` and `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_report.md`.
- Calibration scope: this is a drawing-semantics calibration probe, not a video scene. It uses one light-stage tonal system, `ShapeItem` / `TextItem` only, 11 items, a full-screen BG, a 920x560 `Main Panel`, panel-contained title/body text, center/TL/BR anchor markers, and one thick connector.
- Machine readback: `status=passed`, `ShapeItem=6`, `TextItem=5`, `missing_item_count=0`, `malformed_item_count=0`, `item_name_length_failures=0`, `remark_length_failures=0`, `suspicious_default_item_count=0`, `carrier_modified_in_place=false`, `render_performed=false`, and `creative_acceptance_performed=false`.
- Previous micro scene status: `real_estate_dx_micro_scene_visibility_probe.ymmp` opens and has machine/timeline pass, but user GUI review found preview visibility, visual composition, and scene adequacy insufficient. Do not add more labels/cards/beats or create another micro scene variant before the calibration GUI review passes.
- Verification chain: `node --check scripts/build_g27_primitive_visibility_calibration_probe.js`; `node scripts/build_g27_primitive_visibility_calibration_probe.js --write`; `node scripts/build_g27_primitive_visibility_calibration_probe.js`; `git diff --check`.
- Not done: no minimal render smoke, no production timing, no creative acceptance, no external assets, no TTS, no URL fetch, no publishing, no `sports_news`, no G-26, no INT-02e, no master integration, no new gate/policy/roadmap/dry-run/visual atlas.
- Next concrete move: open `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe.ymmp` in YMM4 and return whether the large panel is visible, title/body text are inside the panel, anchor markers are where expected, connector is visible, item names/Remarks are manageable, plus preview screenshot, one selected panel item property screenshot, and one selected text item property screenshot. Only after this GUI review passes should calibrated geometry/visibility grammar be applied back to the 4-beat micro scene.

---

## HANDOFF SNAPSHOT (2026-05-12 update)

- Branch / remote state: `codex/g24-nod-sync-adoption` at `21ef759 docs: refresh g27 handoff snapshot`; probe generation commit is `3411413 feat(g27): generate minimal ymmp probe`; `HEAD...origin/codex/g24-nod-sync-adoption = 0 0` at handoff. Working tree should be clean after pulling this branch.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. Current frontier is `runtime-state.md` `next_action`; this snapshot only preserves the executable handoff context.
- Current G-27 artifact: `samples/_probe/g24/real_estate_dx_minimal_patched_probe.ymmp` generated from `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json` by `scripts/build_g27_minimal_ymmp_probe.js`.
- Machine readback: `samples/_probe/g24/real_estate_dx_minimal_patched_probe_readback.json` / `.md` reports `status=passed`, `ShapeItem=14`, `TextItem=7`, `candidate_ids_found=7/7`, `layer_values_found=[7,8,9]`, `missing_item_count=0`, `malformed_item_count=0`, `carrier_modified_in_place=false`, and `next_slice_can_safely_proceed_to_YMM4_GUI_readback_preview=true`.
- Candidate scope: only `RE-02-beginning`, `RE-02-development`, `RE-06-beginning`, `RE-06-development`, `RE-06-turn`, `RE-07D-beginning`, and `RE-07D-development` are in the probe. `RE-02-turn` remains blocked outside the output; `RE-07D-turn` remains deferred outside the output.
- Verification chain: `node --check scripts/build_g27_minimal_ymmp_probe.js`; `node scripts/build_g27_minimal_ymmp_probe.js --write`; `node scripts/build_g27_minimal_ymmp_probe.js`; Python openability guard with `success=True`, `is_project_canvas=True`, `item_count=21`; `node scripts/build_g27_ymmp_compact_patch_review.js`; `node scripts/build_g27_adapter_ir_dry_run.js`; `node scripts/check_g27_adapter_route_preflight.js`; `node scripts/check_g27_adapter_authorization_gate.js`; `git diff --check`.
- Not done: no render, no YMM4 GUI preview capture, no production timing, no creative acceptance, no TTS, no URL fetch, no publishing, no `sports_news`, and no pipeline hardening.
- Next concrete move: open or capture `samples/_probe/g24/real_estate_dx_minimal_patched_probe.ymmp` in YMM4 for GUI readback / preview. Treat PASS as file-openability / visible-placement evidence only; short render is a later slice after GUI readback succeeds.

## HANDOFF SNAPSHOT (2026-04-26 update)

- Shared Focus: **G-24 template-analyzed placement after raw clone readback**. The v1 source contains all five templates and `--skit-group-only` can insert exact/fallback cues, but raw clone output is not production acceptance because user visual feedback found spacing/composition too rough. The current shared cycle is no longer motion authoring, alias planning, or user hand placement; it is adding template analyzer + placement planner so reusable YMM4 templates become generated production placement. Canonical current state: [runtime-state.md](runtime-state.md) slice / next_action.
- Restart Governance Delta: **2026-04-27** normal restart read budget is now capped at `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. Protected/canonical docs remain sources of truth, but they are not all full-read requirements. Read `project-context` HANDOFF / DECISION LOG, FEATURE ID, invariant, ledger, workflow, interaction failure class, or AI gate only when the current decision needs that section. Full re-anchoring is an exception, not the default.
- Interaction Governance Delta: **2026-04-27** template formalism is now a structural failure class. Obsolete prompts, archived packets, and superseded roadmap/setup docs remain deleted; `INTERACTION_NOTES.md` treats interaction failures as project risks, and now explicitly blocks prompt/checklist/OK-NG templates from replacing task connectivity. Manual/shared actions must state open target, created artifact, source object, actor, owner artifact, acceptance meaning, and replan condition before using short result codes.
- Roadmap Prep Delta: **2026-04-27** G-24 planned author/export is closed at the v1 set (`enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left`). [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) and [P02-production-adoption-proof.md](verification/P02-production-adoption-proof.md) now point to production-use validation rather than another cautious authoring gate.
- Implementation Delta: **2026-04-27** user completed `delivery_deny_oneshot_v1` and `delivery_exit_left_v1`. Repo inspection found the two target samples use plain body/face `ImageItem` children and no `TachieItem`; `deny_oneshot` is a short X-axis one-shot sway, and `exit_left` uses a leftward OUT `InOutMoveEffect`. `skit_group.intent.deny_oneshot` / `skit_group.intent.exit_left` are now `direct_proven`.
- Validation Delta: **2026-04-27** repo-probe production-use validation PASS. `audit-skit-group` on `samples/canonical.ymmp` + `samples/_probe/skit_01/skit_01_ir.json` returned `exact=5 / fallback=0 / manual_note=0`. No confirmation `.ymmp` was generated.
- Gap Classification Delta: **2026-04-27** production-like gap classification PASS. IR A returned `exact=3 / manual_note=1`; IR B returned `exact=1 / manual_note=3`; this was followed by alias registration for `surprise_jump` and `deny_shake`.
- Safe Next Frontier Packet: **The next concrete move is template analyzer + placement planner for real-estate DX skit_group placement**. Entry route stays `patch-ymmp --skit-group-only`, but raw template clone must be treated as transport proof only. The next proof should show an analyzed placement plan, patched `.ymmp` readback, and no hand-placed cue correction.
- Active Artifact: NLM transcript → YMM4 CSV → Writer IR → Template Registry → YMM4 Adapter → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → IR (Custom GPT) → Registry (JSON) → Adapter (patch-ymmp) → 演出設定 → レンダリング
- Last Change Relation: **2026-04-28** G-24 raw clone placement and image-path readback PASS, followed by user correction that placement spacing/composition must be generated from template analysis rather than fixed by user hand placement.
- Handoff Focus (next): Resume from template analyzer + placement planner. Keep `panic_shake` out of normal Part 2 JSON vocabulary; do not request template reauthoring unless diagnostics prove source data is missing.
- Evidence: Production E2E remains proven, v1 G-24 planned templates are PASS / `direct_proven`, repo-tracked template source is 5/5, and raw clone placement readback inserted the expected Layer 9 cues. That readback is transport proof, not production acceptance.
- 案件モード: CLI artifact
- 現在の主レーン: 方向転換中 (実制作bottleneck直接軽減へ移行)
- 成熟段階: Level 1 (限定変換器) 到達済み、Level 2 (演出IR適用エンジン) 形成中 → Level 3 接近
- Current Trust Assessment:
  - trusted: B-01~B-17 全字幕スタック（実装+検証済み）
  - trusted: G-02 IR 語彙 v1.0、G-02b ymmp 構造解析、G-06 patch-ymmp 実機検証
  - trusted: extract-template (face_map/bg_map 自動抽出)
  - trusted: G-05 v4 proof 完了。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の IR を正常出力
  - trusted: load_ir Multi-Object 対応 (2オブジェクト連結形式の読み込み)
  - trusted: face completion hardening (`PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_PROMPT_PALETTE_*` / `FACE_LATENT_GAP`)
  - trusted: G-11 slot patch hardening (`SLOT_UNKNOWN_LABEL` / `SLOT_REGISTRY_GAP` / `SLOT_CHARACTER_DRIFT` / `SLOT_DEFAULT_DRIFT` + TachieItem X/Y/Zoom patch + `off` hide)
  - trusted: G-12 readback harness (`measure-timeline-routes` で `motion` / `transition` / `bg_anim` candidate route を抽出し、`--expect` / `--profile` で route contract miss を検出)
  - trusted: G-12 packet narrowing (`motion=TachieItem.VideoEffects`、`bg_anim=ImageItem.X/Y/Zoom`、effect-bearing bg=`ImageItem.VideoEffects` まで current corpus で狭め済み)
  - trusted: repo-local `.ymmp` 16 本の corpus audit により fade-family `transition` route は観測済み、`template` route は 0 件と確認済み
  - trusted: G-13 overlay insertion (`OVERLAY_*` validation + deterministic `ImageItem` patch)
  - trusted: G-13/G-18 `se` (`SE_*` validation + G-18 `AudioItem` 挿入、`PatchResult.se_plans` = 挿入数)
  - trusted: H-02 done (dry proof + strict GUI rerun proof pass 2026-04-06)
  - trusted: H-03/H-04 done — `score-visual-density` / `score-evidence` CLI + tests (`test_visual_density_score.py`, `test_evidence_score.py`)
  - trusted: H-05 done — `score-thumbnail-s8`（手動採点 JSON の機械集約、`thumbnail_s8_score.py`、`test_thumbnail_s8_score.py`）
  - trusted: B-18 `diagnose-script` + C-09 `docs/S1-script-refinement-prompt.md`（`test_script_diagnostics.py`）
  - resolved (G-14): `production.ymmp` はタイムラインに ImageItem 無しのため bg_anim 未観測。`production_ai_monitoring_lane` で motion/transition のみ required とし contract pass。背景アニメ patch は ImageItem 含有 ymmp で別パケット
  - needs re-check: non-fade / template-backed `transition` の ymmp route は repo 内 sample 不在のため未固定。新しい sample が入ったときだけ再測定する
  - resolved (G-18): `se` の `AudioItem` 挿入は `samples/AudioItem.ymmp` + コード内骨格で固定。運用で YMM4 バージョン差が出たら readback のみ再確認
  - needs re-check: face label inventory そのものが creative quality として十分かは最終制作物で見る
- Recovered Canonical Context:
  - Python はテキスト変換 + 演出 IR 定義 + ymmp 限定後段適用
  - 視覚配置 IR が中心課題。C-07 系が主系統、D-02 は従属的補助論点
  - patch-ymmp は Level 1 限定変換器。ゼロからの ymmp 生成とは区別する
  - 「未実装」は「境界外」ではない。motion/transition/overlay は正式スコープ内の frontier
  - YMM4 テンプレートは独立ファイルではなく ItemSettings.json の Templates 配列に JSON 保存
  - Custom GPT v4 は 2オブジェクト連結形式 (Macro + Micro) で IR を出力する。load_ir() で対応済み
- Authority Return Items:
  - YMM4 大版本更新時: `AudioItem` 構造差分が出たら readback のみ再確認（G-18）
  - E-02: 旧 standalone template は hold 継続。H-01/H-02/H-04 を入力にした metadata draft は successor-lane として別起票可
  - F-01/F-02: quarantined 継続
- What Not To Do Next:
  - spec/proof 整備をさらに積み増さない (一巡済み。実制作の手間軽減が先)
  - 再スタート時に保護 docs / canonical docs を全部読む運用へ戻さない。通常再開は 3 点 + 必要節だけ
  - interaction failure を個人的な反応ラベルへ戻さない。対話メモは、再質問・停止・手動検証押し戻し・価値経路 drift を防ぐための failure class として保守する
  - Prompt / checklist / `OK/NG` 返却テンプレを、開く対象・作る対象・元 object・判定主体の説明の代替にしない
  - done 件数で進捗を測らない (35件だが実制作カバレッジは限定的)
  - D-02 を主軸として扱わない (従属的補助論点)
  - quarantined 項目を通常候補としてそのまま spec 化しない
  - face 問題を broad な visual retry loop として再開しない
  - E-01/旧 E-02 standalone を制作パイプラインへ自動注入しない（metadata draft は integration point 明示の successor-lane で扱う）
- Expansion Risk: なし

## B-11 workflow proof chronicle (archive)

OPERATOR の workflow proof 節から移した観測メモ。現行条件は [OPERATOR_WORKFLOW.md](OPERATOR_WORKFLOW.md)。

- 2026-04-06: 既存サンプル `samples/AI監視が追い詰める生身の労働.txt` について取込前記録（stats・overflow 警告・111 行 CSV 出力）を [verification/B11-workflow-proof-ai-monitoring-labor.md](verification/B11-workflow-proof-ai-monitoring-labor.md) に固定。取込後表は YMM4 通し確認待ち。
- 2026-03-31 の初回観測では、辞書登録 0 / タイミングのみ 0 に対して、手動改行・再分割したい長文が約 30 箇所と支配的だった。次の L2（Python変換工程）改善は読みではなく字幕改行のバランス改善を優先する。
- 2026-03-31 の B-12 再観測では、手動改行 10 / 再分割したい長文 15 / 不自然な単語分割 5。`。` での改行は効いたが、句読点の少ない長文と 1 文字最終行が残り、次の主 pain は clause-aware split と widow/orphan guard だと判明した。
- 2026-03-31 の B-13 実装では、`--balance-lines` の内部改善として clause-aware split fallback と widow/orphan guard を追加した。sample dry-run では 57 発話 → 62 行に再編され、次に必要なのは YMM4 取込後の fresh visual evidence である。
- 2026-03-31 の B-13 再観測では、手動改行 5 / 再分割したい長文 10 / 不自然な単語分割 5。減りはしたが「まだ多い」という operator judgement で、特に長い一文が 1 字幕に残るケースは未解決だった。次の主 pain は aggressive clause chunking に移った。
- 2026-03-31 の B-14 実装では、複数文発話の中にある単一長文も sentence ごとに再展開し、通常候補が尽きた残り長文には aggressive clause chunking fallback を追加した。sample dry-run では 57 発話 → 95 行、overflow candidates は 3 件まで減少したため、次に必要なのは YMM4 上で「再分割負荷が減ったか」と「細かく切れすぎていないか」を同時に見る post-import visual evidence である。
- 2026-03-31 の追加観測では、`、` 起点の分割強化により長すぎる行はかなり減り、全字幕が 3 行以内には収まる水準まで改善した。残課題は bulk overflow ではなく、`ー`、カギ括弧 `「」`、数値や記号を含む `202/4` のような折り返しなど、個別ケースの良し悪しを集めて傾向化する段階に移った。ここから先は rule の複雑化が急速に進むため、heuristic を足し続ける前に「改行すべき/すべきでない例」の corpus を集める value path が強い。
- 2026-03-31 の B-15 初期コーパス収集では、`AI監視が追い詰める生身の労働_balance_lines_ymm4.csv` から 14 件 (bad-split 10, good 4) を抽出した。傾向パターン: P1=閉じ括弧直後+助詞で不自然分割 (5件)、P2=左側が極端に短い (3件)。P1/P2 はいずれもルール候補 (3件以上)。対策案と初期コーパスの妥当性について手動検証待ち。
- 2026-04-01 の B-15 第1回手動検証: ユーザーが YMM4 取込後に確認。報告: 漢字途中切断 (`事情は完/全に`, `身体的限/界`)、カタカナ途中 (`評価スコ/アが`)、単語途中 (`働/き続ける`, `路上/へと`)、次頁区切りの違和感 (`ロックオン/して`)。原因は小区切り(文字種境界)の誤発動と候補不足時の強制切断。修正: 大区切り限定方式に変更、漢字連続を禁止位置に追加。
- 2026-04-01 の B-15 第2回手動検証: 第1回報告の7パターン全て解消。4行またがりなし。若干の違和感は残るが「明らかなバランス偏りはなくなっている」。追加フィードバック: 漢字→ひらがな境界の小区切りは外すべき (`単/なる`, `見間違/った` 類)。文字種境界より行長精度を優先する方針を確認。小区切り候補から文字種境界を除去。
- 2026-04-01 の B-15 第3回手動検証: ページ間分割はだいぶ改善。行内折り返し (YMM4自動折り返し) の違和感は残存。「1行/1ページの最大文字数から逆算する外殻」が必要で、B-16 として分離。B-15 done。
- 2026-04-01 の C-07 v1 proof: セクション分割 OK、作業時間削減 OK、背景候補 NG。ストック素材検索は方向が違う。必要なのは茶番劇アニメ+図解の演出指示。
- 2026-04-01 の C-07 v2 proof: 4演出パターン (茶番劇/情報埋め込み/雰囲気演出/黒板型) + 発話単位指示 + 表示情報抽出 + 要調査明示。3基準全て OK。C-07 done。
- 画像例から言語化したオペレータ意図（立ち絵＋フキダシ・ゆっくり顔差し替え、リソース列挙、地図/黒板整理、雰囲気ストック）の正本: [C07-visual-pattern-operator-intent.md](C07-visual-pattern-operator-intent.md)。
- 2026-04-03 の production-slice patch-ymmp proof では、実IR先頭11発話を既存 ymmp に適用して face 13 / bg 2 変更を確認した。一方で 11 VoiceItem 中 4 件は `TachieFaceParameter` を持たず、face 差し替え対象外だった。full E2E 前に、台本読込後 ymmp の対象キャラ発話が表情パラメータを保持していることを operator 側で確認する必要がある。
- 2026-04-05 の face completion hardening で、この種の partial apply は `VOICE_NO_TACHIE_FACE` として mechanical failure に昇格した。以後は broad な visual retry loop ではなく、failure class に応じて対処する。
- 2026-04-06 の H-02 dry proof で、C-08 は `Specificity Ledger` と `Brief Compliance Check` を返す契約になった。strict GUI rerun proof は同日 pass で閉じた (4/5案が preferred_specifics 使用、banned pattern なし)。コピー品質の実用改善は別課題として残る。

## 2026-04-05 Structural Linebreak Redesign Note

- B-17 reflow v2 was reworked around structural major/minor boundaries instead of phrase-specific word lists.
- Page carry-over and in-page line breaks are now evaluated separately: page planning prefers major boundaries first, then falls back to minor boundaries only when necessary.
- Inline break scoring now strongly penalizes breaks inside short hiragana connector tails and around quoted/bracketed labels followed by explanatory nouns.
- Short comma-led intro lines are now penalized by width so that later particle/phrase breaks win when they keep the page visually denser.
- Close-bracket/content fallback candidates and major-vs-all page-plan comparison were added, reducing earlier failures around quoted labels and explanatory nouns.
- Emergency inner-break candidates inside long quoted labels were added as a last resort; remaining residuals are now mostly small 41-48 width overruns rather than gross structural breaks.
- Single-hiragana tails after quoted terms are now scored separately, improving `...最適化」 / と聞くと` type boundaries while keeping `」` at the next-line head suppressed.
- Sample proof on `samples/AI監視が追い詰める生身の労働.txt` improved several screen-facing failures (`では / なく`, `）」 / という`, `） / 」`, `19 / 億`) while leaving a smaller residual cluster around `XというY` and quoted explanatory phrases that still need another structural pass.
- Carry-over scoring is now explicitly separated from in-page line breaks: `close+tail` boundaries and extra-page exact plans are allowed to win when they eliminate overflow without creating sparse fragment pages.
- Exact page-count comparisons now use a target-specific ideal page width instead of reusing the base target, which fixed the `完璧に計算されたアルゴリズムが生身の / 人間という...` class by allowing one more page in the surrounding multi-sentence utterance.
- Current sample residuals are down to 2 mechanical frontier cases in `_tmp_structural_balance.csv`: `誰の汗とリスクを動力にして回り始めるのかを / 解剖していくということですね。` and `自発的にリスクを取らせる罠のようなものです。 / データによると、`. Further automatic tightening risks over-fragmenting page flow more than it helps.
