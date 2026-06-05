from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_HAND_ARM: tuple[str, ...] = (
    "gloves",
    "fingerless_gloves",
    "half_gloves",
    "elbow_gloves",
    "mittens",
    "single_glove",
    "mismatched_gloves",
    "arm_warmers",
    "wrist_cuffs",
    "wristband",
    "sweatband",
    "bracelet",
    "bangle",
    "watch",
    "wristwatch",
    "ring",
    "armlet",
    "armband",
    "shoulder_armor",
    "pauldron",
    "vambraces",
    "gauntlets",
)

_NECK: tuple[str, ...] = (
    "necklace",
    "pendant",
    "choker",
    "frilled_choker",
    "collar",
    "neck_ribbon",
    "neck_bow",
    "necktie",
    "bowtie",
    "neckerchief",
    "ascot",
    "scarf",
    "muffler",
    "shawl",
    "cape",
    "capelet",
)

_OTHER: tuple[str, ...] = (
    "earrings",
    "single_earring",
    "ear_piercing",
    "stud_earrings",
    "hoop_earrings",
    "drop_earrings",
    "belt",
    "waist_cape",
    "obi",
    "sash",
    "belt_pouch",
    "apron",
    "frilled_apron",
    "waist_apron",
    "bag",
    "handbag",
    "shoulder_bag",
    "backpack",
    "satchel",
    "school_bag",
    "umbrella",
    "parasol",
    "fan",
    "folding_fan",
    "lip_piercing",
    "nose_piercing",
    "navel_piercing",
    "tongue_piercing",
)


class ClothingHandArm(TagNodeBase):
    TAGS = _HAND_ARM


class ClothingNeck(TagNodeBase):
    TAGS = _NECK


class ClothingAccessoryOther(TagNodeBase):
    TAGS = _OTHER


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ClothingHandArm": ClothingHandArm,
    "ClothingNeck": ClothingNeck,
    "ClothingAccessoryOther": ClothingAccessoryOther,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ClothingHandArm": "Clothing: Hand & Arm",
    "ClothingNeck": "Clothing: Neck",
    "ClothingAccessoryOther": "Clothing: Accessory (other)",
}
