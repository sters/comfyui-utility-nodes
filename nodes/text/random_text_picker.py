import random
from typing import Any, ClassVar


class RandomTextPicker:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("text",)
    FUNCTION: ClassVar[str] = "pick"
    CATEGORY: ClassVar[str] = "UtilityNodes/Text"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "delimiter": ("STRING", {"multiline": False, "default": ","}),
                "count": ("INT", {"default": 1, "min": 1, "max": 1024}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True}),
            },
        }

    def pick(self, text: str, delimiter: str, count: int, seed: int) -> tuple[str]:
        sep = delimiter.encode("utf-8").decode("unicode_escape") if delimiter else ","
        items = [s.strip() for s in text.split(sep)]
        items = [s for s in items if s]

        if not items:
            return ("",)

        rng = random.Random(seed)
        n = min(count, len(items))
        picked = rng.sample(items, n)
        return (sep.join(picked),)


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "RandomTextPicker": RandomTextPicker,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "RandomTextPicker": "Random Text Picker",
}
