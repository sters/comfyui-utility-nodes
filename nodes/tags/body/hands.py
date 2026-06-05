from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_POSE: tuple[str, ...] = (
    "hand_up",
    "hands_up",
    "arm_up",
    "arms_up",
    "arm_behind_back",
    "arms_behind_back",
    "arm_behind_head",
    "arms_behind_head",
    "arm_at_side",
    "arm_support",
    "outstretched_arm",
    "outstretched_arms",
    "crossed_arms",
    "hand_on_own_hip",
    "hand_on_own_chest",
    "hand_on_own_face",
    "hand_to_own_mouth",
    "hand_on_another's_head",
    "hand_in_pocket",
    "own_hands_together",
    "holding_hands",
    "interlocked_fingers",
    "finger_to_mouth",
)

_GESTURE: tuple[str, ...] = (
    "v",
    "peace_sign",
    "double_peace",
    "thumbs_up",
    "pointing",
    "pointing_at_viewer",
    "index_finger_raised",
    "clenched_hand",
    "clenched_hands",
    "open_hand",
    "fist",
    "waving",
)

_DETAIL: tuple[str, ...] = (
    "fingernails",
    "long_fingernails",
    "sharp_fingernails",
    "nail_polish",
    "black_nails",
    "red_nails",
    "pink_nails",
    "blue_nails",
    "claws",
)


class HandsPose(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.hands.pose"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _POSE


class HandsGesture(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.hands.gesture"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _GESTURE


class HandsDetail(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.hands.detail"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _DETAIL


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "HandsPose": HandsPose,
    "HandsGesture": HandsGesture,
    "HandsDetail": HandsDetail,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "HandsPose": "Hands: Pose",
    "HandsGesture": "Hands: Gesture",
    "HandsDetail": "Hands: Detail",
}
