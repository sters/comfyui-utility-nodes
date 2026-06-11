from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection


class TagsBundleInspector:
    """Pass-through visualizer for a merged CUUN_TAGS bundle.

    Sits between `TagsMerge` and downstream consumers. Renders the
    surviving selections grouped by layer/category, and optionally
    appends the merge `warnings` string so kept and dropped tags are
    visible in one UI box.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE, "STRING")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle", "report")
    FUNCTION: ClassVar[str] = "inspect"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {"bundle": (TAGS_TYPE,)},
            "optional": {"warnings": ("STRING", {"multiline": True, "default": "", "forceInput": True})},
        }

    def inspect(
        self, bundle: tuple[TaggedSelection, ...], warnings: str = ""
    ) -> tuple[tuple[TaggedSelection, ...], str]:
        report = _format_report(bundle, warnings)
        return (tuple(bundle), report)


def _format_report(bundle: tuple[TaggedSelection, ...], warnings: str) -> str:
    lines: list[str] = []
    if not bundle:
        lines.append("(empty bundle)")
    else:
        # Group selections by layer in first-seen order, preserving the
        # selection order within each layer so the report mirrors the
        # flatten order TagsMerge would produce.
        by_layer: dict[str, list[TaggedSelection]] = {}
        for sel in bundle:
            by_layer.setdefault(sel.layer or "(no layer)", []).append(sel)

        cat_width = max((len(sel.category or "") for sel in bundle), default=0)
        for layer, sels in by_layer.items():
            lines.append(f"[{layer}]")
            for sel in sels:
                cat = (sel.category or "").ljust(cat_width)
                lines.append(f"  {cat} : {', '.join(sel.tags)}")

    warnings_stripped = warnings.strip()
    if warnings_stripped:
        lines.append("")
        lines.append("--- dropped ---")
        lines.append(warnings_stripped)
    return "\n".join(lines)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsBundleInspector": TagsBundleInspector}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsBundleInspector": "Bundle Inspector"}
