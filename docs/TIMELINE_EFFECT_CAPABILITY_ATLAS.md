# Timeline / Effect Capability Atlas

> **目的**: ManualSample が無くても、`IR -> registry -> ymmp` の接合点で「何ができるか / どの route が正規か / どこから先が補助や probe か」を operator が 1 枚で判断できるようにする。  
> **機械台帳**: `python scripts/build_capability_atlas.py` -> `samples/_generated/capability_atlas.json`

---

## 1. Decision Ladder

最初に「何を動かしたいか」で分岐する。**effect 名から逆算して IR に直書きしない。**

| 対象 | まず使う入口 | support_level | 位置づけ |
|---|---|---|---|
| `speaker_tachie` | `face` / `idle_face` / `slot` / `motion` | `direct_proven` | 既存の主経路 |
| `skit_group` canonical | `samples/canonical.ymmp` -> `audit-skit-group` | `direct_proven` | canonical anchor は repo 内で成立済み |
| `skit_group` exported intent | **template intent** -> `skit_group_registry` -> `audit-skit-group` | `direct_proven` | v1 planned set 5 件 (`enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left`) は export まで完了 |
| `skit_group` future intent | **template intent** -> `skit_group_registry` -> `audit-skit-group` | `template_catalog_only` | v1 外の新 intent は production gap が出た時だけ起票 |
| `skit_group` の補助調整 | `motion_target` / `group_motion` | `direct_proven` | 補助経路。主経路ではない |
| `bg_layer` | `bg` / `bg_anim` | `direct_proven` | measured route 前提 |
| `overlay_se` | `overlay` / `se` | `direct_proven` | registry + timing anchor 前提 |
| `transition` | `fade` のみ | `direct_proven` | non-fade は未昇格 |
| raw effect atom | `effect_catalog.json` | `probe_only` | 原子辞書。IR の正規入口ではない |

**基本原則**

- `speaker_tachie` は既存 patch path を使う
- `skit_group` は **まず template intent** を書く
- `motion_target` / `group_motion` は、template だけで吸収しきれない時の補助に留める
- raw effect 名は registry 設計の材料であって、production IR の正規契約ではない

---

## 2. Capability Catalog

### 2.1 `direct_proven`

| expression_id | preferred_route | evidence | manual_checks | limitations |
|---|---|---|---|---|
| `speaker_tachie.face` | `face -> face_map/palette -> patch-ymmp` | G-06 / 茶番劇 E2E | 表情ラベルの見え方 | label 名は human-authored |
| `speaker_tachie.idle_face` | `idle_face -> face_map/palette -> patch-ymmp` | G-07 / 茶番劇 E2E | 非話者の待機顔がうるさくないか | palette coverage 前提 |
| `speaker_tachie.slot` | `slot -> slot_map -> patch-ymmp` | G-11 / 茶番劇 E2E | 左右配置の読みやすさ | registry 駆動 |
| `speaker_tachie.motion` | `motion -> tachie_motion_map_library or motion_map` | route contract / G-17 / motion library | 強すぎないか、反復が長すぎないか | `speaker_tachie` 専用 |
| `bg_layer.bg` | `bg -> bg_map -> patch-ymmp` | G-15 / capability matrix | 背景が文脈に合うか | asset choice は人間判断 |
| `bg_layer.bg_anim` | `bg_anim -> measured route -> patch-ymmp` | G-12 / route contract | pan/zoom の強度 | corpus 依存 route あり |
| `overlay_se.overlay` | `overlay -> overlay_map -> timing anchor` | G-13 | 重なり・視認性 | registry 前提 |
| `overlay_se.se` | `se -> se_map -> timing anchor` | G-18 | タイミング・音量 | registry 前提 |
| `transition.fade` | `transition=fade` | G-12 / capability matrix | fade timing | fade 以外は未対応 |
| `skit_group.canonical_anchor` | `samples/canonical.ymmp -> audit-skit-group` | canonical adoption packet | 左向き基準姿勢・ImageItem-only 構成 | **anchor 成立のみ。派生 asset は別** |
| `skit_group.intent.enter_from_left` | `template intent -> registry -> audit-skit-group` | P02 cautious gate + standalone export sync | 着地位置 / overshoot / settle | **starter export 済み** |
| `skit_group.intent.nod` | `template intent -> registry -> audit-skit-group` | P02 cautious gate + standalone export sync | nod amplitude / does not dominate scene | **export 済み** |
| `skit_group.intent.surprise_oneshot` | `template intent -> registry -> audit-skit-group` | P02 cautious gate + standalone export sync | Y-only jump / one-shot | **starter export 済み** |
| `skit_group.intent.deny_oneshot` | `template intent -> registry -> audit-skit-group` | P02 cautious gate + standalone export sync | X-only sway range / one-shot | **export 済み** |
| `skit_group.intent.exit_left` | `template intent -> registry -> audit-skit-group` | P02 cautious gate + standalone export sync | exit direction / scene closure timing | **export 済み** |
| `skit_group.motion_target` | `motion + motion_target -> layer VideoEffects` | B-2 GroupItem proof | 顔/body の同期 | **補助経路** |
| `skit_group.group_motion` | `group_motion + group_target -> X/Y/Zoom` | G-20 / route contract | 構図の破綻 | **幾何補助** |

### 2.2 `template_catalog_only`

現時点の v1 planned set には remaining `template_catalog_only` intent は無い。

future registry 例（production gap が出た時だけ起票）:

- `happy_sway`
- `sad_droop`
- `thinking_zoom`
- `nod_oneshot`
- `reset_center`

意味すること:

- `audit-skit-group` は canonical corpus に対して exact / fallback / manual_note を判定できる
- v1 planned set 5 件は user-owned native template export / sample proof を経て `direct_proven` へ昇格した
- v1 外の intent は production-use validation で concrete gap が出るまで追加しない
- old `skit_01` corpus は引き続き canonical anchor 不足を再現する
- したがって future `skit_group.intent.*` は起票時点では `template_catalog_only` に留める

### 2.3 `probe_only`

`effect_catalog.json` の raw effect atom は **原子辞書**としては useful だが、Atlas では `probe_only` に置く。

例:

- `JumpEffect`
- `GaussianBlurEffect`
- `TilingGroupItemsEffect`
- `InOutMoveFromOutsideImageEffect`

意味すること:

- その effect が repo に存在することは分かる
- `$type` や parameter key を registry に書く材料にもなる
- しかし **それ単体では production IR の正規入口ではない**

`samples/_generated/capability_atlas.json` には raw effect 111 件を `effect_atom.*` として列挙する。`is_community=true` のものは limitation にコミュニティプラグイン依存を明記する。

---

## 3. Negative Catalog

### 3.1 今は主軸にしないもの

- `skit_group` を raw `motion_target` だけで量産すること
- `group_motion` だけで茶番劇演技を表現しようとすること
- raw effect 名から逆算して IR を書くこと

### 3.2 `unsupported`

- non-fade transition
- repo 根拠のない template route
- 任意 item への「主軸としての」direct effect write

`unsupported` は「永遠に不可」ではなく、**repo-local route measurement / verification / approval が未成立**という意味で使う。

---

## 4. No-ManualSample Workflow

ManualSample が無いときは、次の順で確認する。

1. **Atlas で対象を決める**  
   `speaker_tachie` / `skit_group` / `bg_layer` / `overlay_se` / `transition`
2. **主経路か補助経路かを確定する**  
   - canonical anchor が必要なら `samples/canonical.ymmp` を起点にする
   - `skit_group` はまず template intent
   - `motion_target` / `group_motion` は補助
3. **機械判定を走らせる**  
   - template-first 側: `python -m src.cli.main audit-skit-group <ymmp> <ir.json> --skit-group-registry <json>`
   - timeline route 側: `python -m src.cli.main measure-timeline-routes <ymmp> --expect samples/timeline_route_contract.json --profile <profile>`
4. **Atlas の support_level を見る**  
   - `direct_proven`: 既存 adapter path で進める
   - `template_catalog_only`: preflight と registry 整備まで。standalone export / sample proof 完了前の intent は completion 扱いしない
   - `probe_only`: registry/material planning の材料としてのみ使う
   - `unsupported`: route 再測定か方針変更が必要

---

## 5. IR 接合の読み方

IR でまず書くものは次の順。

1. `speaker_tachie`
   - `face` / `idle_face` / `slot` / `motion`
2. `skit_group`
   - **template intent**
   - template だけで不足する場合に `motion_target` / `group_motion`
3. `bg_layer`
   - `bg` / `bg_anim`
4. `transition`
   - 当面 `fade` のみ
5. `overlay` / `se`
   - registry 解決前提

**effect catalog は原子辞書であり、IR の正規入口ではない。**
