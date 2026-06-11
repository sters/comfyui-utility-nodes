from typing import Any, ClassVar

from ._base import TAG_CATEGORY_REGISTRY, TAGS_TYPE, TaggedSelection

_EXTRA_CATEGORY = "extra"
_NONE = "(none)"


def _all_categories() -> list[str]:
    return sorted({c for c in TAG_CATEGORY_REGISTRY.values() if c})


class TagsDecorate:
    """Prefix tags in a bundle that belong to a chosen category with a
    decoration phrase (built from another bundle).

    Accepts lists on `bundle` and `decoration` and emits the **Cartesian
    product** of (bundle × decoration). Single-value inputs are wrapped
    in a 1-element list by ComfyUI's `INPUT_IS_LIST` semantics, so:

    - 1 bundle × 1 decoration → 1 result
    - 1 bundle × N decorations → N results (broadcast)
    - M bundles × N decorations → M × N results (cross product)

    Chain multiple `TagsDecorate` nodes for multi-axis decoration (e.g.
    apply colors to clothing.bottoms in the first stage, then apply a
    different decoration to clothing.tops in the second — each stage
    multiplies the variant count).
    """

    INPUT_IS_LIST: ClassVar[bool] = True
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("warnings", "bundle")
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True, True)
    FUNCTION: ClassVar[str] = "decorate"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "target_category": ([_NONE, *_all_categories()], {"default": _NONE}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
                "decoration": (TAGS_TYPE,),
            },
        }

    def decorate(
        self,
        target_category: list[str],
        bundle: list[tuple[TaggedSelection, ...]] | None = None,
        decoration: list[tuple[TaggedSelection, ...]] | None = None,
    ) -> tuple[list[str], list[tuple[TaggedSelection, ...]]]:
        target = target_category[0] if target_category else _NONE

        # Normalise empty lists to a single-element "empty" axis so that
        # the cross-product doesn't collapse to zero results when one
        # side is unwired.
        bundles: list[tuple[TaggedSelection, ...]] = list(bundle) if bundle else [()]
        decorations: list[tuple[TaggedSelection, ...]] = list(decoration) if decoration else [()]

        warnings_out: list[str] = []
        bundles_out: list[tuple[TaggedSelection, ...]] = []

        for b in bundles:
            for d in decorations:
                w, ob = self._decorate_one(target, b, d)
                warnings_out.append(w)
                bundles_out.append(ob)

        return (warnings_out, bundles_out)

    @staticmethod
    def _decorate_one(
        target: str,
        bundle: tuple[TaggedSelection, ...],
        decoration: tuple[TaggedSelection, ...],
    ) -> tuple[str, tuple[TaggedSelection, ...]]:
        warnings: list[str] = []

        decoration_words: list[str] = []
        for sel in decoration:
            if sel.category == _EXTRA_CATEGORY:
                continue
            for tag in sel.tags:
                decoration_words.append(tag.replace("_", " "))
        prefix = " ".join(decoration_words).strip()

        if target == _NONE or not target:
            if prefix:
                warnings.append(f"decorate: skipped — no target_category selected (prefix='{prefix}')")
            return TagsDecorate._emit(bundle, warnings)

        if not prefix:
            return TagsDecorate._emit(bundle, warnings)

        matched = 0
        new_bundle: list[TaggedSelection] = []
        for sel in bundle:
            if sel.category == _EXTRA_CATEGORY:
                new_bundle.append(sel)
                continue
            new_tags: list[str] = []
            for tag in sel.tags:
                tag_cat = TAG_CATEGORY_REGISTRY.get(tag, "")
                if tag_cat == target:
                    new_tags.append(f"{prefix} {tag.replace('_', ' ')}")
                    matched += 1
                else:
                    new_tags.append(tag)
            if tuple(new_tags) == sel.tags:
                new_bundle.append(sel)
            else:
                new_bundle.append(
                    TaggedSelection(
                        category=sel.category,
                        layer=sel.layer,
                        tags=tuple(new_tags),
                        mutex_within=sel.mutex_within,
                    )
                )

        if matched == 0:
            warnings.append(f"decorate: no tags in bundle matched category '{target}' (prefix '{prefix}' dropped)")

        return TagsDecorate._emit(tuple(new_bundle), warnings)

    @staticmethod
    def _emit(
        bundle: tuple[TaggedSelection, ...],
        warnings: list[str],
    ) -> tuple[str, tuple[TaggedSelection, ...]]:
        return "\n".join(warnings), bundle


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsDecorate": TagsDecorate}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsDecorate": "Decorate"}
