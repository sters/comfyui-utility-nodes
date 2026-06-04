from typing import Any, ClassVar

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


class _CompositionBase:
    TAGS: ClassVar[tuple[str, ...]] = ()
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        required: dict[str, Any] = {
            "separator": ("STRING", {"multiline": False, "default": ", "}),
        }
        for tag in cls.TAGS:
            required[tag] = ("BOOLEAN", {"default": False})
        return {
            "required": required,
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(self, separator: str, extra: str = "", **tags: bool) -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        parts: list[str] = [tag for tag in self.TAGS if tags.get(tag, False)]
        if extra.strip():
            parts.append(extra.strip())
        prompt = sep.join(parts)
        return {"ui": {"text": (prompt,)}, "result": (prompt,)}


class CompositionAngle(_CompositionBase):
    TAGS = _ANGLE


class CompositionFraming(_CompositionBase):
    TAGS = _FRAMING


class CompositionCrop(_CompositionBase):
    TAGS = _CROP


class CompositionFocus(_CompositionBase):
    TAGS = _FOCUS


class CompositionMultiView(_CompositionBase):
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
