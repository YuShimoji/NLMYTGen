# Episode 002 Default-Branch Integration — 2026-07-13

> **Result: approved Option A prepared and validated for one normal fast-forward.**
> This evidence becomes the default-branch integration record when the prepared
> tip is pushed to `master`; the final commit SHA is resolved from Git refs and
> the AGENT_REPORT rather than embedded into its own tracked content.

## Authorization and fixed provenance

- Authorization class: user-approved Option A.
- Pre-integration `origin/master`:
  `b61722454e3e218547fe6220bf1f4aa3802ed4d8`.
- Audited subject:
  `d8e959c54b8c8f28c31cc2b586bbdd8c79f69f97`.
- Direct audit child:
  `a8b81e43616281691b73520a045dfa6ff44d2054`.
- Integration branch: `codex/episode-002-default-branch-integration-v1`.
- Mechanism: normal non-force fast-forward only.
- Subject, audit, and integration branches remain provenance; no history was
  amended, rebased, squashed, cherry-picked, or deleted.

## State-dependent metadata rebind

The final `docs/runtime-state.md` SHA-256 is
`943DB7C5C286B1668F31483E57CADE5370F53422F7DFEB1985072168FD1F61E1`.
The audit-tail runtime-state hash before the final state was
`65D2419CD8876FBBC8AD7567D6DE2B559E61FCA5D3B9E4BE0A441996A9DF92E6`;
the source bundle still carried the immutable subject-era runtime hash
`35A949E6C5E0C658D66DEA721FF4DAA8613307E8E39D0C5661F2577342B96433`.

Only this tracked dependency closure changed:

| file | before SHA-256 | after SHA-256 |
| --- | --- | --- |
| `source_bundle_manifest.json` | `A21D17FF25978E00EEF7C0E2FD052E5CF8CDD98BEFB94A38E8F83B2B44187DBE` | `98ADB8307099A47BA07D6DACAE263AF5759C3FC51D4C904A7DCC648E08473A6D` |
| `input_validation_readback.json` | `04B8D0A725579BB5EBF0B62431028398EA0D9F364FAE9BE6695ED7E73A607203` | `9D4B9C212083D563AD6128153E2080B4F8F4AD5BBECF7B0BFBB5B3AA51C3EDD4` |
| `internal_review_manifest.json` | `2F3BA081BCF38122AAA193274A2E75232DBF683ED1C3BC9336A39360C1BB37A4` | `05118F6D67DAAF2F49A4F2BA365F9EF192C8589D97A81DE1E0AC2E4DE77C2568` |

The bounded helper reads tracked text/JSON only. A second pass produced no
changed file. It did not read or regenerate MP4, proxy, `.local.ymmp`, operator
result, or any file under `local_outputs`.

## Immutable evidence

- Canonical script text/JSON:
  `22F894D713C51D8E688ADB934D0BFB5992B31216443FF430777EC980AA413826` /
  `4249425D680A44DE25BE697262966A44D396AAFE611AA90A0BF769BEC4EE9B16`.
- Claim ledger:
  `BA21FFF7E9725AF00A438213AE3453B84D9E9CFDC1568141AE83F52877C1B587`.
- Canonical/derived CSV:
  `0A7B7F27FFF37E9AD29ADACD93BDB6FECBA6AE2650FE34DBE90E7BCFED9FE967` /
  `D1C5C4C4E61996BDD89398618C0E7353A826D598B642E2397ACD982B1D5CBB1F`.
- Operator result/project/original render/proxy identities remain respectively
  `C2204D10579FFBC9133F21C65F9C60968C19638C29DB4354A529D0CAF1B6E9E5`,
  `318AF09D0B52958555918140AD62AF0E7882A39FFA902C8E5D1304319CE11A01`,
  `ACF2E8B284E7956529F8170B6BA5EC55CBC0A4B511DCF56E579087051DA00BAE`,
  and `45BD0A060BAA45C1BB44068F4ADAE1A6B50DBBF86FABA70F3A1761809BE5A025`.
- Audit Markdown/JSON/path inventory remain respectively
  `93E3518B73046353D896DB5B23872BF02A44C5C66B69D9DE09CFDF86C21FEB32`,
  `97CF2739D2DBDEF0753F3DAECA9DE3A78A0E5FD875159C9CA049FDF7AE76A4FA`,
  and `7D47826D0D9E0DE26D7E57E7E079D351803F513B1FB2D9BE27C44B578760DBC6`.

## Focused validation

The accepted 85-test milestone suite is rerun with bounded metadata-rebind and
integration-receipt coverage added. Project-state sync, all modified/new JSON,
canonical/CSV and render/project identity invariance, ignored-binary tracking,
privacy/path/secret checks, deterministic second pass, merge-tree, and
`git diff --check` are separate required checks. Full pytest is excluded.

## Resulting state and next gate

- Project-State-ID: `episode-002-milestone-integrated-default-branch-v1`.
- Product-State: `episode-002-milestone-integrated-on-default-branch`.
- Product-Gate: `verified-external-editorial-input-selection`.
- Recommended-Next: `select-or-provide-verified-editorial-source`.
- External-State: `public-repo-default-branch`.

Repository placement does not imply external editorial adoption, human visual
or creative acceptance, production readiness, rights/legal approval, upload,
publication, or public availability of any video.

## Negative operations

No force/non-fast-forward update, merge commit, rebase, squash, cherry-pick,
PR/issue, branch deletion, YMM4, Computer Use, media/project regeneration,
dependency installation, publication, rights action, or full pytest was used.
