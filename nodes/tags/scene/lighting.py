from typing import ClassVar

from .._base import TagNodeBase

_LIGHTING: tuple[str, ...] = (
    "backlighting",
    "rim_lighting",
    "soft_lighting",
    "hard_lighting",
    "dramatic_lighting",
    "cinematic_lighting",
    "volumetric_lighting",
    "ambient_lighting",
    "studio_lighting",
    "natural_lighting",
    "harsh_lighting",
    "dappled_sunlight",
    "sunlight",
    "moonlight",
    "candlelight",
    "lamp_light",
    "neon_lights",
    "neon_trim",
    "lens_flare",
    "god_rays",
    "light_rays",
    "sun_dappling",
    "silhouette",
    "chiaroscuro",
    "low_key",
    "high_key",
    "spotlight",
    "rim_light",
)


class SceneLighting(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "scene.lighting"
    LAYER: ClassVar[str] = "scene"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _LIGHTING


NODE_CLASS_MAPPINGS: dict[str, type] = {"SceneLighting": SceneLighting}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"SceneLighting": "Scene: Lighting"}
