from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_FIGURE: tuple[str, ...] = (
    "petite",
    "slim",
    "curvy",
    "toned",
    "muscular",
    "muscular_female",
    "muscular_male",
    "abs",
    "toned_female",
    "toned_male",
    "thick_thighs",
    "wide_hips",
    "thigh_gap",
    "skindentation",
    "pectorals",
    "large_pectorals",
    "narrow_waist",
    "plump",
    "chubby",
)

_SKIN: tuple[str, ...] = (
    "pale_skin",
    "white_skin",
    "fair_skin",
    "tan",
    "tanlines",
    "dark_skin",
    "dark-skinned_female",
    "dark-skinned_male",
    "very_dark_skin",
    "shiny_skin",
    "colored_skin",
)


class BodyFigure(TagNodeBase):
    TAGS = _FIGURE


class BodySkin(TagNodeBase):
    TAGS = _SKIN


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "BodyFigure": BodyFigure,
    "BodySkin": BodySkin,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "BodyFigure": "Body: Figure",
    "BodySkin": "Body: Skin",
}
