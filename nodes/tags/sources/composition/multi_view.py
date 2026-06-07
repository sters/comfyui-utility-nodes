from typing import ClassVar

from ..._base import TagNodeBase

_MULTIVIEW: tuple[str, ...] = (
    "multiple_views",
    "reference_sheet",
    "character_chart",
    "turnaround",
    "sprite_sheet",
    "multiple_expressions",
    "variations",
    "projected_inset",
    "zoom_layer",
    "age_comparison",
    "clothes_on_and_off",
)


class CompositionMultiView(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.multi_view"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _MULTIVIEW


NODE_CLASS_MAPPINGS: dict[str, type] = {"CompositionMultiView": CompositionMultiView}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"CompositionMultiView": "Composition: Multi-View"}
