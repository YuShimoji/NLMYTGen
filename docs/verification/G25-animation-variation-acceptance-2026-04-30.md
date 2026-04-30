# G-25 Animation Variation Acceptance — 2026-04-30

## 結論

G-25 の `.ymmp` openability は修復済みだが、代表 review のアニメーション variation は制作に使える品質ではなかった。

この結果は「YMM4 property route の readback / derivative copy は可能」という技術確認であり、「演出として有効な動きの自動variation生成」ではない。G-25 を production placement へ接続せず、次は G-26 として motion primitive grammar / compatibility probe に切り替える。

## ユーザー確認結果

- `delivery_v1_representative_review.ymmp` は YMM4 で開けた。
- ただし、生成された `nudge / scale / rotate / effect_reuse` はアニメーション variation として使えなかった。
- 手動作成済みの `うなずき` / `退場` / `小ジャンプ` を組み合わせても、動きとして自然なバリエーションになっていない。
- 観測された失敗例:
  - 傾きを反対方向に行う。
  - 退場時に傾いた角度のまま退場する。
  - 傾いた状態で小ジャンプする。
  - 要素ごとの組み合わせは試しているが、意味のある「動きのvariation」にはなっていない。

## 失敗分類

| Failure class | 内容 |
|---|---|
| `STATIC_PROPERTY_VARIANT_NOT_MOTION` | `X/Y/Zoom/Rotation` の小変更は姿勢差分であり、動きの演出差分ではなかった。 |
| `PRIMITIVE_COMPOSITION_DRIFT` | うなずき・退場・小ジャンプ等の要素を機械的に混ぜると、意図しない姿勢や移動が残る。 |
| `RESET_POSE_MISSING` | motion primitive の開始姿勢・終了姿勢・ニュートラル復帰条件が定義されていない。 |
| `DIRECTION_SEMANTICS_MISSING` | 傾き・退場方向・ジャンプ方向の意味が分離されず、反対方向や不自然な向きに合成される。 |
| `MOTION_VARIATION_NOT_ATTEMPTED` | 現行G-25は property variation probe であり、motion primitive の意味単位 variation はまだ試していない。 |

## 判断

- G-25 は `done` のまま維持するが、意味は「property route / openability probe 完了」に限定する。
- G-25 の representative review は production quality proof ではない。
- G-25 の候補を G-24 production placement に自動接続しない。
- 次の開発単位は G-26 として、手動作成済み motion primitive から相性・状態遷移・安全な組み合わせだけを扱う。

## G-26 推奨方向

G-26 は、自由な座標差分や総当たり合成ではなく、motion primitive を意味単位で扱う。

最小メタデータ:

- `primitive_id`: `nod_v1`, `exit_left_v1`, `hop_small_v1`, `tilt_left_v1` など。
- `motion_role`: `acknowledge`, `exit`, `emphasis`, `surprise`, `tilt_pose` など。
- `start_pose` / `end_pose`: `neutral`, `tilt_left`, `tilt_right`, `offscreen_left` など。
- `dominant_channels`: `X`, `Y`, `Rotation`, `Zoom`。
- `reset_policy`: `returns_to_neutral`, `requires_reset`, `terminal`.
- `compatible_after` / `forbidden_after`: 直前primitiveとの接続条件。
- `direction_semantics`: `left`, `right`, `vertical`, `none`。

生成候補は次の順で絞る:

1. 手動primitiveの完全再利用。
2. timing / spacing の軽微変更。
3. `start_pose == previous end_pose` または reset primitive がある場合だけ sequential composition。
4. mirror / direction change は semantic mirror が明示されている場合だけ。
5. `tilt + exit`、`tilt + hop` のような compound motion は、手動で成功例が登録されるまで自動生成しない。

## 次アクション

1. G-26 を `FEATURE_REGISTRY` に proposed として起票する。
2. `probe-ymmp-variations` の現行候補を「motion variation」ではなく「property route probe」として扱う。
3. 次の実装では `probe-motion-primitives` もしくは同等の packet を作り、手動motion clipの start/end pose と compatibility を機械可読化する。
4. まずは新しい `.ymmp` を大量生成せず、JSON compatibility report と小さな review checklist で止める。
