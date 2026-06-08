from typing import ClassVar

from ..._base import TagNodeBase

_FRAMING: tuple[str, ...] = (
    "portrait",
    "upper_body",
    "cowboy_shot",
    "full_body",
    "wide_shot",
    "very_wide_shot",
    "lower_body",
    "close-up",
    "profile",
    "group_profile",
    "cut-in",
    "split_crop",
)


class CompositionFraming(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.framing"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _FRAMING


NODE_CLASS_MAPPINGS: dict[str, type] = {"CompositionFraming": CompositionFraming}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"CompositionFraming": "Framing"}
