from typing import ClassVar

from ..._base import TagNodeBase

_EARS: tuple[str, ...] = (
    "animal_ears",
    "cat_ears",
    "dog_ears",
    "fox_ears",
    "wolf_ears",
    "rabbit_ears",
    "bunny_ears",
    "mouse_ears",
    "horse_ears",
    "cow_ears",
    "sheep_ears",
    "bear_ears",
    "deer_ears",
    "tiger_ears",
    "lion_ears",
    "monkey_ears",
    "raccoon_ears",
    "elf_ears",
    "pointy_ears",
    "fish_ears",
    "bird_ears",
)

_TAIL: tuple[str, ...] = (
    "tail",
    "animal_tail",
    "cat_tail",
    "dog_tail",
    "fox_tail",
    "wolf_tail",
    "rabbit_tail",
    "monkey_tail",
    "horse_tail",
    "cow_tail",
    "lizard_tail",
    "snake_tail",
    "dragon_tail",
    "demon_tail",
    "devil_tail",
    "feathered_tail",
    "multiple_tails",
)

_WINGS: tuple[str, ...] = (
    "wings",
    "angel_wings",
    "demon_wings",
    "fairy_wings",
    "bat_wings",
    "butterfly_wings",
    "dragon_wings",
    "feathered_wings",
    "insect_wings",
    "mechanical_wings",
    "small_wings",
    "large_wings",
)

_HORNS: tuple[str, ...] = (
    "horns",
    "single_horn",
    "multiple_horns",
    "demon_horns",
    "devil_horns",
    "oni_horns",
    "dragon_horns",
    "deer_horns",
    "ram_horns",
    "curled_horns",
    "antlers",
)


class AnimalEars(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.animal.ears"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _EARS


class AnimalTail(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.animal.tail"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _TAIL


class AnimalWings(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.animal.wings"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _WINGS


class AnimalHorns(TagNodeBase):
    CATEGORY_ID: ClassVar[str] = "body.animal.horns"
    LAYER: ClassVar[str] = "anatomy"
    MUTEX_WITHIN: ClassVar[bool] = True
    TAGS = _HORNS


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "AnimalEars": AnimalEars,
    "AnimalTail": AnimalTail,
    "AnimalWings": AnimalWings,
    "AnimalHorns": AnimalHorns,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "AnimalEars": "Body: Animal Ears",
    "AnimalTail": "Body: Animal Tail",
    "AnimalWings": "Body: Wings",
    "AnimalHorns": "Body: Horns",
}
