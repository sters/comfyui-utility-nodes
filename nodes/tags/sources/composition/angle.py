from typing import ClassVar

from ..._base import TagNodeBase

_ANGLE: tuple[str, ...] = (
    "dutch_angle",
    "from_above",
    "from_behind",
    "from_below",
    "from_side",
    "sideways",
    "three-quarter_view",
    "straight-on",
    "upside-down",
    "pov",
    "from_outside",
    "from_inside",
    "partially_underwater_shot",
    "atmospheric_perspective",
    "fisheye",
    "perspective",
    "vanishing_point",
    "foreshortening",
)


class CompositionAngle(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.angle"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _ANGLE


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesCompositionAngle": CompositionAngle}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesCompositionAngle": "Angle"}
