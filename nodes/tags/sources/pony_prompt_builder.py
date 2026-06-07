from typing import Any, ClassVar

from .._base import TAGS_TYPE, TaggedSelection

_SCORE_TAGS = ("score_9", "score_8_up", "score_7_up", "score_6_up", "score_5_up", "score_4_up")
_RATINGS = ("none", "safe", "questionable", "explicit")
_SOURCES = ("none", "pony", "furry", "cartoon", "anime")


class PonyPromptBuilder:
    """Pony-Diffusion quality / rating / source tags as a CUUN_TAGS bundle.

    Emits a single `TaggedSelection` with category `preset.pony` so that
    it composes naturally with `TagsMerge` and the rest of the bundle
    pipeline — wire its `bundle` output alongside `CharacterPreset`,
    `MetaQuality`, etc. into a `TagsMerge` and let conflict rules
    resolve as usual.

    `rating_*` and `source_*` are synthetic tags built from the COMBO
    selections (`rating="safe"` → `rating_safe`); they aren't in the
    tag-category registry, so `TagDecorate` won't latch onto them.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "bundle")
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

        tags: list[str] = [tag for tag in _SCORE_TAGS if scores.get(tag, False)]
        if rating != "none":
            tags.append(f"rating_{rating}")
        if source != "none":
            tags.append(f"source_{source}")

        bundle: list[TaggedSelection] = []
        if tags:
            bundle.append(
                TaggedSelection(
                    category="preset.pony",
                    layer="preset",
                    tags=tuple(tags),
                    mutex_within=False,
                )
            )

        parts: list[str] = list(tags)
        extra_stripped = extra.strip()
        if extra_stripped:
            parts.append(extra_stripped)
            bundle.append(
                TaggedSelection(
                    category="extra",
                    layer="extra",
                    tags=(extra_stripped,),
                    mutex_within=False,
                )
            )

        prompt = sep.join(parts)
        return {"ui": {"text": (prompt,)}, "result": (prompt, tuple(bundle))}


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "PonyPromptBuilder": PonyPromptBuilder,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "PonyPromptBuilder": "Pony Prompt Builder",
}
