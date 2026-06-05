from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from nodes.tags._base import TagNodeBase
else:
    from _cuun_tag_node_base import TagNodeBase

_ASIDE: tuple[str, ...] = (
    "panties_aside",
    "thong_aside",
    "swimsuit_aside",
    "bikini_aside",
    "bra_aside",
    "bra_lift",
    "panties_under_pantyhose_aside",
    "one_breast_out",
    "breast_slip",
    "shoulder_strap_slip",
    "one_side_pulled_down",
    "pulled_by_self",
    "pulled_by_another",
    "exposed_belly",
    "exposed_collarbone",
    "exposed_pussy",
)


class ClothingAside(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "clothing.aside"
    LAYER: ClassVar[str] = "clothing"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _ASIDE


NODE_CLASS_MAPPINGS: dict[str, type] = {"ClothingAside": ClothingAside}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"ClothingAside": "Clothing: Aside & Partial Expose"}
