from typing import ClassVar

from .._base import TagNodeBase

_ASIDE: tuple[str, ...] = (
    # Canonical *_aside family
    "clothing_aside",
    "panties_aside",
    "thong_aside",
    "panties_under_pantyhose_aside",
    "male_underwear_aside",
    "fundoshi_aside",
    "loincloth_aside",
    "pelvic_curtain_aside",
    "bra_aside",
    "bikini_aside",
    "bikini_top_aside",
    "bikini_bottom_aside",
    "swimsuit_aside",
    "leotard_aside",
    "dress_aside",
    "shirt_aside",
    "skirt_aside",
    "shorts_aside",
    "buruma_aside",
    "apron_aside",
    "necktie_aside",
    # Slip / strap-down family (wardrobe_malfunction territory)
    "strap_slip",
    "double_strap_slip",
    "suspenders_slip",
    "shoulder_strap_slip",
    "shirt_slip",
    "breast_slip",
    "one_breast_out",
    "one_side_pulled_down",
    "exposed_gusset",
    # Cause / agent
    "pulled_by_self",
    "pulled_by_another",
    "accidental_exposure",
    "assisted_exposure",
    "wind_lift",
)


class ClothingAside(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.aside"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _ASIDE


NODE_CLASS_MAPPINGS: dict[str, type] = {"ClothingAside": ClothingAside}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"ClothingAside": "Clothing: Aside & Partial Expose"}
