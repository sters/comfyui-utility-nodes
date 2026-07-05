from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, require_fixed


class TagsRandomPick:
    """Describe a random sample of tags out of a resolved bundle, resolved later.

    Packages `count` and the bundle to sample from into an unresolved
    bundle — no randomness happens here, and no seed lives on this node
    either. Wire the `bundle` output into one of `TagsMerge`'s `bundle_i`
    inputs (or a `TagsCombinator`/`TagsBuildFromRules` `axis_i`, where it
    becomes a deferred axis); that's where it gets resolved, alongside the
    usual conflict resolution, using whichever seed the actual build step
    owns.

    Resolution flattens every non-`extra` selection's tags into one pool,
    samples `count` of them without replacement, and emits the chosen tags
    as a single new `TaggedSelection` at category `random_pick`. The
    original categorisation is lost on purpose — the use case is "I want
    some random subset of these tags in the prompt", not "preserve
    structure".

    If `count >= number of available tags`, every tag is returned (in
    shuffled order). `extra` selections are passed through as-is.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "pick"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "count": ("INT", {"default": 1, "min": 1, "max": 1024}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
            },
        }

    def pick(
        self,
        count: int,
        bundle: Spec | None = None,
    ) -> tuple[Spec]:
        pool = require_fixed(bundle, "TagsRandomPick") if bundle is not None else ()
        return (Spec(kind="tag_pick", pool=pool, count=count),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsRandomPick": TagsRandomPick}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsRandomPick": "Random Pick"}
