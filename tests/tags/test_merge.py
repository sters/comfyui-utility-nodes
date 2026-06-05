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


def test_school_uniform_with_swimsuit_underneath() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.uniform", ("school_uniform",), mutex_within=True),),
        bundle_2=(_sel("clothing.swimwear", ("school_swimsuit",), mutex_within=True),),
    )
    assert "school_uniform" in prompt
    assert "school_swimsuit" in prompt
    assert warnings == ""


def test_bikini_with_thighhighs() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.swimwear", ("bikini",), mutex_within=True),),
        bundle_2=(_sel("clothing.legwear", ("thighhighs",), mutex_within=True),),
    )
    assert prompt == "bikini, thighhighs"
    assert warnings == ""


def test_dress_with_jacket_layered_on_top() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.dress", ("sundress",), mutex_within=True),),
        bundle_2=(_sel("clothing.tops", ("jacket",)),),
    )
    assert "sundress" in prompt
    assert "jacket" in prompt


def test_maid_outfit_full_stack() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.uniform", ("maid",), mutex_within=True),),
        bundle_2=(_sel("clothing.accessory.other", ("frilled_apron",)),),
        bundle_3=(_sel("clothing.headwear", ("headband",), mutex_within=True),),
        bundle_4=(_sel("clothing.legwear", ("thighhighs",), mutex_within=True),),
    )
    assert prompt == "maid, frilled_apron, headband, thighhighs"
    assert warnings == ""


def test_kimono_with_western_boots_is_allowed() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.dress", ("kimono",), mutex_within=True),),
        bundle_2=(_sel("clothing.footwear", ("boots",), mutex_within=True),),
        bundle_3=(_sel("clothing.accessory.other", ("obi",)),),
    )
    for tag in ("kimono", "boots", "obi"):
        assert tag in prompt


def test_bottomless_keeps_legwear_and_footwear() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.state", ("bottomless",)),),
        bundle_2=(_sel("clothing.legwear", ("thighhighs",), mutex_within=True),),
        bundle_3=(_sel("clothing.footwear", ("boots",), mutex_within=True),),
    )
    for tag in ("bottomless", "thighhighs", "boots"):
        assert tag in prompt


def test_multiple_uniforms_collapse_to_first() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(
            _sel(
                "clothing.uniform",
                ("school_uniform", "maid", "nurse"),
                mutex_within=True,
            ),
        ),
    )
    assert prompt == "school_uniform"
    assert "maid" in warnings
    assert "nurse" in warnings


def test_topless_with_explicit_nipples_keeps_nipples() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.state", ("topless",)),),
        bundle_2=(
            _sel(
                "body.breasts.shape_state",
                ("nipples", "puffy_nipples", "breasts_apart"),
            ),
        ),
        bundle_3=(_sel("body.breasts.size", ("large_breasts",), mutex_within=True),),
    )
    for tag in ("topless", "nipples", "puffy_nipples", "breasts_apart", "large_breasts"):
        assert tag in prompt


def test_bunny_girl_outfit() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(
            _sel(
                "clothing.uniform",
                ("bunny_girl", "playboy_bunny"),
                mutex_within=True,
            ),
        ),
        bundle_2=(_sel("clothing.legwear", ("pantyhose",), mutex_within=True),),
        bundle_3=(_sel("clothing.footwear", ("high_heels",), mutex_within=True),),
    )
    assert "bunny_girl" in prompt
    assert "playboy_bunny" not in prompt.split(", ")
    assert "pantyhose" in prompt
    assert "high_heels" in prompt
    assert "playboy_bunny" in warnings


def test_long_hair_ponytail_stack_with_ribbon() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "ponytail")),),
        bundle_2=(_sel("body.hair.color", ("black_hair",), mutex_within=True),),
        bundle_3=(_sel("body.hair.details", ("hair_ribbon",)),),
    )
    assert prompt == "long_hair, ponytail, black_hair, hair_ribbon"


def test_fit_layers_with_outfit_and_body_size() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.fit", ("skin_tight", "impossible_dress")),),
        bundle_2=(_sel("clothing.dress", ("sundress",), mutex_within=True),),
        bundle_3=(_sel("body.breasts.size", ("large_breasts",), mutex_within=True),),
    )
    for tag in ("skin_tight", "impossible_dress", "sundress", "large_breasts"):
        assert tag in prompt
    assert warnings == ""


def test_taut_clothes_with_bursting_breasts_and_size() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.fit", ("taut_clothes", "taut_shirt", "bursting_breasts")),),
        bundle_2=(_sel("clothing.tops", ("shirt",)),),
        bundle_3=(_sel("body.breasts.size", ("huge_breasts",), mutex_within=True),),
    )
    for tag in ("taut_clothes", "taut_shirt", "bursting_breasts", "shirt", "huge_breasts"):
        assert tag in prompt


def test_loose_oversized_stack() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.fit", ("loose_clothes", "oversized_shirt")),),
        bundle_2=(_sel("clothing.tops", ("sweater",)),),
    )
    for tag in ("loose_clothes", "oversized_shirt", "sweater"):
        assert tag in prompt


def test_panties_aside_and_bra_aside_coexist_with_actual_items() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.aside", ("panties_aside", "bra_aside")),),
        bundle_2=(_sel("clothing.underwear", ("bra", "panties")),),
    )
    for tag in ("panties_aside", "bra_aside", "bra", "panties"):
        assert tag in prompt


def test_bottomless_drops_panties_but_keeps_panties_aside_marker() -> None:
    # Edge case: bottomless removes the panties tag itself, but
    # `panties_aside` lives in clothing.aside (separate category) and is
    # not in any TAG_CONFLICTS drop set. The bundle ends up showing
    # "bottomless, panties_aside" without panties — semantically odd
    # but documents current behavior.
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.state", ("bottomless",)),),
        bundle_2=(_sel("clothing.aside", ("panties_aside",)),),
        bundle_3=(_sel("clothing.underwear", ("panties",)),),
    )
    assert "bottomless" in prompt
    assert "panties_aside" in prompt
    assert "panties" not in prompt.split(", ")
    assert "panties" in warnings


def test_strap_slip_family_stacks() -> None:
    prompt, _, _ = _run(
        bundle_1=(
            _sel(
                "clothing.aside",
                ("strap_slip", "double_strap_slip", "suspenders_slip"),
            ),
        ),
        bundle_2=(_sel("clothing.tops", ("tank_top",)),),
    )
    for tag in ("strap_slip", "double_strap_slip", "suspenders_slip", "tank_top"):
        assert tag in prompt


def test_wind_lift_skirt_panchira() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.aside", ("wind_lift", "exposed_gusset")),),
        bundle_2=(_sel("clothing.state", ("skirt_lift",)),),
        bundle_3=(_sel("clothing.bottoms", ("pleated_skirt",)),),
        bundle_4=(_sel("clothing.underwear", ("panties",)),),
    )
    for tag in ("wind_lift", "exposed_gusset", "skirt_lift", "pleated_skirt", "panties"):
        assert tag in prompt


def test_goggles_on_head_now_coexists_with_glasses() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.eyewear", ("glasses",), mutex_within=True),),
        bundle_2=(_sel("clothing.position", ("goggles_on_head",)),),
    )
    assert "glasses" in prompt
    assert "goggles_on_head" in prompt


def test_hood_item_with_hood_up_state_coexist() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.headwear", ("hood",), mutex_within=True),),
        bundle_2=(_sel("clothing.position", ("hood_up",)),),
        bundle_3=(_sel("clothing.eyewear", ("glasses",), mutex_within=True),),
    )
    for tag in ("hood", "hood_up", "glasses"):
        assert tag in prompt


def test_jacket_on_shoulders_with_jacket_and_inner_top() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.position", ("jacket_on_shoulders",)),),
        bundle_2=(_sel("clothing.tops", ("jacket", "tank_top")),),
    )
    for tag in ("jacket_on_shoulders", "jacket", "tank_top"):
        assert tag in prompt


def test_clothes_around_waist_layered_with_actual_clothes() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.position", ("clothes_around_waist", "shirt_around_waist")),),
        bundle_2=(_sel("clothing.bottoms", ("shorts",)),),
        bundle_3=(_sel("clothing.tops", ("tank_top",)),),
    )
    for tag in ("clothes_around_waist", "shirt_around_waist", "shorts", "tank_top"):
        assert tag in prompt


def test_breast_lift_and_bra_lift_with_exposed_nipples() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.state", ("bra_lift", "breast_lift")),),
        bundle_2=(_sel("body.breasts.shape_state", ("nipples", "areola_slip")),),
        bundle_3=(_sel("clothing.underwear", ("bra",)),),
    )
    for tag in ("bra_lift", "breast_lift", "nipples", "areola_slip", "bra"):
        assert tag in prompt


def test_lift_family_panchira_full_combo() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.state", ("skirt_lift", "lifting_own_clothes")),),
        bundle_2=(_sel("clothing.aside", ("wind_lift", "exposed_gusset")),),
        bundle_3=(_sel("clothing.bottoms", ("pleated_skirt",)),),
        bundle_4=(_sel("clothing.underwear", ("panties",)),),
    )
    for tag in (
        "skirt_lift",
        "lifting_own_clothes",
        "wind_lift",
        "exposed_gusset",
        "pleated_skirt",
        "panties",
    ):
        assert tag in prompt


def test_bunny_outfit_with_fit_and_position() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "ponytail")),),
        bundle_2=(_sel("body.hair.color", ("black_hair",), mutex_within=True),),
        bundle_3=(_sel("body.breasts.size", ("huge_breasts",), mutex_within=True),),
        bundle_4=(_sel("body.figure", ("thick_thighs", "wide_hips")),),
        bundle_5=(_sel("clothing.fit", ("skin_tight", "impossible_clothes", "bursting_breasts")),),
        bundle_6=(_sel("clothing.uniform", ("bunny_girl",), mutex_within=True),),
        bundle_7=(_sel("clothing.legwear", ("pantyhose",), mutex_within=True),),
        bundle_8=(_sel("clothing.footwear", ("high_heels",), mutex_within=True),),
        bundle_9=(_sel("clothing.eyewear", ("glasses",), mutex_within=True),),
        bundle_10=(_sel("clothing.position", ("goggles_on_head",)),),
    )
    for tag in (
        "long_hair",
        "ponytail",
        "huge_breasts",
        "bursting_breasts",
        "bunny_girl",
        "pantyhose",
        "high_heels",
        "glasses",
        "goggles_on_head",
    ):
        assert tag in prompt


def test_nude_currently_does_not_drop_fit_aside_position_tags() -> None:
    # Documents current behavior: nude drops items in tops/bottoms/dress/
    # uniform/underwear/swimwear/footwear/legwear (TAG_CONFLICTS["nude"] =
    # _ALL_CLOTHING), but fit/aside/position categories aren't in that set.
    # Semantically `nude + skin_tight` is incoherent; flagged for future
    # refinement.
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.exposure", ("nude",)),),
        bundle_2=(_sel("clothing.fit", ("skin_tight",)),),
        bundle_3=(_sel("clothing.aside", ("panties_aside",)),),
        bundle_4=(_sel("clothing.position", ("goggles_on_head",)),),
        bundle_5=(_sel("clothing.underwear", ("panties",)),),
    )
    assert "nude" in prompt
    assert "panties" not in prompt.split(", ")  # actual underwear dropped
    assert "skin_tight" in prompt  # fit not dropped (edge case)
    assert "panties_aside" in prompt  # aside not dropped (edge case)
    assert "goggles_on_head" in prompt  # position fine (independent item)
    assert "panties" in warnings


def test_panchira_from_below_with_skirt_lift_and_panties() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("composition.angle", ("from_below",), mutex_within=True),),
        bundle_2=(_sel("clothing.state", ("skirt_lift",)),),
        bundle_3=(_sel("clothing.bottoms", ("pleated_skirt",)),),
        bundle_4=(_sel("clothing.underwear", ("panties",)),),
    )
    assert prompt == "from_below, skirt_lift, pleated_skirt, panties"
    assert warnings == ""


def test_five_layer_tops_all_kept() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.tops", ("shirt", "sweater", "cardigan", "jacket", "coat")),),
    )
    for t in ("shirt", "sweater", "cardigan", "jacket", "coat"):
        assert t in prompt


def test_wet_seethrough_tank_top_nipples() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("clothing.material", ("wet_clothes", "see-through")),),
        bundle_2=(_sel("clothing.tops", ("tank_top",)),),
        bundle_3=(_sel("body.breasts.shape_state", ("nipples",)),),
    )
    for tag in ("wet_clothes", "see-through", "tank_top", "nipples"):
        assert tag in prompt


def test_bondage_setup_with_clothing_layers() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("nsfw.bdsm", ("tied_up", "handcuffs", "ball_gag", "bondage")),),
        bundle_2=(_sel("clothing.legwear", ("thighhighs",), mutex_within=True),),
        bundle_3=(_sel("clothing.underwear", ("corset",)),),
    )
    for tag in ("tied_up", "handcuffs", "ball_gag", "bondage", "thighhighs", "corset"):
        assert tag in prompt


def test_lewd_expression_stack() -> None:
    prompt, _, _ = _run(
        bundle_1=(
            _sel(
                "nsfw.state.aftermath",
                ("ahegao", "tongue_out", "heart-shaped_pupils", "drooling", "blush"),
            ),
        ),
    )
    for tag in ("ahegao", "tongue_out", "heart-shaped_pupils", "drooling", "blush"):
        assert tag in prompt


def test_full_body_tattoo_stack() -> None:
    prompt, _, _ = _run(
        bundle_1=(
            _sel(
                "body.marks.tattoos",
                (
                    "arm_tattoo",
                    "back_tattoo",
                    "chest_tattoo",
                    "thigh_tattoo",
                    "facial_tattoo",
                    "neck_tattoo",
                ),
            ),
        ),
    )
    for tag in (
        "arm_tattoo",
        "back_tattoo",
        "chest_tattoo",
        "thigh_tattoo",
        "facial_tattoo",
        "neck_tattoo",
    ):
        assert tag in prompt


def test_eleventh_bundle_is_ignored() -> None:
    bundles = {f"bundle_{i + 1}": (_sel("test", (f"t{i + 1}",)),) for i in range(11)}
    prompt, _, _ = _run(**bundles)
    tokens = prompt.split(", ")
    assert "t10" in tokens
    assert "t11" not in tokens


def test_hair_details_stack_with_headwear() -> None:
    prompt, _, _ = _run(
        bundle_1=(
            _sel(
                "body.hair.details",
                ("ahoge", "bangs", "hair_over_one_eye", "hair_ornament", "hair_bow"),
            ),
        ),
        bundle_2=(_sel("clothing.headwear", ("tiara",), mutex_within=True),),
    )
    for tag in (
        "ahoge",
        "bangs",
        "hair_over_one_eye",
        "hair_ornament",
        "hair_bow",
        "tiara",
    ):
        assert tag in prompt


def test_composition_crop_layers_keep_all() -> None:
    # Crops are non-mutex — overlapping crop tags coexist (over-cropped
    # framing is intentional, mostly for negative prompts).
    prompt, _, _ = _run(
        bundle_1=(
            _sel(
                "composition.crop",
                ("cropped_legs", "cropped_head", "head_out_of_frame", "feet_out_of_frame"),
            ),
        ),
    )
    for tag in ("cropped_legs", "cropped_head", "head_out_of_frame", "feet_out_of_frame"):
        assert tag in prompt


def test_three_hair_colors_collapsed_by_mutex_within() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(
            _sel(
                "body.hair.color",
                ("blonde_hair", "black_hair", "brown_hair"),
                mutex_within=True,
            ),
        ),
    )
    assert prompt == "blonde_hair"
    assert "black_hair" in warnings
    assert "brown_hair" in warnings


def test_eyewear_and_position_goggles_and_monocle() -> None:
    # Eyewear keeps mutex_within=True; monocle vs glasses collapses.
    # goggles_on_head (Position) is independent and survives alongside.
    prompt, warnings, _ = _run(
        bundle_1=(_sel("clothing.eyewear", ("glasses", "monocle"), mutex_within=True),),
        bundle_2=(_sel("clothing.position", ("goggles_on_head",)),),
    )
    assert "glasses" in prompt
    assert "monocle" not in prompt.split(", ")
    assert "goggles_on_head" in prompt
    assert "monocle" in warnings


def test_solo_kink_stack() -> None:
    prompt, _, _ = _run(
        bundle_1=(
            _sel(
                "nsfw.solo",
                ("masturbation", "female_masturbation", "spread_pussy", "nipple_tweak"),
            ),
        ),
        bundle_2=(_sel("nsfw.toy", ("dildo", "vibrator_on_nipple")),),
    )
    for tag in (
        "masturbation",
        "female_masturbation",
        "spread_pussy",
        "nipple_tweak",
        "dildo",
        "vibrator_on_nipple",
    ):
        assert tag in prompt


def test_archetype_miko() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair",)),),
        bundle_2=(_sel("body.hair.color", ("black_hair",), mutex_within=True),),
        bundle_3=(_sel("body.hair.details", ("bangs",)),),
        bundle_4=(_sel("clothing.uniform", ("miko",), mutex_within=True),),
        bundle_5=(_sel("clothing.dress", ("hakama",), mutex_within=True),),
        bundle_6=(_sel("clothing.legwear", ("tabi",), mutex_within=True),),
        bundle_7=(_sel("clothing.footwear", ("zouri",), mutex_within=True),),
    )
    for tag in ("long_hair", "black_hair", "bangs", "miko", "hakama", "tabi", "zouri"):
        assert tag in prompt
    assert warnings == ""


def test_archetype_nurse() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("short_hair",)),),
        bundle_2=(_sel("body.hair.color", ("brown_hair",), mutex_within=True),),
        bundle_3=(_sel("body.breasts.size", ("medium_breasts",), mutex_within=True),),
        bundle_4=(_sel("clothing.uniform", ("nurse",), mutex_within=True),),
        bundle_5=(_sel("clothing.headwear", ("nurse_cap",), mutex_within=True),),
        bundle_6=(_sel("clothing.legwear", ("pantyhose",), mutex_within=True),),
        bundle_7=(_sel("clothing.footwear", ("loafers",), mutex_within=True),),
    )
    for tag in ("short_hair", "brown_hair", "medium_breasts", "nurse", "nurse_cap", "pantyhose", "loafers"):
        assert tag in prompt


def test_archetype_office_lady() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("medium_hair",)),),
        bundle_2=(_sel("body.hair.color", ("black_hair",), mutex_within=True),),
        bundle_3=(_sel("body.breasts.size", ("large_breasts",), mutex_within=True),),
        bundle_4=(_sel("clothing.uniform", ("business_suit",), mutex_within=True),),
        bundle_5=(_sel("clothing.tops", ("blouse",)),),
        bundle_6=(_sel("clothing.bottoms", ("pencil_skirt",)),),
        bundle_7=(_sel("clothing.legwear", ("pantyhose",), mutex_within=True),),
        bundle_8=(_sel("clothing.footwear", ("high_heels",), mutex_within=True),),
        bundle_9=(_sel("clothing.eyewear", ("glasses",), mutex_within=True),),
    )
    for tag in (
        "medium_hair",
        "black_hair",
        "large_breasts",
        "business_suit",
        "blouse",
        "pencil_skirt",
        "pantyhose",
        "high_heels",
        "glasses",
    ):
        assert tag in prompt


def test_archetype_witch() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("very_long_hair",)),),
        bundle_2=(_sel("body.hair.color", ("purple_hair",), mutex_within=True),),
        bundle_3=(_sel("clothing.uniform", ("witch",), mutex_within=True),),
        bundle_4=(_sel("clothing.headwear", ("witch_hat",), mutex_within=True),),
        bundle_5=(_sel("clothing.dress", ("long_dress",), mutex_within=True),),
        bundle_6=(_sel("clothing.legwear", ("thighhighs",), mutex_within=True),),
        bundle_7=(_sel("clothing.footwear", ("boots",), mutex_within=True),),
    )
    for tag in ("very_long_hair", "purple_hair", "witch", "witch_hat", "long_dress", "thighhighs", "boots"):
        assert tag in prompt


def test_archetype_wet_school_swimsuit() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("medium_hair", "ponytail")),),
        bundle_2=(_sel("body.hair.color", ("brown_hair",), mutex_within=True),),
        bundle_3=(_sel("body.skin", ("tan", "tanlines"), mutex_within=True),),
        bundle_4=(_sel("clothing.swimwear", ("school_swimsuit",), mutex_within=True),),
        bundle_5=(_sel("clothing.material", ("wet_clothes",)),),
        bundle_6=(_sel("body.feet.anatomy", ("barefoot",)),),
    )
    for tag in ("medium_hair", "ponytail", "brown_hair", "tan", "school_swimsuit", "wet_clothes", "barefoot"):
        assert tag in prompt


def test_archetype_naked_apron() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "ponytail")),),
        bundle_2=(_sel("body.hair.color", ("blonde_hair",), mutex_within=True),),
        bundle_3=(_sel("body.breasts.size", ("large_breasts",), mutex_within=True),),
        bundle_4=(_sel("clothing.state", ("naked_apron",)),),
        bundle_5=(_sel("body.feet.anatomy", ("barefoot",)),),
    )
    for tag in ("long_hair", "ponytail", "blonde_hair", "large_breasts", "naked_apron", "barefoot"):
        assert tag in prompt
    assert warnings == ""


def test_archetype_cheerleader() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("twintails",)),),
        bundle_2=(_sel("body.hair.color", ("orange_hair",), mutex_within=True),),
        bundle_3=(_sel("body.hair.details", ("hair_ribbon",)),),
        bundle_4=(_sel("clothing.uniform", ("cheerleader",), mutex_within=True),),
        bundle_5=(_sel("clothing.bottoms", ("miniskirt",)),),
        bundle_6=(_sel("clothing.legwear", ("socks",), mutex_within=True),),
        bundle_7=(_sel("clothing.footwear", ("sneakers",), mutex_within=True),),
    )
    for tag in ("twintails", "orange_hair", "hair_ribbon", "cheerleader", "miniskirt", "socks", "sneakers"):
        assert tag in prompt


def test_archetype_nun() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair",)),),
        bundle_2=(_sel("body.hair.color", ("silver_hair",), mutex_within=True),),
        bundle_3=(_sel("clothing.uniform", ("nun",), mutex_within=True),),
        bundle_4=(_sel("clothing.headwear", ("veil",), mutex_within=True),),
        bundle_5=(_sel("clothing.dress", ("long_dress",), mutex_within=True),),
        bundle_6=(_sel("clothing.neck", ("necklace",)),),
    )
    for tag in ("long_hair", "silver_hair", "nun", "veil", "long_dress", "necklace"):
        assert tag in prompt


def test_archetype_female_knight() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "ponytail")),),
        bundle_2=(_sel("body.hair.color", ("blonde_hair",), mutex_within=True),),
        bundle_3=(_sel("body.figure", ("toned", "abs")),),
        bundle_4=(_sel("clothing.uniform", ("armor",), mutex_within=True),),
        bundle_5=(_sel("clothing.hand_arm", ("gauntlets", "pauldron", "vambraces")),),
        bundle_6=(_sel("clothing.neck", ("cape",)),),
        bundle_7=(_sel("clothing.footwear", ("knee_boots",), mutex_within=True),),
    )
    for tag in (
        "long_hair",
        "ponytail",
        "blonde_hair",
        "toned",
        "abs",
        "armor",
        "gauntlets",
        "pauldron",
        "vambraces",
        "cape",
        "knee_boots",
    ):
        assert tag in prompt


def test_archetype_princess() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("very_long_hair", "drill_hair")),),
        bundle_2=(_sel("body.hair.color", ("blonde_hair",), mutex_within=True),),
        bundle_3=(_sel("body.skin", ("pale_skin",), mutex_within=True),),
        bundle_4=(_sel("clothing.dress", ("ball_gown",), mutex_within=True),),
        bundle_5=(_sel("clothing.headwear", ("tiara",), mutex_within=True),),
        bundle_6=(_sel("clothing.neck", ("necklace",)),),
        bundle_7=(_sel("clothing.hand_arm", ("elbow_gloves",)),),
        bundle_8=(_sel("clothing.footwear", ("high_heels",), mutex_within=True),),
    )
    for tag in (
        "very_long_hair",
        "drill_hair",
        "blonde_hair",
        "pale_skin",
        "ball_gown",
        "tiara",
        "necklace",
        "elbow_gloves",
        "high_heels",
    ):
        assert tag in prompt


def test_archetype_china_dress() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "double_bun")),),
        bundle_2=(_sel("body.hair.color", ("black_hair",), mutex_within=True),),
        bundle_3=(_sel("body.breasts.size", ("large_breasts",), mutex_within=True),),
        bundle_4=(_sel("body.figure", ("thick_thighs",)),),
        bundle_5=(_sel("clothing.dress", ("china_dress",), mutex_within=True),),
        bundle_6=(_sel("clothing.fit", ("skin_tight", "form_fitting")),),
        bundle_7=(_sel("clothing.legwear", ("pantyhose",), mutex_within=True),),
        bundle_8=(_sel("clothing.footwear", ("high_heels",), mutex_within=True),),
    )
    for tag in (
        "long_hair",
        "double_bun",
        "black_hair",
        "large_breasts",
        "thick_thighs",
        "china_dress",
        "skin_tight",
        "form_fitting",
        "pantyhose",
        "high_heels",
    ):
        assert tag in prompt


def test_archetype_jersey_girl() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("medium_hair", "ponytail")),),
        bundle_2=(_sel("body.hair.color", ("brown_hair",), mutex_within=True),),
        bundle_3=(_sel("clothing.uniform", ("track_suit",), mutex_within=True),),
        bundle_4=(_sel("clothing.bottoms", ("track_pants",)),),
        bundle_5=(_sel("clothing.footwear", ("sneakers",), mutex_within=True),),
    )
    for tag in ("medium_hair", "ponytail", "brown_hair", "track_suit", "track_pants", "sneakers"):
        assert tag in prompt


def test_archetype_gothic_lolita() -> None:
    prompt, _, _ = _run(
        bundle_1=(_sel("body.hair.length_style", ("long_hair", "twin_drills")),),
        bundle_2=(_sel("body.hair.color", ("black_hair",), mutex_within=True),),
        bundle_3=(_sel("body.skin", ("pale_skin",), mutex_within=True),),
        bundle_4=(_sel("clothing.dress", ("frilled_dress",), mutex_within=True),),
        bundle_5=(_sel("clothing.material", ("lace", "frills", "satin")),),
        bundle_6=(_sel("clothing.headwear", ("headband",), mutex_within=True),),
        bundle_7=(_sel("clothing.legwear", ("thighhighs",), mutex_within=True),),
        bundle_8=(_sel("clothing.footwear", ("mary_janes",), mutex_within=True),),
        bundle_9=(_sel("clothing.neck", ("frilled_choker",)),),
    )
    for tag in (
        "long_hair",
        "twin_drills",
        "black_hair",
        "pale_skin",
        "frilled_dress",
        "lace",
        "frills",
        "satin",
        "headband",
        "thighhighs",
        "mary_janes",
        "frilled_choker",
    ):
        assert tag in prompt


def test_returned_bundle_can_be_re_merged() -> None:
    _, _, bundle = _run(
        bundle_1=(_sel("a", ("x",)),),
        bundle_2=(_sel("b", ("y",)),),
    )
    prompt2, _, _ = _run(bundle_1=bundle)
    assert prompt2 == "x, y"
