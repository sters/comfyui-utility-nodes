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

from nodes.tags.clothing.legwear_footwear import _FOOTWEAR, _LEGWEAR
from nodes.tags.clothing.outfit import _BOTTOMS, _DRESS_ONEPIECE, _TOPS, _UNIFORM
from nodes.tags.clothing.underwear_swimwear import _SWIMWEAR, _UNDERWEAR

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
