import random
from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection


class TagsShuffle:
    """Reorder tags inside each `TaggedSelection` of a CUUN_TAGS bundle.

    Selection structure (category / layer / mutex_within) is preserved —
    only the per-selection `tags` tuple is shuffled. Use this when you
    want to randomise the **textual order** of tags in the final prompt
    without breaking the merge-pipeline contract (categories still
    matter for `TagsMerge` mutex / `TagsDecorate` lookup).

    `extra` selections are passed through untouched (they're free-form
    text, not orderable tag lists).
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "shuffle"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
            },
        }

    def shuffle(
        self,
        seed: int,
        bundle: tuple[TaggedSelection, ...] = (),
    ) -> tuple[tuple[TaggedSelection, ...]]:
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

        return (tuple(out),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsShuffle": TagsShuffle}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagsShuffle": "Shuffle"}
