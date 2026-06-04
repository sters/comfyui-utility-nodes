from typing import Any

import pytest

from nodes.danbooru_bad_tags import (
    DanbooruBadBody,
    DanbooruBadGeneral,
    DanbooruBadHeadFace,
    DanbooruBadLimbs,
    DanbooruBadNSFW,
    _BadTagsBase,
)

ALL_NODES: list[type[_BadTagsBase]] = [
    DanbooruBadGeneral,
    DanbooruBadHeadFace,
    DanbooruBadBody,
    DanbooruBadLimbs,
    DanbooruBadNSFW,
]


def _prompt(result: dict[str, Any]) -> str:
    assert result["ui"]["text"] == result["result"]
    return str(result["result"][0])


@pytest.mark.parametrize("cls", ALL_NODES)
def test_all_on_includes_every_tag_in_order(cls: type[_BadTagsBase]) -> None:
    node = cls()
    tags = dict.fromkeys(cls.TAGS, True)
    out = _prompt(node.build(", ", "", **tags))
    assert out == ", ".join(cls.TAGS)


@pytest.mark.parametrize("cls", ALL_NODES)
def test_all_off_returns_empty(cls: type[_BadTagsBase]) -> None:
    node = cls()
    tags = dict.fromkeys(cls.TAGS, False)
    out = _prompt(node.build(", ", "", **tags))
    assert out == ""


@pytest.mark.parametrize("cls", ALL_NODES)
def test_default_input_types_all_default_true(cls: type[_BadTagsBase]) -> None:
    spec = cls.INPUT_TYPES()
    for tag in cls.TAGS:
        meta = spec["required"][tag]
        assert meta[0] == "BOOLEAN"
        assert meta[1]["default"] is True


@pytest.mark.parametrize("cls", ALL_NODES)
def test_output_node_flag(cls: type[_BadTagsBase]) -> None:
    assert cls.OUTPUT_NODE is True


def test_general_specific_tags() -> None:
    assert "bad_anatomy" in DanbooruBadGeneral.TAGS
    assert "artistic_error" in DanbooruBadGeneral.TAGS


def test_some_off() -> None:
    node = DanbooruBadHeadFace()
    tags = dict.fromkeys(DanbooruBadHeadFace.TAGS, True)
    tags["extra_horns"] = False
    tags["extra_tusks"] = False
    out = _prompt(node.build(", ", "", **tags))
    parts = out.split(", ")
    assert "extra_horns" not in parts
    assert "extra_tusks" not in parts
    assert "bad_face" in parts
    assert len(parts) == len(DanbooruBadHeadFace.TAGS) - 2


def test_extra_appended() -> None:
    node = DanbooruBadGeneral()
    tags = dict.fromkeys(DanbooruBadGeneral.TAGS, False)
    tags["bad_anatomy"] = True
    out = _prompt(node.build(", ", "lowres, blurry", **tags))
    assert out == "bad_anatomy, lowres, blurry"


def test_custom_separator_escape() -> None:
    node = DanbooruBadLimbs()
    tags = dict.fromkeys(DanbooruBadLimbs.TAGS, False)
    tags["bad_hands"] = True
    tags["wrong_hand"] = True
    out = _prompt(node.build("\\n", "", **tags))
    assert out == "bad_hands\nwrong_hand"


def test_no_tag_overlap_between_groups() -> None:
    seen: set[str] = set()
    for cls in ALL_NODES:
        for tag in cls.TAGS:
            assert tag not in seen, f"duplicate tag across groups: {tag}"
            seen.add(tag)


def test_total_tag_count() -> None:
    total = sum(len(cls.TAGS) for cls in ALL_NODES)
    assert total == 52
