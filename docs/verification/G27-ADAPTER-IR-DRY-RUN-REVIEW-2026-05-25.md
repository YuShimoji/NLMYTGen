# G-27 Adapter IR Dry-Run Review 2026-05-25

この closeout は、`authorize_adapter_IR_dry_run_for_7_candidates_only` 採用後の dry-run review を閉じ、次 gate へ進む条件を明文化するためのもの。Feed / RSS reader 連携の差分は別作業として扱い、この G-27 記録では参照・変更しない。

## 確認した artifact

- Primary: `samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.json`
- Human-readable: `samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.md`
- Gate: `samples/_probe/g24/real_estate_dx_adapter_authorization_gate.json`

## Dry-run review 結論

| 区分 | beat | 状態 | 次 gate への意味 |
| --- | --- | --- | --- |
| ready | `RE-02-beginning` | `abstract_ui_route` / `ready` | 次 gate 候補 |
| ready | `RE-02-development` | `abstract_ui_route` / `ready` | 次 gate 候補 |
| ready | `RE-06-beginning` | `property_card_route` / `ready` | 次 gate 候補 |
| ready | `RE-06-development` | `document_proxy_route` / `ready` | 次 gate 候補 |
| ready | `RE-06-turn` | `document_proxy_route` / `ready` | 次 gate 候補 |
| ready | `RE-07D-beginning` | `ai_panel_route` / `ready` | 次 gate 候補 |
| ready | `RE-07D-development` | `risk_marker_route` / `ready` | 次 gate 候補 |
| excluded | `RE-02-turn` | `blocked` | opacity-layer adjustment が route candidate に反映されるまで除外 |
| deferred | `RE-07D-turn` | `deferred` | specialist / cast / silhouette 方針が決まるまで保留 |

7 件は adapter IR dry-run として ready。`RE-02-turn` と `RE-07D-turn` は今回の dry-run から外したままにする。

## まだ開けない境界

この closeout は `.ymmp` compact review や patch-output の材料を整理するだけで、次の作業はまだ許可しない。

- YMM4 patch: まだ禁止
- `.ymmp` write: まだ禁止
- render: まだ禁止
- production timing: まだ禁止
- creative acceptance: まだ禁止

既存の `real_estate_dx_ymmp_compact_patch_review.*` と `real_estate_dx_minimal_patched_probe.*` は参考証跡として存在するが、この closeout では更新・昇格しない。

## 次 gate へ進む条件

次に進むなら、7 ready candidates だけを対象に **compact review / patch-output candidate gate** を別 slice として開く。そこで必要になる判断は次の 3 点。

| 条件 | 内容 | 満たすと可能になること |
| --- | --- | --- |
| candidate 固定 | 7 ready candidates のみを対象にする | `RE-02-turn` / `RE-07D-turn` 混入を防げる |
| output 境界 | YMM4 patch / `.ymmp` write を行うかは別 gate で明示する | dry-run と実出力を混同しない |
| review surface | compact review を primary にするか、minimal patched probe を primary にするかを slice 開始時に固定する | 次の user / assistant 確認面が一本化される |

推奨は、まず **compact review candidate gate** として 7 件の表示意図・レイヤー・duration・placeholder を再確認し、`.ymmp` write を伴う作業はその後の明示 gate に分けること。

## 機械確認

- `node scripts/build_g27_adapter_ir_dry_run.js`
- `node scripts/check_g27_adapter_authorization_gate.js`
- `node scripts/check_g27_adapter_route_preflight.js`
- `node scripts/check_g27_review_packet.js`

上記が通れば、この dry-run review closeout は再現可能とみなす。
