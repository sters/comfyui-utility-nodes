from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_POSITION: tuple[str, ...] = (
    "missionary",
    "cowgirl_position",
    "reverse_cowgirl_position",
    "doggystyle",
    "anal_doggystyle",
    "mating_press",
    "prone_bone",
    "piledriver_(sex)",
    "standing_sex",
    "suspended_congress",
    "leg_lock",
    "full_nelson",
    "side-by-side",
    "spooning",
    "lotus_position",
    "carrying_sex",
    "wall_slam",
    "doggystyle_(animal)",
    "threesome",
    "foursome",
    "gangbang",
    "orgy",
    "mmf_threesome",
    "ffm_threesome",
    "mmm_threesome",
    "fff_threesome",
)


class NsfwPosition(TagNodeBase):
    TAGS = _POSITION


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "NsfwPosition": NsfwPosition,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "NsfwPosition": "NSFW: Position",
}
