from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec

_MAX_INPUTS = 10


class TagsConcat:
    """Concatenate several bundles into one bundle, verbatim.

    No mutex/conflict resolution happens here — every selection from every
    wired input is kept exactly as-is, in input order. This is the node for
    combining two or more tag sources into one pool *before* something that
    only accepts a single bundle — either `TagsBuild` (merge several
    tag-toggle nodes/presets into its one `bundle` input) or `TagsRandomPick`,
    when you want to sample from the union of several nodes' tags (e.g.
    "pick 1 out of everything checked on `SceneIndoor` and `SceneOutdoor`
    combined") without prematurely dropping candidates via `TagsBuild`'s
    conflict rules, which would run before the pick even happens.

    If every wired input is already resolved (`kind="fixed"`), the result is
    also `kind="fixed"` — a single flat pool. If any wired input is still
    unresolved (a `TagsRandomPick`/`TagsRandomBundle` output, or another
    unresolved combo), the result is a `kind="composite"` Spec carrying every
    input through untouched, in order; resolving it later (typically via
    `TagsBuild`) resolves each child independently and flattens them
    together — so a still-random source can ride alongside already-fixed
    ones into a single `TagsBuild` input without a full `TagsCombinator`.

    `TagsBuild` can technically do this concatenation too (feed its `bundle`
    output onward instead of `prompt`), but it always applies MUTEX_GROUPS /
    TAG_CONFLICTS first — fine when you actually want the final, validated
    result, wrong when you want the raw combined candidate pool for
    `TagsRandomPick` to pick from later. Use `TagsConcat` for that case.
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
        specs: list[Spec] = []
        for i in range(1, _MAX_INPUTS + 1):
            bundle = kwargs.get(f"bundle_{i}")
            if bundle is None:
                continue
            specs.append(bundle)

        if all(spec.kind == "fixed" for spec in specs):
            pool = tuple(sel for spec in specs for sel in spec.pool)
            return (Spec(kind="fixed", pool=pool),)

        return (Spec(kind="composite", children=tuple(specs)),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsConcat": TagsConcat}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsConcat": "Concat"}
