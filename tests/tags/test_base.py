from typing import Any, ClassVar

from nodes.tags._base import TagNodeBase


class _SampleNode(TagNodeBase):
    TAGS: ClassVar[tuple[str, ...]] = (
        "alpha",
        "beta",
        "gamma",
        "with-hyphen",
        "with_apostrophe's",
    )


class _DefaultTrueNode(TagNodeBase):
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    TAGS: ClassVar[tuple[str, ...]] = ("x", "y")


def _prompt(result: dict[str, Any]) -> str:
    assert result["ui"]["text"] == result["result"]
    return str(result["result"][0])


def test_class_constants() -> None:
    assert TagNodeBase.RETURN_TYPES == ("STRING",)
    assert TagNodeBase.RETURN_NAMES == ("prompt",)
    assert TagNodeBase.FUNCTION == "build"
    assert TagNodeBase.CATEGORY == "utility/text"
    assert TagNodeBase.OUTPUT_NODE is True


def test_input_types_has_separator_and_preset() -> None:
    spec = _SampleNode.INPUT_TYPES()
    assert spec["required"]["separator"][0] == "STRING"
    options, meta = spec["required"]["preset"]
    assert options == ["custom", "all_on", "all_off", "invert"]
    assert meta["default"] == "custom"


def test_input_types_boolean_default_false() -> None:
    spec = _SampleNode.INPUT_TYPES()
    for tag in _SampleNode.TAGS:
        kind, meta = spec["required"][tag]
        assert kind == "BOOLEAN"
        assert meta["default"] is False


def test_input_types_boolean_default_true_when_overridden() -> None:
    spec = _DefaultTrueNode.INPUT_TYPES()
    for tag in _DefaultTrueNode.TAGS:
        assert spec["required"][tag][1]["default"] is True


def test_input_types_extra_is_optional_multiline_string() -> None:
    spec = _SampleNode.INPUT_TYPES()
    kind, meta = spec["optional"]["extra"]
    assert kind == "STRING"
    assert meta["multiline"] is True


def test_build_no_tags_selected_returns_empty() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    assert _prompt(node.build(", ", "", **tags)) == ""


def test_build_custom_honors_booleans_and_preserves_order() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["gamma"] = True
    tags["alpha"] = True
    assert _prompt(node.build(", ", "", **tags)) == "alpha, gamma"


def test_build_all_on_ignores_booleans() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    assert _prompt(node.build(", ", "", preset="all_on", **tags)) == ", ".join(_SampleNode.TAGS)


def test_build_all_off_ignores_booleans() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, True)
    assert _prompt(node.build(", ", "", preset="all_off", **tags)) == ""


def test_build_invert_flips_booleans() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["alpha"] = True
    out = _prompt(node.build(", ", "", preset="invert", **tags))
    expected = [t for t in _SampleNode.TAGS if t != "alpha"]
    assert out == ", ".join(expected)


def test_build_extra_is_appended_after_tags() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["beta"] = True
    assert _prompt(node.build(", ", "1girl", **tags)) == "beta, 1girl"


def test_build_extra_is_stripped() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    assert _prompt(node.build(", ", "   \n\n  ", **tags)) == ""


def test_build_hyphenated_kwarg() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["with-hyphen"] = True
    assert _prompt(node.build(", ", "", **tags)) == "with-hyphen"


def test_build_apostrophe_kwarg() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["with_apostrophe's"] = True
    assert _prompt(node.build(", ", "", **tags)) == "with_apostrophe's"


def test_build_separator_escape_sequences_decoded() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["alpha"] = True
    tags["beta"] = True
    assert _prompt(node.build(r"\n", "", **tags)) == "alpha\nbeta"


def test_build_empty_separator_falls_back_to_comma_space() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["alpha"] = True
    tags["beta"] = True
    assert _prompt(node.build("", "", **tags)) == "alpha, beta"


def test_build_returns_ui_and_result_with_same_value() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["alpha"] = True
    out = node.build(", ", "", **tags)
    assert out["ui"]["text"] == ("alpha",)
    assert out["result"] == ("alpha",)
