from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_SOLO: tuple[str, ...] = (
    "masturbation",
    "female_masturbation",
    "male_masturbation",
    "pussy_juice",
    "nipple_tweak",
    "nipple_pinch",
    "spread_pussy",
    "spread_ass",
    "presenting",
    "anal_fingering",
)

_TOY: tuple[str, ...] = (
    "sex_toy",
    "dildo",
    "vibrator",
    "anal_beads",
    "butt_plug",
    "anal_tail",
    "huge_dildo",
    "vibrator_in_thighhighs",
    "vibrator_on_nipple",
    "vibrator_under_clothes",
    "onahole",
    "fleshlight",
    "condom",
    "used_condom",
    "egg_vibrator",
    "wand_vibrator",
)

_BDSM: tuple[str, ...] = (
    "bdsm",
    "bondage",
    "restrained",
    "arms_behind_back",
    "tied_up",
    "rope",
    "shibari",
    "suspension_bondage",
    "handcuffs",
    "shackles",
    "chained",
    "leash",
    "ball_gag",
    "ring_gag",
    "gag",
    "tape_gag",
    "spanking",
    "hair_pull",
    "choking",
    "torture",
    "humiliation",
    "slave",
)


class NsfwSolo(TagNodeBase):
    TAGS = _SOLO


class NsfwToy(TagNodeBase):
    TAGS = _TOY


class NsfwBdsm(TagNodeBase):
    TAGS = _BDSM


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "NsfwSolo": NsfwSolo,
    "NsfwToy": NsfwToy,
    "NsfwBdsm": NsfwBdsm,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "NsfwSolo": "NSFW: Solo",
    "NsfwToy": "NSFW: Toy",
    "NsfwBdsm": "NSFW: BDSM",
}
