from typing import ClassVar

from ..._base import TagNodeBase

_TOPS: tuple[str, ...] = (
    "shirt",
    "t-shirt",
    "dress_shirt",
    "blouse",
    "collared_shirt",
    "polo_shirt",
    "tank_top",
    "camisole",
    "crop_top",
    "tube_top",
    "off-shoulder_shirt",
    "sleeveless_shirt",
    "frilled_shirt",
    "sweater",
    "turtleneck",
    "ribbed_sweater",
    "sweater_vest",
    "hoodie",
    "cardigan",
    "vest",
    "waistcoat",
    "jacket",
    "blazer",
    "coat",
    "trench_coat",
    "long_coat",
    "winter_coat",
    "raincoat",
    "windbreaker",
)

_BOTTOMS: tuple[str, ...] = (
    "skirt",
    "miniskirt",
    "long_skirt",
    "pleated_skirt",
    "high-waist_skirt",
    "frilled_skirt",
    "pencil_skirt",
    "tutu",
    "hakama_skirt",
    "pants",
    "jeans",
    "denim_pants",
    "leggings",
    "harem_pants",
    "wide-leg_pants",
    "cargo_pants",
    "track_pants",
    "shorts",
    "short_shorts",
    "hot_pants",
    "denim_shorts",
    "bike_shorts",
    "bloomers",
    "overalls",
    "suspenders",
)

_DRESS_ONEPIECE: tuple[str, ...] = (
    "dress",
    "sundress",
    "long_dress",
    "short_dress",
    "evening_gown",
    "ball_gown",
    "wedding_dress",
    "off-shoulder_dress",
    "halter_dress",
    "pinafore_dress",
    "frilled_dress",
    "kimono",
    "yukata",
    "furisode",
    "hakama",
    "qipao",
    "china_dress",
    "hanfu",
    "ao_dai",
    "sari",
    "robe",
    "jumpsuit",
    "romper",
    "leotard",
)

_UNIFORM: tuple[str, ...] = (
    "school_uniform",
    "serafuku",
    "sailor_collar",
    "sailor_dress",
    "blazer_uniform",
    "gym_uniform",
    "business_suit",
    "suit",
    "pant_suit",
    "skirt_suit",
    "military_uniform",
    "uniform",
    "maid",
    "waitress",
    "nurse",
    "police_uniform",
    "cheerleader",
    "miko",
    "nun",
    "kunoichi",
    "witch",
    "santa_costume",
    "bunny_girl",
    "playboy_bunny",
    "ninja",
    "armor",
    "dougi",
    "track_suit",
)


class ClothingTops(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.tops"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _TOPS


class ClothingBottoms(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.bottoms"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _BOTTOMS


class ClothingDress(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.dress"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _DRESS_ONEPIECE


class ClothingUniform(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.uniform"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _UNIFORM


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ClothingTops": ClothingTops,
    "ClothingBottoms": ClothingBottoms,
    "ClothingDress": ClothingDress,
    "ClothingUniform": ClothingUniform,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ClothingTops": "Tops",
    "ClothingBottoms": "Bottoms",
    "ClothingDress": "Dress & One-piece",
    "ClothingUniform": "Uniform & Costume",
}
