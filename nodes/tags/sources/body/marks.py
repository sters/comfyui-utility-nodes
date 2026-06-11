from typing import ClassVar

from ..._base import TagNodeBase

_MOLES_FRECKLES: tuple[str, ...] = (
    "mole",
    "mole_under_eye",
    "mole_under_mouth",
    "mole_on_cheek",
    "mole_on_neck",
    "mole_on_breast",
    "mole_on_stomach",
    "mole_on_thigh",
    "mole_on_ass",
    "mole_on_armpit",
    "freckles",
    "beauty_mark",
    "birthmark",
)

_SCARS: tuple[str, ...] = (
    "scar",
    "scar_on_face",
    "scar_on_cheek",
    "scar_across_eye",
    "scar_on_nose",
    "scar_on_forehead",
    "scar_on_arm",
    "scar_on_chest",
    "scar_on_stomach",
    "scar_on_back",
    "scar_on_neck",
    "scar_on_leg",
    "bandages",
    "bandaged_arm",
    "bandaged_leg",
    "bandage_over_one_eye",
)

_TATTOOS: tuple[str, ...] = (
    "tattoo",
    "facial_tattoo",
    "neck_tattoo",
    "shoulder_tattoo",
    "arm_tattoo",
    "hand_tattoo",
    "chest_tattoo",
    "breast_tattoo",
    "back_tattoo",
    "lower_back_tattoo",
    "stomach_tattoo",
    "thigh_tattoo",
    "leg_tattoo",
)


class BodyMolesFreckles(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.marks.moles"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _MOLES_FRECKLES


class BodyScars(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.marks.scars"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _SCARS


class BodyTattoos(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.marks.tattoos"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _TATTOOS


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesBodyMolesFreckles": BodyMolesFreckles,
    "UtilityNodesBodyScars": BodyScars,
    "UtilityNodesBodyTattoos": BodyTattoos,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesBodyMolesFreckles": "Moles & Freckles",
    "UtilityNodesBodyScars": "Scars",
    "UtilityNodesBodyTattoos": "Tattoos",
}
