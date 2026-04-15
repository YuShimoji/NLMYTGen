# haitatsuin 立ち絵パス復旧 (2026-04-16)

**ブロック**: 復旧 B (user 報告「立ち絵が表示されない」の対応)
**対象**: [samples/characterAnimSample/haitatsuin_2026-04-12.ymmp](../../samples/characterAnimSample/haitatsuin_2026-04-12.ymmp)

## 症状

user が YMM4 で haitatsuin_2026-04-12.ymmp を開くと立ち絵が表示されない。

## 原因

2026-04-13 commit `17339dd` で立ち絵パーツ参照を `D:\MovieCreationWorkspace\...` → `migrated_tachie/...` に書き換えた migration が実行されたが、`samples/characterAnimSample/migrated_tachie/` 配下の全ファイルが **`reimu_easy.png` の複製プレースホルダ**だった([TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §2.1 に既往記載)。

検証:
- `migrated_tachie/新まりさ/目/00.png` md5 = `2b73fdfae08cd760da552b4c8f9b0928`
- `reimu_easy.png` md5 = 同じ = **placeholder clone 確定**

YMM4 が「目パーツ」として reimu 全身画像を、「口パーツ」として同じ reimu 全身を… と重ねようとして立ち絵合成が破綻。

## 復旧 B 対応

`samples/Mat/` には 2026-04-14 commit `e22bf75` で**実パーツがコミット済**([samples/Mat/新まりさ/](../../samples/Mat/新まりさ/) / [samples/Mat/新れいむ/](../../samples/Mat/新れいむ/))。
haitatsuin ymmp のパス参照を `migrated_tachie\` → `..\Mat\` (相対 from characterAnimSample/) に書き換えた。

## 実施

1. **書き換えスクリプト**: [samples/characterAnimSample/_repoint_to_samples_mat.py](../../samples/characterAnimSample/_repoint_to_samples_mat.py) を新規作成
2. **backup**: 元 ymmp を [samples/_probe/b2/haitatsuin_backup_before_repoint.ymmp](../../samples/_probe/b2/haitatsuin_backup_before_repoint.ymmp) に保存
3. **実行**: `uv run python samples/characterAnimSample/_repoint_to_samples_mat.py` → "migrated_tachie refs left: 0"
4. **検証**: [samples/_probe/b2/verify_paths.py](../../samples/_probe/b2/verify_paths.py) で 15 パーツパス全て `samples/Mat/` 配下に解決、Missing 0

## 変更パス一覧 (15 件)

| 旧 | 新 |
|---|---|
| `migrated_tachie\新まりさ\他\00b.png` | `..\Mat\新まりさ\他\00b.png` |
| `migrated_tachie\新まりさ\他\00o.png` | `..\Mat\新まりさ\他\00o.png` |
| `migrated_tachie\新まりさ\体\01.png` | `..\Mat\新まりさ\体\01.png` |
| `migrated_tachie\新まりさ\口\00.png` | `..\Mat\新まりさ\口\00.png` |
| `migrated_tachie\新まりさ\目\00.png` | `..\Mat\新まりさ\目\00.png` |
| `migrated_tachie\新まりさ\眉\06c.png` | `..\Mat\新まりさ\眉\06c.png` |
| `migrated_tachie\新まりさ\髪\00o.png` | `..\Mat\新まりさ\髪\00o.png` |
| `migrated_tachie\新れいむ\他\00a.png` | `..\Mat\新れいむ\他\00a.png` |
| `migrated_tachie\新れいむ\他\00o.png` | `..\Mat\新れいむ\他\00o.png` |
| `migrated_tachie\新れいむ\体\00.png` | `..\Mat\新れいむ\体\00.png` |
| `migrated_tachie\新れいむ\口\00.png` | `..\Mat\新れいむ\口\00.png` |
| `migrated_tachie\新れいむ\後\00o.png` | `..\Mat\新れいむ\後\00o.png` |
| `migrated_tachie\新れいむ\目\00.png` | `..\Mat\新れいむ\目\00.png` |
| `migrated_tachie\新れいむ\眉\05c.png` | `..\Mat\新れいむ\眉\05c.png` |
| `migrated_tachie\新れいむ\髪\00o.png` | `..\Mat\新れいむ\髪\00o.png` |

## user 視覚確認依頼

YMM4 で haitatsuin_2026-04-12.ymmp を開き、立ち絵(ゆっくり魔理沙 + ゆっくり霊夢)が正常に表示されるかを確認してください。

- OK → B-2 次ステップ (face_map / overlay_map / IR / dry-run) に進む
- NG → パス解決の追加 failure class を特定

## 副次対応

- `migrated_tachie/` 配下は placeholder のため、将来的にディレクトリ削除 or archived 化を検討 (本ブロック非対象)
- B-3 や X-2a など他の proof で参照されていないことは確認済み (grep で migrated_tachie 参照は haitatsuin 関連のみ)

## 関連

- 事前調査: [TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §2.1
- 原因 commit: `17339dd` (2026-04-13)
- 復旧後の commit: `HEAD` (2026-04-16)
