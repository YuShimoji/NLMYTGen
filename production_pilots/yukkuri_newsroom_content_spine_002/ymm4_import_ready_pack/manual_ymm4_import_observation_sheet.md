# Episode 002 YMM4観測前確認チェック

目的: YMM4観測前の確認チェック。Episode 002限定で、3 scenes / 9 cues のimport-ready表示がoperatorに読めるかを見る。
範囲: cue順、仮timing、VoiceItem/subtitle、visual/overlay、placeholder/diagnostic境界の観測準備だけ。
対象外: render承認、production `.ymmp` write、real input replacement、rights承認、public承認、final thumbnail承認、upload。
次に残す成果物: 明示的なgateが開いた場合だけ `YMM4 observation readback` を別artifactとして作る。

1. cue順はS1 -> S2 -> S3の流れで読め、行順の入れ替わりを検出できるか。
2. VoiceItem/subtitleの対応は、speaker、cue、placeholder text statusをoperatorが追える粒度になっているか。
3. visual templateとoverlay/citationの指示は、final素材ではないplaceholderとして誤解なく読めるか。
4. real source、rights、final thumbnailの判断が、diagnostic/placeholder assetから明確に分離されているか。
5. renderより前に残るblockerが、real input、YMM4 timing/readback、rights/public approval、final thumbnail approvalのどれか一つ以上として記録できるか。
