# Episode 002 実入力置換準備pack

Primary review: `real_input_replacement_preview.html`
Operator contract: `real_input_replacement_contract.md`
Machine readback: `validation_readback.json`

このpackは、実入力置換の前に必要なローカルsource/transcript/receiptを明確にする。現在のcandidate inputは `0` 件で、置換は未実行。

- required local input count: `5`
- source episode pack: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack`
- cue map: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/edit_slice_to_ymm4_cue_map.json`
- next gate: `provide_verified_local_source_and_transcript`

Allowed material: ローカルに存在し、由来と照合方法を書ける source/transcript/receipt だけ。

Forbidden material: live fetch、scraping、外部media download、OAuth/API/payment、public-ready承認、YMM4実行結果は対象外。
