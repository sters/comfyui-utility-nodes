from typing import ClassVar

from ..._base import TagNodeBase

_SIZE: tuple[str, ...] = (
    "flat_chest",
    "small_breasts",
    "medium_breasts",
    "large_breasts",
    "huge_breasts",
    "gigantic_breasts",
)

_SHAPE_STATE: tuple[str, ...] = (
    "cleavage",
    "sideboob",
    "underboob",
    "backboob",
    "breasts_apart",
    "breast_press",
    "between_breasts",
    "covered_nipples",
    "cleavage_cutout",
    "asymmetrical_docking",
    "sagging_breasts",
    "downblouse",
    "nipples",
    "puffy_nipples",
    "inverted_nipples",
    "pointy_breasts",
    "areolae",
    "areola_slip",
    "nipple_slip",
    "breasts_out",
    "no_bra",
    "pasties",
    "nipple_piercing",
)


class BreastsSize(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.breasts.size"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _SIZE


class BreastsShapeState(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.breasts.shape_state"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _SHAPE_STATE


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "BreastsSize": BreastsSize,
    "BreastsShapeState": BreastsShapeState,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "BreastsSize": "Breasts: Size",
    "BreastsShapeState": "Breasts: Shape & State",
}
