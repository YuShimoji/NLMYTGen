# G-24 Real Estate DX Skit Group IR Validation (2026-04-27)

## Purpose

Accept the corrected NotebookLM-derived real estate DX script as the production input for this case, then generate and validate a skit_group actor IR using the synced G-24 flow.

This pass does not search more repo-local IRs, author new YMM4 motions, edit registry aliases, change CLI/API contracts, or generate a confirmation `.ymmp`.

## Inputs

- Corrected script: `samples/不動産DX_魔法の鍵とキュレーション.txt`
- CSV artifact: `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv`
- Skit group IR: `samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json`
- Corpus: `samples/canonical.ymmp`
- Registry: `samples/registry_template/skit_group_registry.template.json`

The typo-heavy earlier prompt text is superseded by the corrected script file above.

## Script QC

Command:

```bash
python3 -m src.cli.main diagnose-script \
  samples/不動産DX_魔法の鍵とキュレーション.txt \
  --speaker-map "語り手A=れいむ,語り手B=まりさ" \
  --format json
```

Result:

- `utterance_count=152`
- `NLM_STYLE_MARKER` warning: utterance 97
- `EXPLAINER_ROLE_MISMATCH` / `LISTENER_ROLE_MISMATCH` warnings: expected under this case because the requested mapping makes `語り手A` / `れいむ` the explanation-heavy side and `語り手B` / `まりさ` the question-heavy side

NotebookLM output remains low-trust. Do not pass future raw NLM text directly into CSV/IR without at least B-18 diagnostics or equivalent manual QC.

## CSV Build

Command:

```bash
python3 -m src.cli.main build-csv \
  samples/不動産DX_魔法の鍵とキュレーション.txt \
  -o samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv \
  --speaker-map "語り手A=れいむ,語り手B=まりさ" \
  --max-lines 2 \
  --chars-per-line 40 \
  --balance-lines \
  --stats
```

Result:

- CSV rows: `352`
- Speaker stats: `れいむ=196 utterances / 4178 chars`; `まりさ=156 utterances / 3505 chars`
- Overflow candidates: 18 rows still estimate at 3 lines after balancing; handle later as normal B-17/YMM4 residual observation if needed

## Skit Group IR

The skit_group actor represents the symbolic gatekeeper / guide. Every targeted utterance uses `motion_target: "layer:9"`.

| utt | scene beat | requested intent | resolution class |
| --- | --- | --- | --- |
| 1 | magic key / secret library opener | `enter_from_left` | exact |
| 15 | REINS as private VIP club | `nod` | exact |
| 35 | hidden “darkness” reveal | `surprise_jump` | fallback |
| 39 | dual agency / conflict of interest | `deny_shake` | fallback |
| 104 | SNS gray zone warning | `panic_shake` | manual_note |
| 143 | gatekeeper exits, curator remains | `exit_left` | exact |

## Audit

Command:

```bash
python3 -m json.tool samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json

python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

Result:

- Anchor group: `haitatsuin_delivery_v1`
- Anchor remark: `haitatsuin_delivery_main`
- Anchor layer: `9`
- Summary: `exact=3 / fallback=2 / manual_note=1`
- Verdict: **PASS as real-case skit_group IR validation**

## Manual Note Classification

`panic_shake` remains intentionally unresolved.

- **Current handling**: `manual_note`
- **New-template candidate**: only if future production cases repeatedly need stronger panic/shaking acting
- **IR wording avoidance**: acceptable when the beat can be represented by narration, `surprise_jump`, or `deny_shake`
- **Registry action**: none; do not alias `panic_shake` without user acceptance
