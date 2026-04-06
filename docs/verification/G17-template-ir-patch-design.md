# G-17 IR `template` と YMM4 ItemSettings（設計メモ・承認前）

> ステータス: **proposed**（[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md)）。実装は **corpus 測定後**かつ承認後。

## 目的

IR の `template`（skit / data / board / mood 等）を、**palette ymmp 上のネイティブテンプレ参照・ItemSettings**に機械的に寄せるかどうかを決め、可能なら patch で差し替える。

## 制約

- [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) の C-02/C-03（ymmp ゼロ生成）は **rejected** のまま。対象は **既存タイムラインの Adapter 書き込み**のみ。

## 手順（案）

1. 制作で使う **1 プロジェクト**を選び、`measure-timeline-routes` および手動調査で、`template` 意図と対応する **YMM4 項目**（`TemplateName`、Voice 系設定等）を列挙する。
2. **Template Registry** の `scene_presets` / `ymm4_template` との二重定義を避けるため、**単一の正本**（registry か IR か）を決める。
3. 差し替え対象が VoiceItem 以外に及ぶ場合は、G-11/G-13 と同様に **failure class** を先に定義する。

## 関連

- [C07-visual-pattern-operator-intent.md](../C07-visual-pattern-operator-intent.md)（運用テンプレ vs IR 意味）
