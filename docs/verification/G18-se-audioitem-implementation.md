# G-18 — SE `AudioItem` 挿入（実装記録・正本）

## 状態（2026-04-07）

**ゲート解除済み。** [samples/AudioItem.ymmp](../../samples/AudioItem.ymmp) を readback 正本とし、[src/pipeline/ymmp_patch.py](../../src/pipeline/ymmp_patch.py) の **`_apply_se_items`** が `AudioItem` をタイムラインに挿入する。

- タイムラインに既存 `AudioItem` があれば **その構造を deepcopy してテンプレート**にする。
- 無ければ **`_AUDIO_ITEM_SKELETON_JSON`**（上記サンプル由来の骨格）を使う。

運用メモ（入手前の手順）は下記「オペレーター向けハンズオン」を参照。

---

## readback 記録（実測）

サンプル: [samples/AudioItem.ymmp](../../samples/AudioItem.ymmp)

| 項目 | 観測値 |
|------|--------|
| サンプルパス（repo 内） | `samples/AudioItem.ymmp` |
| `AudioItem` の `$type` 完全名 | `YukkuriMovieMaker.Project.Items.AudioItem, YukkuriMovieMaker` |
| 主要キー | `IsWaveformEnabled`, `FilePath`, `AudioTrackIndex`, `Volume`, `Pan`, `PlaybackRate`, `ContentOffset`, `FadeIn`, `FadeOut`, `IsLooped`, `EchoIsEnabled`, `EchoInterval`, `EchoAttenuation`, `AudioEffects`, `Group`, `Frame`, `Layer`, `KeyFrames`, `Length`, `Remark`, `IsLocked`, `IsHidden` |
| 典型 Layer | 0（サンプル 1 件） |
| VoiceItem との関係 | サンプルは VoiceItem なしの最小プロジェクト。本番では `se_map` の `layer` で上書き可能 |

---

## オペレーター向けハンズオン（あなたが行う作業）

この節は **readback 用サンプルを追加するとき**の参考です。

### ゴール

タイムラインに **少なくとも 1 件の `AudioItem`** が載った `.ymmp` を用意し、必要なら `samples/` に置く。

### 手順 1 — YMM4 で最小サンプルを作る

1. **新規または既存のゆっくりプロジェクト**を開く。
2. タイムライン上に **効果音・SE 用の音声アイテム**を 1 本置く。
3. 参照する **音声ファイル**は権利のある短いクリップに限定する。
4. **プロジェクトを保存**する。

### 手順 2 — 著作権・サイズ・共有方法

- repo に載せる場合は配布可能な素材のみ。巨大な ymmp は避けるか、readback 結果だけ共有。

### 手順 3 — readback

```text
uv run python -m src.cli.main measure-timeline-routes "C:/path/to/your_project.ymmp" --format json
```

（列挙されない場合は ymmp を開き `AudioItem` を検索してキー構造をメモする。）

### よくあるつまずき

| 状況 | 対処 |
|------|------|
| ymmp に AudioItem が見つからない | 保存し直し、タイムライン配置を確認 |
| サンプルが巨大 | readback 結果だけ共有 |

---

## 実装メモ（開発者）

- `se_map`: `path`（必須）, `anchor`（start/end）, `offset`, `length`, 任意 `layer`, `audio_track_index`。
- [G13-overlay-se-insertion-packet.md](G13-overlay-se-insertion-packet.md) の SE registry 形式と整合。
- `PatchResult.se_plans` は **挿入件数**。CLI は `SE insertions:` と表示。
- 広義の自動配置は避ける（[AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md)）。

---

## 参照

- [G18-se-audioitem-deferred.md](G18-se-audioitem-deferred.md)
- [P2C-se-audioitem-boundary.md](P2C-se-audioitem-boundary.md)
- [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) G-18
