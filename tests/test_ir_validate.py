"""IR 品質 gate テスト."""

from __future__ import annotations

from src.pipeline.ir_validate import extract_prompt_face_labels, validate_ir


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


def _utt(index, face="serious", idle=None, section="S1", speaker="sp", slot=None):
    d = {"index": index, "speaker": "sp", "text": "t",
         "section_id": section, "face": face}
    d["speaker"] = speaker
    if idle:
        d["idle_face"] = idle
    if slot:
        d["slot"] = slot
    return d


def _utt_with_timeline(
    index,
    *,
    overlay=None,
    se_label=None,
):
    d = _utt(index)
    if overlay:
        d["overlay"] = overlay
    if se_label:
        d["se"] = se_label
    return d


class TestUnknownLabels:
    def test_unknown_label_is_error(self):
        ir = _make_ir([_utt(1, "neutral"), _utt(2, "serious")])
        vr = validate_ir(ir, known_face_labels={"serious", "smile"})
        assert vr.has_errors
        assert "neutral" in vr.unknown_labels

    def test_unknown_idle_face_label_is_error(self):
        ir = _make_ir([_utt(1, "serious", idle="neutral")])
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


class TestCharFaceCoverage:
    """キャラ別 face カバレッジチェック."""

    def _utt2(self, index, speaker, face, idle=None, section="S1"):
        d = {"index": index, "speaker": speaker, "text": "t",
             "section_id": section, "face": face}
        if idle:
            d["idle_face"] = idle
        return d

    def test_missing_face_for_character_is_error(self):
        """霊夢に surprised がないケース: error で止まる."""
        ir = _make_ir([
            self._utt2(1, "まりさ", "surprised", idle="serious"),
            self._utt2(2, "れいむ", "surprised"),
        ])
        char_face = {
            "まりさ": {"serious", "smile", "surprised"},
            "れいむ": {"serious", "smile"},  # surprised 欠落
        }
        vr = validate_ir(ir, char_face_map=char_face)
        errors = [e for e in vr.errors if "surprised" in e and "れいむ" in e]
        assert len(errors) == 1
        assert "FACE_ACTIVE_GAP" in errors[0]

    def test_idle_face_missing_for_non_speaker_is_error(self):
        """まりさが発話中、idle_face=surprised が霊夢にないケース."""
        ir = _make_ir([
            self._utt2(1, "まりさ", "serious", idle="surprised"),
        ])
        char_face = {
            "まりさ": {"serious", "surprised"},
            "れいむ": {"serious", "smile"},  # surprised 欠落
        }
        vr = validate_ir(ir, char_face_map=char_face)
        errors = [e for e in vr.errors if "surprised" in e and "れいむ" in e]
        assert len(errors) == 1

    def test_all_covered_no_warning(self):
        """両キャラに全ラベルがある場合: warning なし."""
        ir = _make_ir([
            self._utt2(1, "まりさ", "surprised", idle="smile"),
            self._utt2(2, "れいむ", "smile", idle="surprised"),
        ])
        char_face = {
            "まりさ": {"serious", "smile", "surprised"},
            "れいむ": {"serious", "smile", "surprised"},
        }
        vr = validate_ir(ir, char_face_map=char_face)
        coverage_errors = [e for e in vr.errors if "FACE_ACTIVE_GAP" in e]
        assert len(coverage_errors) == 0

    def test_none_char_face_map_skips_check(self):
        """char_face_map=None の場合はチェックしない."""
        ir = _make_ir([
            self._utt2(1, "れいむ", "surprised"),
        ])
        vr = validate_ir(ir, char_face_map=None)
        coverage_errors = [e for e in vr.errors if "FACE_ACTIVE_GAP" in e]
        assert len(coverage_errors) == 0

    def test_speaker_not_in_map_ignored(self):
        """face_map にないキャラの発話はチェックしない."""
        ir = _make_ir([
            self._utt2(1, "unknown", "surprised"),
        ])
        char_face = {
            "まりさ": {"serious", "surprised"},
        }
        vr = validate_ir(ir, char_face_map=char_face)
        coverage_errors = [e for e in vr.errors if "FACE_ACTIVE_GAP" in e]
        assert len(coverage_errors) == 0


class TestPromptFaceContract:
    def test_extract_prompt_face_labels(self):
        prompt = """
### face (表情 -- 必ず以下から選択)
serious, smile, surprised, thinking, angry, sad

**face 分布制約:**
"""
        labels = extract_prompt_face_labels(prompt)
        assert labels == {
            "serious", "smile", "surprised",
            "thinking", "angry", "sad",
        }

    def test_used_label_outside_prompt_is_error(self):
        ir = _make_ir([_utt(1, "neutral")])
        vr = validate_ir(
            ir,
            known_face_labels={"neutral", "serious"},
            prompt_face_labels={"serious", "smile"},
        )
        errors = [e for e in vr.errors if "PROMPT_FACE_DRIFT" in e]
        assert len(errors) == 1

    def test_prompt_palette_drift_warns(self):
        ir = _make_ir([_utt(1, "serious")])
        vr = validate_ir(
            ir,
            known_face_labels={"serious", "smile", "thinking"},
            prompt_face_labels={"serious", "smile", "sad"},
        )
        gap_warnings = [w for w in vr.warnings if "FACE_PROMPT_PALETTE_GAP" in w]
        extra_warnings = [w for w in vr.warnings if "FACE_PROMPT_PALETTE_EXTRA" in w]
        assert len(gap_warnings) == 1
        assert len(extra_warnings) == 1
        assert vr.prompt_palette_missing_labels == ["sad"]
        assert vr.palette_only_labels == ["thinking"]

    def test_latent_palette_gap_report_warns(self):
        ir = _make_ir([{
            "index": 1,
            "speaker": "まりさ",
            "text": "t",
            "section_id": "S1",
            "face": "serious",
        }])
        char_face = {
            "まりさ": {"serious", "smile"},
            "れいむ": {"serious"},
        }
        vr = validate_ir(
            ir,
            known_face_labels={"serious", "smile"},
            char_face_map=char_face,
            prompt_face_labels={"serious", "smile", "surprised"},
        )
        warnings = [w for w in vr.warnings if "FACE_LATENT_GAP" in w]
        assert len(warnings) == 2
        assert vr.latent_face_gaps["まりさ"] == ["surprised"]
        assert vr.latent_face_gaps["れいむ"] == ["smile", "surprised"]


class TestSlotValidation:
    def test_unknown_slot_is_error(self):
        ir = _make_ir([_utt(1, slot="left"), _utt(2, slot="sky")])
        vr = validate_ir(ir, known_slot_labels={"left", "right"})
        assert vr.has_errors
        assert vr.unknown_slot_labels == ["sky"]

    def test_character_slot_drift_is_error(self):
        ir = _make_ir([
            _utt(1, speaker="marisa", slot="left"),
            _utt(2, speaker="marisa", slot="right"),
        ])
        vr = validate_ir(ir, known_slot_labels={"left", "right"})
        errors = [e for e in vr.errors if "SLOT_CHARACTER_DRIFT" in e]
        assert len(errors) == 1

    def test_slot_default_drift_is_error(self):
        ir = _make_ir([
            _utt(1, speaker="marisa", slot="right"),
        ])
        vr = validate_ir(
            ir,
            known_slot_labels={"left", "right"},
            char_default_slots={"marisa": "left"},
        )
        errors = [e for e in vr.errors if "SLOT_DEFAULT_DRIFT" in e]
        assert len(errors) == 1

    def test_slot_registry_gap_is_error(self):
        ir = _make_ir([
            _utt(1, speaker="marisa", slot="left"),
        ])
        vr = validate_ir(
            ir,
            known_slot_labels={"left", "right"},
            char_default_slots={"marisa": "center"},
        )
        errors = [e for e in vr.errors if "SLOT_REGISTRY_GAP" in e]
        assert len(errors) == 1


class TestTimelineLabelValidation:
    def test_unknown_overlay_is_error(self):
        ir = _make_ir([_utt_with_timeline(1, overlay="flash_red")])
        vr = validate_ir(ir, known_overlay_labels={"arrow_red"})
        assert vr.has_errors
        assert vr.unknown_overlay_labels == ["flash_red"]

    def test_unknown_se_is_error(self):
        ir = _make_ir([_utt_with_timeline(1, se_label="surprise")])
        vr = validate_ir(ir, known_se_labels={"click"})
        assert vr.has_errors
        assert vr.unknown_se_labels == ["surprise"]

    def test_known_timeline_labels_pass(self):
        ir = _make_ir([_utt_with_timeline(1, overlay="arrow_red", se_label="click")])
        vr = validate_ir(
            ir,
            known_overlay_labels={"arrow_red"},
            known_se_labels={"click"},
        )
        assert not [e for e in vr.errors if "OVERLAY_UNKNOWN_LABEL" in e]
        assert not [e for e in vr.errors if "SE_UNKNOWN_LABEL" in e]


class TestRowRangeValidation:
    def test_partial_row_range_is_error(self):
        ir = _make_ir([_utt(1), _utt(2)])
        ir["utterances"][0]["row_start"] = 1
        vr = validate_ir(ir)
        errors = [e for e in vr.errors if "ROW_RANGE_MISSING" in e]
        assert len(errors) == 2

    def test_invalid_row_range_is_error(self):
        ir = _make_ir([_utt(1)])
        ir["utterances"][0]["row_start"] = 3
        ir["utterances"][0]["row_end"] = 1
        vr = validate_ir(ir)
        errors = [e for e in vr.errors if "ROW_RANGE_INVALID" in e]
        assert len(errors) == 1

    def test_overlapping_row_range_is_error(self):
        ir = _make_ir([_utt(1), _utt(2)])
        ir["utterances"][0]["row_start"] = 1
        ir["utterances"][0]["row_end"] = 2
        ir["utterances"][1]["row_start"] = 2
        ir["utterances"][1]["row_end"] = 3
        vr = validate_ir(ir)
        errors = [e for e in vr.errors if "ROW_RANGE_OVERLAP" in e]
        assert len(errors) == 1


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
