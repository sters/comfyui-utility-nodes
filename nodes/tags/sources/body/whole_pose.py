from typing import ClassVar

from ..._base import TagNodeBase

_POSTURE: tuple[str, ...] = (
    "standing",
    "sitting",
    "lying",
    "on_back",
    "on_side",
    "on_stomach",
    "prone",
    "supine",
    "all_fours",
    "crawling",
    "crouching",
    "leaning_forward",
    "leaning_back",
    "leaning_to_the_side",
    "arched_back",
    "bent_over",
    "bending_forward",
    "jumping",
    "running",
    "walking",
    "stretching",
    "dynamic_pose",
    "contrapposto",
    "fetal_position",
    "yoga_pose",
)

_SEATING: tuple[str, ...] = (
    "sitting_on_floor",
    "sitting_on_chair",
    "sitting_on_bed",
    "sitting_on_table",
    "sitting_on_rock",
    "sitting_on_lap",
    "sitting_on_object",
    "yokozuwari",
)


class WholePosture(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.pose.posture"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _POSTURE


class WholeSeating(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.pose.seating"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _SEATING


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "WholePosture": WholePosture,
    "WholeSeating": WholeSeating,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "WholePosture": "Posture",
    "WholeSeating": "Seating Style",
}
