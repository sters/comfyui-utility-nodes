from typing import Any, ClassVar

_GENERAL: tuple[str, ...] = (
    "artistic_error",
    "bad_anatomy",
    "anatomical_nonsense",
    "bad_proportions",
    "bad_perspective",
    "bad_reflection",
    "bad_multiple_views",
    "bad_shadow",
    "bad_gun_anatomy",
    "bad_vehicle_anatomy",
    "bad_internal_anatomy",
)

_HEAD_FACE: tuple[str, ...] = (
    "bad_face",
    "bad_neck",
    "bad_ears",
    "bad_teeth",
    "extra_ears",
    "extra_eyes",
    "extra_eyelids",
    "extra_eyebrows",
    "extra_pupils",
    "extra_mouth",
    "extra_tongue",
    "extra_teeth",
    "extra_noses",
    "extra_faces",
    "extra_horns",
    "extra_tusks",
)

_BODY: tuple[str, ...] = (
    "bad_torso",
    "bad_ass",
    "extra_pectorals",
    "extra_nipples",
    "extra_breasts",
    "extra_tails",
)

_LIMBS: tuple[str, ...] = (
    "bad_arm",
    "bad_hands",
    "bad_leg",
    "bad_knees",
    "bad_feet",
    "wrong_hand",
    "wrong_foot",
    "extra_digits",
    "extra_arms",
    "extra_hands",
    "extra_legs",
    "extra_toes",
    "fewer_digits",
)

_NSFW: tuple[str, ...] = (
    "bad_vulva",
    "extra_penises",
    "extra_testicles",
    "extra_pussies",
    "extra_clitorises",
    "extra_anus",
)


class _BadTagsBase:
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
            required[tag] = ("BOOLEAN", {"default": True})
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


class DanbooruBadGeneral(_BadTagsBase):
    TAGS = _GENERAL


class DanbooruBadHeadFace(_BadTagsBase):
    TAGS = _HEAD_FACE


class DanbooruBadBody(_BadTagsBase):
    TAGS = _BODY


class DanbooruBadLimbs(_BadTagsBase):
    TAGS = _LIMBS


class DanbooruBadNSFW(_BadTagsBase):
    TAGS = _NSFW


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "DanbooruBadGeneral": DanbooruBadGeneral,
    "DanbooruBadHeadFace": DanbooruBadHeadFace,
    "DanbooruBadBody": DanbooruBadBody,
    "DanbooruBadLimbs": DanbooruBadLimbs,
    "DanbooruBadNSFW": DanbooruBadNSFW,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "DanbooruBadGeneral": "Danbooru Bad: General",
    "DanbooruBadHeadFace": "Danbooru Bad: Head & Face",
    "DanbooruBadBody": "Danbooru Bad: Body",
    "DanbooruBadLimbs": "Danbooru Bad: Limbs",
    "DanbooruBadNSFW": "Danbooru Bad: NSFW",
}
