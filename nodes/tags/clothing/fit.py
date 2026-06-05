from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_FIT: tuple[str, ...] = (
    "skin_tight",
    "form_fitting",
    "tight_clothes",
    "tight_shirt",
    "tight_dress",
    "tight_pants",
    "taut_clothes",
    "taut_shirt",
    "taut_dress",
    "taut_swimsuit",
    "loose_clothes",
    "loose_shirt",
    "loose_pants",
    "baggy_clothes",
    "baggy_pants",
    "oversized_clothes",
    "oversized_shirt",
    "bursting_breasts",
)


class ClothingFit(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.fit"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _FIT


NODE_CLASS_MAPPINGS: dict[str, type] = {"ClothingFit": ClothingFit}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"ClothingFit": "Clothing: Fit"}
