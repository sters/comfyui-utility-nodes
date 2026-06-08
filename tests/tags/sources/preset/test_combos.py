"""Integration tests for layering CharacterPreset + PersonalityPreset + NsfwScenePreset.

Each row of COMBOS is one realistic 1/2/3-preset stack. The test asserts
which tags must end up in the final prompt and which must have been
dropped by mutex/conflict resolution.
"""

from typing import Any

import pytest

from nodes.tags.merge import TagsMerge
from nodes.tags.sources.preset.character import CharacterPreset
from nodes.tags.sources.preset.nsfw_scene import NsfwScenePreset
from nodes.tags.sources.preset.personality import PersonalityPreset


def _bundle(node_cls: type, name: str) -> Any:
    return tuple(node_cls().build(name, ", ")["result"][0])


def _combo(
    *,
    char: str | None = None,
    pers: str | None = None,
    scene: str | None = None,
    extra: str = "",
) -> list[str]:
    bundles: dict[str, Any] = {}
    i = 1
    for cls, name in (
        (CharacterPreset, char),
        (PersonalityPreset, pers),
        (NsfwScenePreset, scene),
    ):
        if name is None:
            continue
        bundles[f"bundle_{i}"] = _bundle(cls, name)
        i += 1
    out = TagsMerge().merge(", ", extra=extra, **bundles)
    prompt = str(out["result"][0])
    return prompt.split(", ") if prompt else []


# (id, char, pers, scene, must_have, must_not)
COMBOS: list[tuple[str, str | None, str | None, str | None, list[str], list[str]]] = [
    # --- character + personality ---
    (
        "schoolgirl_tsundere",
        "serafuku_schoolgirl",
        "tsundere",
        None,
        ["serafuku", "long_hair", "blush", "embarrassed", "pouting", "frown", "crossed_arms"],
        [],
    ),
    (
        "miko_kuudere",
        "miko",
        "kuudere",
        None,
        ["miko", "hakama", "expressionless", "narrowed_eyes", "serious", "closed_mouth"],
        [],
    ),
    (
        "maid_dandere",
        "maid",
        "dandere",
        None,
        ["maid", "frilled_apron", "shy", "light_blush", "looking_down", "embarrassed"],
        [],
    ),
    (
        "office_lady_ojou",
        "office_lady",
        "ojou_sama",
        None,
        ["business_suit", "glasses", "smug", "laughing", "looking_down", "hand_on_own_hip"],
        [],
    ),
    (
        "catgirl_mesugaki",
        "catgirl_basic",
        "mesugaki",
        None,
        ["cat_ears", "cat_tail", "slit_pupils", "smug_grin", "smug", "fang"],
        [],
    ),
    (
        "vampire_yandere",
        "vampire",
        "yandere",
        None,
        ["fangs", "red_eyes", "pale_skin", "smirk", "heart-shaped_pupils", "yandere"],
        [],
    ),
    (
        "princess_ojou",
        "princess",
        "ojou_sama",
        None,
        ["ball_gown", "tiara", "blonde_hair", "smug", "laughing", "looking_down"],
        [],
    ),
    (
        "nun_seiso",
        "nun",
        "seiso",
        None,
        ["nun", "veil", "silver_hair", "smile", "light_blush", "parted_lips"],
        [],
    ),
    (
        "magical_girl_genki",
        "magical_girl",
        "genki",
        None,
        ["frilled_dress", "tiara", "smile", "grin", "sparkling_eyes", "open_mouth", ":d"],
        [],
    ),
    (
        "santa_genki",
        "santa_girl",
        "genki",
        None,
        ["santa_hat", "santa_costume", "red_hair", "smile", "grin", "open_mouth"],
        [],
    ),
    (
        "knight_confident",
        "knight",
        "confident",
        None,
        ["armor", "gauntlets", "smug", "grin", "determined", "hand_on_own_hip"],
        [],
    ),
    (
        "bunny_gyaru",
        "bunny_girl",
        "gyaru",
        None,
        ["bunny_ears", "rabbit_tail", "tan", "tanlines", "smirk", "sparkling_eyes"],
        [],
    ),
    (
        "yukata_seiso",
        "yukata_festival",
        "seiso",
        None,
        ["yukata", "obi", "hair_flower", "smile", "light_blush", "parted_lips"],
        [],
    ),
    (
        "gothic_lolita_apathetic",
        "gothic_lolita",
        "apathetic",
        None,
        ["frilled_dress", "twin_drills", "pale_skin", "expressionless", "tired", "narrowed_eyes"],
        [],
    ),
    (
        "yandere_jk_yandere",
        "yandere_schoolgirl",
        "yandere",
        None,
        ["serafuku", "very_long_hair", "yandere", "smirk", "narrowed_eyes", "heart-shaped_pupils"],
        [],
    ),
    # --- character + NSFW scene (nude drops outfit) ---
    (
        "schoolgirl_first_time",
        "serafuku_schoolgirl",
        None,
        "first_time_shy",
        ["long_hair", "nude", "blush", "embarrassed", "vaginal", "missionary"],
        ["serafuku", "pleated_skirt", "thighhighs", "loafers"],
    ),
    (
        "maid_masturbation",
        "maid",
        None,
        "masturbation_solo",
        ["long_hair", "twin_braids", "nude", "masturbation", "spread_pussy", "fingering"],
        # `frilled_apron` is accessory (not clothing.uniform), so nude doesn't drop it.
        # That's actually fine — "naked apron" is a thing.
        ["maid", "thighhighs"],
    ),
    (
        "witch_femdom",
        "witch",
        None,
        "femdom_dominant",
        ["very_long_hair", "purple_hair", "witch_hat", "smug", "leash", "spanking"],
        # femdom_dominant has no `nude`, so witch_hat / long_dress aren't dropped
        [],
    ),
    (
        "princess_lingerie",
        "princess",
        None,
        "lingerie_tease",
        ["blonde_hair", "pale_skin", "tiara", "lingerie", "bra", "panties", "garter_belt"],
        # lingerie_tease has no `nude`, ball_gown survives too
        [],
    ),
    (
        "yandere_jk_first_time",
        "yandere_schoolgirl",
        None,
        "first_time_shy",
        ["very_long_hair", "yandere", "smirk", "nude", "vaginal", "blush"],
        ["serafuku"],
    ),
    (
        "catgirl_paizuri",
        "catgirl_basic",
        None,
        "paizuri_scene",
        ["cat_ears", "cat_tail", "slit_pupils", "fang", "paizuri", "huge_breasts", "cum_on_breasts", "topless"],
        [],
    ),
    # --- personality + NSFW ---
    (
        "yandere_shibari",
        None,
        "yandere",
        "shibari_suspension",
        ["yandere", "smirk", "heart-shaped_pupils", "shibari", "rope", "suspension_bondage", "nude"],
        [],
    ),
    (
        "tsundere_first_time",
        None,
        "tsundere",
        "first_time_shy",
        ["blush", "embarrassed", "vaginal", "missionary", "nude", "tearful"],
        [],
    ),
    (
        "genki_squirting",
        None,
        "genki",
        "squirting",
        ["smile", "grin", "sparkling_eyes", "squirting", "spread_legs", "female_ejaculation"],
        [],
    ),
    # --- triple stack ---
    (
        "schoolgirl_tsundere_first_time",
        "serafuku_schoolgirl",
        "tsundere",
        "first_time_shy",
        ["long_hair", "blush", "embarrassed", "nude", "vaginal", "missionary", "tearful", "frown"],
        ["serafuku", "pleated_skirt"],
    ),
    (
        "catgirl_mesugaki_paizuri",
        "catgirl_basic",
        "mesugaki",
        "paizuri_scene",
        ["cat_ears", "cat_tail", "slit_pupils", "smug_grin", "paizuri", "huge_breasts", "cum_on_breasts"],
        [],
    ),
    (
        "princess_ojou_lingerie",
        "princess",
        "ojou_sama",
        "lingerie_tease",
        # MUTEX_GROUPS is last-wins, so the scene's gaze (looking_at_viewer)
        # overrides ojou_sama's looking_down.
        ["blonde_hair", "tiara", "smug", "looking_at_viewer", "lingerie", "bra", "panties", "garter_belt"],
        [],
    ),
    (
        "magical_girl_genki_squirting",
        "magical_girl",
        "genki",
        "squirting",
        ["pink_hair", "sparkling_eyes", "squirting", "spread_legs", "nude", "ahegao"],
        ["frilled_dress", "mary_janes"],
    ),
    (
        "vampire_yandere_breast_play",
        "vampire",
        "yandere",
        "breast_play",
        ["fangs", "smirk", "heart-shaped_pupils", "nipple_sucking", "breast_grab", "topless"],
        ["long_dress"],
    ),
    (
        "bunny_gyaru_lingerie",
        "bunny_girl",
        "gyaru",
        "lingerie_tease",
        ["bunny_ears", "rabbit_tail", "tan", "smirk", "lingerie", "bra"],
        [],
    ),
    (
        "maid_dandere_shower",
        "maid",
        "dandere",
        "shower_scene",
        ["long_hair", "shy", "light_blush", "bathroom", "shower", "steam", "nude"],
        # frilled_apron is accessory, not dropped by nude
        ["maid", "thighhighs"],
    ),
    (
        "office_lady_apathetic_handjob",
        "office_lady",
        "apathetic",
        "handjob_dominant",
        ["business_suit", "glasses", "expressionless", "tired", "handjob", "smug"],
        [],
    ),
    (
        "kunoichi_confident_bound",
        "kunoichi",
        "confident",
        "bound_submissive",
        # kunoichi (uniform) IS dropped by nude. tabi (legwear) also dropped.
        # scarf_over_mouth is clothing.position, not in _ALL_CLOTHING, so it survives.
        ["ponytail", "black_hair", "toned", "smug", "grin", "restrained", "tied_up", "ball_gag", "nude"],
        ["kunoichi", "tabi"],
    ),
    (
        "yandere_jk_yandere_shibari",
        "yandere_schoolgirl",
        "yandere",
        "shibari_suspension",
        ["very_long_hair", "yandere", "smirk", "heart-shaped_pupils", "shibari", "rope"],
        ["serafuku"],
    ),
    (
        "cheerleader_genki_public_exposure",
        "cheerleader",
        "genki",
        "public_exposure",
        ["twintails", "orange_hair", "cheerleader", "smile", "grin", "blush", "embarrassed", "outdoors", "park"],
        # public_exposure has `bottomless` — cheerleader's miniskirt drops, sneakers stay
        ["miniskirt"],
    ),
]


@pytest.mark.parametrize(
    "char,pers,scene,must_have,must_not",
    [(c[1], c[2], c[3], c[4], c[5]) for c in COMBOS],
    ids=[c[0] for c in COMBOS],
)
def test_preset_combo(
    char: str | None,
    pers: str | None,
    scene: str | None,
    must_have: list[str],
    must_not: list[str],
) -> None:
    tokens = _combo(char=char, pers=pers, scene=scene)
    for tag in must_have:
        assert tag in tokens, f"expected '{tag}' in output, got: {tokens}"
    for tag in must_not:
        assert tag not in tokens, f"'{tag}' should have been dropped, got: {tokens}"
