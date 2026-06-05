from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_HEADWEAR: tuple[str, ...] = (
    "hat",
    "baseball_cap",
    "beret",
    "cap",
    "peaked_cap",
    "newsboy_cap",
    "flat_cap",
    "fedora",
    "top_hat",
    "bowler_hat",
    "mob_cap",
    "sun_hat",
    "straw_hat",
    "witch_hat",
    "wizard_hat",
    "santa_hat",
    "party_hat",
    "nurse_cap",
    "police_hat",
    "military_hat",
    "helmet",
    "bicycle_helmet",
    "motorcycle_helmet",
    "hood",
    "hood_up",
    "hood_down",
    "hooded_jacket",
    "hooded_cape",
    "headphones",
    "headset",
    "earmuffs",
    "headband",
    "head_wreath",
    "head_scarf",
    "veil",
    "crown",
    "mini_crown",
    "tiara",
    "hat_ribbon",
    "hat_bow",
    "hat_flower",
    "hat_feather",
)

_EYEWEAR: tuple[str, ...] = (
    "glasses",
    "sunglasses",
    "round_eyewear",
    "semi-rimless_eyewear",
    "rimless_eyewear",
    "over-rim_eyewear",
    "under-rim_eyewear",
    "goggles",
    "goggles_on_head",
    "swim_goggles",
    "eyepatch",
    "medical_eyepatch",
    "monocle",
    "pince-nez",
    "blindfold",
)


class ClothingHeadwear(TagNodeBase):
    TAGS = _HEADWEAR


class ClothingEyewear(TagNodeBase):
    TAGS = _EYEWEAR


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ClothingHeadwear": ClothingHeadwear,
    "ClothingEyewear": ClothingEyewear,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ClothingHeadwear": "Clothing: Headwear",
    "ClothingEyewear": "Clothing: Eyewear",
}
