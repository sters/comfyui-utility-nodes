from typing import ClassVar

from ..._base import TagNodeBase

# Generic color words intended to be wired into TagDecorate as the
# `decoration` input. These are deliberately the bare color names — not
# the `*_hair` / `*_eyes` variants — so prefixing onto e.g. `pleated_skirt`
# yields a natural phrase like `red pleated_skirt`.
_COLORS: tuple[str, ...] = (
    "red",
    "pink",
    "orange",
    "yellow",
    "green",
    "blue",
    "light_blue",
    "dark_blue",
    "purple",
    "violet",
    "brown",
    "tan",
    "beige",
    "black",
    "white",
    "gray",
    "silver",
    "gold",
    "navy",
    "teal",
    "cyan",
    "magenta",
    "crimson",
    "maroon",
    "olive",
    "lime",
    "aqua",
    "ivory",
    "pastel",
    "neon",
)


class ColorPalette(TagNodeBase):
    """Generic color tags for use as a `TagDecorate` decoration input."""

    CATEGORY_ID: ClassVar[str] = "decoration.color"
    LAYER: ClassVar[str] = "decoration"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _COLORS


NODE_CLASS_MAPPINGS: dict[str, type] = {"ColorPalette": ColorPalette}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"ColorPalette": "Decoration: Color Palette"}
