from typing import ClassVar

from ..._base import TagNodeBase

_FOCUS: tuple[str, ...] = (
    "armpit_focus",
    "ass_focus",
    "back_focus",
    "breast_focus",
    "eye_focus",
    "foot_focus",
    "hand_focus",
    "hip_focus",
    "leg_focus",
    "navel_focus",
    "pectoral_focus",
    "penis_focus",
    "thigh_focus",
)


class CompositionFocus(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.focus"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _FOCUS


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesCompositionFocus": CompositionFocus}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesCompositionFocus": "Focus"}
