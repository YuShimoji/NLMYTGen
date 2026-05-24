# P2C — SE / `AudioItem` write route（現状境界）

## 更新（2026-04-07）

[samples/AudioItem.ymmp](../../samples/AudioItem.ymmp) を追加し、G-18 で **`_apply_se_items` による `AudioItem` 挿入**を実装した。以下の「ゲート前の記録」は履歴として残す。

---

## 状態（G-13 当時の正本・履歴）

- `patch-ymmp` の `se` は **`--se-map` まで label / timing anchor を解決**できる。
- 当時 repo-local corpus の `.ymmp` には **タイムライン上の `AudioItem` が含まれておらず**、`measure-timeline-routes` でも **SE 用の確定 write JSON パスが観測できない**。
- そのため当時の実装は **SE write-route unsupported failure で fail-fast** する境界とした（FEATURE_REGISTRY G-13）。

## 次に実装を進めるゲート

1. **AudioItem を 1 件以上含む ymmp** を入手する（ユーザー生成の YMM4 プロジェクトで OK。著作権・サイズに注意し、repo に載せる場合はサンプルとして許容される範囲に限定）。
2. `measure-timeline-routes <that.ymmp> --format json` で `AudioItem` 周りのキー構造を記録する。
3. FEATURE_REGISTRY に **新規 ID（例: G-15 拡張）を `proposed`→承認**してから、`ymmp_patch.py` に write 経路を追加する。

## 本スライスでの扱い

- **コード変更なし。** 境界を本文書で固定し、プラン todo「AudioItem 入手後」を満たすまで **実装保留**とする。

## 参照

- [G13-overlay-se-insertion-packet.md](G13-overlay-se-insertion-packet.md)
- [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) G-13
