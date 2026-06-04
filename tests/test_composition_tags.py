from typing import Any

import pytest

from nodes.composition_tags import (
    CompositionAngle,
    CompositionCrop,
    CompositionFocus,
    CompositionFraming,
    CompositionMultiView,
    _CompositionBase,
)

ALL_NODES: list[type[_CompositionBase]] = [
    CompositionAngle,
    CompositionFraming,
    CompositionCrop,
    CompositionFocus,
    CompositionMultiView,
]


def _prompt(result: dict[str, Any]) -> str:
    assert result["ui"]["text"] == result["result"]
    return str(result["result"][0])


@pytest.mark.parametrize("cls", ALL_NODES)
def test_default_input_types_all_default_false(cls: type[_CompositionBase]) -> None:
    spec = cls.INPUT_TYPES()
    for tag in cls.TAGS:
        meta = spec["required"][tag]
        assert meta[0] == "BOOLEAN"
        assert meta[1]["default"] is False


@pytest.mark.parametrize("cls", ALL_NODES)
def test_output_node_flag(cls: type[_CompositionBase]) -> None:
    assert cls.OUTPUT_NODE is True


@pytest.mark.parametrize("cls", ALL_NODES)
def test_no_tags_selected_returns_empty(cls: type[_CompositionBase]) -> None:
    node = cls()
    tags = dict.fromkeys(cls.TAGS, False)
    out = _prompt(node.build(", ", "", **tags))
    assert out == ""


@pytest.mark.parametrize("cls", ALL_NODES)
def test_all_tags_selected_preserves_order(cls: type[_CompositionBase]) -> None:
    node = cls()
    tags = dict.fromkeys(cls.TAGS, True)
    out = _prompt(node.build(", ", "", **tags))
    assert out == ", ".join(cls.TAGS)


def test_angle_pick_one() -> None:
    node = CompositionAngle()
    tags = dict.fromkeys(CompositionAngle.TAGS, False)
    tags["from_above"] = True
    out = _prompt(node.build(", ", "", **tags))
    assert out == "from_above"


def test_angle_pick_multiple() -> None:
    node = CompositionAngle()
    tags = dict.fromkeys(CompositionAngle.TAGS, False)
    tags["from_behind"] = True
    tags["dutch_angle"] = True
    out = _prompt(node.build(", ", "", **tags))
    assert out == "dutch_angle, from_behind"


def test_hyphenated_tag_kwarg() -> None:
    node = CompositionFraming()
    tags = dict.fromkeys(CompositionFraming.TAGS, False)
    tags["close-up"] = True
    out = _prompt(node.build(", ", "", **tags))
    assert out == "close-up"


def test_extra_appended() -> None:
    node = CompositionFocus()
    tags = dict.fromkeys(CompositionFocus.TAGS, False)
    tags["eye_focus"] = True
    out = _prompt(node.build(", ", "1girl", **tags))
    assert out == "eye_focus, 1girl"


def test_no_overlap_between_groups() -> None:
    seen: set[str] = set()
    for cls in ALL_NODES:
        for tag in cls.TAGS:
            assert tag not in seen, f"duplicate tag across groups: {tag}"
            seen.add(tag)


def test_total_tag_count() -> None:
    total = sum(len(cls.TAGS) for cls in ALL_NODES)
    assert total == 64
