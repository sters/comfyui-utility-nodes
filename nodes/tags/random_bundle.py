from typing import Any, ClassVar

from ._base import RANDOM_SPEC_TYPE, TAGS_TYPE, RandomSpec, TaggedSelection

_MAX_INPUTS = 10


class TagsRandomBundle:
    """Describe a choice of one whole CUUN_TAGS bundle out of several alternatives, resolved later.

    The bundle-level counterpart to `TagsRandomPick`: where `TagsRandomPick`
    flattens one bundle's tags into a pool and samples *tags*, this node
    treats each wired input as one indivisible candidate. No randomness
    happens here — it packages the candidates and `seed` into a
    `RandomSpec`. Wire the `spec` output into one of `TagsMerge`'s `spec_i`
    inputs; that's the pipeline's terminal build step, and it resolves the
    choice to exactly one of the wired bundles **intact** — categories,
    layers and `mutex_within` preserved. Use it for "pick one of these N
    alternatives each run": one of several `CharacterPreset`s, one of
    several pre-composed scene/NSFW bundles, etc.

    This is the node to reach for instead of feeding a `TagsCollect` list into
    `TagsRandomPick` — `TagsRandomPick` does not consume a list (ComfyUI would
    broadcast it per element and keep them all). `TagsRandomBundle` takes the
    candidates as discrete inputs and collapses them to one bundle, so no
    `TagsCombinator` / `TagsSelect` is needed for the random-one-per-run case.

    Empty / unwired inputs are ignored. With `seed`'s `control_after_generate`
    set to `randomize`, every run re-rolls a fresh choice.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (RANDOM_SPEC_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("spec",)
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

    def pick(self, seed: int, **kwargs: Any) -> tuple[RandomSpec]:
        candidates: list[tuple[TaggedSelection, ...]] = []
        for i in range(1, _MAX_INPUTS + 1):
            bundle = kwargs.get(f"bundle_{i}")
            if not bundle:
                continue
            candidates.append(tuple(bundle))

        return (RandomSpec(kind="bundle_choice", seed=seed, bundles=tuple(candidates)),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsRandomBundle": TagsRandomBundle}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsRandomBundle": "Random Bundle"}
