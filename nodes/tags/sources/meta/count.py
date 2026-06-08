from typing import ClassVar

from ..._base import TagNodeBase

_TOTAL: tuple[str, ...] = (
    "solo",
    "solo_focus",
    "duo",
    "trio",
    "group",
    "pov",
)

_GIRLS: tuple[str, ...] = (
    "1girl",
    "2girls",
    "3girls",
    "4girls",
    "5girls",
    "6+girls",
    "multiple_girls",
)

_BOYS: tuple[str, ...] = (
    "1boy",
    "2boys",
    "3boys",
    "4boys",
    "5boys",
    "6+boys",
    "multiple_boys",
)

_OTHER: tuple[str, ...] = (
    "1other",
    "multiple_others",
    "couple",
    "yuri",
    "yaoi",
)


class MetaCountTotal(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "meta.count.total"
    LAYER: ClassVar[str] = "meta"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _TOTAL


class MetaCountGirls(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "meta.count.girls"
    LAYER: ClassVar[str] = "meta"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _GIRLS


class MetaCountBoys(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "meta.count.boys"
    LAYER: ClassVar[str] = "meta"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _BOYS


class MetaCountOther(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "meta.count.other"
    LAYER: ClassVar[str] = "meta"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _OTHER


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "MetaCountTotal": MetaCountTotal,
    "MetaCountGirls": MetaCountGirls,
    "MetaCountBoys": MetaCountBoys,
    "MetaCountOther": MetaCountOther,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "MetaCountTotal": "Subject Count: Total",
    "MetaCountGirls": "Subject Count: Girls",
    "MetaCountBoys": "Subject Count: Boys",
    "MetaCountOther": "Subject Count: Other",
}
