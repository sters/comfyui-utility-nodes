from typing import Any

from nodes.tags._base import TaggedSelection
from nodes.tags.merge import TagsMerge


def _run(**kwargs: Any) -> tuple[str, str, tuple[TaggedSelection, ...]]:
    out = TagsMerge().merge(", ", **kwargs)
    return (
        str(out["result"][0]),
        str(out["result"][1]),
        tuple(out["result"][2]),
    )


def _sel(category: str, tags: tuple[str, ...], **kw: Any) -> TaggedSelection:
    return TaggedSelection(
        category=category,
        layer=kw.get("layer", "test"),
        tags=tags,
        mutex_within=kw.get("mutex_within", False),
    )


def test_merge_concatenates_in_input_order() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("a", ("x",)),),
        bundle_2=(_sel("b", ("y", "z")),),
    )
    assert prompt == "x, y, z"
    assert warnings == ""


def test_merge_empty_inputs_yield_empty_prompt() -> None:
    prompt, warnings, bundle = _run()
    assert (prompt, warnings, bundle) == ("", "", ())


def test_merge_extra_is_appended() -> None:
    prompt, _, _ = _run(extra="1girl", bundle_1=(_sel("a", ("x",)),))
    assert prompt == "x, 1girl"


def test_mutex_within_drops_second_selection_with_same_category() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("hair.length", ("long_hair",), mutex_within=True),),
        bundle_2=(_sel("hair.length", ("short_hair",), mutex_within=True),),
    )
    assert prompt == "long_hair"
    assert "mutex:" in warnings
    assert "short_hair" in warnings


def test_mutex_within_keeps_first_tag_of_a_multi_tag_selection() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(
            _sel(
                "hair.length",
                ("long_hair", "short_hair"),
                mutex_within=True,
            ),
        ),
    )
    assert prompt == "long_hair"
    assert "short_hair" in warnings


def test_non_mutex_categories_allow_multiple_selections() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.marks.moles", ("mole_under_eye",)),),
        bundle_2=(_sel("body.marks.moles", ("freckles",)),),
    )
    assert prompt == "mole_under_eye, freckles"
    assert warnings == ""


def test_nude_overrides_drop_clothing_layer() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.exposure", ("nude",), layer="exposure"),),
        bundle_2=(_sel("clothing.tops", ("shirt",), layer="clothing"),),
        bundle_3=(_sel("clothing.footwear", ("boots",), layer="clothing"),),
    )
    assert prompt == "nude"
    assert "clothing.tops" in warnings
    assert "clothing.footwear" in warnings


def test_barefoot_only_drops_footwear() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.feet.anatomy", ("barefoot",)),),
        bundle_2=(_sel("clothing.footwear", ("sneakers",)),),
        bundle_3=(_sel("clothing.tops", ("shirt",)),),
    )
    assert "sneakers" not in prompt
    assert "shirt" in prompt
    assert "barefoot" in prompt
    assert "clothing.footwear" in warnings


def test_topless_drops_tops_and_underwear() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.state", ("topless",)),),
        bundle_2=(_sel("clothing.tops", ("shirt",)),),
        bundle_3=(_sel("clothing.underwear", ("bra",)),),
        bundle_4=(_sel("clothing.bottoms", ("skirt",)),),
    )
    assert "shirt" not in prompt
    assert "bra" not in prompt
    assert "skirt" in prompt
    assert "topless" in prompt


def test_extra_selection_is_not_subject_to_override() -> None:
    prompt, _, _ = _run(
        bundle_1=(
            _sel("body.exposure", ("nude",), layer="exposure"),
            _sel("extra", ("1girl",), layer="extra"),
        ),
        bundle_2=(_sel("clothing.tops", ("shirt",), layer="clothing"),),
    )
    assert "shirt" not in prompt
    assert "1girl" in prompt


def test_topless_keeps_panties_and_garter_belt() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.state", ("topless",)),),
        bundle_2=(_sel("clothing.underwear", ("bra", "panties", "garter_belt")),),
    )
    assert "bra" not in prompt
    assert "panties" in prompt
    assert "garter_belt" in prompt


def test_bottomless_drops_panties_but_keeps_bra() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.state", ("bottomless",)),),
        bundle_2=(_sel("clothing.underwear", ("bra", "panties")),),
    )
    assert "panties" not in prompt
    assert "bra" in prompt


def test_barefoot_drops_thighhighs() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.feet.anatomy", ("barefoot",)),),
        bundle_2=(_sel("clothing.legwear", ("thighhighs",)),),
    )
    assert "thighhighs" not in prompt
    assert "barefoot" in prompt


def test_no_shoes_keeps_legwear() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.feet.anatomy", ("no_shoes",)),),
        bundle_2=(_sel("clothing.legwear", ("thighhighs",)),),
        bundle_3=(_sel("clothing.footwear", ("boots",)),),
    )
    assert "boots" not in prompt
    assert "thighhighs" in prompt


def test_trigger_tag_itself_is_never_dropped() -> None:
    # If "nude" appears in a selection that also lists clothing tags
    # (unlikely but possible), the trigger itself must survive.
    prompt, _, _ = _run(
        bundle_1=(_sel("body.exposure", ("nude",), layer="exposure"),),
    )
    assert "nude" in prompt


def test_returned_bundle_can_be_re_merged() -> None:
    _, _, bundle = _run(
        bundle_1=(_sel("a", ("x",)),),
        bundle_2=(_sel("b", ("y",)),),
    )
    prompt2, _, _ = _run(bundle_1=bundle)
    assert prompt2 == "x, y"
