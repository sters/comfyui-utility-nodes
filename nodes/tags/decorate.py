from typing import Any, ClassVar

from ._base import TAG_CATEGORY_REGISTRY, TAGS_TYPE, TaggedSelection

_EXTRA_CATEGORY = "extra"
_NONE = "(none)"


def _all_categories() -> list[str]:
    return sorted({c for c in TAG_CATEGORY_REGISTRY.values() if c})


class TagDecorate:
    """Prefix tags in a bundle that belong to a chosen category with a
    decoration phrase (built from another bundle).

    Wire one tag-toggle node (e.g. `ColorPalette` + `ClothingPattern`
    merged) into `decoration`, pick the `target_category` you want to
    decorate (e.g. `clothing.bottoms`), and every tag in the main
    `bundle` whose original category matches the target is rewritten
    from `pleated_skirt` to `red green plaid pleated_skirt`. Chain
    multiple `TagDecorate` nodes for multiple decoration rules.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "warnings", "bundle")
    FUNCTION: ClassVar[str] = "decorate"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "separator": ("STRING", {"multiline": False, "default": ", "}),
                "target_category": ([_NONE, *_all_categories()], {"default": _NONE}),
            },
            "optional": {
                "bundle": (TAGS_TYPE,),
                "decoration": (TAGS_TYPE,),
            },
        }

    def decorate(
        self,
        separator: str,
        target_category: str,
        bundle: tuple[TaggedSelection, ...] = (),
        decoration: tuple[TaggedSelection, ...] = (),
    ) -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        warnings: list[str] = []

        decoration_words: list[str] = []
        for sel in decoration or ():
            if sel.category == _EXTRA_CATEGORY:
                continue
            for tag in sel.tags:
                decoration_words.append(tag.replace("_", " "))
        prefix = " ".join(decoration_words).strip()

        bundle = tuple(bundle or ())

        if target_category == _NONE or not target_category:
            if prefix:
                warnings.append(f"decorate: skipped — no target_category selected (prefix='{prefix}')")
            return self._emit(sep, bundle, warnings)

        if not prefix:
            return self._emit(sep, bundle, warnings)

        matched = 0
        new_bundle: list[TaggedSelection] = []
        for sel in bundle:
            if sel.category == _EXTRA_CATEGORY:
                new_bundle.append(sel)
                continue
            new_tags: list[str] = []
            for tag in sel.tags:
                tag_cat = TAG_CATEGORY_REGISTRY.get(tag, "")
                if tag_cat == target_category:
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
            warnings.append(
                f"decorate: no tags in bundle matched category '{target_category}' (prefix '{prefix}' dropped)"
            )

        return self._emit(sep, tuple(new_bundle), warnings)

    @staticmethod
    def _emit(
        sep: str,
        bundle: tuple[TaggedSelection, ...],
        warnings: list[str],
    ) -> dict[str, Any]:
        parts: list[str] = []
        for sel in bundle:
            parts.extend(sel.tags)
        prompt = sep.join(parts)
        warnings_str = "\n".join(warnings)
        return {
            "ui": {"text": (prompt,)},
            "result": (prompt, warnings_str, bundle),
        }


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagDecorate": TagDecorate}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagDecorate": "Tags: Decorate"}
