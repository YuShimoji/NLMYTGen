"""IR 品質 gate テスト."""

from __future__ import annotations

from src.pipeline.ir_validate import validate_ir


def _make_ir(utterances, sections=None):
    if sections is None:
        sections = [{"section_id": "S1", "start_index": 1,
                     "end_index": len(utterances), "default_face": "serious",
                     "default_bg": "bg1"}]
    return {
        "ir_version": "1.0", "video_id": "test",
        "macro": {"sections": sections},
        "utterances": utterances,
    }


def _utt(index, face="serious", idle=None, section="S1"):
    d = {"index": index, "speaker": "sp", "text": "t",
         "section_id": section, "face": face}
    if idle:
        d["idle_face"] = idle
    return d


class TestUnknownLabels:
    def test_unknown_label_is_error(self):
        ir = _make_ir([_utt(1, "neutral"), _utt(2, "serious")])
        vr = validate_ir(ir, known_face_labels={"serious", "smile"})
        assert vr.has_errors
        assert "neutral" in vr.unknown_labels

    def test_all_known_no_error(self):
        ir = _make_ir([_utt(1, "serious"), _utt(2, "smile")])
        vr = validate_ir(ir, known_face_labels={"serious", "smile"})
        assert not vr.has_errors
        assert not vr.unknown_labels

    def test_no_known_labels_skips_check(self):
        ir = _make_ir([_utt(1, "anything")])
        vr = validate_ir(ir, known_face_labels=None)
        assert not vr.has_errors


class TestSeriousThreshold:
    def test_over_threshold_warns(self):
        utts = [_utt(i, "serious") for i in range(1, 6)]
        ir = _make_ir(utts)
        vr = validate_ir(ir, serious_threshold=0.40)
        warnings = [w for w in vr.warnings if "serious" in w and "%" in w]
        assert len(warnings) == 1

    def test_under_threshold_no_warning(self):
        utts = [_utt(1, "serious"), _utt(2, "smile"),
                _utt(3, "thinking"), _utt(4, "angry"), _utt(5, "sad")]
        ir = _make_ir(utts)
        vr = validate_ir(ir, serious_threshold=0.40)
        warnings = [w for w in vr.warnings if "serious" in w and "%" in w]
        assert len(warnings) == 0


class TestConsecutiveRun:
    def test_long_run_warns(self):
        utts = [_utt(i, "serious") for i in range(1, 7)]
        ir = _make_ir(utts)
        vr = validate_ir(ir, max_consecutive_run=4)
        warnings = [w for w in vr.warnings if "consecutive" in w]
        assert len(warnings) == 1
        assert vr.longest_face_run == 6

    def test_short_run_no_warning(self):
        utts = [_utt(1, "serious"), _utt(2, "serious"),
                _utt(3, "smile"), _utt(4, "serious")]
        ir = _make_ir(utts)
        vr = validate_ir(ir, max_consecutive_run=4)
        warnings = [w for w in vr.warnings if "consecutive" in w]
        assert len(warnings) == 0


class TestIdleFace:
    def test_no_idle_face_warns(self):
        ir = _make_ir([_utt(1), _utt(2)])
        vr = validate_ir(ir)
        warnings = [w for w in vr.warnings if "idle_face" in w]
        assert len(warnings) == 1

    def test_has_idle_face_no_warning(self):
        ir = _make_ir([_utt(1, idle="serious"), _utt(2, idle="serious")])
        vr = validate_ir(ir)
        warnings = [w for w in vr.warnings if "idle_face" in w]
        assert len(warnings) == 0


class TestBgLabels:
    def test_no_bg_warns(self):
        ir = _make_ir([_utt(1)], sections=[
            {"section_id": "S1", "start_index": 1, "end_index": 1,
             "default_face": "serious"}
        ])
        vr = validate_ir(ir)
        warnings = [w for w in vr.warnings if "bg" in w]
        assert len(warnings) == 1

    def test_has_bg_no_warning(self):
        ir = _make_ir([_utt(1)])
        vr = validate_ir(ir)
        warnings = [w for w in vr.warnings if "no bg" in w]
        assert len(warnings) == 0


class TestRowStart:
    def test_no_row_start_info(self):
        ir = _make_ir([_utt(1)])
        vr = validate_ir(ir)
        info = [i for i in vr.info if "row_start" in i]
        assert len(info) == 1

    def test_has_row_start_no_info(self):
        ir = _make_ir([_utt(1)])
        ir["utterances"][0]["row_start"] = 1
        ir["utterances"][0]["row_end"] = 1
        vr = validate_ir(ir)
        info = [i for i in vr.info if "row_start" in i]
        assert len(info) == 0
