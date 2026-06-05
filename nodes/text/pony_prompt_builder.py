from typing import Any, ClassVar

_SCORE_TAGS = ("score_9", "score_8_up", "score_7_up", "score_6_up", "score_5_up", "score_4_up")
_RATINGS = ("none", "safe", "questionable", "explicit")
_SOURCES = ("none", "pony", "furry", "cartoon", "anime")


class PonyPromptBuilder:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        required: dict[str, Any] = {
            "separator": ("STRING", {"multiline": False, "default": ", "}),
        }
        for tag in _SCORE_TAGS:
            required[tag] = ("BOOLEAN", {"default": True})
        required["rating"] = (list(_RATINGS), {"default": "none"})
        required["source"] = (list(_SOURCES), {"default": "none"})
        return {
            "required": required,
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(
        self,
        separator: str,
        rating: str,
        source: str,
        extra: str = "",
        **scores: bool,
    ) -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "

        parts: list[str] = [tag for tag in _SCORE_TAGS if scores.get(tag, False)]
        if rating != "none":
            parts.append(f"rating_{rating}")
        if source != "none":
            parts.append(f"source_{source}")
        if extra.strip():
            parts.append(extra.strip())

        prompt = sep.join(parts)
        return {"ui": {"text": (prompt,)}, "result": (prompt,)}


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "PonyPromptBuilder": PonyPromptBuilder,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "PonyPromptBuilder": "Pony Prompt Builder",
}
