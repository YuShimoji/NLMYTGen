# 素材調達・運用ルール

> **読み物**: [VISUAL_EFFECT_SELECTION_GUIDE.md](VISUAL_EFFECT_SELECTION_GUIDE.md)
> **姉妹**: [VISUAL_TOOL_DECISION.md](VISUAL_TOOL_DECISION.md)
> **目的**: Step 2「素材調達ルール」を 1 ファイルに固定する。保存場所・命名・ライセンス・差し替えの運用を後から参照できる形で残す。

## 記入方法

各セクションの `(未記入)` を埋める。推奨例をそのまま採用する場合も明示的に書く。

---

## 1. 保存場所

現状: `samples/Mat/` にゆっくり立ち絵パーツを蓄積中 (haitatsuin 復旧で実証済み)。

**方針選択**:

- [✓] A: `samples/Mat/` を続投 — 全案件共通の素材置き場。リポで共有
- [ ] B: 案件ごとに別フォルダ — `samples/<project_name>/mat/` のように案件隔離
- [ ] C: リポ外 (外部ディスク) — ライセンス都合でリポにコミットできない素材用

**決定**: A (`samples/Mat/` 続投)
**備考**: 全案件共通の素材置き場として続投。案件固有素材が出てきたら B 方針 (`samples/<project_name>/`) を併用する余地あり。

### 推奨ディレクトリ構造

```
samples/
├── Mat/                       # A 方針: 共通素材
│   ├── reimu/
│   ├── marisa/
│   └── ...
├── <project_name>/            # B 方針: 案件隔離
│   ├── backgrounds/
│   ├── overlays/
│   ├── se/
│   └── scripts/
└── registry_template/         # 既存: registry 雛形
```

---

## 2. 命名規約

**方針選択** (複数採用可、レイヤー別に分ける):

### 2-a. 立ち絵パーツ

- [✓] `{speaker}_{emotion}.png` — 例: `reimu_anger.png`, `marisa_smile.png`
- [ ] `{speaker}/{part}/{variant}.png` — 例: `reimu/mouth/03.png`
- [ ] その他: `(未記入)`

**決定**: `{speaker}_{emotion}.png`

### 2-b. 背景

- [✓] `bg_{scene_type}_{variant}.png` — 例: `bg_studio_blue.png`, `bg_outdoor_park_01.png`
- [ ] `{category}/{name}.png` — 例: `backgrounds/studio_blue.png`
- [ ] その他: `(未記入)`

**決定**: `bg_{scene_type}_{variant}.png`

### 2-c. オーバーレイ (吹き出し・図解等)

- [✓] `ov_{type}_{variant}.png` — 例: `ov_bubble_right.png`, `ov_arrow_red.png`
- [ ] `overlays/{type}_{variant}.png`
- [ ] その他: `(未記入)`

**決定**: `ov_{type}_{variant}.png`

### 2-c-i. 立ち絵レンダリング PNG (G-22 dual-rendering 経路 B)

立ち絵を YMM4 で 1 フレーム透明 PNG に書き出して overlay として使う場合は、**`{speaker}_{emotion}.png`** (立ち絵パーツと同一規約、§2-a) を基本とする。`ov_` プレフィクスは付けない。

- 基本: `{speaker}_{emotion}.png` — 例: `reimu_surprised.png`, `marisa_angry.png`
- **派生が必要な場合のみ** `_rendered` suffix を付与する (同名の立ち絵パーツファイルと衝突回避が必要な場合に限る。通常は不要)
- overlay_map.json 側の**キー名も同じ**に揃える: `"reimu_surprised": "./samples/Mat/reimu_surprised.png"`

**理由**: IR / overlay_map / ファイル名の三者でラベルが一致していないと `OVERLAY_UNKNOWN_LABEL` が頻発する。経路 A (TachieItem) と経路 B (書き出し PNG) は **IR 上のフィールドが異なる** (`face` vs `overlay`) ため、ラベル名自体はキャラ × 表情で共通化してよい。

詳細手順: [STEP3_TACHIE_RENDERING_PIPELINE.md](STEP3_TACHIE_RENDERING_PIPELINE.md)

### 2-d. SE

- [✓] `se_{action}.wav` — 例: `se_click.wav`, `se_tension_hit.wav`
- [ ] `se/{category}/{name}.wav`
- [ ] その他: `(未記入)`

**決定**: `se_{action}.wav`

---

## 3. ライセンス記録

### 方針選択

- [✓] A: 素材ごとに `LICENSE.csv` を同階層に置く (推奨)
- [ ] B: プロジェクトルートに `samples/LICENSE.md` で一括管理
- [ ] C: 記録しない (自作素材のみの案件)

**決定**: A (`LICENSE.csv` を素材同階層に配置)

### LICENSE.csv の推奨フォーマット

```csv
filename,source_url,license,usage_scope,download_date,notes
reimu_anger.png,https://example.com/...,CC-BY-4.0,commercial_ok,2026-04-16,
bg_studio_blue.png,https://pixabay.com/...,Pixabay_License,commercial_ok,2026-04-16,"cropped to 1920x1080"
se_click.wav,https://freesound.org/...,CC0,any_use,2026-04-16,
```

### 重要な運用ルール

- いらすとや: 1 つの作品内で 20 点まで無料。超える場合は要問合せ
- Pixabay / Pexels: 商用可だが人物が識別できる場合はモデルリリース確認
- Freesound: ライセンスが素材ごとに異なる (CC0 / CC-BY / CC-BY-NC)。CC-BY は credit 必須
- フリー素材の再配布禁止: リポに commit する場合はライセンス要確認

---

## 4. 差し替え方針

**決定**: 既定フローに従う (2026-04-16 確認済み)。

素材を更新・差し替えたときの registry 再生成フロー。

### 4-a. 立ち絵パーツ更新時

1. palette.ymmp に新パーツを反映
2. `uv run python -m src.cli.main extract-template --labeled palette.ymmp -o face_map.json`
3. `validate-ir` で `FACE_UNKNOWN_LABEL` が出ないか確認

### 4-b. 背景・オーバーレイ追加時

1. 素材を保存場所に配置
2. `bg_map.json` / `overlay_map.json` にラベル追加
3. `validate-ir --bg-map ... --overlay-map ...` で `*_UNKNOWN_LABEL` が出ないか確認

### 4-c. 案件ごとに素材セットを切り替える

- 推奨: 案件ごとに registry JSON を別ディレクトリに分け、CLI 引数で指定 (`--face-map samples/<project>/face_map.json`)
- 共通素材は `samples/Mat/` から相対パス参照

---

## 5. 絶対パス禁止

`D:\...` 等のローカル絶対パスは ymmp / registry では使わない。リポ外マシンで再現できないため。

- ymmp 内のパス: リポ同階層にコピーしたうえで YMM4 から保存し直す
- registry JSON: リポルートまたは案件フォルダからの相対パス
- `_migrate_moviecreation_paths.py` のようなパス移植スクリプトがあれば活用

---

## 6. 変更履歴

- 2026-04-16: 初版。ユーザー記入用テンプレ
- 2026-04-16: 全項目記入完了。保存場所=A (`samples/Mat/` 続投) / 命名規約=各レイヤーのフラット形式 (`{speaker}_{emotion}.png` / `bg_{scene_type}_{variant}.png` / `ov_{type}_{variant}.png` / `se_{action}.wav`) / ライセンス=A (`LICENSE.csv` 素材同階層) / 差し替え=既定フロー
- 2026-04-17: §2-c-i を追加。G-22 dual-rendering 経路 B の立ち絵レンダリング PNG は `{speaker}_{emotion}.png` (§2-a と同一規約) を基本とし、`_rendered` suffix は衝突時のみ。overlay_map のキー名と揃えることで `OVERLAY_UNKNOWN_LABEL` を防ぐ
