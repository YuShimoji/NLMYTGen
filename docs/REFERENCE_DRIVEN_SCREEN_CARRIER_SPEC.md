# Reference-Driven Generic Screen Carrier Spec v0.1

参照画像ベース汎用画面 carrier 設計の薄い正本。これは G-27 Real Estate DX
固有の production carrier 待ちを続けるための文書ではなく、既存の G-27
proof / diagnostic carrier / Review Console / SCS lessons を汎用 screen carrier
設計へ再利用するための入口である。

## 目的

- 人間が渡す参照画像から、見た目そのものではなく構図原理を抽出する。
- 抽出対象は余白、密度、色階層、視線誘導、UI感、カード配置、gated
  information 感、YouTube 解説 / ニュース図解としての読みやすさに限る。
- 抽出結果を [SCENE_COMPOSITION_SCHEMA.md](SCENE_COMPOSITION_SCHEMA.md) の
  composition type、visual role、text budget、safe area、subtitle clearance
  へ変換する。
- YMM4 で人間が作れる generic screen carrier archetype と item/group 構成案を
  出す。

## 非目的

- 参照画像の丸コピー。
- reference image URL、raw image、著作権不明画像、private data の repo commit。
- 素材や画像の自動取得。
- Python による画像生成、画像合成、YMM4 `.ymmp` ゼロ生成。
- G-27 diagnostic carrier の production 昇格。
- render、production timing、creative final acceptance。

## 入力

- 参照画像 3-7 枚。画像ファイル自体は repo に commit しない。
- 各画像の参考対象メモ。最低 1 つ、できれば複数:
  - 余白
  - 色
  - カード密度
  - DB感
  - lock / gated information 感
  - YouTube 解説感
  - ニュース図解感

画像の出所や権利が不明な場合も、抽出するのは構図原理だけに限定する。画像名、
URL、人物・組織・個人情報、記事本文、private data は成果物に入れない。

## 抽出ルール

1. 画像を `copy target` ではなく `principle source` として読む。
2. 各画像から次を短く抽出する:
   - frame density: sparse / balanced / dense
   - negative space: title / side / bottom / center のどこに余白があるか
   - hierarchy: focal、supporting、boundary、label の優先順位
   - color hierarchy: background、panel、accent、warning の階層
   - eye path: 視線がどこからどこへ動くか
   - UI feel: dashboard / database / editorial card / warning panel / search UI など
3. 抽出結果をそのまま画面に再現せず、SCS の 5 composition type
   (`split`, `center-focal`, `chain`, `reveal`, `mediator`) に写像する。
4. G-27 由来の失敗例は、`indexed_whiteboard`、`shape_size_mode_invalid`、
   `drawing_semantics_calibration` を避けるチェックとして使う。

## 出力 artifact contract

初回は text/JSON-ready な設計 artifact までに留める。

- reference style brief:
  - source image count
  - extracted principles
  - rejected copy-like details
  - copyright / privacy handling note
- SCS mapping:
  - selected composition type
  - visual role allocation
  - text budget
  - safe area / subtitle clearance note
  - expected anti-pattern checks
- generic carrier archetype:
  - carrier purpose
  - frame grid
  - item/group naming pattern
  - patch-allowed fields
  - patch-forbidden fields
- variant plan:
  - first pilot theme candidates
  - theme-specific motif slots
  - what must remain generic

## YMM4 handoff boundary

Assistant may prepare the design artifact, item naming proposal, group structure
proposal, readback checklist, and SCS mapping. Human/YMM4 remains responsible
for native carrier authoring, material registration, final layout judgement, and
creative acceptance. Adapter work starts only after an approved YMM4-saved
carrier or an explicit scoped implementation slice exists.

## First pilot candidates

- Real Estate DX information asymmetry as a retained G-27 reference case.
- Newsroom-produced explainer packet that needs a database / gated-information
  screen.
- Existing pipeline smoke topics where the visual problem is not character
  acting but a readable screen carrier.

These are pilot candidates, not implementation approvals. G-28 remains
`proposed` until the registry status is explicitly changed.
