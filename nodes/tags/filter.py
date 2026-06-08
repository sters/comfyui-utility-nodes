from typing import Any, ClassVar

from ._base import TAG_CATEGORY_REGISTRY, TAGS_TYPE, TaggedSelection

_EXTRA_CATEGORY = "extra"
_NONE = "(none)"


def _all_categories() -> list[str]:
    return sorted({c for c in TAG_CATEGORY_REGISTRY.values() if c})


class TagsFilter:
    """Drop every tag whose registered category matches `target_category`.

    Per-tag lookup against `TAG_CATEGORY_REGISTRY` (the same registry
    `TagsDecorate` uses), not against the selection's own `category` field.
    That way a preset like `CharacterPreset(serafuku_schoolgirl)` — which
    packs all its tags into one selection with category `preset.X` — can
    still have `thighhighs` removed by targeting `clothing.legwear`.

    Tags in the `extra` selection always pass through. A selection that
    loses every tag is dropped entirely. Chain multiple `TagsFilter`
    nodes to drop more than one category.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE,)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle",)
    FUNCTION: ClassVar[str] = "filter"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "target_category": ([_NONE, *_all_categories()], {"default": _NONE}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
            },
        }

    def filter(
        self,
        target_category: str,
        bundle: tuple[TaggedSelection, ...] | None = None,
    ) -> tuple[tuple[TaggedSelection, ...]]:
        src = bundle or ()
        target = target_category if target_category and target_category != _NONE else ""

        out: list[TaggedSelection] = []
        for sel in src:
            if sel.category == _EXTRA_CATEGORY or not target:
                out.append(sel)
                continue
            kept = tuple(t for t in sel.tags if TAG_CATEGORY_REGISTRY.get(t, "") != target)
            if not kept:
                continue
            if kept == sel.tags:
                out.append(sel)
            else:
                out.append(
                    TaggedSelection(
                        category=sel.category,
                        layer=sel.layer,
                        tags=kept,
                        mutex_within=sel.mutex_within,
                    )
                )

        return (tuple(out),)


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsFilter": TagsFilter}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagsFilter": "Filter"}
