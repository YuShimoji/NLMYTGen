"""StructuredScript 契約テスト。"""

import pytest

from src.contracts.structured_script import Utterance, StructuredScript


def test_utterance_is_frozen():
    """Utterance は immutable。"""
    u = Utterance(speaker="Host1", text="hello")
    with pytest.raises(AttributeError):
        u.speaker = "Host2"  # type: ignore[misc]


def test_empty_utterances_raises():
    """空の utterances は ValueError。"""
    with pytest.raises(ValueError, match="must not be empty"):
        StructuredScript(utterances=())


def test_empty_speaker_or_text_raises():
    """空の speaker/text は ValueError。"""
    with pytest.raises(ValueError, match="speaker must not be empty"):
        Utterance(speaker="", text="hello")

    with pytest.raises(ValueError, match="text must not be empty"):
        Utterance(speaker="Host1", text="")

    with pytest.raises(ValueError, match="speaker must not be empty"):
        Utterance(speaker="   ", text="hello")
