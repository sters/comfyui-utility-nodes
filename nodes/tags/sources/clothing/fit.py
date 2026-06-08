from typing import ClassVar

from ..._base import TagNodeBase

_FIT: tuple[str, ...] = (
    # Skin-tight family (no gap to body, contours shown)
    "skin_tight",
    "form_fitting",
    "impossible_clothes",
    "impossible_shirt",
    "impossible_dress",
    "impossible_leotard",
    "impossible_swimsuit",
    "impossible_bodysuit",
    # Tight-fit items
    "tight_clothes",
    "tight_top",
    "tight_shirt",
    "tight_dress",
    "tight_pants",
    "tight_bottoms",
    "tight_jacket",
    # Taut (fabric stress / wrinkles from tension)
    "taut_clothes",
    "taut_shirt",
    "taut_dress",
    "taut_skirt",
    "taut_shorts",
    "taut_jacket",
    "taut_sweater",
    "taut_sweater_vest",
    "taut_vest",
    "taut_camisole",
    "taut_bandeau",
    "taut_leotard",
    "taut_bodysuit",
    "taut_bodystocking",
    "taut_swimsuit",
    "taut_bikini",
    # Loose / baggy / oversized
    "loose_clothes",
    "loose_shirt",
    "loose_pants",
    "baggy_clothes",
    "baggy_pants",
    "oversized_clothes",
    "oversized_shirt",
    # Fit-failure
    "bursting_breasts",
    "button_gap",
    "popped_button",
    "undersized_clothes",
    # Body-hugging full-body garments (often appear with tight/skin-tight)
    "bodysuit",
    "catsuit",
    "unitard",
    "bikesuit",
)


class ClothingFit(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.fit"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _FIT


NODE_CLASS_MAPPINGS: dict[str, type] = {"ClothingFit": ClothingFit}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"ClothingFit": "Fit"}
