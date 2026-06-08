from typing import ClassVar

from ..._base import TagNodeBase

_POSITION: tuple[str, ...] = (
    "goggles_on_head",
    "glasses_on_head",
    "sunglasses_on_head",
    "hood_up",
    "hood_down",
    "headphones_around_neck",
    "mask_pull",
    "mask_down",
    "mask_up",
    "hat_over_eyes",
    "hat_tip",
    "jacket_on_shoulders",
    "coat_on_shoulders",
    "jacket_partially_removed",
    "off_shoulder",
    "single_off_shoulder",
    "clothes_around_waist",
    "shirt_around_waist",
    "scarf_over_mouth",
    "necktie_over_shoulder",
)


class ClothingPosition(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.position"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _POSITION


NODE_CLASS_MAPPINGS: dict[str, type] = {"ClothingPosition": ClothingPosition}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"ClothingPosition": "Position"}
