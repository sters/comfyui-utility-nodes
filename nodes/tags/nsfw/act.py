from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

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
    TAGS = _PENETRATIVE


class NsfwActOralContact(TagNodeBase):
    TAGS = _ORAL_CONTACT


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "NsfwActPenetrative": NsfwActPenetrative,
    "NsfwActOralContact": NsfwActOralContact,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "NsfwActPenetrative": "NSFW Act: Penetrative",
    "NsfwActOralContact": "NSFW Act: Oral & Contact",
}
