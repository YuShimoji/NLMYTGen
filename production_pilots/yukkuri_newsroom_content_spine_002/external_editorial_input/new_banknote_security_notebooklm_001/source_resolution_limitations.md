# Source Resolution Limitations

- S04は同名の現行公式PDFへ解決したが、凍結snapshotがtitleのみなのでNotebookLM投入時のbyte版と同一とは証明していない。
- S05のexact titleと`PDF 572KB`に一致する現行assetは見つからず、exact identityは未解決のまま。現行公式HTMLをofficial equivalentとして別登録した。
- `publication_date`は資料が公開・刊行日と明示した場合だけに限定した。HTMLの`Last-Modified`、page metadataのdate、可視の更新日、出来事の日、取得時刻は、それぞれbasis付きの別fieldへ分けた。
- 画像ベースPDFはOCRせず、既存text extractionの可否確認とpage renderの目視照合だけを行った。
- source body、長い引用、private notebook識別子はtracked artifactへ含めていない。
