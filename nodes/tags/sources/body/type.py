from typing import ClassVar

from ..._base import TagNodeBase

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
    CATEGORY_ID: ClassVar[str] = "body.figure"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _FIGURE


class BodySkin(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.skin"
    LAYER: ClassVar[str] = "anatomy"
    # Not category-mutex: tone (pale/tan/dark) combined with state
    # (tanlines/shiny_skin) is the normal pattern. Tone exclusivity
    # is enforced by a MUTEX_GROUP entry in _conflicts.py.
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _SKIN


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesBodyFigure": BodyFigure,
    "UtilityNodesBodySkin": BodySkin,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesBodyFigure": "Figure",
    "UtilityNodesBodySkin": "Skin",
}
