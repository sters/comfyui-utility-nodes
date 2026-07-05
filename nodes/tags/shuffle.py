import random
from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, TaggedSelection, require_fixed


class TagsShuffle:
    """Reorder tags inside each `TaggedSelection` of a CUUN_TAGS bundle.

    Selection structure (category / layer / mutex_within) is preserved —
    only the per-selection `tags` tuple is shuffled. Use this when you
    want to randomise the **textual order** of tags in the final prompt
    without breaking the merge-pipeline contract (categories still
    matter for `TagsBuild` mutex / `TagsDecorate` lookup).

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
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
            },
        }

    def shuffle(
        self,
        seed: int,
        bundle: Spec | None = None,
    ) -> tuple[Spec]:
        rng = random.Random(seed)
        pool = require_fixed(bundle, "TagsShuffle") if bundle is not None else ()

        out: list[TaggedSelection] = []
        for sel in pool:
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

        return (Spec(kind="fixed", pool=tuple(out)),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsShuffle": TagsShuffle}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsShuffle": "Shuffle"}
