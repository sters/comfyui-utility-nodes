from typing import Any, ClassVar

_MAX_INPUTS = 10


class TextConcat:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("text",)
    FUNCTION: ClassVar[str] = "concat"
    CATEGORY: ClassVar[str] = "utility/text"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "separator": ("STRING", {"multiline": False, "default": ", "}),
            },
            "optional": {f"text_{i}": ("STRING", {"forceInput": True}) for i in range(1, _MAX_INPUTS + 1)},
        }

    def concat(self, separator: str, **kwargs: str | None) -> tuple[str]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ""
        parts: list[str] = []
        for i in range(1, _MAX_INPUTS + 1):
            v = kwargs.get(f"text_{i}")
            if v is None or v == "":
                continue
            parts.append(v)
        return (sep.join(parts),)


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "TextConcat": TextConcat,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "TextConcat": "Text Concat",
}
