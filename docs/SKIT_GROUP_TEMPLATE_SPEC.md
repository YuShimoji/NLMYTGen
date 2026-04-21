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

上記 2 件は user report により standalone native template library export まで完了。次の拡張順は `nod` → `deny_oneshot` → `exit_left` を既定とする。

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
- その後に派生テンプレート 6〜8 件へ拡張
- template registry 台帳
- 「自動生成で触れた箇所 / 手動確認が必要な箇所」の注記

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

### 4.3 本番で主軸にしないもの

- `motion` の direct write 拡張
- ImageItem への任意 `VideoEffects` 直書きの量産依存
- テスト追加だけで production value path を説明したつもりになること

---

## 5. IR との関係

本仕様は **「IR から何でも直接書く」路線ではない**。

IR 側の責務は次の順にする。

1. まず高水準の演出意図を出す
2. その意図を template registry に解決する
3. `intent_fallbacks` にあれば fallback template を返す
4. それも無ければ manual note を返す

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

この registry は **patch-time resolver ではない**が、`audit-skit-group` / `patch-ymmp --skit-group-registry` / `apply-production --skit-group-registry` の **preflight 入力**として使う。
先に canonical anchor / exact / fallback / manual note の成立可否を機械判定し、その後で必要なら resolver 実装へ広げる。

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
2. 小演出テンプレートを 6〜8 件量産する
3. registry 台帳を埋める
4. production では template 解決 + fallback note を返す

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
