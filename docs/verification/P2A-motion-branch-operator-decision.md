# P2A — feat/phase2-motion-segmentation 取り込み判断（オペレータ記録）

> 正本レビュー: [P2A-phase2-motion-segmentation-branch-review.md](P2A-phase2-motion-segmentation-branch-review.md)  
> ロードマップ連携: [FUTURE_DEVELOPMENT_ROADMAP.md](../FUTURE_DEVELOPMENT_ROADMAP.md)（G-17）

## 現状の判断（2026-04-06）

| 項目 | 結論 |
|------|------|
| 一括マージ | **しない**（P2A レビューどおり） |
| 部分取り込み | **未実施・保留**。必要になったタイミングで、テスト単位または設計ドキュメント単位で検討する |
| G-17（motion 書き込み Adapter）との関係 | 将来 G-17 を `approved` にする際、リモートブランチから **再利用するコード・テスト**を選別するかどうかを再評価する |

## 次にオペレータがやること（任意）

1. 本番の制作で **motion / transition を IR から自動で載せたい痛点**が顕在化したか確認する。  
2. 顕在化したら、P2A の差分要約と [FUTURE_DEVELOPMENT_ROADMAP.md](../FUTURE_DEVELOPMENT_ROADMAP.md) の G-17 行を読み、**小さなパッチ**として取り込む範囲を決める。  
3. 決定したら FEATURE_REGISTRY・verification を更新し、`approved` スライスとして実装する。

## 承認記録（取り込みを実行したときに追記）

| 日付 | 取り込み範囲 | PR / コミット | メモ |
|------|--------------|---------------|------|
| （未） | | | |
