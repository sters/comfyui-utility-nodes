from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection


class TagsExplode:
    """Splits a bundle into a list of single-tag bundles, one per tag.

    Designed to feed `TagsCombinator` — wire a tag-toggle node (e.g.
    `HairColor` with 4 colors checked) through `TagsExplode` to get 4
    axis values. Each output bundle preserves the original selection's
    category / layer / mutex_within so downstream `TagsMerge` still
    enforces cross-bundle conflict rules per value.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundles",)
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True,)
    FUNCTION: ClassVar[str] = "explode"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {"required": {"bundle": (TAGS_TYPE,)}}

    def explode(self, bundle: tuple[TaggedSelection, ...]) -> tuple[list[tuple[TaggedSelection, ...]]]:
        out: list[tuple[TaggedSelection, ...]] = []
        for sel in bundle:
            if sel.category == "extra":
                continue
            for tag in sel.tags:
                out.append(
                    (
                        TaggedSelection(
                            category=sel.category,
                            layer=sel.layer,
                            tags=(tag,),
                            mutex_within=sel.mutex_within,
                        ),
                    )
                )
        if not out:
            out = [()]
        return (out,)


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsExplode": TagsExplode}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagsExplode": "Explode"}
