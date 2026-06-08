from typing import ClassVar

from ..._base import TagNodeBase

_ACTION: tuple[str, ...] = (
    "eating",
    "drinking",
    "licking",
    "smoking",
    "reading",
    "writing",
    "drawing",
    "painting",
    "sleeping",
    "dreaming",
    "napping",
    "dancing",
    "singing",
    "playing_instrument",
    "playing_guitar",
    "playing_piano",
    "cooking",
    "baking",
    "cleaning",
    "washing",
    "bathing",
    "showering",
    "swimming",
    "diving",
    "fishing",
    "shopping",
    "studying",
    "gaming",
    "praying",
    "meditating",
    "phone_call",
    "texting",
    "selfie",
    "waving",
    "pointing",
    "carrying",
    "hugging",
    "petting",
)


class BodyAction(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.action"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _ACTION


NODE_CLASS_MAPPINGS: dict[str, type] = {"BodyAction": BodyAction}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"BodyAction": "Action"}
