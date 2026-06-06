from typing import ClassVar

from .._base import TagNodeBase

_MATERIAL: tuple[str, ...] = (
    "see-through",
    "see-through_silhouette",
    "transparent",
    "wet_clothes",
    "torn_clothes",
    "lace",
    "lace_trim",
    "frilled",
    "frills",
    "ribbed",
    "knit",
    "mesh",
    "fishnets",
    "denim",
    "leather",
    "latex",
    "rubber",
    "vinyl",
    "silk",
    "satin",
    "velvet",
    "fur",
    "fur_trim",
    "wool",
    "metallic",
    "shiny_clothes",
)

_PATTERN: tuple[str, ...] = (
    "striped",
    "vertical_stripes",
    "horizontal_stripes",
    "diagonal_stripes",
    "striped_clothes",
    "polka_dot",
    "plaid",
    "checkered",
    "checkered_clothes",
    "argyle",
    "houndstooth",
    "floral_print",
    "leaf_print",
    "star_print",
    "heart_print",
    "animal_print",
    "leopard_print",
    "zebra_print",
    "camouflage",
    "tie-dye",
    "gradient_clothes",
    "two-tone_clothes",
    "multicolored_clothes",
    "print_shirt",
    "print_dress",
    "print_skirt",
)


class ClothingMaterial(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.material"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _MATERIAL


class ClothingPattern(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.pattern"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _PATTERN


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ClothingMaterial": ClothingMaterial,
    "ClothingPattern": ClothingPattern,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ClothingMaterial": "Clothing: Material",
    "ClothingPattern": "Clothing: Pattern",
}
