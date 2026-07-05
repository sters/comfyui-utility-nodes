from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, require_fixed

_MAX_INPUTS = 10


class TagsCollect:
    """Gather several whole resolved bundles into one list of Specs (a Combinator axis).

    Each wired bundle becomes one element of the output list, kept intact —
    no merging, no per-tag explosion. Feed the result into a `TagsCombinator`
    axis to vary over whole bundles: e.g. several `CharacterPreset`s as
    alternative characters, producing one combination per character rather
    than a cartesian blow-up of their individual tags.

    This is the multi-bundle counterpart to `TagsExplode` (which splits a
    single bundle into per-tag axis values). The route that *doesn't* work —
    `TagsBuild` then `TagsExplode` — flattens the characters together and then
    re-splits per tag; `TagsCollect` is the node that preserves each bundle as
    one discrete axis value.

    Every wired input must already be resolved (`kind="fixed"`) — an
    unresolved `TagsRandomPick`/`TagsRandomBundle` spec belongs on a
    `TagsCombinator`/`TagsBuildFromRules` `axis_i` directly, not here.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundles",)
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True,)
    FUNCTION: ClassVar[str] = "collect"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        optional: dict[str, Any] = {}
        for i in range(1, _MAX_INPUTS + 1):
            optional[f"bundle_{i}"] = (TAGS_TYPE,)
        return {"required": {}, "optional": optional}

    def collect(self, **kwargs: Any) -> tuple[list[Spec]]:
        out: list[Spec] = []
        for i in range(1, _MAX_INPUTS + 1):
            bundle = kwargs.get(f"bundle_{i}")
            if bundle is None:
                continue
            pool = require_fixed(bundle, "TagsCollect")
            if not pool:
                continue
            out.append(Spec(kind="fixed", pool=pool))
        return (out,)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsCollect": TagsCollect}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsCollect": "Collect"}
