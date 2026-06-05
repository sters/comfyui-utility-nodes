from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

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
    TAGS = _EXPOSURE


class BodyLowerAnatomy(TagNodeBase):
    TAGS = _LOWER_ANATOMY


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "BodyExposure": BodyExposure,
    "BodyLowerAnatomy": BodyLowerAnatomy,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "BodyExposure": "Body: Exposure",
    "BodyLowerAnatomy": "Body: Lower Anatomy",
}
