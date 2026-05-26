# G-27 実装停滞監査 2026-05-25

この監査は、G-27 Layout Instruction Proof の YMM4 preview PASS 後に、機能実装そのものが止まっている箇所と、意図的に gate で止めている箇所を分けるためのもの。

## 現在閉じた gate

`samples/_probe/g24/layout_instruction_proof.ymmp` は、機械 readback と user-side YMM4 preview の両方で PASS。これにより「自然言語レイアウト指示が YMM4 上で安定した slot / region proof へ変換できるか」は閉じた。

ただし、これは layout grammar proof であり、scene composition acceptance、render proof、production carrier replacement、production readiness ではない。

## 停滞に見える箇所の切り分け

| 領域 | 実装状態 | 止まっている理由 | 推奨扱い |
| --- | --- | --- | --- |
| G-27 layout instruction proof | 機械 readback / YMM4 preview とも PASS | ここは停滞なし | 追加 screenshot は不要。production review へ戻す |
| G-27 production review | review packet / route preflight / authorization gate は機械 OK。7 candidates の adapter IR dry-run は許可済み | `background_skit_blueprint_validate.json` は引き続き `blocked`。YMM4 adapter output / render / timing はまだ許可されない | adapter IR dry-run review で次 gate 条件を短文化する |
| G-27 adapter route | 7 candidate は planning-ready、authorization は `authorize_adapter_IR_dry_run_for_7_candidates_only` を採用済み | 許可されたのは adapter IR dry-run だけ。YMM4 patch / `.ymmp` write / render は禁止 | dry-run artifact をレビューし、次 gate へ進む条件を整理 |
| G-20 geometry helper | approved。group_target validation と relative mode は完了済み | face_map_bundle 整合、template 監査、反転 key 調査が残る | 主軸ではなく、G-27 の詰まりが geometry に戻った時だけ再開 |
| G-26 motion primitive | proposed | visual acceptance / calibration threshold 未確定、production placement 未接続 | 未承認のまま本線投入しない |
| H-01 packaging | approved。brief template / session manifest は実装済み | 自動注入・score closed loop は未承認 | 実動画 run の handoff で必要になった時だけ下位タスク化 |
| H-02 thumbnail | done。template slot audit / patch route は実装済み | 実サムネ YMM4 template proof は未完了 | packaging bottleneck が出た時の低負荷並行候補 |
| E-01/E-02 YouTube | hold | 投稿 integration point 未確定。metadata draft は successor-lane 扱い | 動画制作 loop が閉じるまで触らない |
| F-01/F-02 GUI | quarantined | 汚染バッチ由来。専用 GUI が最短価値か未検証 | 既存 GUI で吸収できない痛点が出るまで触らない |
| Baseball / sports_news | sidequest | 本流を置き換えない | 明示起動時だけ screen plan から開始 |

## 機械確認

- `node scripts/check_g27_review_packet.js` → review packet contract OK。
- `node scripts/check_g27_adapter_route_preflight.js` → 7 candidates、`output_generation_allowed=false`。
- `node scripts/check_g27_adapter_authorization_gate.js` → 7 candidates、`authorization_granted=true`、`output_generation_allowed=false`。
- `node scripts/build_g27_layout_instruction_proof.js` → no-write drift check PASS。
- `node scripts/render_g27_layout_instruction_proof_html.js` → HTML proof regenerated, readback status PASS。

## 次に詰まりを減らす入口

| 入口 | 摩擦が減る工程 | 次に可能になること |
| --- | --- | --- |
| Advance: adapter IR dry-run review | 7 candidates の dry-run と除外 2 件の境界が明確になる | 次 gate の判断材料を作れる |
| Audit: G-27 output 禁止境界の短文化 | `output_generation_allowed=false` の理由が operator に伝わる | dry-run と `.ymmp` patch を混同しにくくなる |
| Verify: H-02 実サムネ template proof | packaging の実制作接続が見える | `thumbnail_design` → template patch の実用確認へ進める |
| Explore: G-20 残スライス | geometry helper の未整理が消える | skit_group template 微調整が必要になった時の足場になる |

推奨は G-27 を継続し、adapter IR dry-run review で次 gate の判断材料を作ること。現時点の停滞は「機能実装がない」よりも、「YMM4 output / render / production timing へ進める gate がまだ閉じている」ことが主因。
