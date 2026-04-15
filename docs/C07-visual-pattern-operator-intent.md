# C-07 系・演出の「見た目」意図（オペレータ言語化・正本）

## 文脈

過去セッションで**画像付きの例**を提示し、言語化したが、そのメモがリポジトリに固定されておらず、後続開発（IR 語彙・`patch-ymmp` 際限・YMM4 手動範囲）で**意図が抜けうる**問題があった。  
本書は、そのとき合意に近かった**再現目標**を文章で正本化する。**画像ファイル自体は本 repo には含めない**（著作権・再配布の都合）。必要なら別ストレージや issue 添付で管理する。

## 再現を目指していたパターン（4 類）

以下は **字幕（台本読込のジムク）とは別レイヤー**の「画面上の情報・演出」を指す。NotebookLM 主台本とは切り離し、**解説ナレーション**と**作中の人物表現**も区別する。

### 1. 立ち絵＋フキダシ（心の声・せりふ・別系統の台詞）

- **見た目**: 人物の立ち絵に吹き出し。内容は「考えていること」「別路線のせりふ」「字幕に載せない台詞」など。
- **変則パターン（ゆっくり茶番劇）**: フリー素材の人物画（配達員・消防員・アイドル等）に、**ゆっくり頭を重畳**して同一キャラとして一貫して振る舞わせる。**実装寄せ先は [FEATURE_REGISTRY G-21](FEATURE_REGISTRY.md)**（外部素材 ImageItem + ゆっくり頭 TachieItem を GroupItem で束ねる方式）。**G-19（ゆっくり系 body_variant 束ね）とは別物**で、ゆっくり立ち絵自体には新しい body を足さない。顔の位置合わせは YMM4 上でテンプレ化し `body_map` で再利用する。  
  - **解説用の立ち絵**と**作中人物としての立ち絵**を用途で分ける（同じ画面レイヤーでも意味役割が違う）。

**IR / 語彙上の寄せどころ**

- `template`: **`skit`**（茶番劇・人物芝居）
- `overlay`: 吹き出し系ラベル（例: [PRODUCTION_IR_SPEC](PRODUCTION_IR_SPEC.md) の `speech_bubble` 等）。実体は registry / YMM4 テンプレで定義。
- `face` / `slot`: 表情・左右配置。顔差し替えは **palette / face_map のラベル設計**とセット。

**自動化の際限（現状）**

- 吹き出しの**中身テキスト**を IR で持つか、YMM4 上のみかは別途決める。Python は [PRODUCTION_IR_CAPABILITY_MATRIX](PRODUCTION_IR_CAPABILITY_MATRIX.md) のとおり **overlay 挿入まで（map 前提）**が機械範囲。  
- 「フリー素材体＋ゆっくり顔」の**見た目の一貫性**は **YMM4 テンプレ＋素材準備**が主。

---

### 2. リソースの列挙（所持品・属性・場面で揃っている情報）

- **見た目**: その時点の**登場人物の所持品**、**属性**、**場に出そろっている情報**などをリスト・カード状に列挙。**黒板形式**も含む。

**IR / 語彙上の寄せどころ**

- `template`: **`data`**（情報埋め込み）または **`board`**（黒板型の整理）
- `overlay` / 複数 `ImageItem`: 箇条書き・図枠（registry でラベル化）
- Macro の `consumer_hints` や Packaging brief 側の「今回の画面に出す根拠」と連携しうる（H-01 系）

---

### 3. 地図・位置関係・譲歩・整理（黒板スタイル含む）

- **見た目**: **地図上の位置関係**、**譲歩やトレードオフ**の整理を、黒板・図解レイアウトで見せる。

**IR / 語彙上の寄せどころ**

- `template`: **`data`**（図・位置関係）と **`board`**（整理・対比）の併用もありうる
- `bg`: `map_world` / `map_region` / `diagram` 等（[PRODUCTION_IR_SPEC](PRODUCTION_IR_SPEC.md) §3.3）
- 複雑な図は **YMM4 手動 or 外部ツールで画像化して overlay** になりやすい

---

### 4. 雰囲気のみのストック映像・静止画

- **見た目**: **説明の主役ではない**ストック動画・写真を全面に出し、**ムード**だけ載せる。

**IR / 語彙上の寄せどころ**

- `template`: **`mood`**
- `bg` + `bg_anim`（`bg_anim` は **セクション単位の ImageItem X/Y/Zoom プリセット**として [PRODUCTION_IR_CAPABILITY_MATRIX](PRODUCTION_IR_CAPABILITY_MATRIX.md) / G-14 で patch 可能）

---

## `template` 値との対応表（要約）

| オペレータ意図（本書） | `template`（C-07 v3） |
|------------------------|----------------------|
| 立ち絵・フキダシ・作中人物の一貫表現 | `skit` |
| 列挙・インベントリ・黒板リスト | `data` / `board` |
| 地図・関係・整理図 | `data` / `board` |
| 雰囲気のみのストック表示 | `mood` |

`intro` / `closing` は動画構成上の枠であり、上記 4 類の**置き換え**ではない。

## 量産・自動化の方針（2026-04 固定）

本書 §1〜4（吹き出し・列挙・地図整理・**雰囲気ストック**）は、**再現目標**として **YMM4 ネイティブテンプレ＋ Template Registry＋手微調整**を許容する。**雰囲気のみのストック映像・静止画**（`template: mood`）は素材選定と画面上の見せ方が主で、**完全自動化を最優先の約束にはしない**。

**それ以外**—本書に無い定型パターン、または **IR の意味ラベル＋ registry で表現できる差分**—については、**可能な限り L2（Python アダプタ＋ JSON registry）で自動化**する。無理に画像生成や ymmp ゼロ生成を Python に寄せない（[AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md)）。

**優先順位**

1. **意味ラベル＋ face_map / bg_map / slot_map / overlay_map / se_map** で決定的に寄せられる範囲は、**同じ palette ymmp・同じ registry 束**に対し、**別 `video_id`・別 utterances の IR を差し替える**形で量産する（IR 差分の量産）。
2. 上記 **4 類＋ mood ストック**は、**テンプレ資産の再利用**を第一とし、Python で見た目を合成生成しない。
3. **「テンプレを用意しておく」**の実体は、[PRODUCTION_IR_SPEC.md](PRODUCTION_IR_SPEC.md) §6 の **Template Registry**（`scene_presets` の `ymm4_template` 等）と、**1 本の親 palette ymmp**（表情・背景・slot の解決元）をプロジェクト単位に複製・差し替えする運用と捉える。

**量産試験の手順**は [verification/mass-production-pilot-checklist.md](verification/mass-production-pilot-checklist.md)。

**機械の際限**は [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md)（`motion` / `transition` の patch 未接続、`bg_anim` の VideoEffects 系は未接続等）。

## 後続開発で迷わないための注意

1. **本書は「何を再現したいか」**の正本。**「Python がどこまで書くか」**は [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md)。  
2. **画像付き例の再提示**は、必要なら `docs/verification/` に「参照画像の置き場 URL または社内パス」の 1 行だけを足す運用も可（画像バイナリは repo にコミットしない方針でもよい）。  
3. Custom GPT / [S6-production-memo-prompt.md](S6-production-memo-prompt.md) を更新する際は、**吹き出し＝字幕と別**・**skit＝作中人物**をプロンプトに明示すると文脈が切れにくい。

## 関連ドキュメント

- [PRODUCTION_IR_SPEC.md](PRODUCTION_IR_SPEC.md) §3.1 `template`、§3.7 `overlay`、§6 Template Registry
- [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md)
- [verification/mass-production-pilot-checklist.md](verification/mass-production-pilot-checklist.md)
- [OPERATOR_WORKFLOW.md](OPERATOR_WORKFLOW.md)（C-07 v2 proof の一行）
- [AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md) L2/L3
