from typing import Any, ClassVar

NODE_CLASS_MAPPINGS: dict[str, type] = {}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {}


class TagNodeBase:
    TAGS: ClassVar[tuple[str, ...]] = ()
    DEFAULT_BOOLEAN: ClassVar[bool] = False
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        required: dict[str, Any] = {
            "separator": ("STRING", {"multiline": False, "default": ", "}),
            "preset": (
                ["custom", "all_on", "all_off", "invert"],
                {"default": "custom"},
            ),
        }
        for tag in cls.TAGS:
            required[tag] = ("BOOLEAN", {"default": cls.DEFAULT_BOOLEAN})
        return {
            "required": required,
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(self, separator: str, extra: str = "", **kwargs: Any) -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        preset = str(kwargs.pop("preset", "custom"))
        tags: dict[str, bool] = {k: bool(v) for k, v in kwargs.items()}
        if preset == "all_on":
            parts: list[str] = list(self.TAGS)
        elif preset == "all_off":
            parts = []
        elif preset == "invert":
            parts = [tag for tag in self.TAGS if not tags.get(tag, False)]
        else:
            parts = [tag for tag in self.TAGS if tags.get(tag, False)]
        if extra.strip():
            parts.append(extra.strip())
        prompt = sep.join(parts)
        return {"ui": {"text": (prompt,)}, "result": (prompt,)}
