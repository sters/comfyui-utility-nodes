from typing import ClassVar

from ...._base import TagNodeBase

_STATE: tuple[str, ...] = (
    "open_mouth",
    "closed_mouth",
    "parted_lips",
    "gritted_teeth",
    "clenched_teeth",
    "pout",
    "biting_lip",
    ":3",
    ":d",
    ":o",
    ":p",
    ":q",
    ":t",
    ":<",
    ":>",
    "wavy_mouth",
)

_DETAILS: tuple[str, ...] = (
    "tongue",
    "tongue_out",
    "licking_lips",
    "uvula",
    "teeth",
    "fang",
    "fangs",
    "sharp_teeth",
    "gap_teeth",
    "lipstick",
    "shiny_lips",
    "thick_lips",
    "drooling",
)


class FaceMouthState(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.face.mouth.state"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _STATE


class FaceMouthDetails(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.face.mouth.details"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _DETAILS


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "FaceMouthState": FaceMouthState,
    "FaceMouthDetails": FaceMouthDetails,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "FaceMouthState": "Mouth: State",
    "FaceMouthDetails": "Mouth: Details",
}
