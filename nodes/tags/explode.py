from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, TaggedSelection, require_fixed


class TagsExplode:
    """Splits a resolved bundle into a list of single-tag Specs, one per tag.

    Designed to feed `TagsCombinator` — wire a tag-toggle node (e.g.
    `HairColor` with 4 colors checked) through `TagsExplode` to get 4
    axis values. Each output Spec preserves the original selection's
    category / layer / mutex_within so downstream `TagsBuild` still
    enforces cross-bundle conflict rules per value.

    The input must already be resolved (`kind="fixed"`) — you can't explode
    an unresolved `TagsRandomPick`/`TagsRandomBundle` spec; wire that
    straight into a `TagsCombinator`/`TagsBuildFromRules` `axis_i` instead.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundles",)
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True,)
    FUNCTION: ClassVar[str] = "explode"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {"required": {"bundle": (TAGS_TYPE,)}}

    def explode(self, bundle: Spec) -> tuple[list[Spec]]:
        pool = require_fixed(bundle, "TagsExplode")
        out: list[Spec] = []
        for sel in pool:
            if sel.category == "extra":
                continue
            for tag in sel.tags:
                out.append(
                    Spec(
                        kind="fixed",
                        pool=(
                            TaggedSelection(
                                category=sel.category,
                                layer=sel.layer,
                                tags=(tag,),
                                mutex_within=sel.mutex_within,
                            ),
                        ),
                    )
                )
        if not out:
            out = [Spec(kind="fixed", pool=())]
        return (out,)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsExplode": TagsExplode}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsExplode": "Explode"}
