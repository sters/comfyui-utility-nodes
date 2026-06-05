from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

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


class CompositionAngle(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.angle"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _ANGLE


class CompositionFraming(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.framing"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _FRAMING


class CompositionCrop(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.crop"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _CROP


class CompositionFocus(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.focus"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _FOCUS


class CompositionMultiView(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "composition.multi_view"
    LAYER: ClassVar[str] = "composition"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _MULTIVIEW


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "CompositionAngle": CompositionAngle,
    "CompositionFraming": CompositionFraming,
    "CompositionCrop": CompositionCrop,
    "CompositionFocus": CompositionFocus,
    "CompositionMultiView": CompositionMultiView,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "CompositionAngle": "Composition: Angle",
    "CompositionFraming": "Composition: Framing",
    "CompositionCrop": "Composition: Crop",
    "CompositionFocus": "Composition: Focus",
    "CompositionMultiView": "Composition: Multi-View",
}
