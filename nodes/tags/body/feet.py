from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_FEET: tuple[str, ...] = (
    "barefoot",
    "no_shoes",
    "feet",
    "toes",
    "toenails",
    "soles",
    "feet_together",
    "feet_up",
    "crossed_ankles",
    "tiptoes",
)

_LEGS_POSE: tuple[str, ...] = (
    "legs",
    "thighs",
    "bare_legs",
    "thigh_gap",
    "spread_legs",
    "crossed_legs",
    "leg_up",
    "leg_lift",
    "knee_up",
    "knees_up",
    "knees_together_feet_apart",
    "standing_on_one_leg",
    "on_one_leg",
    "kneeling",
    "squatting",
    "wariza",
    "seiza",
    "indian_style",
)


class FeetAnatomy(TagNodeBase):
    TAGS = _FEET


class FeetLegsPose(TagNodeBase):
    TAGS = _LEGS_POSE


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "FeetAnatomy": FeetAnatomy,
    "FeetLegsPose": FeetLegsPose,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "FeetAnatomy": "Feet: Anatomy",
    "FeetLegsPose": "Feet: Legs & Pose",
}
