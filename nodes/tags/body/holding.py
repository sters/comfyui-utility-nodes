from typing import ClassVar

from .._base import TagNodeBase

_OBJECT: tuple[str, ...] = (
    "holding",
    "holding_book",
    "holding_phone",
    "holding_food",
    "holding_cup",
    "holding_bottle",
    "holding_drink",
    "holding_pen",
    "holding_pencil",
    "holding_paper",
    "holding_letter",
    "holding_envelope",
    "holding_flower",
    "holding_bouquet",
    "holding_umbrella",
    "holding_microphone",
    "holding_camera",
    "holding_stuffed_toy",
    "holding_bag",
    "holding_basket",
    "holding_chopsticks",
    "holding_fork",
    "holding_spoon",
    "holding_cigarette",
    "holding_fan",
    "holding_mask",
    "holding_clothes",
    "holding_underwear",
    "holding_leash",
)

_WEAPON: tuple[str, ...] = (
    "holding_weapon",
    "holding_sword",
    "holding_katana",
    "holding_knife",
    "holding_dagger",
    "holding_gun",
    "holding_handgun",
    "holding_rifle",
    "holding_bow_(weapon)",
    "holding_arrow",
    "holding_staff",
    "holding_wand",
    "holding_polearm",
    "holding_spear",
    "holding_lance",
    "holding_scythe",
    "holding_axe",
    "holding_hammer",
    "holding_shield",
    "holding_whip",
    "holding_chain",
)


class HoldingObject(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.holding.object"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _OBJECT


class HoldingWeapon(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.holding.weapon"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = False
    TAGS = _WEAPON


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "HoldingObject": HoldingObject,
    "HoldingWeapon": HoldingWeapon,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "HoldingObject": "Body: Holding (object)",
    "HoldingWeapon": "Body: Holding (weapon)",
}
