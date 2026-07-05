from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, TaggedSelection, require_fixed

_MAX_INPUTS = 10


class TagsConcat:
    """Concatenate several whole resolved bundles into one bundle, verbatim.

    No mutex/conflict resolution happens here — every selection from every
    wired input is kept exactly as-is, just appended in input order into a
    single `kind="fixed"` bundle. This is the node for combining two or more
    tag-toggle nodes' outputs into one pool *before* something that only
    accepts a single bundle — most commonly `TagsRandomPick`, when you want
    to sample from the union of several nodes' tags (e.g. "pick 1 out of
    everything checked on `SceneIndoor` and `SceneOutdoor` combined") without
    prematurely dropping candidates via `TagsBuild`'s conflict rules, which
    would run before the pick even happens.

    `TagsBuild` can technically do this concatenation too (feed its `bundle`
    output onward instead of `prompt`), but it always applies MUTEX_GROUPS /
    TAG_CONFLICTS first — fine when you actually want the final, validated
    result, wrong when you want the raw combined candidate pool for
    something else to pick from later. Use `TagsConcat` for the latter.

    Every wired input must already be resolved (`kind="fixed"`) — an
    unresolved `TagsRandomPick`/`TagsRandomBundle` output belongs on a
    `TagsCombinator`/`TagsBuildFromRules` `axis_i` directly, not here.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "concat"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        optional: dict[str, Any] = {}
        for i in range(1, _MAX_INPUTS + 1):
            optional[f"bundle_{i}"] = (TAGS_TYPE,)
        return {"required": {}, "optional": optional}

    def concat(self, **kwargs: Any) -> tuple[Spec]:
        out: list[TaggedSelection] = []
        for i in range(1, _MAX_INPUTS + 1):
            bundle = kwargs.get(f"bundle_{i}")
            if bundle is None:
                continue
            out.extend(require_fixed(bundle, "TagsConcat"))
        return (Spec(kind="fixed", pool=tuple(out)),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsConcat": TagsConcat}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsConcat": "Concat"}
