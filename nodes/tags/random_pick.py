import random
from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection


class TagsRandomPick:
    """Pick N random tags out of a CUUN_TAGS bundle.

    Flattens every non-`extra` selection's tags into one pool, samples
    `count` of them without replacement using `seed`, and emits the
    chosen tags as a single new `TaggedSelection` at category
    `random_pick`. The original categorisation is lost on purpose —
    the use case is "I want some random subset of these tags in the
    prompt", not "preserve structure".

    If `count >= number of available tags`, every tag is returned (in
    shuffled order). `extra` selections are passed through as-is.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "pick"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "count": ("INT", {"default": 1, "min": 1, "max": 1024}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
            },
        }

    def pick(
        self,
        count: int,
        seed: int,
        bundle: tuple[TaggedSelection, ...] = (),
    ) -> dict[str, Any]:
        rng = random.Random(seed)

        pool: list[str] = []
        extras: list[TaggedSelection] = []
        for sel in bundle or ():
            if sel.category == "extra":
                extras.append(sel)
            else:
                pool.extend(sel.tags)

        n = min(count, len(pool))
        picked = rng.sample(pool, n) if n else []

        out: list[TaggedSelection] = []
        if picked:
            out.append(
                TaggedSelection(
                    category="random_pick",
                    layer="random",
                    tags=tuple(picked),
                    mutex_within=False,
                )
            )
        out.extend(extras)

        parts: list[str] = []
        for sel in out:
            parts.extend(sel.tags)
        preview = ", ".join(parts)
        return {"ui": {"text": (preview,)}, "result": (tuple(out),)}


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsRandomPick": TagsRandomPick}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagsRandomPick": "Random Pick"}
