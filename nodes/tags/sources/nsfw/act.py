from typing import ClassVar

from ..._base import TagNodeBase

_PENETRATIVE: tuple[str, ...] = (
    "sex",
    "vaginal",
    "anal",
    "double_penetration",
    "triple_penetration",
    "deepthroat",
    "vaginal_object_insertion",
    "anal_object_insertion",
    "fingering",
    "vaginal_fingering",
    "anal_fingering",
    "rough_sex",
    "sex_from_behind",
    "imminent_penetration",
    "spitroast",
)

_ORAL_CONTACT: tuple[str, ...] = (
    "fellatio",
    "irrumatio",
    "cunnilingus",
    "paizuri",
    "handjob",
    "footjob",
    "thigh_sex",
    "kissing",
    "french_kiss",
    "breast_sucking",
    "nipple_sucking",
    "breast_grab",
    "ass_grab",
    "groping",
    "frottage",
    "tribadism",
    "autofellatio",
    "autocunnilingus",
    "licking",
    "biting",
    "bukkake",
)


class NsfwActPenetrative(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "nsfw.act.penetrative"
    LAYER: ClassVar[str] = "nsfw_act"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _PENETRATIVE


class NsfwActOralContact(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "nsfw.act.oral_contact"
    LAYER: ClassVar[str] = "nsfw_act"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _ORAL_CONTACT


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesNsfwActPenetrative": NsfwActPenetrative,
    "UtilityNodesNsfwActOralContact": NsfwActOralContact,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesNsfwActPenetrative": "Act: Penetrative",
    "UtilityNodesNsfwActOralContact": "Act: Oral & Contact",
}
