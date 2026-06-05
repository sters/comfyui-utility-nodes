from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_STATE: tuple[str, ...] = (
    "topless",
    "bottomless",
    "no_panties",
    "undressing",
    "dressing",
    "half-undressed",
    "open_clothes",
    "open_shirt",
    "open_jacket",
    "open_coat",
    "open_robe",
    "open_kimono",
    "open_dress",
    "open_vest",
    "open_cardigan",
    "partially_unbuttoned",
    "unbuttoned",
    "untied",
    "loose_clothes",
    "loose_shirt",
    "loose_necktie",
    "wardrobe_malfunction",
)

_LIFT_PULL: tuple[str, ...] = (
    "clothes_lift",
    "shirt_lift",
    "skirt_lift",
    "dress_lift",
    "kimono_lift",
    "clothes_pull",
    "panty_pull",
    "bra_pull",
    "shirt_pull",
    "skirt_pull",
    "clothes_down",
    "panties_down",
    "shirt_tug",
    "clothes_tug",
    "clothes_removed",
    "shirt_removed",
    "panties_removed",
    "bra_removed",
    "clothes_around_waist",
    "clothes_in_mouth",
)

_NAKED_X: tuple[str, ...] = (
    "naked_shirt",
    "naked_apron",
    "naked_towel",
    "naked_ribbon",
    "naked_sheet",
    "naked_jacket",
    "naked_scarf",
    "naked_overalls",
    "naked_cape",
    "naked_coat",
    "naked_hoodie",
    "naked_sweater",
)


class ClothingState(TagNodeBase):
    TAGS = _STATE


class ClothingLiftPull(TagNodeBase):
    TAGS = _LIFT_PULL


class ClothingNakedX(TagNodeBase):
    TAGS = _NAKED_X


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ClothingState": ClothingState,
    "ClothingLiftPull": ClothingLiftPull,
    "ClothingNakedX": ClothingNakedX,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ClothingState": "Clothing: State",
    "ClothingLiftPull": "Clothing: Lift & Pull",
    "ClothingNakedX": "Clothing: Naked X (wearing only)",
}
