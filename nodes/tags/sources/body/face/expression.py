from typing import ClassVar

from ...._base import TagNodeBase

_EXPRESSION: tuple[str, ...] = (
    "smile",
    "grin",
    "smirk",
    "smug",
    "happy",
    "laughing",
    "wry_smile",
    "embarrassed",
    "nervous",
    "shy",
    "worried",
    "confused",
    "frown",
    "scowl",
    "angry",
    "annoyed",
    "pouting",
    "sad",
    "depressed",
    "tearful",
    "surprised",
    "shocked",
    "scared",
    "frightened",
    "yandere",
    "ahegao",
    "fucked_silly",
    "serious",
    "expressionless",
    "blank_expression",
    "bored",
    "sleepy",
    "drowsy",
    "tired",
    "determined",
    "smug_grin",
)

_BLUSH_FLUSH: tuple[str, ...] = (
    "blush",
    "light_blush",
    "full-face_blush",
    "embarrassed_blush",
    "nose_blush",
    "blush_stickers",
    "scribble_blush",
    "heavy_breathing",
    "panting",
    "sweatdrop",
    "trembling",
    "shaking",
    "flying_sweatdrops",
)


class FaceExpression(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.face.expression"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _EXPRESSION


class FaceBlushFlush(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.face.blush_flush"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _BLUSH_FLUSH


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesFaceExpression": FaceExpression,
    "UtilityNodesFaceBlushFlush": FaceBlushFlush,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesFaceExpression": "Expression",
    "UtilityNodesFaceBlushFlush": "Blush & Flush",
}
