from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_LEGWEAR: tuple[str, ...] = (
    "thighhighs",
    "over-the-knee_socks",
    "kneehighs",
    "socks",
    "ankle_socks",
    "loose_socks",
    "bobby_socks",
    "tabi",
    "stockings",
    "pantyhose",
    "leg_warmers",
    "single_thighhigh",
    "single_kneehigh",
    "single_sock",
    "zettai_ryouiki",
    "no_socks",
    "no_legwear",
)

_FOOTWEAR: tuple[str, ...] = (
    "shoes",
    "sneakers",
    "loafers",
    "mary_janes",
    "high_heels",
    "stiletto_heels",
    "platform_heels",
    "platform_footwear",
    "wedge_heels",
    "pumps",
    "boots",
    "ankle_boots",
    "knee_boots",
    "thigh_boots",
    "cross-laced_footwear",
    "combat_boots",
    "rain_boots",
    "sandals",
    "flip-flops",
    "geta",
    "okobo",
    "zouri",
    "slippers",
    "uwabaki",
    "ballet_slippers",
    "cleats",
)


class ClothingLegwear(TagNodeBase):
    TAGS = _LEGWEAR


class ClothingFootwear(TagNodeBase):
    TAGS = _FOOTWEAR


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ClothingLegwear": ClothingLegwear,
    "ClothingFootwear": ClothingFootwear,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ClothingLegwear": "Clothing: Legwear",
    "ClothingFootwear": "Clothing: Footwear",
}
