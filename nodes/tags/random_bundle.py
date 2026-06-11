import random
from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection

_MAX_INPUTS = 10


class TagsRandomBundle:
    """Pick one whole CUUN_TAGS bundle at random out of several wired alternatives.

    The bundle-level counterpart to `TagsRandomPick`: where `TagsRandomPick`
    flattens one bundle's tags into a pool and samples *tags*, this node treats
    each wired input as one indivisible candidate and returns exactly one of
    them **intact** — categories, layers and `mutex_within` preserved. Use it
    for "pick one of these N alternatives each run": one of several
    `CharacterPreset`s, one of several pre-composed scene/NSFW bundles, etc.

    This is the node to reach for instead of feeding a `TagsCollect` list into
    `TagsRandomPick` — `TagsRandomPick` does not consume a list (ComfyUI would
    broadcast it per element and keep them all). `TagsRandomBundle` takes the
    candidates as discrete inputs and collapses them to one bundle, so no
    `TagsCombinator` / `TagsSelect` is needed for the random-one-per-run case.

    Empty / unwired inputs are ignored. With `seed`'s `control_after_generate`
    set to `randomize`, every run re-rolls a fresh choice.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "pick"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        optional: dict[str, Any] = {}
        for i in range(1, _MAX_INPUTS + 1):
            optional[f"bundle_{i}"] = (TAGS_TYPE,)
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True}),
            },
            "optional": optional,
        }

    def pick(self, seed: int, **kwargs: Any) -> tuple[tuple[TaggedSelection, ...]]:
        candidates: list[tuple[TaggedSelection, ...]] = []
        for i in range(1, _MAX_INPUTS + 1):
            bundle = kwargs.get(f"bundle_{i}")
            if not bundle:
                continue
            candidates.append(tuple(bundle))

        if not candidates:
            return ((),)

        chosen = random.Random(seed).choice(candidates)
        return (chosen,)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsRandomBundle": TagsRandomBundle}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsRandomBundle": "Random Bundle"}
