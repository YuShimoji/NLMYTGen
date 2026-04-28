# Skit Group Template Spec

> **目的**: 配達員・消防員・アイドル等の **外部素材ベースの茶番劇演者**を、`TachieItem` の派生としてではなく **GroupItem テンプレート資産**として扱う。  
> **ねらい**: 開発段階では 1 つの canonical template から小演出を量産し、実制作では既存テンプレートの組み合わせで全体演出を組み立てる。IR から直接任意エフェクトを書き込むことを主軸にしない。

---

## 1. この仕様が直す混同

現行 repo では次の 3 つが混ざりやすい。

1. **speaker_tachie**
   - 解説役のゆっくり立ち絵 (`TachieItem` / 連番アニメ + TachieFaceParameter)
   - `face` / `idle_face` / `slot` / `motion` の主対象
   - 既存の「ゆっくり霊夢 / ゆっくり魔理沙」等を**そのまま流用**。新規立ち絵セットアップ(AnimationTachieプラグイン設定・パーツ分解・表情マッピング)は禁止

2. **skit_group**
   - 配達員などの外部人物素材を束ねた **GroupItem テンプレート**
   - 配下は **全て `ImageItem` の 1 枚画像重ね合わせ** (body / 顔 / 装飾)
   - `TachieItem` は配下に**含めない**。連番アニメ / TachieFaceParameter / パーツ分解は使わない
   - 本仕様の主対象

3. **overlay_render**
   - YMM4 で書き出した透過 PNG を `overlay_map` で使う補助経路
   - 背景キャラや一枚絵補助に使うが、主軸ではない

**固定ルール**:

- `TachieItem` は **解説役のゆっくり立ち絵専用**。外部茶番劇演者には使わない
- 外部茶番劇演者の body / 顔 / 装飾は **すべて `ImageItem` (1 枚画像)** で構成する
- 顔の感情差し替えは「顔 `ImageItem` の Source パスを差し替える」運用 (TachieFaceParameter は使わない)
- `motion` は **speaker_tachie の motion** として扱う
- 配達員等の茶番劇演者は **skit_group template** で扱う
- `group_motion` は **skit_group の幾何補助**であり、感情モーションの主表現ではない

**背景**:

立ち絵 (連番アニメ TachieItem) を新規セットアップするコストが過大なため、外部演者では採用しない決定が既に固定されている。配達員・消防員等の茶番劇演者は「body + 顔」の 2 枚画像重ね合わせで十分であり、感情表現は顔画像の差し替えで吸収する。

---

## 2. 現行コードの事実

### 2.1 できること

- `motion` Phase2 / G-17:
  - `TachieItem.VideoEffects`
- `bg_anim`:
  - Layer 0 背景の `X/Y/Zoom` または `VideoEffects`
- `group_motion`:
  - `GroupItem.X/Y/Zoom`

### 2.2 できないこと

- 任意 Layer の ImageItem に対する汎用 `VideoEffects` 自動適用
- 茶番劇演者の body/head を直接対象にした `motion` 解決
- 1 つの GroupItem に時系列で複数の感情モーションを安全に積むこと

したがって、**茶番劇演者の主経路は「テンプレート解決」**であり、任意 item への direct write 拡張ではない。

---

## 3. 開発段階の主経路

### 3.1 目的

- 1 つの canonical template を起点に、再利用可能な小演出テンプレートを量産する
- 量産物は「JSON の数値台帳」ではなく **YMM4 native template 資産**として蓄積する

### 3.2 canonical template

最初に 1 つだけ、以下を満たす GroupItem テンプレートを作る。

- `GroupItem` に安定した `Remark` を付ける
- 配下構成は **body `ImageItem` + 顔 `ImageItem` + (任意で装飾 `ImageItem`)** の重ね合わせ
- `TachieItem` は配下に含めない (解説役専用、§1 固定ルール)
- 基準点は中央
- 配下アイテムは相対配置
- 長さ・初期座標・初期倍率を基準化する

**具体構成例 (haitatsuin)**:

| 配下アイテム | 型 | 実体 | 備考 |
|---|---|---|---|
| body | `ImageItem` | 配達員イラスト (例: Layer 10 相当) | 1 枚画像。複数ポーズが必要なら別テンプレで分岐 |
| 顔 | `ImageItem` | `reimu_easy.png` 等の 1 枚顔画像 | 感情差し替えは Source パス置換で対応 |
| 装飾 | `ImageItem` | 荷物 / 矢印 / エフェクト素材 | 省略可。案件ごとに足す |

### 3.3 小演出の量産

canonical template から次のような小演出を派生テンプレートとして作る。

**skit_01 proof で実証済み** (library motion 名。registry は `skit_group_registry.template.json`):

- `enter_from_left` — 登場 (横接近→着地 one-shot)
- `surprise_oneshot` — 驚き (Y 軸のみ one-shot)
- `deny_oneshot` — 否定 (X 軸のみ one-shot)
- `exit_left` — 退場 (InOutMove OUT)
- `nod` — 会釈 (RepeatMove、短尺)

**2026-04-21 starter batch（初回 authoring 固定範囲）:**

- `enter_from_left`
- `surprise_oneshot`
- 上記 2 件を **user-owned native template authoring の初回対象** とする
- `deny_oneshot` / `exit_left` / `nod` は registry catalog と canonical corpus 上の preflight exact を維持するが、starter batch 完了扱いには含めない

**2026-04-21 cautious gate（standalone export 前提条件）:**

1. `samples/canonical.ymmp` 内 starter copy 2 件の **manual acceptance** を閉じる
2. `enter_from_left` / `surprise_oneshot` の両方を含む **1 件の production adoption proof** を閉じる
3. 上記 2 段が PASS のときだけ standalone native template library export に進む
4. `motion_target` / `group_motion` を starter 2 件の代替に使った場合は **template-first 未成立** として standalone export をブロックする
5. 受入済みでも、canonical anchor を持つ voice-anchored production ymmp が無い間は canonical-project copy 運用を継続する

**2026-04-21 export sync:**

- `delivery_enter_from_left_v1`
- `delivery_surprise_oneshot_v1`

上記 2 件は user report により standalone native template library export まで完了。

**2026-04-27 `nod` export sync:**

- `delivery_nod_v1`

`delivery_nod_v1` は user report により GroupItem template として保存済み。body / face の 2 `ImageItem` が一緒に動き、nod は見えるが支配的ではなく、`TachieItem` 混入なし。`skit_group.intent.nod` は `direct_proven` へ昇格済み。

**2026-04-27 v1 planned set completion sync:**

- `delivery_deny_oneshot_v1`
- `delivery_exit_left_v1`

User completed the remaining 2 samples. Repo inspection of `samples/haitatsuin_2026-04-12_g24_proof.ymmp` confirmed body + face are plain `ImageItem` children, target motion is held by Layer 9 `GroupItem` snippets with matching Remarks, and `TachieItem` count is 0. `delivery_deny_oneshot_v1` is represented as a short X-axis one-shot sway; `delivery_exit_left_v1` uses an OUT `InOutMoveEffect` toward left. `skit_group.intent.deny_oneshot` and `skit_group.intent.exit_left` are now `direct_proven`.

Note: the repo-tracked proof `.ymmp` is now a compact template/sample proof, not the earlier voice-anchored adoption corpus. Production-use validation should use `samples/canonical.ymmp` + real/probe IR for template resolution, then only create new motions if a concrete production gap appears.

**未実証・将来候補** (skit_02 以降で起票):

- `happy_sway`
- `sad_droop`
- `thinking_zoom`
- `nod_oneshot` (ループしない会釈)
- `reset_center`

ここでの自動化対象は **テンプレート派生の叩き台作成**であり、任意案件へ直接焼くことではない。

### 3.4 開発段階の成果物

- canonical template 1 件
- 初回スターターバッチ 2 件（`enter_from_left` / `surprise_oneshot`）
- manual acceptance + 1 件の production adoption proof + standalone export
- 現行 v1 の planned author/export 5 件は完了済み
- template registry 台帳
- 「自動生成で触れた箇所 / 手動確認が必要な箇所」の注記

### 3.5 ループ停止条件

小演出テンプレート author/export は、動きの数を増やすこと自体を目的にしない。

- v1 planned set は `enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left` の 5 件で一旦止める
- 5 件が閉じたので、次は新規 motion 作成ではなく **実制作 IR で template 解決が手作業を減らすか**を見る
- `happy_sway` / `sad_droop` / `thinking_zoom` / `nod_oneshot` / `reset_center` は、実制作で exact / fallback / manual note の不足が出た時だけ再起票する
- 「それらしい動きをさらに作る」は、具体的な production gap がない限り G-24 の次 frontier にしない

### 3.6 役割分担

G-24 は user が全サンプルを手作りする運用ではない。

- user: 少数の reusable YMM4 native GroupItem template を author/export し、見え方の PASS / FAIL を判断する
- assistant: registry / audit / Capability Atlas を同期し、既存テンプレートの組み合わせと fallback / manual note で production-like sample を組み立てる
- user: assistant が組み立てた sample / 解決結果を YMM4 上で確認し、template 不足や違和感だけを返す
- 追加テンプレート作成は、この確認で concrete production gap が出た時にだけ再開する

---

## 4. 実制作の主経路

### 4.1 方針

本番では IR の要求を **まず template 解決**する。

1. exact template がある
   - そのまま採用
2. exact template がないが近い演出がある
   - fallback template を採用
   - 差分を注記
3. 汎用テンプレートで吸収できない
   - 未自動化として注記
   - 手動確認ポイントを明記

重要: template 解決は、operator に named template を選ばせるための手順票ではない。現段階の主経路は、IR / registry / repo-tracked `.ymmp` template source を `patch-ymmp --skit-group-template-source --skit-group-only` へ渡し、YMM4 で作った GroupItem template を対象発話の timeline に自動挿入することである。`audit-skit-group` は read-only の補助診断に降格する。

### 4.2 自動生成側が返すべきもの

- 採用 template 名
- fallback の有無
- 未自動化理由
- 手動確認ポイント

例:

- `requested: surprise_oneshot`
- `resolved: delivery_surprise_oneshot_v1`
- `resolution: exact`
- `manual_checks: Y-axis only jump height, one-shot (no loop)`

または

- `requested: collapse_then_runaway`
- `resolved: delivery_surprise_oneshot_v1`
- `resolution: fallback (via intent_fallbacks)`
- `note: multi-stage acting is not covered by current template set`
- `manual_checks: second beat transition, exit timing`

2026-04-27 時点の production-like alias:

- `surprise_jump` -> `delivery_surprise_oneshot_v1`
- `deny_shake` -> `delivery_deny_oneshot_v1`
- `panic_shake` は通常の Writer IR 語彙に含めず、必要なら自然文メモ側の新テンプレ候補として扱う

2026-04-27 時点の IR 生成フロー反映:

- skit_group actor 用 utterance は `motion_target: "layer:9"` を必須にする
- `motion` は v1 intent（`enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left`）または alias intent（`surprise_jump` / `deny_shake`）を使う
- `panic_shake` など未登録 label は `validate-ir --strict-skit-group-intents` で止め、Part 2 JSON には出さない
- 最小入力形は `samples/g24_skit_group_minimal_production_ir.json`

### 4.3 本番で主軸にしないもの

- `motion` の direct write 拡張
- ImageItem への任意 `VideoEffects` 直書きの量産依存
- テスト追加だけで production value path を説明したつもりになること

---

## 5. IR との関係

本仕様は **「IR から何でも直接書く」路線ではない**。

IR 側の責務は次の順にする。

1. まず高水準の演出意図を出す
2. skit_group actor 用発話なら `motion_target: "layer:9"` を入れ、既存 v1 intent または登録済み alias intent を `motion` に置く
3. その意図を template registry に解決する
4. `intent_fallbacks` にあれば fallback template を返す
5. それも無ければ manual note を返す

このため、将来 IR を拡張する場合も **raw effect の列挙ではなく template 解決を先に置く**。

---

## 6. template registry の最小形

`samples/registry_template/skit_group_registry.template.json` を最小雛形とする。

記録するもの:

- canonical group 名
- GroupItem の `Remark`
- template 名
- 目的 (`intent`)
- `intent_fallbacks`
- manual check
- 適用対象 (`speaker_tachie` / `skit_group` / `overlay_render`)

この registry は GroupItem 本体を埋め込まない。GroupItem 本体は repo-tracked `.ymmp` template source に置き、registry は intent / fallback / template_name の解決表として `patch-ymmp --skit-group-registry --skit-group-template-source --skit-group-only` の patch-time resolver に渡す。
`audit-skit-group` は canonical anchor / exact / fallback / manual note の read-only 確認に限り使う。

---

## 7. 旧 G 系の位置づけ

### G-20

- 残す
- 役割は **GroupItem geometry helper**
- 茶番劇の主経路ではなく、テンプレートの微調整補助

### G-21

- 旧「body_map / ImageItem 挿入」案は主軸から外す
- template-first で吸収できないときだけ再開する

### G-22

- dual-rendering は補助経路
- `overlay_render` の実務補助としては有効
- ただし skit_group の主仕様ではない

### G-23

- motion preset library は `motion_target` 経由で ImageItem/GroupItem にも補助的に適用可
- ただし茶番劇の**主経路は canonical template**。library は主経路にしない

---

## 8. 推奨対応

### 8.1 直近の正規 frontier

1. canonical skit_group template を 1 件固定する
2. v1 planned set（`enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left`）を閉じる（完了）
3. registry / Capability Atlas を `direct_proven` へ同期する（完了）
4. production-like alias を登録する（`surprise_jump` / `deny_shake` は完了、`panic_shake` は manual/new-template）
5. production では template 解決 + fallback を `.ymmp` timeline へ自動配置し、manual note ではなく write capability の成立で評価する
6. 追加 motion は production gap が出た時だけ再起票する

実制作 IR 生成時の固定導線:

```bash
python -m src.cli.main validate-ir \
  <production_skit_group_ir.json> \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --strict-skit-group-intents \
  --format text

python -m src.cli.main patch-ymmp \
  samples/_probe/g24/real_estate_dx_csv_import_base.ymmp \
  samples/_probe/g24/real_estate_dx_skit_group_ir_aligned.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --skit-group-template-source samples/templates/skit_group/delivery_v1_templates.ymmp \
  --skit-group-only \
  -o samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp
```

`exact` / `fallback` は自動配置対象、未登録 label は strict validation で停止する。real estate DX スライスでは YMM4 CSV 読込後に長文が複数 VoiceItem へ分割されるため、`real_estate_dx_skit_group_ir_aligned.json` の `row_start` / `row_end` を placement anchor として使う。template source 欠落は `SKIT_TEMPLATE_SOURCE_MISSING` として fail-fast し、operator 手順で補完しない。

template source 内で複数テンプレートが同一 frame/layer に重なる場合、GroupItem と同じ `Remark` を持つ ImageItem だけを同一 clip として扱う。古い絶対パス等で ImageItem の `FilePath` が repo-local asset に解決できない場合は `SKIT_TEMPLATE_SOURCE_ASSET_MISSING` として fail-fast する。

2026-04-28 以後の placement は raw clone ではなく template-analyzed placement とする。`patch-ymmp` / `apply-production` は repo-tracked template source の GroupItem 群から rest pose を中央値で導出し、各 template の `X` / `Y` / `Zoom` を template-local baseline から rest pose へ平行移動して配置する。これにより authoring 用の外側座標を production timeline へそのまま持ち込まず、`surprise_oneshot` の Y ジャンプや `deny_oneshot` の X 揺れなどの相対 delta は維持する。数値 transform を導出できない場合は `SKIT_TEMPLATE_ANALYSIS_INSUFFICIENT` で fail-fast する。

YMM4 での確認は production timing artifact と compact review artifact を分ける。production artifact は実発話 frame へ配置するため演出が動画全体に散る。visual acceptance では `--skit-group-compact-review` を使い、同じ IR / registry / template source から skit_group cue だけを短い間隔で並べた `samples/_probe/g24/real_estate_dx_skit_group_compact_review.ymmp` を見る。ImageItem の `FilePath` は YMM4 が読める Windows path として書き出し、WSL の `/mnt/c/...` path を production artifact に混入させない。

### 8.2 やらないこと

- `motion` の意味を広げて配達員演者まで含める
- GroupItem / ImageItem / TachieItem を同一 feature として扱う
- **外部茶番劇演者の配下に `TachieItem` (連番アニメ / TachieFaceParameter) を入れる**
- 外部演者のために新規立ち絵セットアップ (AnimationTachie プラグイン設定 / パーツ分解) を行う
- 顔の感情差し替えを `TachieFaceParameter` で実装する (ImageItem の Source パス差し替えで吸収)
- route contract や unit test の成立だけで production readiness とみなす

---

## 9. 成功条件

- 茶番劇演者が `speaker_tachie` と明確に分離される
- 開発段階で 1 canonical → 複数小演出の量産が回る
- 本番で「exact / fallback / manual note」を返せる
- 古い G 系の提案が、主軸でないのに次の実装を支配しない
