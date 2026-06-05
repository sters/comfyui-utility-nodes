from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_UNDERWEAR: tuple[str, ...] = (
    "underwear",
    "underwear_only",
    "bra",
    "sports_bra",
    "strapless_bra",
    "frilled_bra",
    "lace_bra",
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
    "lingerie",
    "babydoll",
    "chemise",
    "teddy",
    "bodystocking",
    "garter_belt",
    "garter_straps",
    "corset",
    "bustier",
    "camisole_(underwear)",
    "slip_(clothing)",
    "fundoshi",
)

_SWIMWEAR: tuple[str, ...] = (
    "swimsuit",
    "one-piece_swimsuit",
    "school_swimsuit",
    "competition_swimsuit",
    "bikini",
    "string_bikini",
    "side-tie_bikini",
    "front-tie_bikini",
    "micro_bikini",
    "sling_bikini",
    "halterneck_bikini",
    "frilled_bikini",
    "polka_dot_bikini",
    "striped_bikini",
    "o-ring_bikini",
    "bikini_top",
    "bikini_bottom",
    "swim_briefs",
    "swim_trunks",
    "rash_guard",
    "wetsuit",
    "highleg_swimsuit",
    "thong_bikini",
)


class ClothingUnderwear(TagNodeBase):
    TAGS = _UNDERWEAR


class ClothingSwimwear(TagNodeBase):
    TAGS = _SWIMWEAR


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ClothingUnderwear": ClothingUnderwear,
    "ClothingSwimwear": ClothingSwimwear,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ClothingUnderwear": "Clothing: Underwear",
    "ClothingSwimwear": "Clothing: Swimwear",
}
