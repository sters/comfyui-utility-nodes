from typing import ClassVar

from .._base import TagNodeBase

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


class BadGeneral(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "bad.general"
    LAYER: ClassVar[str] = "bad"
    MUTEX_WITHIN: ClassVar[bool] = False
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    TAGS = _GENERAL


class BadHeadFace(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "bad.head_face"
    LAYER: ClassVar[str] = "bad"
    MUTEX_WITHIN: ClassVar[bool] = False
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    TAGS = _HEAD_FACE


class BadBody(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "bad.body"
    LAYER: ClassVar[str] = "bad"
    MUTEX_WITHIN: ClassVar[bool] = False
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    TAGS = _BODY


class BadLimbs(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "bad.limbs"
    LAYER: ClassVar[str] = "bad"
    MUTEX_WITHIN: ClassVar[bool] = False
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    TAGS = _LIMBS


class BadNSFW(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "bad.nsfw"
    LAYER: ClassVar[str] = "bad"
    MUTEX_WITHIN: ClassVar[bool] = False
    DEFAULT_BOOLEAN: ClassVar[bool] = True
    TAGS = _NSFW


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "BadGeneral": BadGeneral,
    "BadHeadFace": BadHeadFace,
    "BadBody": BadBody,
    "BadLimbs": BadLimbs,
    "BadNSFW": BadNSFW,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "BadGeneral": "Bad: General",
    "BadHeadFace": "Bad: Head & Face",
    "BadBody": "Bad: Body",
    "BadLimbs": "Bad: Limbs",
    "BadNSFW": "Bad: NSFW",
}
