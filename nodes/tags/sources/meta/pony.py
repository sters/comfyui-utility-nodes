from typing import Any, ClassVar

from ..._base import TAGS_TYPE, TaggedSelection

_SCORE_TAGS = ("score_9", "score_8_up", "score_7_up", "score_6_up", "score_5_up", "score_4_up")
_RATING_TAGS = ("rating_safe", "rating_questionable", "rating_explicit")
_SOURCE_TAGS = ("source_pony", "source_furry", "source_cartoon", "source_anime")


class MetaPony:
    """Pony-Diffusion quality / rating / source tags as a CUUN_TAGS bundle.

    A meta / template node (not a character or scene preset): the Pony
    Diffusion model needs its own score / rating / source prefix on
    every prompt the same way `MetaQuality` adds generic quality
    descriptors. Wire its `bundle` output through `TagsMerge` together
    with the rest of the pipeline.

    Rating/source tags aren't in the tag-category registry, so
    `TagsDecorate` won't latch onto them.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster/Meta"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        required: dict[str, Any] = {}
        # All toggles default off (like MetaQuality): the user opts into the
        # score / rating / source tags they want per workflow rather than
        # getting the full score_9..score_4_up stack baked into every prompt.
        for tag in _SCORE_TAGS:
            required[tag] = ("BOOLEAN", {"default": False})
        for tag in _RATING_TAGS:
            required[tag] = ("BOOLEAN", {"default": False})
        for tag in _SOURCE_TAGS:
            required[tag] = ("BOOLEAN", {"default": False})
        return {
            "required": required,
            "optional": {
                "extra": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    def build(
        self,
        extra: str = "",
        **toggles: bool,
    ) -> dict[str, Any]:
        ordered = (*_SCORE_TAGS, *_RATING_TAGS, *_SOURCE_TAGS)
        tags: list[str] = [tag for tag in ordered if toggles.get(tag, False)]

        bundle: list[TaggedSelection] = []
        if tags:
            bundle.append(
                TaggedSelection(
                    category="meta.pony",
                    layer="meta",
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

        preview = ", ".join(parts)
        return {"ui": {"text": (preview,)}, "result": (tuple(bundle),)}


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "MetaPony": MetaPony,
}

NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "MetaPony": "Pony",
}
