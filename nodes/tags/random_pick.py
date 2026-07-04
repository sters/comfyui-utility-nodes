from typing import Any, ClassVar

from ._base import RANDOM_SPEC_TYPE, TAGS_TYPE, RandomSpec, TaggedSelection


class TagsRandomPick:
    """Describe a random sample of tags out of a CUUN_TAGS bundle, resolved later.

    Packages `count`, `seed`, and the bundle to sample from into a
    `RandomSpec` — no randomness happens here. Wire the `spec` output into
    one of `TagsMerge`'s `spec_i` inputs; that's the pipeline's terminal
    build step, and it resolves specs alongside the usual conflict
    resolution.

    Resolution flattens every non-`extra` selection's tags into one pool,
    samples `count` of them without replacement using `seed`, and emits the
    chosen tags as a single new `TaggedSelection` at category
    `random_pick`. The original categorisation is lost on purpose —
    the use case is "I want some random subset of these tags in the
    prompt", not "preserve structure".

    If `count >= number of available tags`, every tag is returned (in
    shuffled order). `extra` selections are passed through as-is.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (RANDOM_SPEC_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("spec",)
    FUNCTION: ClassVar[str] = "pick"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "count": ("INT", {"default": 1, "min": 1, "max": 1024}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True}),
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
    ) -> tuple[RandomSpec]:
        return (RandomSpec(kind="tag_pick", seed=seed, pool=tuple(bundle or ()), count=count),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsRandomPick": TagsRandomPick}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsRandomPick": "Random Pick"}
