from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_COLOR: tuple[str, ...] = (
    "blue_eyes",
    "red_eyes",
    "brown_eyes",
    "green_eyes",
    "purple_eyes",
    "violet_eyes",
    "yellow_eyes",
    "gold_eyes",
    "orange_eyes",
    "pink_eyes",
    "black_eyes",
    "grey_eyes",
    "aqua_eyes",
    "white_eyes",
    "multicolored_eyes",
    "heterochromia",
    "gradient_eyes",
)

_STATE: tuple[str, ...] = (
    "closed_eyes",
    "one_eye_closed",
    "half-closed_eyes",
    "narrowed_eyes",
    "wide-eyed",
    "looking_at_viewer",
    "looking_away",
    "looking_down",
    "looking_up",
    "looking_back",
    "looking_to_the_side",
    "looking_ahead",
    "looking_at_another",
    "side_glance",
    "eye_contact",
    "glaring",
    "rolling_eyes",
    "crying",
    "teary_eyes",
    "streaming_tears",
)

_DETAILS: tuple[str, ...] = (
    "heart-shaped_pupils",
    "star-shaped_pupils",
    "plus-shaped_pupils",
    "cross-shaped_pupils",
    "slit_pupils",
    "dot_pupils",
    "mismatched_pupils",
    "no_pupils",
    "white_pupils",
    "glowing_eyes",
    "shiny_eyes",
    "sparkling_eyes",
    "jeweled_eyes",
    "empty_eyes",
    "blank_eyes",
    "long_eyelashes",
    "thick_eyebrows",
    "thin_eyebrows",
    "aegyo_sal",
    "eyeshadow",
    "eyeliner",
    "tsurime",
    "tareme",
)


class FaceEyesColor(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.face.eyes.color"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _COLOR


class FaceEyesState(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.face.eyes.state"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _STATE


class FaceEyesDetails(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.face.eyes.details"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _DETAILS


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "FaceEyesColor": FaceEyesColor,
    "FaceEyesState": FaceEyesState,
    "FaceEyesDetails": FaceEyesDetails,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "FaceEyesColor": "Face / Eyes: Color",
    "FaceEyesState": "Face / Eyes: State & Gaze",
    "FaceEyesDetails": "Face / Eyes: Pupils & Details",
}
