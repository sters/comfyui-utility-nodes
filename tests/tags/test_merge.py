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


def test_no_bra_drops_bras_only() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.breasts.shape_state", ("no_bra",)),),
        bundle_2=(_sel("clothing.underwear", ("bra", "panties")),),
    )
    tokens = prompt.split(", ")
    assert "bra" not in tokens
    assert "no_bra" in tokens
    assert "panties" in tokens


def test_bare_legs_drops_legwear() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.feet.legs_pose", ("bare_legs",)),),
        bundle_2=(_sel("clothing.legwear", ("thighhighs",)),),
        bundle_3=(_sel("clothing.footwear", ("boots",)),),
    )
    assert "thighhighs" not in prompt
    assert "boots" in prompt


def test_trigger_tag_itself_is_never_dropped() -> None:
    # If "nude" appears in a selection that also lists clothing tags
    # (unlikely but possible), the trigger itself must survive.
    prompt, _, _ = _run(
        bundle_1=(_sel("body.exposure", ("nude",), layer="exposure"),),
    )
    assert "nude" in prompt


def test_mutex_group_drops_conflicting_length_tags() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "short_hair")),),
    )
    tokens = prompt.split(", ")
    assert "long_hair" in tokens
    assert "short_hair" not in tokens
    assert "mutex_group" in warnings


def test_mutex_group_lets_orthogonal_tags_coexist() -> None:
    # long_hair (length) + ponytail (style) belong to different mutex
    # groups (style is not in MUTEX_GROUPS), so both survive.
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "ponytail")),),
    )
    assert "long_hair" in prompt
    assert "ponytail" in prompt


def test_tops_can_layer() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.tops", ("shirt", "cardigan", "jacket")),),
    )
    for t in ("shirt", "cardigan", "jacket"):
        assert t in prompt


def test_bottoms_layer_but_skirt_length_is_mutex() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.bottoms", ("bike_shorts", "long_skirt", "miniskirt")),),
    )
    tokens = prompt.split(", ")
    assert "bike_shorts" in tokens
    assert "long_skirt" in tokens
    assert "miniskirt" not in tokens
    assert "mutex_group" in warnings


def test_realistic_schoolgirl_passes_through_unchanged() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair",)),),
        bundle_2=(_sel("body.hair.color", ("black_hair",), mutex_within=True),),
        bundle_3=(_sel("body.hair.details", ("bangs", "hair_ribbon")),),
        bundle_4=(_sel("body.breasts.size", ("medium_breasts",), mutex_within=True),),
        bundle_5=(_sel("clothing.uniform", ("serafuku",), mutex_within=True),),
        bundle_6=(_sel("clothing.legwear", ("thighhighs",), mutex_within=True),),
        bundle_7=(_sel("clothing.footwear", ("loafers",), mutex_within=True),),
    )
    expected = "long_hair, black_hair, bangs, hair_ribbon, medium_breasts, serafuku, thighhighs, loafers"
    assert prompt == expected
    assert warnings == ""


def test_marks_and_accessories_stack_on_nude_body() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.exposure", ("nude",)),),
        bundle_2=(_sel("body.marks.moles", ("mole_under_eye", "freckles")),),
        bundle_3=(_sel("body.marks.tattoos", ("arm_tattoo", "back_tattoo")),),
        bundle_4=(_sel("clothing.hand_arm", ("bracelet", "ring", "watch")),),
        bundle_5=(_sel("clothing.neck", ("necklace", "choker")),),
        bundle_6=(_sel("clothing.accessory.other", ("earrings",)),),
    )
    for tag in (
        "nude",
        "mole_under_eye",
        "freckles",
        "arm_tattoo",
        "bracelet",
        "ring",
        "necklace",
        "choker",
        "earrings",
    ):
        assert tag in prompt
    assert warnings == ""


def test_composition_mutex_picks_first_angle_framing_focus() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("composition.angle", ("from_above",), mutex_within=True),),
        bundle_2=(_sel("composition.angle", ("dutch_angle",), mutex_within=True),),
        bundle_3=(_sel("composition.framing", ("portrait",), mutex_within=True),),
        bundle_4=(_sel("composition.framing", ("full_body",), mutex_within=True),),
        bundle_5=(_sel("composition.focus", ("hand_focus",), mutex_within=True),),
    )
    tokens = prompt.split(", ")
    assert tokens == ["from_above", "portrait", "hand_focus"]
    assert "dutch_angle" in warnings
    assert "full_body" in warnings


def test_nsfw_solo_toy_bdsm_stack_independently() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("nsfw.solo", ("masturbation", "spread_pussy")),),
        bundle_2=(_sel("nsfw.toy", ("dildo", "vibrator")),),
        bundle_3=(_sel("nsfw.bdsm", ("restrained", "ball_gag")),),
    )
    for tag in ("masturbation", "spread_pussy", "dildo", "vibrator", "restrained", "ball_gag"):
        assert tag in prompt
    assert warnings == ""


def test_paizuri_with_topless_drops_only_outer_top() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("nsfw.act.oral_contact", ("paizuri",)),),
        bundle_2=(_sel("clothing.state", ("topless",)),),
        bundle_3=(_sel("clothing.tops", ("shirt",)),),
    )
    assert "paizuri" in prompt
    assert "topless" in prompt
    assert "shirt" not in prompt.split(", ")
    assert "topless" in warnings or "conflict" in warnings
    _, _, bundle = _run(
        bundle_1=(_sel("a", ("x",)),),
        bundle_2=(_sel("b", ("y",)),),
    )
    prompt2, _, _ = _run(bundle_1=bundle)
    assert prompt2 == "x, y"
