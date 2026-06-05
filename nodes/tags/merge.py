from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from nodes.tags._base import TAGS_TYPE, TaggedSelection
    from nodes.tags._conflicts import TAG_OVERRIDES, category_matches
else:
    from _cuun_tag_node_base import TAGS_TYPE, TaggedSelection
    from _cuun_tags_conflicts import TAG_OVERRIDES, category_matches


_MAX_INPUTS = 10


class TagsMerge:
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "warnings", "bundle")
    FUNCTION: ClassVar[str] = "merge"
    CATEGORY: ClassVar[str] = "utility/text"
    OUTPUT_NODE: ClassVar[bool] = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        optional: dict[str, Any] = {
            "extra": ("STRING", {"multiline": True, "default": ""}),
        }
        for i in range(1, _MAX_INPUTS + 1):
            optional[f"bundle_{i}"] = (TAGS_TYPE,)
        return {
            "required": {
                "separator": ("STRING", {"multiline": False, "default": ", "}),
            },
            "optional": optional,
        }

    def merge(self, separator: str, extra: str = "", **kwargs: Any) -> dict[str, Any]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        warnings: list[str] = []

        # 1. Collect all selections in input order.
        selections: list[TaggedSelection] = []
        for i in range(1, _MAX_INPUTS + 1):
            bundle = kwargs.get(f"bundle_{i}")
            if not bundle:
                continue
            selections.extend(bundle)

        # 2. Apply mutex_within: per category, keep only the first selection
        #    that has mutex_within=True (warn if multiple).
        seen_mutex: dict[str, TaggedSelection] = {}
        post_mutex: list[TaggedSelection] = []
        for sel in selections:
            if sel.mutex_within and sel.category:
                if sel.category in seen_mutex:
                    warnings.append(f"mutex: dropped extra '{sel.category}' selection ({', '.join(sel.tags)})")
                    continue
                # Also if multiple tags within one selection that's mutex,
                # keep only the first.
                if len(sel.tags) > 1:
                    warnings.append(
                        f"mutex: '{sel.category}' had {len(sel.tags)} tags; "
                        f"kept '{sel.tags[0]}', dropped {list(sel.tags[1:])}"
                    )
                    sel = TaggedSelection(
                        category=sel.category,
                        layer=sel.layer,
                        tags=(sel.tags[0],),
                        mutex_within=True,
                    )
                seen_mutex[sel.category] = sel
            post_mutex.append(sel)

        # 3. Apply cross-layer overrides: if any tag in TAG_OVERRIDES is
        #    present, drop selections whose category matches an override prefix.
        all_tags = {t for sel in post_mutex for t in sel.tags}
        drop_prefixes: set[str] = set()
        for tag in all_tags:
            if tag in TAG_OVERRIDES:
                drop_prefixes.update(TAG_OVERRIDES[tag])

        final: list[TaggedSelection] = []
        for sel in post_mutex:
            if sel.category and any(category_matches(sel.category, frozenset({p})) for p in drop_prefixes):
                warnings.append(f"override: dropped '{sel.category}' ({', '.join(sel.tags)})")
                continue
            final.append(sel)

        # 4. Flatten into prompt.
        parts: list[str] = []
        for sel in final:
            parts.extend(sel.tags)
        extra_stripped = extra.strip()
        if extra_stripped:
            parts.append(extra_stripped)
        prompt = sep.join(parts)
        warnings_str = "\n".join(warnings)
        return {
            "ui": {"text": (prompt,)},
            "result": (prompt, warnings_str, tuple(final)),
        }


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsMerge": TagsMerge}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"TagsMerge": "Tags: Merge & Validate"}
