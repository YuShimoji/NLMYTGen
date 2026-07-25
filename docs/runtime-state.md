# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-standard-production-loop-gui-ready-v1
State-Revision: 2026-07-25.4
Updated: 2026-07-25 JST
Product-State: runtime-doctor-backed-end-to-end-episode-operation-gui
Product-Gate: second-real-topic-factory-validation
Recommended-Next: run-second-real-topic-through-standard-production-loop
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-standard-production-loop-gui-v1
Handoff-PR: none
Required-Base: 55507cb6f8940152f6ffae132186bcbcc0a700b0
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked state clean required after handoff; pre-existing ignored/private state preserved

## Current Slice

- Electronの既定画面は日本語の`自動動画生成`になった。日常経路は
  `エピソード` → `実行環境` → `生成内容` → `実行` → `結果`の単一縦導線で、
  CSV変換、演出適用、デザインレビュー、品質診断は副次タブとして残る。
- 採用済みnew-banknote manifestの直接読込とsafe file dialog選択を実装した。
  episode ID、9 cues、3 scenes、2 speakers、1920x1080/60 fps、internal-review
  境界、11 content locksとsource projectの計12 protected inputを表示する。
- GUIのdoctorは実コマンド
  `uv run python -m src.cli.main doctor-runtime --profile all --deep --format json`
  を呼び、code/review/render/regenerateを独立表示する。receiptだけをlive
  readinessへ昇格せず、blocking checkを次の機械作業として表示する。
- `書き込みなしで工程を確認`は選択manifestを実
  `build-episode-video --dry-run`へ渡す。採用済みmanifestの実dry-runはpassし、
  YMM4 launch、render、playback、public network writeは発生していない。
- `内部レビュー動画を生成`はprotected inputs exact、regenerate ready、
  dry-run pass、単一ジョブ、safe resumeの条件でだけ有効になる。実Python bridgeは
  `build-episode-video --render [--resume]`へ接続済みだが、このsliceの最終render
  呼出しはdeterministic test doubleだけで検証した。
- ジョブ制御は同時に1件だけを所有する。最近240行だけを保持し、開始、実行中、
  完了、失敗、取消を表示する。Windows取消は記録したchild PIDだけを
  `taskkill /PID <pid> /T /F`へ渡し、既存出力を削除しない。
- 結果はgenerated project、MP4、pipeline receipt、run directory、acceptance
  identityを別々に読む。missing、present-unverified、generated-unaccepted、
  stale/mismatch、accepted-exactを区別し、自動再生もYMM4起動もしない。
- 採用済みrunはMP4 SHA-256
  `423553e0aff40619ffb0fd88bcc80344417788aa6128f0a8778aefbdd19ca476`
  とgenerated project SHA-256
  `244c05ae6fe6179e9dace4b569cd5f3f9f496cfe70d46ac16ac459e787712611`
  がhuman acceptance receiptへexact一致する。
- hidden/offscreen Electron 43.2.0で1280x720と1920x1080を実測した。既定surface、
  first viewportのepisode/readiness/primary action、横overflowなし、実dry-run、
  render test double、active/cancelled、accepted output、console/preload/security/
  unhandled errorなしを確認した。
- Tasteまたは`redesign-existing-projects` skillは環境に無かったため使用も取得も
  していない。明示UI制約だけで監査し、SVG、生成画像、hero、card grid、pill
  collection、gradient、新font、別design directionを追加していない。
- Narrow gateはNode contract 6件、GUI/IPC/Electron/runtime-doctor/dependency
  authority Python 37件、既存Electron compatibility smokeがpass。outcome commit後の
  canonical Regression Integrityを一度だけ実行し、failure/error 0とvalid
  declared-locator skip contractを最終handoff条件にする。

## Product Position

CLIに分散していたmanifest選択、live runtime判定、preflight、生成dispatch、
progress/cancel、accepted output確認がElectronの日常経路へ接続された。採用済みcutの
creative dimensionsとbytesは変更していない。次の製品証明はGUI polishではなく、
異なる実トピックを同じmanifest/pipeline/GUI契約へ通すfactory validationである。

## Exact Next Action

`npm --prefix gui start`でGUIを開き、権利と入力承認が別途揃った第2実トピックの
`nlmytgen.episode_manifest.v1`を選ぶ。doctor 4 profile ready、protected inputs
exact、dry-run passを確認し、既存出力collisionが無ければ内部レビュー生成へ進む。
成功信号は新runのproject/MP4/validation receiptが相互一致すること。creative
acceptance、rights、publicationはその後の別gateであり、このstateは承認しない。

## Evidence and Access

- GUI contract: `gui/standard_production_loop.js`
- Electron evidence probe: `gui/standard_production_loop_probe.js`
- Focused JS tests: `gui/standard_production_loop.test.js`
- Focused DOM/IPC tests: `tests/test_standard_production_loop_gui.py`
- Canonical regression runner: `scripts/check_regression_integrity.py`
- Accepted-cut authority:
  `auto_video_pipeline/human_real_media_cut_acceptance_receipt.json`

## Cross-Terminal Re-entry

- Fetch and track `origin/codex/nlmytgen-standard-production-loop-gui-v1`; require
  `HEAD...@{upstream}=0/0` and a clean tracked worktree.
- Read `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
- Run `uv sync --extra dev --locked`, `npm --prefix gui ci`, then
  `npm --prefix gui ls --depth=0`; require Electron 43.2.0.
- Run `npm --prefix gui run test:standard-production-loop` and, when private
  accepted artifacts are present, `npm --prefix gui run smoke:standard-production-loop`.
- Start normal operation with `npm --prefix gui start`.

## Active Boundaries

- Accepted speech, wording/order, cue/subtitle timing, line breaks, and real-media
  visual treatment remain closed for the exact stable internal cut.
- Electron 43.2.0 remains current. Electron 35.7.5 at
  `2e11987ff0732d21df4a5da83d1ea557614991ac` remains rollback authority.
- This GUI grants no private transfer, rights, production, publication, upload,
  release, PR, merge, or master authority.
- This slice performed no YMM4 launch, new render, playback, system-volume change,
  rights action, publication, upload, release, PR, or master mutation.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit regression and parity evidence belongs in
the supervising handoff report, not in a second implementation commit.
