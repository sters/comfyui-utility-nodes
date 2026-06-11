from typing import ClassVar

from ..._base import TagNodeBase

_BG_TYPE: tuple[str, ...] = (
    "simple_background",
    "white_background",
    "black_background",
    "grey_background",
    "gradient_background",
    "blurry_background",
    "transparent_background",
    "abstract_background",
    "two-tone_background",
    "checkered_background",
    "floral_background",
    "striped_background",
    "dotted_background",
    "patterned_background",
    "scenery",
    "no_background",
)

_INDOOR: tuple[str, ...] = (
    "indoors",
    "classroom",
    "school",
    "kitchen",
    "bedroom",
    "bathroom",
    "shower",
    "bathtub",
    "library",
    "hospital",
    "office",
    "gym",
    "cafe",
    "restaurant",
    "bar",
    "train_interior",
    "car_interior",
    "dressing_room",
    "locker_room",
    "shrine",
    "church",
    "club",
    "casino",
    "stage",
)

_OUTDOOR: tuple[str, ...] = (
    "outdoors",
    "beach",
    "ocean",
    "lake",
    "river",
    "pool",
    "forest",
    "jungle",
    "mountain",
    "field",
    "meadow",
    "garden",
    "park",
    "street",
    "alley",
    "city",
    "skyline",
    "rooftop",
    "schoolyard",
    "playground",
    "festival",
    "snowfield",
    "desert",
    "ruins",
    "shrine_outdoors",
)


class SceneBackgroundType(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "scene.bg_type"
    LAYER: ClassVar[str] = "scene"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _BG_TYPE


class SceneIndoor(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "scene.indoor"
    LAYER: ClassVar[str] = "scene"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _INDOOR


class SceneOutdoor(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "scene.outdoor"
    LAYER: ClassVar[str] = "scene"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _OUTDOOR


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesSceneBackgroundType": SceneBackgroundType,
    "UtilityNodesSceneIndoor": SceneIndoor,
    "UtilityNodesSceneOutdoor": SceneOutdoor,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesSceneBackgroundType": "Background Type",
    "UtilityNodesSceneIndoor": "Indoor Location",
    "UtilityNodesSceneOutdoor": "Outdoor Location",
}
