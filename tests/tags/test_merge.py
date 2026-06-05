"""Integration tests for TagsMerge.

Most scenarios fit a simple shape: "given this comma-separated tag list,
expect this comma-separated output." `_scenario(input)` auto-categorizes
each tag by walking nodes.tags.* and returns the merged prompt. Use the
parametrized table tests for these.

Specialized tests (cross-bundle mutex, max-input cap, extra preservation,
unknown-tag edge cases) stay in long-form at the bottom.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import Any

import pytest

import nodes.tags
from nodes.tags._base import TaggedSelection, TagNodeBase
from nodes.tags.merge import TagsMerge

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _build_tag_index() -> dict[str, tuple[str, str, bool]]:
    """Walk nodes.tags.* and map each tag → (category_id, layer, mutex_within).

    First occurrence wins (the package has no cross-file duplicates by
    design, so this is deterministic).
    """
    index: dict[str, tuple[str, str, bool]] = {}
    for _finder, name, ispkg in pkgutil.walk_packages(nodes.tags.__path__, "nodes.tags."):
        if ispkg or name.endswith(("._base", "._conflicts", ".merge")):
            continue
        mod = importlib.import_module(name)
        for attr in vars(mod).values():
            if not isinstance(attr, type):
                continue
            if attr is TagNodeBase or not issubclass(attr, TagNodeBase):
                continue
            for tag in attr.TAGS:
                index.setdefault(tag, (attr.CATEGORY_ID, attr.LAYER, attr.MUTEX_WITHIN))
    return index


_TAG_INDEX = _build_tag_index()


def _scenario(tags_str: str, *, extra: str = "") -> str:
    """Run TagsMerge for a comma-separated tag list, returning the prompt.

    Tags are auto-grouped by (category_id, layer, mutex_within). Bundle order
    follows the input order of categories' first appearances.
    """
    if not tags_str.strip():
        tags: list[str] = []
    else:
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    by_cat: dict[str, list[str]] = {}
    cat_meta: dict[str, tuple[str, bool]] = {}
    for t in tags:
        cat, layer, mutex = _TAG_INDEX.get(t, ("_unknown", "unknown", False))
        if cat not in by_cat:
            by_cat[cat] = []
            cat_meta[cat] = (layer, mutex)
        by_cat[cat].append(t)
    bundles: dict[str, tuple[TaggedSelection, ...]] = {}
    for i, (cat, ts) in enumerate(by_cat.items(), 1):
        layer, mutex = cat_meta[cat]
        bundles[f"bundle_{i}"] = (TaggedSelection(category=cat, layer=layer, tags=tuple(ts), mutex_within=mutex),)
    out = TagsMerge().merge(", ", extra=extra, **bundles)
    return str(out["result"][0])


# --------------------------------------------------------------------------
# Parametrized scenarios
# --------------------------------------------------------------------------


# `PASS` means "expected output equals the input" (pure pass-through).
PASS = object()

# (id, input, expected_or_PASS). `id` becomes the pytest test id.
CASES: list[tuple[str, str, object]] = [
    # --- mutex groups (physically impossible combos) ---
    ("hair_length", "long_hair, short_hair", "long_hair"),
    ("skirt_length", "long_skirt, miniskirt", "long_skirt"),
    ("skirt_with_layer", "bike_shorts, long_skirt, miniskirt", "bike_shorts, long_skirt"),
    ("eye_openness", "closed_eyes, wide-eyed", "closed_eyes"),
    ("eye_openness_3", "closed_eyes, narrowed_eyes, half-closed_eyes", "closed_eyes"),
    ("gaze_direction", "looking_up, looking_down, looking_at_viewer", "looking_up"),
    ("mouth_open_close", "open_mouth, closed_mouth", "open_mouth"),
    ("emoticons", ":d, :3, :o, :p", ":d"),
    ("smile_vs_frown", "smile, frown", "smile"),
    ("grin_vs_scowl", "grin, scowl", "grin"),
    ("laughing_vs_frown", "laughing, frown", "laughing"),
    ("happy_vs_sad", "happy, sad", "happy"),
    ("expressionless_wins", "expressionless, smile, frown", "expressionless"),
    ("blank_vs_smile", "blank_expression, smile", "blank_expression"),
    # --- tag-level conflicts (cross-category drops) ---
    ("nude_drops_clothing", "nude, shirt, pleated_skirt, boots", "nude"),
    ("nude_keeps_accessory", "nude, beret, earrings, necklace", PASS),
    ("completely_nude_drops_all", "completely_nude, sundress, bra, panties", "completely_nude"),
    ("topless_drops_bra_keeps_panties", "topless, bra, panties, garter_belt", "topless, panties, garter_belt"),
    ("topless_drops_dress", "topless, sundress", "topless"),
    ("bottomless_drops_panties", "bottomless, bra, panties", "bottomless, bra"),
    ("bottomless_drops_skirt", "bottomless, pleated_skirt", "bottomless"),
    ("barefoot_drops_footwear_and_legwear", "barefoot, sneakers, thighhighs", "barefoot"),
    ("no_shoes_keeps_legwear", "no_shoes, sneakers, thighhighs", "no_shoes, thighhighs"),
    ("no_legwear", "no_legwear, thighhighs, boots", "no_legwear, boots"),
    ("no_panties", "no_panties, panties, bra", "no_panties, bra"),
    ("no_bra_drops_bras", "no_bra, bra, panties", "no_bra, panties"),
    ("bare_legs_drops_legwear", "bare_legs, thighhighs, boots", "bare_legs, boots"),
    # --- pass-through: every tag survives ---
    ("smile_grin_laughing", "smile, grin, laughing", PASS),
    ("smile_sad_tearful", "smile, sad, tearful", PASS),
    ("smile_smug_smirk", "smile, smug, smirk", PASS),
    ("embarrassed_blush", "embarrassed, blush", PASS),
    ("five_layer_tops", "shirt, sweater, cardigan, jacket, coat", PASS),
    ("bike_shorts_under_skirt", "long_skirt, bike_shorts", PASS),
    ("hair_layered", "long_hair, ponytail, black_hair, hair_ribbon", PASS),
    ("panties_aside_with_underwear", "panties_aside, bra_aside, bra, panties", PASS),
    ("skin_tight_impossible_dress", "skin_tight, impossible_dress, sundress, large_breasts", PASS),
    ("skirt_lift_panchira", "skirt_lift, pleated_skirt, panties, thighhighs", PASS),
    ("wet_seethrough_tank", "wet_clothes, see-through, tank_top, nipples", PASS),
    ("bondage_corset", "tied_up, handcuffs, ball_gag, bondage, thighhighs, corset", PASS),
    ("six_tattoos", "arm_tattoo, back_tattoo, chest_tattoo, thigh_tattoo, facial_tattoo, neck_tattoo", PASS),
    ("santa_bikini", "twintails, red_hair, bikini, santa_hat, fur_trim, thighhighs, thigh_boots", PASS),
    ("armor_bikini", "abs, bikini, armor, gauntlets, vambraces, cape, knee_boots", PASS),
    ("foxgirl_miko", "fox_ears, fox_tail, yellow_eyes, slit_pupils, miko, shrine_outdoors", PASS),
    ("demon_girl", "demon_horns, demon_tail, demon_wings, red_eyes, slit_pupils, fangs", PASS),
    ("classroom_afternoon", "scenery, classroom, afternoon, sunlight, dust", PASS),
    ("beach_sunset", "beach, ocean, sunset, sunny, backlighting, lens_flare", PASS),
    ("snowy_mountain_night", "mountain, snowfield, night, snowing, moonlight, snowflakes, mist", PASS),
    ("cherry_blossom_park", "park, sunny, afternoon, cherry_blossoms, petals, dappled_sunlight", PASS),
    ("rainy_neon", "city, alley, night, rain, neon_lights, lens_flare, wet_clothes", PASS),
    ("bent_over_panchira", "bent_over, skirt_lift, pleated_skirt, striped_panties, thighhighs", PASS),
    (
        "full_stack",
        "masterpiece, best_quality, highres, 1girl, solo, long_hair, blonde_hair, blue_eyes, smile, simple_background",
        PASS,
    ),
    ("schoolgirl", "long_hair, black_hair, bangs, hair_ribbon, medium_breasts, serafuku, thighhighs, loafers", PASS),
    ("office_lady", "medium_hair, business_suit, blouse, pencil_skirt, pantyhose, high_heels, glasses", PASS),
    ("maid_stack", "maid, frilled_apron, headband, thighhighs", PASS),
    ("kimono_boots", "kimono, boots, obi", PASS),
    ("naked_apron", "naked_apron, barefoot", PASS),
    ("yukata_festival", "long_hair, hair_bun, ahoge, hair_flower, yukata, obi, tabi, geta", PASS),
    ("wedding", "very_long_hair, blonde_hair, pale_skin, wedding_dress, veil, elbow_gloves, high_heels", PASS),
    (
        "gothic_lolita",
        "twin_drills, pale_skin, frilled_dress, lace, frills, headband, thighhighs, mary_janes, frilled_choker",
        PASS,
    ),
    ("nsfw_solo_toy_bdsm", "masturbation, spread_pussy, dildo, vibrator, restrained, ball_gag", PASS),
    (
        "cyber_bodysuit",
        "silver_hair, bodysuit, skin_tight, impossible_bodysuit, latex, shiny_clothes, goggles_on_head, knee_boots",
        PASS,
    ),
    ("glasses_and_hood", "glasses, hood, hood_up", PASS),
    ("glasses_goggles_position", "glasses, goggles_on_head", PASS),
    (
        "sleepy_morning",
        "messy_hair, half-closed_eyes, parted_lips, sleepy, oversized_shirt, sitting_on_bed, bedroom, morning",
        PASS,
    ),
    (
        "crying_schoolgirl",
        "brown_hair, blue_eyes, crying, teary_eyes, looking_down, sad, tearful, light_blush, serafuku",
        PASS,
    ),
    (
        "smug_yandere",
        "very_long_hair, black_hair, red_eyes, narrowed_eyes, heart-shaped_pupils, slit_pupils, yandere, smirk, licking_lips",  # noqa: E501
        PASS,
    ),
    ("genki", "ponytail, sparkling_eyes, smile, grin, blush_stickers, open_mouth, :d, jumping", PASS),
    (
        "tan_athletic",
        "ponytail, brown_hair, tan, tanlines, muscular_female, abs, toned, thick_thighs, sports_bra, bike_shorts, sneakers",  # noqa: E501
        PASS,
    ),
]


def _norm(s: str) -> str:
    return s.replace(", ", ",")


@pytest.mark.parametrize(
    "tags_in,expected",
    [(c[1], c[2]) for c in CASES],
    ids=[c[0] for c in CASES],
)
def test_scenario(tags_in: str, expected: object) -> None:
    target = tags_in if expected is PASS else expected
    assert isinstance(target, str)
    assert _norm(_scenario(tags_in)) == _norm(target)


# --------------------------------------------------------------------------
# Specialized tests (can't reduce to single-bundle parametrize)
# --------------------------------------------------------------------------


def _run(**kwargs: Any) -> tuple[str, str, tuple[TaggedSelection, ...]]:
    out = TagsMerge().merge(", ", **kwargs)
    return (str(out["result"][0]), str(out["result"][1]), tuple(out["result"][2]))


def _sel(category: str, tags: tuple[str, ...], **kw: Any) -> TaggedSelection:
    return TaggedSelection(
        category=category,
        layer=kw.get("layer", "test"),
        tags=tags,
        mutex_within=kw.get("mutex_within", False),
    )


def test_merge_empty_inputs_yield_empty_prompt() -> None:
    prompt, warnings, bundle = _run()
    assert (prompt, warnings, bundle) == ("", "", ())


def test_merge_extra_is_appended() -> None:
    prompt, _, _ = _run(extra="1girl", bundle_1=(_sel("a", ("x",)),))
    assert prompt == "x, 1girl"


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


def test_mutex_within_drops_second_selection_with_same_category() -> None:
    # Cross-bundle: two selections claim the same mutex category.
    prompt, warnings, _ = _run(
        bundle_1=(_sel("hair.length", ("long_hair",), mutex_within=True),),
        bundle_2=(_sel("hair.length", ("short_hair",), mutex_within=True),),
    )
    assert prompt == "long_hair"
    assert "mutex:" in warnings


def test_mutex_within_collapses_multi_tag_selection() -> None:
    prompt, warnings, _ = _run(
        bundle_1=(_sel("hair.length", ("long_hair", "short_hair"), mutex_within=True),),
    )
    assert prompt == "long_hair"
    assert "short_hair" in warnings


def test_separator_escape_sequence_decoded() -> None:
    out = TagsMerge().merge(r"\n", bundle_1=(_sel("a", ("x", "y")),))
    assert out["result"][0] == "x\ny"


def test_eleventh_bundle_is_silently_ignored() -> None:
    bundles = {f"bundle_{i + 1}": (_sel("c", (f"t{i + 1}",)),) for i in range(11)}
    prompt, _, _ = _run(**bundles)
    tokens = prompt.split(", ")
    assert "t10" in tokens
    assert "t11" not in tokens


def test_returned_bundle_can_be_re_merged() -> None:
    _, _, bundle = _run(
        bundle_1=(_sel("a", ("x",)),),
        bundle_2=(_sel("b", ("y",)),),
    )
    prompt2, _, _ = _run(bundle_1=bundle)
    assert prompt2 == "x, y"


def test_nude_does_not_drop_fit_aside_position_tags() -> None:
    # Documented edge: nude drops items in clothing categories listed in
    # TAG_CONFLICTS["nude"] (tops/bottoms/dress/uniform/underwear/swimwear/
    # footwear/legwear) but does NOT extend into fit/aside/position.
    prompt = _scenario("nude, skin_tight, panties_aside, goggles_on_head, panties")
    tokens = prompt.split(", ")
    assert "nude" in tokens
    assert "panties" not in tokens  # actual clothing dropped
    assert "skin_tight" in tokens
    assert "panties_aside" in tokens
    assert "goggles_on_head" in tokens


def test_trigger_tag_itself_is_never_dropped() -> None:
    assert _scenario("nude") == "nude"


def test_unknown_tags_pass_through() -> None:
    # Tags not registered with any node land in an "_unknown" bucket and
    # survive as-is.
    assert _scenario("hand_made_super_special_tag_xyz, smile") == ("hand_made_super_special_tag_xyz, smile")
