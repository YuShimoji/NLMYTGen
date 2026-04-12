# 立ち絵 ymmp 幾何調査メモ（G-20 前提・readback）

**日付**: 2026-04-13  
**正本パック**: [TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §3  
**readback 対象**: リポジトリ内 [samples/test_verify_2_mouth.ymmp](../../samples/test_verify_2_mouth.ymmp)（AnimationTachie、`TachieItem` / `VoiceItem` 双方を含む）

---

## 1. 観測項目（§3 の三問への対応）

| §3 の問い | readback で確認したこと | 未確認・要 GUI 確認 |
|-----------|-------------------------|---------------------|
| 体の反転はどこか | **`TachieItem`** に **`IsInverted`**（bool）、**`X` / `Y` / `Z` / `Zoom` / `Rotation` / `Opacity`** がアニメーション値オブジェクトとして存在。`TachieItemParameter`（`AnimationTachie.ItemParameter`）は **パーツ FilePath**（`Body`, `Eyebrow`, …）であり、反転フラグは見当たらない。 | `IsInverted` を true にしたとき **体のみ**か **合成全体**かの見た目は YMM4 プレビューで要確認。 |
| 顔（発話表情）はどこか | **`VoiceItem`** にも **`IsInverted`** および **`X` / `Y` / `Zoom` / `Rotation`** 等が **別ストリーム**として存在。発話ごとのパーツは **`TachieFaceParameter`**（`AnimationTachie.FaceParameter`）内の FilePath。 | 発話中の「顔」描画が **VoiceItem 幾何**と **TachieItem 幾何**のどちらに従うかはテンプレ・版依存のため、代表プロジェクトで 1 回 GUI 確認推奨。 |
| 顔と体を同量移動 | **同一 GroupItem 配下に入れる**運用は G02b で言及あり（本サンプルでは `TachieFaceItem` は未出現）。機械同期をするなら **複数アイテムの X/Y に同一デルタを patch** する設計が候補。 | **確認済み（2026-04-13）**: グループ制御で破綻なく移動・拡大縮小が可能。詳細は §7。 |

---

## 2. patch アンカー（現行コードとの整合）

| 操作の意図 | 第一候補アンカー | 根拠 |
|------------|------------------|------|
| 発話中の眉・目・口・髪・体パス差し替え | **`VoiceItem.TachieFaceParameter`** | [ymmp_patch.py](../../src/pipeline/ymmp_patch.py) の `_apply_face_to_voice_item` がここを更新。 |
| 待機中表情 | **`TachieFaceItem`**（タイムライン挿入） | `idle_face` 経路（同一ファイル内 `_apply_idle_face`）。本サンプル ymmp には `TachieFaceItem` 無し。 |
| 立ち絵全体の位置・ズーム・左右反転 | **`TachieItem`** の **`X` / `Y` / `Zoom` / `IsInverted` 等** | G02b・readback 一致。既存 **`slot`** patch は registry 経由で **TachieItem** 系を触る契約（[PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)）。 |
| 字幕・ボイス表示ブロックの幾何 | **`VoiceItem`** 側の X/Y/Zoom/… | 立ち絵と **別レイヤ**の可能性。G-20 で「顔の見た目」を VoiceItem 幾何まで含めるかは **スコープ分岐**が必要。 |

---

## 3. G-20 スコープ案（Tier A / Tier B）

### Tier A — 既存 IR / 既存 patch で吸収しうる範囲

- **`slot`（+ slot_map / registry）** による **`TachieItem` の配置・Zoom**（左右スロットの切替え等）。  
- **`motion`（Phase2 の `tachie_motion_effects_map` / G-17 の timeline profile）** による **`TachieItem` の `VideoEffects`** や区間分割（「より複雑な動き」の第一候補はここ。別 FEATURE 起票は **G-17 で足りない**と判明した場合）。

### Tier B — G-20 承認後に新語彙・patch 拡張が必要になりうる範囲

- **`TachieItem.IsInverted`** および **必要なら `VoiceItem.IsInverted`** を IR から決定的に同期させる（**反転**）。  
- **`TachieItem` と `VoiceItem` の X/Y に相対オフセット**を同時に適用する（**平行移動の視覚整合**）。アンカー二系統のため、**片方だけ patch すると破綻**しうる。  
- **キーフレーム付き `X`/`Y` オブジェクト**への書き込みは、現行 `_apply_slots` より広い契約が要る可能性あり（readback では `Values[0].Value` 形式）。

**契約確定の条件**: 上記「要 GUI 確認」を含め §1 の未確認を潰し、**どのキーを Writer 語彙に載せるか**を一文で固定してから G-20 を `approved` に昇格させる。

---

## 4. モーション（パックゴール 3）

[PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) に従い、**`motion` は既に `TachieItem` を主アンカー**とする二経路（`--tachie-motion-map` / `--timeline-profile` + `--motion-map`）がある。**追加 FEATURE は不要な可能性が高い**。レイアウト微調整が目的なら Tier A を先に exhaust してから判断する。

---

## 5. 参照ファイル

- [G02b-ymmp-structure-analysis.md](G02b-ymmp-structure-analysis.md)  
- [samples/test_verify_2_mouth.ymmp](../../samples/test_verify_2_mouth.ymmp)（本メモの readback 源）

---

## 6. サンプル補足 readback: `haitatsuin_2026-04-12.ymmp`（AnimationTachie）

**正本パック**: [TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §2.1 フェーズ B。

| 項目 | 観測 |
|------|------|
| 対象 | [samples/characterAnimSample/haitatsuin_2026-04-12.ymmp](../../samples/characterAnimSample/haitatsuin_2026-04-12.ymmp)。キャラ名は **`ゆっくり魔理沙黄縁`** / **`ゆっくり霊夢赤縁`**。プラグインは **`YukkuriMovieMaker.Plugin.Tachie.AnimationTachie`**（PREP §2.1 の A 行と一致）。 |
| Tier A（パス・再現性） | 旧参照（`MovieCreationWorkspace` 配下の絶対パス）をやめ、[samples/characterAnimSample/migrated_tachie/](../../samples/characterAnimSample/migrated_tachie/) を指す **相対パス**へ寄せた。未ラベル `extract-template` では **2 パターン**（`face_01_*` / `face_02_*`）が抽出され、パーツキーはいずれも `Eyebrow` / `Eye` / `Mouth` / `Hair` / `Body`。成果 JSON: [samples/characterAnimSample/face_map_extracted.json](../../samples/characterAnimSample/face_map_extracted.json)。 |
| `--labeled` | [samples/characterAnimSample/extract_template_labeled/face_map.json](../../samples/characterAnimSample/extract_template_labeled/face_map.json) は空オブジェクト（VoiceItem の **Remark 未設定**のため 0 パターン）。「ラベル安定」の確認は YMM4 で Remark を付与したうえで再実行が必要。 |
| Tier B 示唆 | 同一プラグインで **Body** のファイル名が `01.png`（魔理沙側）と `00.png`（霊夢側）に分かれており、体バリエーション差分が **パーツパス差**として readback 上は分離可能。反転・同量移動は §1〜§3 の **`TachieItem` / `VoiceItem` 二系統**がそのまま当てはまる（GUI 未確認項目は変更なし）。 |
| 素材注意 | `migrated_tachie` 内の PNG はリポ既存の `reimu_easy.png` を複製した **プレースホルダ**であり、本番の見た目整合はオペレータが実パーツへ差し替える必要がある。 |

---

## 7. YMM4 グループ制御の運用知見（2026-04-13 オペレータ確認済み）

**目的**: ゆっくり頭（TachieItem）と別の体素材（ImageItem）をタイムライン上で重ねて配置し、まとめて移動・拡大縮小できるかの確認。

### 確認結果: 破綻なく移動・拡大縮小が可能

AnimationTachie は合成後の 1 アイテムとして動くため、TachieItem 単体の位置・拡大率変更で顔パーツ（眉・目・口）は全て追従する。複数アイテム（頭 + 体）をまとめて動かすには YMM4 のグループ制御を使う。

### グループ制御の仕様・制約

| 項目 | 内容 |
|------|------|
| グループの追加 | タイムラインに 1 列分が必要 |
| 影響範囲 | レイヤー指定で限定する。余計なアイテムを巻き込まないよう注意 |
| 影響対象 | グループのすぐ下（指定レイヤー以内）に配置されたアイテム |
| 影響期間 | グループの長さまでしか影響しない |
| 移動後の保持 | 中間点を使う。例: 位置 0→500→500 のように、留めたい値を繰り返す |
| 中間点の配置 | アイテムの表示時間内の任意位置に自由に決められる |
| 拡大縮小の注意 | グループの中心位置が基準になる。画面中央にグループがある場合、縮小すると画面中央に引き寄せられるように見える。位置をグループ中心から逆算する必要がある |
| 左右反転 | グループ制御では不可。素材を分割して反転チェックを入れるか、アニメーションで工夫する必要がある。首を振るだけでも回数分の素材コピーペーストまたは複雑なアニメーション設定が必要になる可能性 |

### 体テンプレ構想への示唆

- 位置合わせは手動で 1 回行い、テンプレとして保存する運用が現実的
- テンプレを蓄積すれば、台本→IR で「配達員テンプレを使う」のように指定できる将来像が成立する
- 自動化するには IR 語彙（`body_template`）と body_map レジストリの追加が必要（将来 FEATURE）
- 左右反転の自動化は制約が大きく、当面は手動運用
