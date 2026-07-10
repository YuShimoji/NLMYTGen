# Episode 002 YMM4観測前確認チェック

目的: YMM4観測前の確認チェック。Episode 002限定で、3 scenes / 9 cues のimport-ready表示がoperatorに読めるかを見る。
範囲: derived CSVのcue順、VoiceItem、character binding、linked subtitle text、timing order、CSV responsibility boundaryだけ。
対象外: render承認、production `.ymmp` write、real input replacement、rights承認、public承認、final thumbnail承認、upload。
次に残す成果物: 明示的なgateが開いた場合だけ `YMM4 observation readback` を別artifactとして作る。

1. derived CSV import後、cue順がS1 -> S2 -> S3、csv_row_1 -> csv_row_9として維持されるか。
2. VoiceItemが9件で、欠落・重複・順序入れ替わりがないか。
3. mapping dialogが出ず、れいむ行はゆっくり霊夢、まりさ行はゆっくり魔理沙として結び付くか。
4. linked subtitle textとrow orderがcanonical CSVと一致し、timing orderが維持されるか（duration再計算はinformational）。
5. CSV importの責務がVoiceItem + linked subtitleに限定され、ImageItem/独立TextItemのdiagnostic projectがnot_authorized/not_attemptedのままか。
