# Background Skit Blueprint / Timetable Workflow

この文書は、背景茶番劇を「それっぽい演出案」から、実制作に投入できる **精密な図面と時刻表**へ落とすための正本である。対象は `pilot_yukkuri_theater_v1` を含む、`skit_group` / props / overlay / YMM4 item を使う背景無言劇全般。

## Core Premise

- 背景茶番劇は合いの手ではない。語りと並走する visual story である。
- `scene bible` は必要条件だが十分条件ではない。IR や演出指定へ進めるには、総尺・絶対時刻・各演出の秒数・空白密度・素材/制御・台本成熟度を同じ表で検査する。
- `time budget %` は構成比であり、IR ではない。IR へ進めるには `00:00-00:12` のような実時間 window、または frame range へ変換する。
- `readback が通る` は transport proof であり、動画として成立する証明ではない。動画として成立するには、タイムライン密度・画面内物語・脚本の論理連結が通る必要がある。
- 脚本が杭だけの状態なら、演出で家に見せかけない。先に script maturity gate で止め、理想脚本への修正要求を出す。

## Required Deliverables

| deliverable | purpose | must include | owner |
|---|---|---|---|
| `background_skit_blueprint.json` | validator に渡す正本 artifact | source_lock / script_diagnostic / duration_model / blocks / asset_control_matrix / density_thresholds / blockers | assistant |
| `validator_result` | 偽装数値を落とす機械 gate | `validate-background-skit-blueprint` の `status`, `errors`, `blockers`, `allowed_next_actions`, `forbidden_next_actions`, `derived_metrics` | assistant |
| `script_diagnostic` | 脚本が動画として成立するかを見る | thesis / block logic / missing transitions / weak claims / ideal-script delta / line ranges | assistant |
| `duration_model` | 全体尺を固定または推定する | total duration, source, confidence, chars/sec or YMM4/voice readback source | assistant |
| `scene_bible` | 背景劇の物語設計 | script line range / cast continuity / props / screen placement / rest spans | assistant |
| `timetable` | IR前の時刻表 | block start/end, skit start/end, duration sec, rest windows, density flags | assistant |
| `asset_control_matrix` | 何が必要で何を制御するか | cast, assets, template_name, IR intent, layer, motion/hold requirements, missing controls | assistant |
| `density_thresholds` | スカスカ判定の基準 | minimum coverage / maximum unexplained gap / visual states per min band / repeated motion cap | assistant |
| `density_audit` | スカスカ判定 | active visual duration, intentional rest, unexplained empty, longest gap, visual states/min | assistant |
| `revised_skit_ir` | 実配置候補 | intent/template separation, layer target, start/end anchor, proof path | assistant after gates |
| `compact_review_plan` | YMM4確認前の確認設計 | short review order, expected readable story, NG return criteria | assistant |

Deliverables are not field-name checklists. A response that says `総尺 / mm:ss / 演出秒数 / 密度監査が必要` but does not fill values is still incomplete. If a value cannot be calculated, return a blocker code such as `TIMETABLE_BLOCKED_SOURCE_MISSING` with the exact missing source and assistant-owned next action. Even a numeric table is not enough for IR/YMM4: it must be encoded as `background_skit_blueprint.json` and paired with a `validate-background-skit-blueprint` result.

### Blueprint Artifact Contract

The required JSON root is:

- `source_lock`: `script_source`, `script_sha256`, `line_count`, `ymmp_source`, `fps`, `total_duration_formula`, `duration_source`.
- `script_diagnostic`: source line citations plus `ideal_script_delta`; semantic quality is not fully automated, but citations and deltas are mandatory.
- `duration_model`: `total_duration_sec`, source, confidence, and revision trigger when available.
- `blocks`: line range, timing windows, cast/props, proof path, and `negative_rationale` for each block.
- `asset_control_matrix`: every cast/prop/template reuse with availability, owner, control need, control route, and readback check.
- `density_thresholds`: numeric coverage/gap/state/repetition limits.
- `blockers`: explicit blocker codes when a truthful artifact cannot yet be calculated.

The validator recomputes line count, script hash, YMM4 duration, block coverage, active/rest windows, density, and asset/control bindings. `status: passed` is the only state that can feed cast/revised motion IR. `status: blocked` may feed only the actions explicitly listed in `allowed_next_actions` such as `overlay_only_compact_review`; `failed` and other `blocked` results are acceptable closeouts only when they report remaining blockers and forbidden next actions.

## Gate 0: Script Maturity

IR を作る前に、台本を次の観点で診断する。

| check | pass condition | fail output |
|---|---|---|
| thesis | 1文で動画の主張が言える | `SCRIPT_THESIS_WEAK` |
| block causality | 各章が前章の疑問に答えて次章の問いを作る | `SCRIPT_BLOCK_CAUSALITY_GAP` |
| visualizability | 各章に背景劇で見せられる行動・対立・変化がある | `SCRIPT_VISUAL_ANCHOR_MISSING` |
| evidence level | 断言・数字・制度説明に根拠または保留がある | `SCRIPT_EVIDENCE_WEAK` |
| role clarity | 消費者 / 対立役 / 変化後の専門家が脚本上でも見える | `SCRIPT_ROLE_DRIFT` |
| ending payoff | 最後に視聴者の判断基準が変わる | `SCRIPT_PAYOFF_WEAK` |

fail が出た場合は、`理想ならどんな台本だったか` を書く。例: 「REINSの説明」だけでなく、消費者が何を疑問に思い、業者が何を守ると言い、どこで利益相反が露出し、最後に何を基準に専門家を選ぶかが台本内で連結している状態。

## Gate 1: Duration Model

`time budget %` を絶対時刻へ変換する前に、総尺を固定する。

| field | meaning |
|---|---|
| `total_duration_sec` | 動画全体の秒数。未確定なら estimate と明記 |
| `duration_source` | `YMM4 voice readback` / `CSV timing` / `chars-per-second estimate` / `manual target` |
| `confidence` | `confirmed` / `estimated-high` / `estimated-low` |
| `speech_rate_assumption` | estimate の場合だけ、文字/秒や読上げ速度を記録 |
| `revision_trigger` | voice/readback 後に再計算が必要な条件 |

未確定の総尺で IR を確定しない。未確定時は `estimated timetable` として扱い、voice / CSV / YMM4 readback 後に `confirmed timetable` へ更新する。

Estimate is not encouragement. If confirmed timing is unavailable, the estimate must include the timing source, formula, source text length or line count, assumed speech rate, confidence, and revision trigger. A statement such as `総尺は未確定だが後で調整する` is invalid unless it is paired with `TIMETABLE_BLOCKED_*` or an actual estimated timetable.

## Gate 2: Quantitative Timetable

各 block は、構成比ではなく時刻表へ変換する。

| column | required | note |
|---|---|---|
| `block_id` | yes | `RE-01` など |
| `script_source` | yes | CSV / transcript / line readback source |
| `line_count` | yes | source の総行数 |
| `range_basis` | yes | なぜその行範囲か。台本上の節・問い・転換点 |
| `script_line_range` | yes | 台本行範囲 |
| `block_start` / `block_end` | yes | `mm:ss` |
| `block_duration_sec` | yes | 秒 |
| `skit_active_start` / `skit_active_end` | yes | 背景劇が動く時間 |
| `skit_active_duration_sec` | yes | 秒 |
| `rest_windows` | yes | 意図的に休ませる区間 |
| `visual_state` | yes | 画面状態名 |
| `cast_on_screen` | yes | 出ている人物 |
| `props_on_screen` | yes | 読解に必要な小道具 |
| `intent` | conditional | IR intent。template 名を入れない |
| `template_name` | conditional | `delivery_*_v1` 等 |
| `layer` | conditional | skit_group なら `layer:9` 相当 |
| `proof_path` | yes | 何で検査するか |
| `density_flag` | yes | `ok` / `intentional_rest` / `sparse_risk` / `unknown` |

`mm:ss` is a format, not a value. `block_start/end: mm:ss`, `演出秒数: 必要`, or `lines 1-12` without `script_source / line_count / range_basis` is not a quantitative timetable. Use concrete values such as `block_start/end: 00:00-01:15`, `skit_active_duration_sec: 28`, and `script_source: csv/...`.

## Gate 3: Timeline Density Audit

「スカスカではない」を主観で済ませない。次を算出する。

Before audit, declare episode-specific thresholds. They can be provisional, but they must be numeric.

| threshold | example |
|---|---|
| `minimum_active_visual_coverage_pct` | `55%` |
| `maximum_unexplained_gap_sec` | `8 sec` |
| `visual_states_per_min_range` | `2.0-5.0` |
| `maximum_repeated_motion_ratio` | `35%` |

| metric | definition | fail condition |
|---|---|---|
| `active_visual_duration_sec` | 背景劇・props・overlay が意味を持って画面に出る合計秒数 | block ごとに 0 のまま |
| `active_visual_coverage_pct` | active / total | 低すぎる場合は `SPARSE_TIMELINE_RISK`。数値閾値は案件別に設定 |
| `intentional_rest_duration_sec` | 語りを邪魔しないための明示休止 | 理由なしなら empty 扱い |
| `unexplained_empty_duration_sec` | 意図不明の空白 | 0 を目標 |
| `longest_unexplained_gap_sec` | 意図不明空白の最大長 | 長い場合は block 再設計 |
| `visual_states_per_min` | 1分あたりの意味ある画面状態数 | 少なすぎる/多すぎる場合に再配分 |
| `repeated_motion_ratio` | 同じ motion cue に依存する比率 | 高い場合は props/blocking に戻す |

閾値は固定魔法数字にしない。episode の語り密度、視聴者に読ませる props の複雑さ、YMM4 の視認性で変える。ただし、値を置かずに「スカスカか確認する」とだけ書くのは禁止する。`unexplained_empty_duration_sec` は常に説明対象にする。

## Gate 4: Asset / Cast / Control Matrix

演出指定は「何を置くか」ではなく「何を制御できるか」まで書く。

| field | required example |
|---|---|
| `cast` | 消費者 / ゲートキーパー業者 / キュレーター / 配達員 |
| `asset_needed` | body, face, PC, card, QR, door, package |
| `availability` | existing / missing / proxy-only / reskin-candidate |
| `control_needed` | enter, hold, point/look, card reveal, gate open, exit |
| `control_route` | existing template / new template / overlay / static item / manual YMM4 |
| `ir_intent` | `enter_from_left` 等。template 名と分離 |
| `template_name` | `delivery_enter_from_left_v1` 等 |
| `readback_check` | layer, frame, duration, position, asset path, group children |
| `creative_check` | 背景だけで何が起きたか読めるか |

## Gate 5: IR Authoring

IR は Gate 0-4 が通った後にだけ作る。

- 毎発話に置かない。scene beat の時刻表 anchor に置く。
- `motion_target: "layer:9"` は skit_group actor の機械接続であり、演出品質の証明ではない。
- `intent` は registry で解決できるものに限定する。
- 未登録 intent は `SKIT_GROUP_UNKNOWN_INTENT` として止め、新 template candidate に戻す。
- props / overlay / card / door / QR は、motion cue ではなく画面読解の主役として扱う。

## Gate 6: Compact Review Before Production Timing

production timing に散らす前に、同じ cue を compact review で短く並べる。

| check | pass condition |
|---|---|
| story read | 背景だけで setup / complication / change / resolution が読める |
| cast continuity | 同じ人物が同じ役割として見える |
| density | 空白が意図的か分かる |
| control | motion / hold / reveal / exit が破綻しない |
| props readability | 小道具が一瞬で読める、または読むための hold がある |

compact review が NG の場合、production timing へ進めない。

overlay/card-only compact review is allowed only when the validator result explicitly lists `overlay_only_compact_review` in `allowed_next_actions`. A generated compact-review closeout must include the generated artifact path, readback or validation result, remaining blockers, `forbidden_next_actions`, and an explicit statement that the output is not creative acceptance. Supporting files such as gap reports or row-time maps are not enough unless the validator result is the authority chain.

## Gate 7: Production Timing Readback

本番タイムラインでは、全体尺と実発話位置に合わせて再検査する。

- `block_start/end` と実発話のズレ
- `skit_active_duration_sec` が短すぎないか
- 意図しない長空白が出ていないか
- layer / asset path / group children / frame の readback
- compact review で通った順序が production timing で崩れていないか

## Pilot Application Order

`pilot_yukkuri_theater_v1` では次の順で進める。

1. `script_diagnostic`: 現台本が「杭だけ」になっている箇所を行範囲で列挙する。
2. `duration_model`: 総尺を estimate / confirmed に分けて記録する。
3. `quantitative_timetable`: 7 ブロックを `mm:ss` と秒数へ変換する。
4. `density_audit`: 空白・休ませる区間・visual states/min を出す。
5. `asset_control_matrix`: 消費者 / ゲートキーパー / キュレーター / props / 既存 delivery template の proxy 限界を分ける。
6. `script_repair_brief`: 理想台本なら何を追加/削除/接続すべきかを書く。
7. `revised_skit_group_ir案`: Gate 0-6 が通った cue だけを IR にする。
8. `compact_review_plan`: YMM4 確認はここから。旧 line-cue IR は creative acceptance に渡さない。

## Full Workflow: Grand Design to IR

1. Source lock: 台本 / CSV / 既存 `.ymmp` / template registry / template source を列挙し、line count と timing source を固定する。
2. Script architecture: thesis, causality, evidence, payoff, visualizability を診断し、「杭だけ」の箇所を line range で止める。
3. Ideal-script delta: 理想ならどの問い・反論・根拠・転換・結論が必要だったかを、追加/削除/接続単位で書く。
4. Grand design: cast roles, conflict, transformation, visual metaphor, ending payoff を固定する。
5. Scene bible: block ごとの story beat / placement / props / rest span / proof path を固定する。
6. Duration model: confirmed または estimated の total duration を作り、estimate なら式と confidence を添える。
7. Quantitative timetable: `mm:ss` start/end と `duration sec` を全 block / skit active window へ埋める。
8. Asset/control matrix: 登場人物・素材・動き・制御ルート・不足・owner を分ける。
9. Density thresholds + audit: coverage, unexplained empty, longest gap, visual states/min, repeated motion ratio を数値化する。
10. Blueprint validation: `validate-background-skit-blueprint <blueprint.json> --script <txt> --ymmp <ymmp> --fps 60` を実行し、`passed / failed / blocked` を得る。
11. Revised IR candidate: validator `passed` の cue だけを `intent` と `template_name` を分けて入れる。`blocked` の場合は `allowed_next_actions` に明示された overlay/card-only scope だけ許可する。
12. Compact review: production timing に散らす前に、背景劇だけで読めるか短縮版で見る。
13. Production timing readback: 実発話位置へ戻し、空白・ズレ・レイヤー・duration を再計算する。
14. Loop: NG が出たら IR だけ直さず、script / scene / asset / timing のどこへ戻るかを明示する。

This workflow rejects optimistic copy. No line in the chain may rely on `まあ下流が完成させる`, `YMM4で見れば分かる`, or a tone-only phrase such as `舞台監督の香り`. The output must be values, blockers, or explicit deltas.

## Reject Conditions

- `time budget %` だけで IR / 演出指定に進む。
- `background_skit_blueprint.json` と validator result なしに IR / YMM4 / production timing へ進む。
- 数値入り表だけで validator の `derived_metrics` と照合しない。
- 総尺・開始時刻・終了時刻・演出秒数がない。
- `総尺 / mm:ss / 演出秒数` の項目名だけを並べ、値を埋めない。
- `lines 1-12` のような行範囲を、`script_source / line_count / range_basis` なしで使う。
- `スカスカかどうか` を density audit なしで主観判断する。
- density audit の閾値・結果を数値化せず、`確認する` で止める。
- 脚本未成熟を認めながら、演出側で補えばよいとする。
- `下流で完成させる` / `YMM4で見れば分かる` として、assistant 側の gap report を飛ばす。
- 登場人物・素材・動き・制御・検証経路が分かれていない。
- ideal script delta がないまま、現台本を production-ready と扱う。
- 励まし、雰囲気、比喩だけで closeout する。
