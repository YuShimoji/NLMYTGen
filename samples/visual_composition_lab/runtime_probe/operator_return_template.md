# Operator return template

次の最大3項目だけを返してください。

1. `result`: `pass | fail | uncertain`
2. `operator_result path`: batchが表示したignored JSON path
3. `error`: failure時だけ、batchが表示したerror 1件

観測回答はresult JSON内の次の3 fieldに個別保存されます。

- `subtitle_readability_nonoverlap`
- `image_visibility_crop_anchor`
- `text_visibility_wrapping_anchor`
