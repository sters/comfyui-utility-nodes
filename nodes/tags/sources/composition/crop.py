from typing import ClassVar

from ..._base import TagNodeBase

_CROP: tuple[str, ...] = (
    "cropped_legs",
    "cropped_torso",
    "cropped_arms",
    "cropped_shoulders",
    "cropped_head",
    "head_out_of_frame",
    "feet_out_of_frame",
    "eyes_out_of_frame",
    "foot_out_of_frame",
    "knees_out_of_frame",
)


class CompositionCrop(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.crop"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _CROP


NODE_CLASS_MAPPINGS: dict[str, type] = {"CompositionCrop": CompositionCrop}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"CompositionCrop": "Composition: Crop"}
