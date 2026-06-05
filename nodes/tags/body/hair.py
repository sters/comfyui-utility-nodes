from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_LENGTH_STYLE: tuple[str, ...] = (
    "very_long_hair",
    "long_hair",
    "medium_hair",
    "short_hair",
    "short_hair_with_long_locks",
    "low-tied_long_hair",
    "ponytail",
    "high_ponytail",
    "low_ponytail",
    "side_ponytail",
    "twintails",
    "low_twintails",
    "short_twintails",
    "twin_braids",
    "side_braid",
    "single_braid",
    "braid",
    "bob_cut",
    "hair_bun",
    "double_bun",
    "single_hair_bun",
    "drill_hair",
    "twin_drills",
    "one_side_up",
    "two_side_up",
    "half_updo",
    "wavy_hair",
    "straight_hair",
    "curly_hair",
    "messy_hair",
    "spiked_hair",
    "floating_hair",
)

_COLOR: tuple[str, ...] = (
    "blonde_hair",
    "black_hair",
    "brown_hair",
    "blue_hair",
    "light_blue_hair",
    "pink_hair",
    "white_hair",
    "grey_hair",
    "silver_hair",
    "purple_hair",
    "red_hair",
    "green_hair",
    "orange_hair",
    "aqua_hair",
    "multicolored_hair",
    "two-tone_hair",
    "streaked_hair",
    "gradient_hair",
    "colored_inner_hair",
)

_DETAILS: tuple[str, ...] = (
    "bangs",
    "blunt_bangs",
    "parted_bangs",
    "swept_bangs",
    "crossed_bangs",
    "double-parted_bangs",
    "hair_between_eyes",
    "hair_over_one_eye",
    "hair_over_eyes",
    "hair_over_shoulder",
    "hair_behind_ear",
    "hair_flaps",
    "sidelocks",
    "ahoge",
    "antenna_hair",
    "hair_intakes",
    "hair_tubes",
    "blunt_ends",
    "hair_ornament",
    "x_hair_ornament",
    "star_hair_ornament",
    "hair_bow",
    "hair_ribbon",
    "hair_flower",
    "hairband",
    "hairclip",
    "hair_bobbles",
    "hair_rings",
    "hair_scrunchie",
)


class HairLengthStyle(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.hair.length_style"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _LENGTH_STYLE


class HairColor(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.hair.color"
    LAYER: ClassVar[str] = "anatomy"
    # multicolored/two-tone/gradient layer on top of a base color, so
    # don't lock the category to one tag. Base-color exclusivity is
    # enforced via MUTEX_GROUPS in _conflicts.py.
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _COLOR


class HairDetails(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.hair.details"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _DETAILS


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "HairLengthStyle": HairLengthStyle,
    "HairColor": HairColor,
    "HairDetails": HairDetails,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "HairLengthStyle": "Hair: Length & Style",
    "HairColor": "Hair: Color",
    "HairDetails": "Hair: Details",
}
