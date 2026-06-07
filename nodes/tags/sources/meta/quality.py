from typing import ClassVar

from ..._base import TagNodeBase

_QUALITY: tuple[str, ...] = (
    "masterpiece",
    "best_quality",
    "high_quality",
    "highres",
    "absurdres",
    "ultra-detailed",
    "ultra_high_res",
    "ultra_realistic",
    "intricate_details",
    "fine_details",
    "detailed_background",
    "official_art",
    "photorealistic",
    "realistic",
    "8k",
    "4k",
    "newest",
    "very_aesthetic",
)


class MetaQuality(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "meta.quality"
    LAYER: ClassVar[str] = "meta"
    MUTEX_WITHIN: ClassVar[bool] = False
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    TAGS = _QUALITY


NODE_CLASS_MAPPINGS: dict[str, type] = {"MetaQuality": MetaQuality}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"MetaQuality": "Meta: Quality (defaults all-on)"}
