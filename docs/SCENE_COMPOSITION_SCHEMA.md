# Scene Composition Schema (SCS) v0.1

NLMYTGen の 1 frame 構成 (画面領域分割 + 要素の役割割当 + 要素生成則) を、carrier 作成・adapter 生成・readback 検証の各段階で参照できる **実行可能な手順** として固定する schema。

G-27 の各 probe (`visual_proxy_v2*`、`micro_scene_probe`、`micro_scene_visibility_probe`、`primitive_visibility_calibration_probe`) が openability=pass / readback=pass しても "indexed whiteboard" / "drawing-semantics calibration" 止まりだった失敗を、構図設計の rule violation として分類し直すために置く。

---

## 0. 責務境界

- **対象**: 16:9 / 1920×1080 production frame の **静止構図** (要素の grid 配置、視覚 role の割当、ShapeItem / TextItem / GroupItem / ImageItem の生成則)。
- **対象外**:
  - 1 frame 内の motion / transition (= Motion Beat Plan の責務、`docs/PRODUCTION_PIPELINE_CONTRACT.md` 参照)。
  - 場面と場面の編集論 (cut / dissolve / 章構成) (= Script Beat IR の責務)。
  - 色 / フォント / ブランド方針 (= Visual Direction Contract の責務、`docs/G27_REVIEW_CONSOLE_SPEC.md` 参照)。
  - 創造的最終判断 (creative acceptance)。本 schema は readable / production-ready の必要条件であり、十分条件ではない。
- **位置づけ**:
  - `G27_REVIEW_CONSOLE_SPEC.md` の Visual Direction Layer + Shot Layout Layer に対する **実装手順 spec**。
  - `PRODUCTION_PIPELINE_CONTRACT.md` の Shot Layout Plan stage で生成される `shot_layout_plan.json` の **schema 規範**。
  - `G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md` の carrier 設計の **理論的根拠**。

---

## 1. Composition Grid (画面領域分割)

1920×1080 を機能領域に分割する fixed grid。carrier 設計・adapter 生成・readback の全段階でこの分割を尊重する。

```
┌────────────────────────────────────────────────────────────┐ y=0
│ outer safe band (top 5% / 54px) — 何も置かない              │
├────────────────────────────────────────────────────────────┤ y=54
│ title band (8-12% / 86-130px)                              │
│   全体タイトル / anchor 一行のみ                            │
├────────────────────────────────────────────────────────────┤ y=140
│                                                            │
│   main canvas (60-65% / 648-702px)                         │
│   focal anchor + supporting + connector + risk-marker      │
│   ここが構図 type ごとに further subdivide される           │
│                                                            │
├────────────────────────────────────────────────────────────┤ y=842
│ caption safe area (bottom 18-22% / 194-238px)              │
│   字幕 (YMM4 JimakuItem) の予約領域。carrier item を置かない │
├────────────────────────────────────────────────────────────┤ y=1026
│ outer safe band (bottom 5% / 54px) — 何も置かない           │
└────────────────────────────────────────────────────────────┘ y=1080

  outer safe band (left 5% / 96px)     outer safe band (right 5% / 96px)
```

数値要約:
- frame: 1920×1080 / 16:9
- outer safe margin: 上下左右 5% (54 / 96 px)
- title band: y=54-140 程度
- main canvas: y=140-842 程度
- caption safe area: y=842-1026 (これは YMM4 字幕領域、可侵してはならない)
- bottom outer safe band: y=1026-1080

YMM4 の字幕は `caption safe area` を使う前提で sizing する。production frame の主要要素・読ませる label は **main canvas** の内側に収める。

---

## 2. Composition Types (主要構図パターン)

Beat の **意味の論理形** から逆算して選ぶ 5 つの主要 composition type。これ以外を採用しない。anti-pattern の "indexed whiteboard" / "grid-overload" / "narrative-strip" は意図しない限り発生させない。

### 2.1 `split` — 二項対比 / 対立

- **発火条件**: Beat が「A vs B」「公開 vs 隠匿」「過去 vs 現在」「期待 vs 実態」を主張する
- **main canvas の subdivide**:
  - left panel: x=96-826 (画面左 42-44%)
  - center boundary / lock / threshold: x=826-1094 (中央 6-10%)
  - right panel: x=1094-1824 (画面右 42-44%)
- **必須 visual role**: 左 focal_anchor + 右 focal_anchor + 中央 boundary。boundary は機能的意味 (lock / wall / arrow) を持つ
- **例**: G27_PublicVsBrokerDB carrier (REINS vs 公開ポータル)、見える情報 vs 見えない情報

### 2.2 `center-focal` — 単一焦点

- **発火条件**: Beat が「核心はこれ」「100% マッチ」「一点突破」「決定的瞬間」を主張する
- **main canvas の subdivide**:
  - focal: 画面中央付近 (x=560-1360, y=200-780) に占有率 25-40%
  - 周辺要素は焦点を引き立てる小型に限定 (各 8% 以下)
- **必須 visual role**: focal_anchor 1 個 + supporting 最大 3 個
- **例**: AI panel が confident green match で点灯、編集力 lens が 1 物件に焦点

### 2.3 `chain` — 因果 / 流れ

- **発火条件**: Beat が「A → B → C」「原因 → 結果」「選択 → 推薦」を主張する
- **main canvas の subdivide**:
  - node を左→右 / 上→下 に 3-4 個まで配置 (4 個を上限とする)
  - 各 node 間に connector (矢印 / 線 / gradient)
- **必須 visual role**: focal_anchor を node の最後 (結論側) に置き、他は supporting + connector
- **anti-pattern**: 5+ node にすると flowchart 化して読めなくなる
- **例**: 多数の listings → curation → 一つの選定

### 2.4 `reveal` — 隠匿 / 段階開示

- **発火条件**: Beat が「見えていなかったものが現れる」「裏に潜む」「実は」を主張する
- **main canvas の subdivide**:
  - 上層 (z 軸前面): visible element (画面の表側に見える物)
  - 下層 (z 軸背面): hidden element、初期は opacity 低 or partial occlusion
- **必須 visual role**: focal_anchor (visible) + risk_marker または hidden focal_anchor (背面)
- **motion 前提**: 1 frame では透過率の関係で表現するが、motion 段では opacity 変化を予定する
- **例**: property card の下に boundary dispute / inheritance icon が浮き上がる

### 2.5 `mediator` — 媒介 / 統合

- **発火条件**: Beat が「A と B を繋ぐ」「専門家が緩衝する」「相補的に働く」を主張する
- **main canvas の subdivide**:
  - left source: x=96-660 (画面左 30%)
  - center mediator: x=760-1160 (中央 20%)
  - right target: x=1260-1824 (画面右 30%)
- **必須 visual role**: 左 source + 中央 mediator (人物 silhouette + connector) + 右 target
- **例**: AI panel と viewer の間に specialist が立つ

### 2.6 明示的に anti-pattern とみなす構図

- **indexed whiteboard**: 全要素を equal-weight cards として並べる (visual proxy v2/v2.1)
- **grid-overload**: 4×3 以上の cell に同質要素を詰める (presentation card 風)
- **narrative-strip**: 横に 5+ panel を等間隔で並べる (comic strip 風)
- **drawing-semantics calibration**: tonal system だけ整え focal が無い (primitive_visibility_calibration_probe)

これらは Frame Contract 違反として `composition_violation` に記録する。

---

## 3. Visual Role Vocabulary (要素の役割割当)

1 frame に配置される全要素は以下の role のいずれかに分類される。**全要素が必ず 1 個の role を持つ**。role 不在の要素 (= 装飾でも focal でも無いもの) は除去する。

| role            | 説明                                  | 個数上限 / frame   | 占有率目安   |
|-----------------|---------------------------------------|--------------------|--------------|
| `focal_anchor`  | 主被写体。視線が最初に止まる対象      | 1 (split のみ 2)   | 25-40%       |
| `supporting`    | focal を補強する小要素                | ≤ 3                | 各 5-12%     |
| `boundary`      | split の中央仕切り / lock / threshold | 0 or 1             | 6-10% (縦帯) |
| `connector`     | 因果矢印・線・gradient                | ≤ 2                | 線状         |
| `risk_marker`   | 警告・注意のアクセント                | 0-1                | 3-6%         |
| `decoration`    | 単独で意味を持たない装飾              | ≤ 3                | 各 ≤3%       |
| `label`         | title / panel title / card title      | ≤ 2 (text 合計 30 文字以内 / frame) | text |

合計要素数の許容範囲: **8-14 個 / frame**。

- 7 個以下 → focal の周辺が薄い (sparse-focal anti-pattern)
- 15 個以上 → indexed whiteboard anti-pattern

参考: G-27 の各 probe 実績
- `micro_scene_visibility_probe` v2: 57 inserted items → **過密** (whiteboard 化)
- `primitive_visibility_calibration_probe`: 11 items → 範囲内だが role 分類が無く focal 不在
- `visual_proxy_v2` / `v2.1`: card 数のみ多く role 不明 → indexed whiteboard

---

## 4. Reading Order (視線誘導) と Typography Hierarchy

### 4.1 Reading Order

Composition type ごとに固定する。

| composition type | reading order (1→N の順)                         |
|------------------|--------------------------------------------------|
| `split`          | left focal → boundary → right focal (Z 字)       |
| `center-focal`   | center focal → supporting → label                |
| `chain`          | node 1 → node 2 → node 3 (→ node 4) 左→右 / 上→下 |
| `reveal`         | 上層 visible → 下層 hidden (focus が裏に落ちる)  |
| `mediator`       | source → mediator → target                       |

これは `shot_layout_plan.json` の `reading_order` フィールドとして配列で保持する。adapter が patch するときに reading order の整合性を sidecar で確認する。

### 4.2 Typography Hierarchy

スマホ視聴 (1080p 縦持ち相当の縮小) で読めることを最低条件とする。

| 位置 / 役割                          | FontSize (1080p basis) |
|--------------------------------------|------------------------|
| title band label (`G27PBD_Title` 等) | 72-96 px               |
| main canvas focal label              | 48-64 px               |
| supporting / card label              | 32-42 px               |
| caption (YMM4 字幕 default)          | 28-36 px               |

これより小さい text (metadata 風の極小注釈、20 px 以下) は production frame に **入れない**。説明が必要なら narration へ移すか shot を分割する。

### 4.3 In-frame Text Budget

- in-frame label 数: ≤ 2 / frame
- in-frame text 合計: 30 文字以内 / frame (Frame Contract と同じ)
- 字幕 (caption safe area) はこの予算に含めない

---

## 5. Element Primitive Rules (要素生成則)

YMM4 native primitive のうち adapter で扱う ShapeItem / TextItem / GroupItem / ImageItem の各生成則。

### 5.1 ShapeItem

- `ShapeParameter.SizeMode` は **必ず `WidthHeight`**。
  - `SizeAspect` + `Size=100` + `AspectRate=0` は **anti-pattern** (G-27 `micro_scene_probe` v1 の失敗原因。意図した大型 panel が 100px 矩形に潰れた)
- `Width` / `Height` は §1 の grid 内の絶対値 px で書く (比率指定はしない)
- visible shape の `StrokeThickness` は 0 にしない (default は 4-8 px、focal_anchor は 8-16 px)
- `Opacity` の default は 100。透過用途 (reveal の下層) のみ 30-70 の特定値を使う
- color は **文字列形式** で書く (`#1a2b3c` または YMM4 期待の string form。FontColor を JSON color object として書く schema 違反は G-27 minimal probe で修正済み)

### 5.2 TextItem

- `FontSize` は §4.2 の hierarchy に従う
- in-frame text 量は §4.3 の予算内
- light stage / dark stage の方針に従う font color (混在禁止)
- text の配置は parent panel の内側に収める (panel 外への食み出し禁止)

### 5.3 GroupItem

- 1 つの logical role を担う要素群を group 化する (例: 1 card = body Shape + label Text → group)
- group の `item name` は SCS visual_role と対応させる (例: `G27PBD_PublicCard1` = focal_anchor or supporting)
- group 内に冗長 item を残さない
- nested group は深さ 2 までを推奨

### 5.4 ImageItem

- carrier 作成時の素材登録、または registry で解決済みの slot patch でのみ追加する
- adapter が新規外部画像を assemble しない (Python 画像生成禁止と整合)
- `FilePath` は YMM4-readable Windows path (絶対 / 相対の混在禁止。POSIX path 禁止 — G-24 placement で確定済み境界)

---

## 6. Beat → Composition Type Mapping Procedure

Script Beat IR の `narration_cue` / `claim` / `local_context` から composition type を選ぶ機械的手順。`shot_layout_plan.json` 生成時に必ず通す。

### 6.1 論理形の抽出

Beat の主張を以下の論理形に分類:

| 論理形         | 言い換え例                                         | → composition type |
|----------------|----------------------------------------------------|--------------------|
| 対比 / 対立    | A is not B / A vs B / A unlike B / 公開 vs 隠匿    | `split`            |
| 単一焦点       | A is the answer / A is the core / これが核心       | `center-focal`     |
| 因果 / 流れ    | A causes B / A leads to B / 選択 → 結果            | `chain`            |
| 段階開示       | behind A is B / A hides B / 実は裏には             | `reveal`           |
| 媒介 / 統合    | A connects B and C / 専門家が緩衝する              | `mediator`         |

論理形が複数該当する場合は **最も支配的な一つ** を選ぶ。複数構図の合成は anti-pattern (`indexed whiteboard` へ落ちやすい)。

### 6.2 構図確定後の手順

1. §1 grid に従って outer safe band / title band / main canvas / caption safe area を確保する
2. §2 の選ばれた composition type の main canvas subdivide を適用する
3. §3 の visual role table に従って要素を割当てる
4. §4 の reading order と typography hierarchy を確認する
5. §5 の primitive rules で各要素を生成する
6. §7 の compliance check 用 fields を sidecar JSON に出力する

### 6.3 違反検出

各段階で違反した場合は `composition_violation` を sidecar に記録 (silently normalize しない)。修正は別 slice。

---

## 7. SCS Compliance Check (sidecar fields)

`shot_layout_plan.json` / `visual_treatment_proof_readback.json` の各 frame entry に以下のフィールドを含める。

```json
{
  "frame_id": "RE-02-development",
  "composition_type": "split",
  "visual_roles": {
    "focal_anchor": ["G27PBD_PublicCard1", "G27PBD_BrokerCard1"],
    "supporting":   ["G27PBD_PublicCard2", "G27PBD_BrokerCard2", "G27PBD_BrokerCard3"],
    "boundary":     ["G27PBD_Lock"],
    "connector":    [],
    "risk_marker":  [],
    "decoration":   [],
    "label":        ["G27PBD_Title", "G27PBD_PublicTitle"]
  },
  "element_count": 10,
  "element_count_check": "pass",
  "reading_order": [
    "G27PBD_PublicCard1",
    "G27PBD_Lock",
    "G27PBD_BrokerCard1"
  ],
  "typography_hierarchy_check": "pass",
  "in_frame_text_budget": {"labels": 2, "chars": 18},
  "in_frame_text_budget_check": "pass",
  "safe_area_check": "pass",
  "subtitle_clearance_check": "pass",
  "shape_size_mode_check": "pass",
  "color_format_check": "pass",
  "composition_violations": []
}
```

判定:
- `composition_type` が §2 の 5 種類のいずれでもない → `production_readiness: no`
- `element_count` が 8 未満または 14 超 → `composition_violations` に `ELEMENT_COUNT_OUT_OF_RANGE`
- `visual_roles.focal_anchor` が 0 個 (または split 以外で 2 個以上) → `FOCAL_ANCHOR_MISCOUNT`
- §5.1 の `shape_size_mode_check: fail` → `SHAPE_SIZE_MODE_INVALID`
- §5.1 の `color_format_check: fail` → `COLOR_FORMAT_INVALID`
- `safe_area_check` / `subtitle_clearance_check` のいずれかが fail → `FRAME_CONTRACT_VIOLATION`

readback で visibility = pass しても、上記いずれかが fail なら production-readiness は `no` のまま。

---

## 8. Failure Examples and Lessons

過去の G-27 probe を SCS の lens で再分類する。

### 8.1 `visual_proxy_v2` / `v2.1` (2026-05-12)

- 観察: 7 candidate visual を card として並べた contact sheet。openable pass。
- 失敗: focal_anchor 不在、全要素 equal-weight → `indexed whiteboard` anti-pattern (§2.6)
- 違反した SCS rule: §3 visual role 不在、§4 reading order 不在、§6 composition type mapping 未実施
- 教訓: card 並列 ≠ scene。focal を 1-2 個に限定し、supporting で焦点を強める

### 8.2 `micro_scene_probe` v1 (2026-05-12)

- 観察: 4 beat / 60 sec / 54 items / ShapeItem=38 / TextItem=16。openable pass、readback pass。
- 失敗: 意図した大 panel が `SizeMode=SizeAspect, Size=100, AspectRate=0` で 100px 矩形に潰れた → 視覚的に panel が消えた
- 違反した SCS rule: §5.1 `ShapeParameter.SizeMode=WidthHeight` の必須化違反
- 教訓: ShapeItem 生成は SizeMode を明示固定する。default に依存しない

### 8.3 `micro_scene_visibility_probe` v2 (2026-05-13)

- 観察: SizeMode は WidthHeight に修正、57 inserted items / 4 beat / 60 sec。focal panel 4 個。
- 失敗: 57 items に膨らみ scene として読めない → `indexed whiteboard` (§2.6)
- 違反した SCS rule: §3 element count 8-14 範囲超過、§4 reading order 未定義
- 教訓: visibility が確保されても密度違反は production-readiness=no。要素削減と role 分類が必要

### 8.4 `primitive_visibility_calibration_probe` (2026-05-13)

- 観察: 11 items / ShapeItem=6 / TextItem=5 / 1 light-stage tonal system / 920×560 Main Panel / center/TL/BR anchor markers
- 失敗: tonal system / anchor marker は整ったが、composition type の意図が無く drawing-semantics calibration として止まった
- 違反した SCS rule: §6 Beat → composition type mapping 不在、§3 focal_anchor 不在
- 教訓: tonal system は frame contract の必要条件だが scene にはならない。composition type を先に決める

これらの教訓は §3 元素数上限・§5.1 SizeMode 必須・§6 composition type mapping 必須として schema 本体に反映済み。

---

## 9. Adapter Patch Boundary in SCS Context

`G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md` の patch boundary を SCS の文脈で再表記。

### 9.1 adapter が patch してよい (carrier 受領後)

- TextItem の表示文字列 (typography hierarchy / text budget 内)
- ShapeItem / GroupItem / TextItem の visibility (`IsHidden`)
- timing (開始 frame、長さ)
- sidecar JSON / readback report の provenance id

### 9.2 adapter が patch してはいけない

- composition grid (§1 領域分割)
- composition type (§2)
- visual role 割当 (§3)
- focal anchor の geometry (X / Y / Width / Height / Zoom)
- boundary / lock の placement (split の場合)
- safe area / caption clearance / outer safe band
- stage の light / dark 方針
- color hierarchy

これらの **構造的設計判断は carrier 側 (= 人手 YMM4 author) が決定** し、adapter は内容流し込みに専念する。template-first / slot-fill の境界はここで切る。

---

## 10. 適用順序

1. **carrier 設計時** (人手): §1 grid + §2 composition type + §3 visual role + §4 typography + §5 primitive を参照
2. **`shot_layout_plan.json` 生成時** (assistant): §6 で beat から composition type を選び、§7 sidecar fields を構成
3. **`visual_treatment_proof_readback.json` 出力時** (assistant): §7 compliance を全 frame entry に出す
4. **G-27 / G-27 後継 case-specific cycle の review 時** (GUI 経由): §7 で fail した item を `composition_violations` で表示

---

## 11. 適用範囲と継続条件

- **現在の対象**: G-27 (Real Estate DX) + その後継 case-specific review cycle
- **拡張対象**: AI monitoring labor / baseball news infographic 等の pipeline smoke topic
- **case-specific motif** (real-estate texture / labor stakes / data density) は §2 の composition type に upper layer で乗せる。同 motif でも composition type は beat 単位で選び直す

本 schema は v0.1。実 carrier 受領後の G-27 readback で composition type 別の adapter slot-fill が動作するかを観測し、v0.2 で composition type 個別の slot 規格 (split の panel slot 数、chain の node slot 数 など) を追加する予定。
