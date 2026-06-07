"""Tag-level conflict rules for TagsMerge.

Each entry maps a trigger tag to the set of tags it suppresses. When the
trigger tag is present anywhere in the merged bundle, the suppressed tags
are dropped from every selection (per-tag, not per-selection — a corset
that lives under ``clothing.underwear`` is not dropped just because
``topless`` is set; only bras/torso pieces are).

Edge cases (intentional, not auto-handled):
- ``no_panties`` only drops panty-style underwear, not bras/corsets.
- ``topless`` keeps lower-body underwear (panties, garter_belt).
- ``barefoot`` also suppresses legwear (thighhighs/socks) since legwear
  covers feet; if you want "barefoot with thighhighs", remove the rule.
"""

from .sources.clothing.legwear_footwear import _FOOTWEAR, _LEGWEAR
from .sources.clothing.outfit import _BOTTOMS, _DRESS_ONEPIECE, _TOPS, _UNIFORM
from .sources.clothing.underwear_swimwear import _SWIMWEAR, _UNDERWEAR

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}

# Hand-curated subsets of underwear (the registry can't infer top-vs-bottom).
_BRAS = frozenset({"bra", "sports_bra", "strapless_bra", "frilled_bra", "lace_bra"})
_TORSO_UNDERWEAR = frozenset({"corset", "bustier", "camisole_(underwear)"})
_PANTIES = frozenset(
    {
        "panties",
        "thong",
        "side-tie_panties",
        "string_panties",
        "frilled_panties",
        "lace_panties",
        "boyshorts",
        "boxers",
        "briefs",
        "boxer_briefs",
        "fundoshi",
    }
)
_FULL_BODY_UNDERWEAR = frozenset(
    {
        "underwear",
        "underwear_only",
        "lingerie",
        "babydoll",
        "chemise",
        "teddy",
        "bodystocking",
        "slip_(clothing)",
    }
)

_ALL_CLOTHING: frozenset[str] = frozenset(
    {*_TOPS, *_BOTTOMS, *_DRESS_ONEPIECE, *_UNIFORM, *_UNDERWEAR, *_SWIMWEAR, *_FOOTWEAR, *_LEGWEAR}
)

# Bidirectional mutex groups. If multiple tags from a single group are
# present in the merged bundle, keep the first one (input order) and drop
# the rest. Use this for sub-category exclusivity that doesn't align with
# the per-category MUTEX_WITHIN flag (e.g. hair length vs hair style are
# in the same TagNode, but only "length" is mutex among itself).
MUTEX_GROUPS: tuple[frozenset[str], ...] = (
    # Hair length descriptors (style descriptors like ponytail/twintails
    # can coexist with any length).
    frozenset({"very_long_hair", "long_hair", "medium_hair", "short_hair"}),
    # Skirt length (tops/bottoms otherwise stack: bike_shorts under skirt, etc.)
    frozenset({"long_skirt", "miniskirt"}),
    # Base skin tone — only one tone, but tanlines/shiny_skin can stack on top.
    frozenset({"pale_skin", "white_skin", "fair_skin", "tan", "dark_skin", "very_dark_skin"}),
    # Hair base color (multicolored/two-tone/gradient/streaked layer on top).
    frozenset(
        {
            "blonde_hair",
            "black_hair",
            "brown_hair",
            "blue_hair",
            "light_blue_hair",
            "aqua_hair",
            "pink_hair",
            "purple_hair",
            "red_hair",
            "white_hair",
            "grey_hair",
            "silver_hair",
            "green_hair",
            "orange_hair",
        }
    ),
    # Eye base color.
    frozenset(
        {
            "blue_eyes",
            "red_eyes",
            "brown_eyes",
            "green_eyes",
            "purple_eyes",
            "violet_eyes",
            "yellow_eyes",
            "gold_eyes",
            "orange_eyes",
            "pink_eyes",
            "black_eyes",
            "grey_eyes",
            "aqua_eyes",
            "white_eyes",
        }
    ),
    # Breast size.
    frozenset(
        {
            "flat_chest",
            "small_breasts",
            "medium_breasts",
            "large_breasts",
            "huge_breasts",
            "gigantic_breasts",
        }
    ),
    # Eye openness — physically one state at a time.
    frozenset({"closed_eyes", "half-closed_eyes", "wide-eyed", "narrowed_eyes"}),
    # Gaze direction — looking somewhere is positional, not stackable.
    frozenset(
        {
            "looking_at_viewer",
            "looking_away",
            "looking_down",
            "looking_up",
            "looking_back",
            "looking_to_the_side",
            "looking_ahead",
            "looking_at_another",
            "side_glance",
        }
    ),
    # Mouth opening — one posture only.
    frozenset(
        {
            "open_mouth",
            "closed_mouth",
            "parted_lips",
            "gritted_teeth",
            "clenched_teeth",
            "biting_lip",
        }
    ),
    # Emoticon mouth shapes — one shape only.
    frozenset({":3", ":d", ":o", ":p", ":q", ":t", ":<", ":>", "wavy_mouth"}),
    # Mouth curve direction — only enumerate the pair-wise "up vs down"
    # contradictions so siblings can stack (smile + grin = ok,
    # smile + frown = collapse to smile).
    frozenset({"smile", "frown"}),
    frozenset({"smile", "scowl"}),
    frozenset({"grin", "frown"}),
    frozenset({"grin", "scowl"}),
    frozenset({"laughing", "frown"}),
    frozenset({"laughing", "scowl"}),
    # Emotion valence — happy vs sad are clear opposites.
    frozenset({"happy", "sad"}),
    # Expressionless contradicts active expressions.
    frozenset({"expressionless", "smile"}),
    frozenset({"expressionless", "grin"}),
    frozenset({"expressionless", "frown"}),
    frozenset({"expressionless", "angry"}),
    frozenset({"expressionless", "happy"}),
    frozenset({"expressionless", "sad"}),
    frozenset({"blank_expression", "smile"}),
    frozenset({"blank_expression", "frown"}),
    frozenset({"blank_expression", "happy"}),
    frozenset({"blank_expression", "sad"}),
)


TAG_CONFLICTS: dict[str, frozenset[str]] = {
    "nude": _ALL_CLOTHING,
    "completely_nude": _ALL_CLOTHING,
    "topless": frozenset({*_TOPS, *_BRAS, *_TORSO_UNDERWEAR, *_FULL_BODY_UNDERWEAR, *_DRESS_ONEPIECE}),
    "bottomless": frozenset({*_BOTTOMS, *_PANTIES, *_FULL_BODY_UNDERWEAR, *_DRESS_ONEPIECE}),
    "barefoot": frozenset({*_FOOTWEAR, *_LEGWEAR}),
    "no_shoes": frozenset(_FOOTWEAR),
    "no_legwear": frozenset(_LEGWEAR),
    "no_panties": _PANTIES,
    "no_bra": _BRAS,
    "bare_legs": frozenset(_LEGWEAR),
}
