import random
from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection


class TagsShuffle:
    """Reorder tags inside each `TaggedSelection` of a CUUN_TAGS bundle.

    Selection structure (category / layer / mutex_within) is preserved —
    only the per-selection `tags` tuple is shuffled. Use this when you
    want to randomise the **textual order** of tags in the final prompt
    without breaking the merge-pipeline contract (categories still
    matter for `TagsMerge` mutex / `TagDecorate` lookup).

    `extra` selections are passed through untouched (they're free-form
    text, not orderable tag lists).
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "shuffle"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "separator": ("STRING", {"multiline": False, "default": ", "}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
            },
        }

    def shuffle(
        self,
        separator: str,
        seed: int,
        bundle: tuple[TaggedSelection, ...] = (),
    ) -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        rng = random.Random(seed)

        out: list[TaggedSelection] = []
        for sel in bundle or ():
            if sel.category == "extra" or len(sel.tags) < 2:
                out.append(sel)
                continue
            tags = list(sel.tags)
            rng.shuffle(tags)
            out.append(
                TaggedSelection(
                    category=sel.category,
                    layer=sel.layer,
                    tags=tuple(tags),
                    mutex_within=sel.mutex_within,
                )
            )

        parts: list[str] = []
        for sel in out:
            parts.extend(sel.tags)
        preview = sep.join(parts)
        return {"ui": {"text": (preview,)}, "result": (tuple(out),)}


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsShuffle": TagsShuffle}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagsShuffle": "Shuffle"}
