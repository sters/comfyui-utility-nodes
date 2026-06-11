from typing import ClassVar

from ..._base import TagNodeBase

_EXPOSURE: tuple[str, ...] = (
    "nude",
    "completely_nude",
    "partially_nude",
)

_LOWER_ANATOMY: tuple[str, ...] = (
    "ass",
    "ass_visible_through_thighs",
    "cameltoe",
    "pussy",
    "anus",
    "clitoris",
    "pubic_hair",
    "female_pubic_hair",
    "presenting",
)


class BodyExposure(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.exposure"
    LAYER: ClassVar[str] = "exposure"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _EXPOSURE


class BodyLowerAnatomy(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.lower_anatomy"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _LOWER_ANATOMY


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesBodyExposure": BodyExposure,
    "UtilityNodesBodyLowerAnatomy": BodyLowerAnatomy,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesBodyExposure": "Exposure",
    "UtilityNodesBodyLowerAnatomy": "Lower Anatomy",
}
