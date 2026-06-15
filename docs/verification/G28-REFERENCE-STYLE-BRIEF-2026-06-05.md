# G-28 Reference Style Brief — 2026-06-05

G-28 `Reference-Driven Generic Screen Carrier` の初回参照画像入力から、
画面文法だけを抽出した design artifact。

この文書は reference image の複製、素材化、URL 記録、production asset 化ではない。
画像は `principle source` としてのみ扱い、YMM4 `.ymmp` 生成、render、
production timing、creative final acceptance には進まない。

## Scope

- source image count: 7
- input visibility: visible in this terminal
- image handling: no image binary, image path, image URL, or raw reference file is committed
- output type: docs-only / design-artifact-only
- active lane: G-28 reference-driven generic screen carrier extraction
- retained boundary: G-27 is evidence only, not the active blocker

## Extraction Lens

抽出対象は「何を真似るか」ではなく「何を carrier 設計へ移すか」に限定する。

- composition: focal の置き方、上下左右の領域分割、host / evidence / subtitle の関係
- density: 情報量を subject に合わせて調整する幅
- negative space: 読み順を作る余白、caption safe area を守る余白
- color hierarchy: 背景、証拠面、強調、字幕帯の階層
- eye path: title / evidence / callout / subtitle の順路
- UI feel: source footage、map evidence、lecture diagram、conversation board の違い
- cut grammar: 数秒単位で切り替える画面と、長めに読ませる画面の分離

## Per-Image Extraction

### Ref-01: dense lecture constants

- composition type: lecture diagram / dense fact stack; SCS では `chain` または
  `center-focal` に寄せる。
- focal element: 中央上部の概念リスト。icon + label + value の行単位が主役。
- supporting element: 暗い高精細背景、左右下の host、下部字幕。
- boundary / subtitle band: 画面下 18-22% 相当を灰色の字幕帯として明確に分離。
- information density: dense。ただし行の単位が揃っているため読める。
- negative space: 中央リストの左右と下部 host 周辺に小さな抜けがある。
- eye path: 上から下のリスト走査 -> 右側の数値 -> 下部字幕の結論。
- color / contrast hierarchy: dark background、white main text、light icon、
  green subtitle。accent は字幕色に寄せている。
- host character usage: lower corners only。主役ではなく会話の anchor。
- likely use-case: 科学 / 抽象概念 / 比較値 / 確率や倍率の説明。
- avoid-notes: exact icon/value layout のコピー、行数過多、host 主役化、
  subtitle band と main label の衝突。

### Ref-02: source footage with minimal overlay

- composition type: source-footage carrier; SCS では `center-focal`。
- focal element: 中央の gameplay / source footage frame。
- supporting element: 上部章タイトル、白枠、下部字幕、元 footage 内 HUD。
- boundary / subtitle band: footage の下端付近に字幕を重ねるが、白枠で主画面を保持。
- information density: source-defined high。追加 overlay は少ない。
- negative space: 余白は少ない。元映像の空間を壊さないことが前提。
- eye path: 上部章タイトル -> footage の action center -> HUD -> 下部字幕。
- color / contrast hierarchy: 元 footage の色を主階層にし、subtitle は yellow / black
  outline で読みを確保。
- host character usage: none。素材が強い時は host を足さない。
- likely use-case: ゲームレビュー、画面操作説明、不動産内見画面、GUI 操作解説。
- avoid-notes: source が強いのに図解を追加しすぎること、HUD を隠す字幕、
  frame 外の背景を主役化すること。

### Ref-03: conversation board buffer

- composition type: conversation / buffer carrier; SCS では `mediator` または
  `center-focal`。
- focal element: 中央の黒板 / board と単純な図。
- supporting element: 左右 host、木目の机 / 下部字幕帯。
- boundary / subtitle band: board frame と bottom band が強く、main canvas と字幕が分離。
- information density: sparse to balanced。会話の間を持たせる低コスト carrier。
- negative space: board 内の背景、host 周辺、字幕帯上部に余白。
- eye path: board illustration -> host reaction -> bottom subtitle。
- color / contrast hierarchy: dark outer background、green board、simple figure colors、
  blue subtitle。
- host character usage: strong but still supporting。会話の温度を持たせる。
- likely use-case: 雑学会話、補足、topic transition、dense evidence の前後の休符。
- avoid-notes: evidence claim の主画面として使いすぎること、board を細かい
  indexed whiteboard にすること、host が focal を奪うこと。

### Ref-04: dense table over evidence background

- composition type: tabular evidence mode inside Map / Evidence Carrier; SCS では
  `center-focal` with pre-authored evidence surface。
- focal element: 中央の multi-column table / list。
- supporting element: 暗い地図調背景、上部タイトル、下部 red comment band。
- boundary / subtitle band: red / gold bottom band が thesis caption として機能。
- information density: very dense。表自体を evidence surface として読ませる。
- negative space: 余白は少ない。列揃えと背景の低コントラストで整理している。
- eye path: title -> left column -> person / origin columns -> bottom thesis。
- color / contrast hierarchy: muted dark background、white list text、red bottom band、
  yellow subtitle。
- host character usage: none。表と thesis が主役。
- likely use-case: 人物リスト、企業リスト、比較表、出身地 / 業界構造の提示。
- avoid-notes: 小さすぎる文字、列数増加、source line を読ませたい位置へ置くこと、
  adapter patch text を表全体へ増やすこと。

### Ref-05: map evidence with callouts

- composition type: map / evidence carrier; SCS では `center-focal`、地域比較時は
  `split`。
- focal element: 日本地図の satellite / night-light surface。
- supporting element: callout labels、source note、bottom thesis band。
- boundary / subtitle band: bottom red band が map と thesis を分離。
- information density: balanced-dense。map surface は高密度だが callout 数で制御。
- negative space: 海域と map 外周が label の逃げ場になる。
- eye path: title -> map center -> regional callouts -> bottom thesis。
- color / contrast hierarchy: dark map、white labels / leader lines、red bottom band、
  yellow thesis。
- host character usage: none。地図が証拠面。
- likely use-case: 地理、産業立地、人口圏、物流、商圏、地域比較。
- avoid-notes: map label 過密、caption safe area 侵入、source note を過度に大きくすること、
  map を装飾背景として扱うこと。

### Ref-06: two-panel mechanism diagram

- composition type: lecture diagram / mechanism contrast; SCS では `split` または `chain`。
- focal element: 左右の device diagram と arrow relation。
- supporting element: 上部の question / answer pair、host、blurred stage background。
- boundary / subtitle band: bottom gray subtitle band。main diagram はその上で完結。
- information density: balanced。2 idea + 2 arrows + 2 devices 程度に制限。
- negative space: 中央左右の空間、device 周囲、blurred background。
- eye path: top question pair -> arrow / answer -> left device -> right device ->
  bottom explanation。
- color / contrast hierarchy: dark interior background、white / yellow text、
  yellow particles / arrows、green subtitle。
- host character usage: lower corners。抽象概念の語り手 anchor。
- likely use-case: 科学の誤解訂正、before/after、因果の可視化、仕組み説明。
- avoid-notes: arrow 連打、question / answer の文字量増加、device を 3 個以上にすること、
  subtitle と下側 device の衝突。

### Ref-07: satellite map with dense label network

- composition type: map / evidence carrier with cluster-label mode; SCS では
  `center-focal`、cluster relation を語る場合は `chain`。
- focal element: satellite map + point cluster + leader-line labels。
- supporting element: title、large labels、bottom thesis band、minimal player UI residue to ignore。
- boundary / subtitle band: bottom red band が thesis を固定。player chrome は carrier 要素にしない。
- information density: very dense but evidence-surface driven。
- negative space: ocean side and terrain areas provide label relief。
- eye path: title -> large company/place labels -> point cluster -> bottom thesis。
- color / contrast hierarchy: natural satellite color、white labels、yellow points、
  red / gold bottom band。
- host character usage: none。map/evidence が主役。
- likely use-case: 産業集積、地理的近接、企業ネットワーク、都市圏の説明。
- avoid-notes: exact label network の複製、ブランド/固有名の羅列過多、動画 player UI の
  carrier 化、bottom band と map callout の衝突。

## Shared Screen Grammar

- 主役は host ではなく、説明対象の evidence surface / diagram / source footage。
- bottom 18-22% は subtitle / thesis band として予約し、main evidence を侵入させない。
- top band は chapter / claim anchor に使い、長文説明を置かない。
- host は lower left / lower right の emotional anchor に留める。source footage や map
  evidence が強い画面では省く。
- 高密度画面は「map surface / table surface」として人間が pre-authored する。
  adapter が小ラベルを大量 patch する carrier にはしない。
- 図解画面は focal 1 個または pair 1 組を中心にし、supporting は 3 個程度まで。
- dense evidence と conversation buffer を数秒単位で切り替え、毎 frame を同じ密度にしない。
- 色階層は background -> evidence / panel -> accent -> subtitle の 4 層以内に抑える。
- 元素材が強い場合は、border / top title / subtitle / small emphasis marker だけで成立させる。
- `indexed whiteboard` は避ける。カードを等価に並べるのではなく、focal / supporting /
  boundary / connector を明示する。

## Generic Carrier Archetypes

### 1. Lecture Diagram Carrier

- primary use: 科学、抽象概念、因果、誤解訂正、before/after。
- SCS composition type: `center-focal`, `chain`, `split`, or `reveal`。
- frame regions:
  - `G28_LDC_TitleBand`: one-line claim
  - `G28_LDC_Background`: high-contrast but low-salience stage
  - `G28_LDC_DiagramGroup`: focal diagram / paired device / node chain
  - `G28_LDC_HostLeft` / `G28_LDC_HostRight`: optional lower-corner hosts
  - `G28_LDC_CaptionReserve`: bottom 18-22% no main item placement
- subtitle handling: gray or transparent band, YMM4 caption kept clear.
- character handling: optional; lower corners only, not focal.
- density ceiling: focal 1 or split focal 2, supporting <= 3, connector <= 2,
  in-frame labels <= 2 / 30 chars.
- suitable topics: mass/energy, nuclear/chemical reactions, AI mechanism,
  market mechanism, cause/effect。
- unsuitable topics: dense source footage, long tables, map-heavy evidence。
- YMM4 item / group proposal:
  - `G28_LDC_Root`
  - `G28_LDC_Title_Text`
  - `G28_LDC_Stage_ImageOrShape`
  - `G28_LDC_Focal_Group`
  - `G28_LDC_Node_A`, `G28_LDC_Node_B`, `G28_LDC_Node_C`
  - `G28_LDC_Connector_1`, `G28_LDC_Connector_2`
  - `G28_LDC_Host_Left`, `G28_LDC_Host_Right`
  - `G28_LDC_CaptionReserve_Guide`

### 2. Map / Evidence Carrier

- primary use: 地図、衛星画像、統計 callout、産業立地、地域比較。
- SCS composition type: `center-focal`, `split`, or `chain`。
- frame regions:
  - `G28_MEC_TitleBand`: topic / region / evidence claim
  - `G28_MEC_EvidenceSurface`: pre-authored map / table / satellite surface
  - `G28_MEC_CalloutGroup`: limited callout slots
  - `G28_MEC_SourceNote`: small provenance note when needed
  - `G28_MEC_ThesisBand`: bottom thesis / caption reserve
- subtitle handling: red / dark thesis band may coexist with YMM4 caption,
  but map labels must not enter caption safe area.
- character handling: default none.
- density ceiling: map/table texture may be visually dense, but patchable callouts
  should stay <= 6 and focal should remain one evidence surface.
- suitable topics: geography, population, industrial clusters, logistics,
  real-estate area explanation, company-location relation。
- unsuitable topics: emotional dialogue, detailed mechanism steps, live source footage。
- YMM4 item / group proposal:
  - `G28_MEC_Root`
  - `G28_MEC_Title_Text`
  - `G28_MEC_EvidenceSurface_Image`
  - `G28_MEC_Callout_1` ... `G28_MEC_Callout_6`
  - `G28_MEC_LeaderLine_1` ... `G28_MEC_LeaderLine_6`
  - `G28_MEC_SourceNote_Text`
  - `G28_MEC_ThesisBand_Group`

### 3. Source-Footage Carrier

- primary use: ゲーム画面、物件映像、GUI 操作、既存 footage が強い説明。
- SCS composition type: `center-focal` or `reveal`。
- frame regions:
  - `G28_SFC_TopChapter`: short chapter label
  - `G28_SFC_FootageFrame`: source image/video surface
  - `G28_SFC_Border`: optional boundary
  - `G28_SFC_EmphasisMarker`: optional small marker
  - `G28_SFC_CaptionReserve`: bottom caption safe area
- subtitle handling: subtitle can overlap the bottom edge only when HUD / important
  source text is not hidden; otherwise use reserved lower band.
- character handling: default none. Add host only in separate reaction cut.
- density ceiling: no additional diagrams unless the footage itself is paused /
  zoomed for explanation.
- suitable topics: game review, UI walkthrough, property tour, screen comparison,
  source video commentary。
- unsuitable topics: abstract mechanism without visual source, map/stat evidence。
- YMM4 item / group proposal:
  - `G28_SFC_Root`
  - `G28_SFC_TopChapter_Text`
  - `G28_SFC_Footage_ImageOrVideo`
  - `G28_SFC_FrameBorder_Shape`
  - `G28_SFC_EmphasisMarker_Group`
  - `G28_SFC_CaptionReserve_Guide`

### 4. Conversation / Buffer Carrier

- primary use: 会話、反応、補足、dense evidence 間の休符、低コスト transition。
- SCS composition type: `mediator` or `center-focal`。
- frame regions:
  - `G28_CBC_Board`: board / simple diagram surface
  - `G28_CBC_HostLeft` / `G28_CBC_HostRight`: dialogue anchors
  - `G28_CBC_DeskOrLowerBand`: visual boundary
  - `G28_CBC_CaptionReserve`: subtitle safe area
- subtitle handling: large readable subtitle; board text is minimal.
- character handling: hosts are stronger than other archetypes but still supporting.
- density ceiling: board visual 1, labels <= 1-2, no evidence table.
- suitable topics: 雑学会話、間の説明、視聴者向け問いかけ、章転換。
- unsuitable topics: proof-heavy claim, numerical comparison, detailed map/stat evidence。
- YMM4 item / group proposal:
  - `G28_CBC_Root`
  - `G28_CBC_Background_ImageOrShape`
  - `G28_CBC_Board_Group`
  - `G28_CBC_BoardVisual_ImageOrShape`
  - `G28_CBC_Host_Left`, `G28_CBC_Host_Right`
  - `G28_CBC_LowerBand_Shape`
  - `G28_CBC_CaptionReserve_Guide`

## SCS Mapping

| Archetype | Default SCS type | Visual role allocation | Text budget | Safe area rule | Anti-pattern checks |
|-----------|------------------|------------------------|-------------|----------------|---------------------|
| Lecture Diagram Carrier | `center-focal` / `chain` | focal diagram, supporting nodes, connector, optional hosts | labels <= 2, chars <= 30 | bottom 18-22% reserved | `indexed_whiteboard`, `ELEMENT_COUNT_OUT_OF_RANGE`, arrow overload |
| Map / Evidence Carrier | `center-focal` / `split` | evidence surface as focal, callouts as supporting, thesis band as boundary | patch labels <= 2; pre-authored evidence labels bounded by human review | map/callouts stay above caption band | label overload, map-as-decoration, source-note dominance |
| Source-Footage Carrier | `center-focal` | footage as focal, top chapter as label, optional marker as supporting | top label only plus subtitle | do not cover HUD/source-critical area | diagram-over-source, HUD collision, decorative border dominance |
| Conversation / Buffer Carrier | `mediator` / `center-focal` | board as focal, hosts as supporting/mediator | board labels <= 1-2 | subtitle band separate from board | host-as-focal, board whiteboard overload, evidence claim without evidence |

## Genre Application Notes

### Science / abstract concepts

- default: Lecture Diagram Carrier。
- use high-contrast, low-salience background to make abstract objects readable.
- represent mechanism with 2-3 nodes, arrows, and one conclusion, not a full list every time.
- host should provide narration warmth, not compete with the diagram.

### Geography / statistics / industrial location

- default: Map / Evidence Carrier。
- make map or table a pre-authored evidence surface; patch only thesis and a small
  number of callouts.
- use bottom thesis band for the conclusion and keep source note subordinate.
- high density is allowed only when the evidence surface itself carries it.

### Real estate

- default: Source-Footage Carrier for property / portal / DB screenshots,
  Map / Evidence Carrier for area and access logic, Lecture Diagram Carrier for
  gated-information mechanism.
- keep G-27 diagnostic evidence as reference only; do not revive its carrier blocker.
- if source screen is strong, use top chapter + border + subtitle, not new diagrams.

### Game review / game explainer

- default: Source-Footage Carrier。
- let footage carry action and credibility; overlays should name the point, not
  explain the whole system at once.
- use pause/zoom cuts for explanation and separate Conversation / Buffer cuts for reactions.

### Trivia / conversation / buffer

- default: Conversation / Buffer Carrier。
- useful for short transition, joke, question, or low-density explanation.
- avoid using it as evidence for claims that need map, footage, or data surface.
- switch every few seconds when the topic has no strong evidence surface.

## Failure Modes To Avoid

- indexed whiteboard: equal-weight cards / bullets without focal hierarchy
- information overload: too many labels, arrows, callouts, or table columns
- host character dominance: host becomes the visual point instead of the topic
- subtitle collision: main evidence or labels enter the bottom caption safe area
- source over-decoration: strong game / property / GUI footage gets buried under diagrams
- map-as-wallpaper: geographic evidence becomes background decoration instead of proof
- adapter-overpatching: carrier depends on patching many tiny labels instead of using
  a human-authored evidence surface

## Next Frontier

This slice removes G-28 input-wait and creates the first extraction artifact.
The next valid G-28 work is refinement from this brief into one of:

- `shot_layout_plan`-ready SCS mapping fields for the four archetypes
- a YMM4 human-author checklist for each generic carrier archetype
- a narrow readback checklist for caption clearance, focal count, label count,
  and element-count compliance
- one theme-specific variant plan that stays design-only until an explicit
  implementation slice is opened

Do not proceed from this brief directly to `.ymmp` generation, render,
production timing, creative final acceptance, G-27 diagnostic promotion, or
RSS / OPML / NotebookLM source-pack work.
