from typing import Any, ClassVar

from nodes.tags._base import TAGS_TYPE, TaggedSelection, TagNodeBase, category_for_module


class _SampleNode(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "test.sample"
    LAYER: ClassVar[str] = "test"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS: ClassVar[tuple[str, ...]] = (
        "alpha",
        "beta",
        "gamma",
        "with-hyphen",
        "with_apostrophe's",
    )


class _MutexNode(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "test.mutex"
    LAYER: ClassVar[str] = "test"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS: ClassVar[tuple[str, ...]] = ("a", "b", "c")


class _DefaultTrueNode(TagNodeBase):
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    CATEGORY_ID: ClassVar[str] = "test.default_true"
    LAYER: ClassVar[str] = "test"
    TAGS: ClassVar[tuple[str, ...]] = ("x", "y")


def _result(out: dict[str, Any]) -> tuple[str, tuple[TaggedSelection, ...]]:
    preview = out["ui"]["text"][0]
    bundle = tuple(out["result"][0])
    return str(preview), bundle


def test_class_constants() -> None:
    assert TagNodeBase.RETURN_TYPES == (TAGS_TYPE,)
    assert TagNodeBase.RETURN_NAMES == ("bundle",)
    assert TagNodeBase.FUNCTION == "build"
    assert TagNodeBase.CATEGORY == "UtilityNodes"
    assert TagNodeBase.OUTPUT_NODE is True


def test_category_for_module_maps_package_path_to_menu() -> None:
    assert category_for_module("nodes.tags.merge") == "UtilityNodes/TagMaster"
    assert category_for_module("nodes.tags.sources.body.hair") == "UtilityNodes/TagMaster/Body"
    assert category_for_module("nodes.tags.sources.body.face.eyes") == "UtilityNodes/TagMaster/Body/Face"
    assert category_for_module("nodes.tags.sources.nsfw.act") == "UtilityNodes/TagMaster/NSFW"
    assert category_for_module("nodes.image.aspect_ratio") == "UtilityNodes/Image"
    assert category_for_module("nodes.text.text_concat") == "UtilityNodes/Text"


def test_category_for_module_handles_comfyui_package_prefix() -> None:
    # ComfyUI imports the pack under its directory name as the top-level
    # package, prefixing every node's __module__. The category must still
    # resolve identically to the bare `nodes.*` form used in tests.
    assert category_for_module("comfyui-utility-nodes.nodes.tags.merge") == "UtilityNodes/TagMaster"
    assert category_for_module("comfyui-utility-nodes.nodes.tags.sources.body.hair") == "UtilityNodes/TagMaster/Body"
    assert category_for_module("custom_nodes.comfyui_utility_nodes.nodes.image.aspect_ratio") == "UtilityNodes/Image"


def test_subclass_inherits_module_derived_category() -> None:
    # _SampleNode lives in the test module (not under `nodes.`), so it falls
    # back to the bare root rather than a TagMaster subpath.
    assert _SampleNode.CATEGORY == "UtilityNodes"


def test_input_types_has_invert_and_no_separator() -> None:
    spec = _SampleNode.INPUT_TYPES()
    assert "separator" not in spec["required"]
    kind, meta = spec["required"]["invert"]
    assert kind == "BOOLEAN"
    assert meta["default"] is False


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


def test_build_no_tags_selected_returns_empty_string_and_empty_bundle() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    prompt, bundle = _result(node.build("", **tags))
    assert prompt == ""
    assert bundle == ()


def test_build_custom_honors_booleans_and_preserves_order() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["gamma"] = True
    tags["alpha"] = True
    prompt, bundle = _result(node.build("", **tags))
    assert prompt == "alpha, gamma"
    assert bundle == (
        TaggedSelection(
            category="test.sample",
            layer="test",
            tags=("alpha", "gamma"),
            mutex_within=False,
        ),
    )


def test_build_invert_flips_booleans() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["alpha"] = True
    prompt, bundle = _result(node.build("", invert=True, **tags))
    expected = tuple(t for t in _SampleNode.TAGS if t != "alpha")
    assert prompt == ", ".join(expected)
    assert bundle[0].tags == expected


def test_build_invert_false_keeps_selection() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["alpha"] = True
    prompt, bundle = _result(node.build("", invert=False, **tags))
    assert prompt == "alpha"
    assert bundle[0].tags == ("alpha",)


def test_build_extra_emitted_as_separate_selection() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["beta"] = True
    prompt, bundle = _result(node.build("1girl", **tags))
    assert prompt == "beta, 1girl"
    assert bundle == (
        TaggedSelection(
            category="test.sample",
            layer="test",
            tags=("beta",),
            mutex_within=False,
        ),
        TaggedSelection(
            category="extra",
            layer="extra",
            tags=("1girl",),
            mutex_within=False,
        ),
    )


def test_build_extra_is_stripped() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    prompt, bundle = _result(node.build("   \n\n  ", **tags))
    assert prompt == ""
    assert bundle == ()


def test_build_hyphenated_kwarg() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["with-hyphen"] = True
    prompt, _ = _result(node.build("", **tags))
    assert prompt == "with-hyphen"


def test_build_apostrophe_kwarg() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["with_apostrophe's"] = True
    prompt, _ = _result(node.build("", **tags))
    assert prompt == "with_apostrophe's"


def test_build_preview_joins_with_comma_space() -> None:
    node = _SampleNode()
    tags = dict.fromkeys(_SampleNode.TAGS, False)
    tags["alpha"] = True
    tags["beta"] = True
    prompt, _ = _result(node.build("", **tags))
    assert prompt == "alpha, beta"


def test_build_bundle_carries_mutex_flag() -> None:
    node = _MutexNode()
    tags = dict.fromkeys(_MutexNode.TAGS, False)
    tags["b"] = True
    _, bundle = _result(node.build("", **tags))
    assert bundle[0].mutex_within is True
    assert bundle[0].category == "test.mutex"
