import random
from typing import Any, ClassVar


class ListShuffle:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("items",)
    INPUT_IS_LIST: ClassVar[bool] = True
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True,)
    FUNCTION: ClassVar[str] = "shuffle"
    CATEGORY: ClassVar[str] = "UtilityNodes/Text"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "items": ("STRING", {"forceInput": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True}),
                "limit": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF}),
            },
        }

    def shuffle(
        self,
        items: list[str],
        seed: list[int],
        limit: list[int],
    ) -> tuple[list[str]]:
        # INPUT_IS_LIST=True makes every input a list, even scalar widgets.
        s = seed[0] if seed else 0
        lim = limit[0] if limit else 0

        if not items:
            return ([],)

        rng = random.Random(s)
        shuffled = list(items)
        rng.shuffle(shuffled)
        if lim > 0:
            shuffled = shuffled[:lim]
        return (shuffled,)


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "ListShuffle": ListShuffle,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "ListShuffle": "List Shuffle",
}
