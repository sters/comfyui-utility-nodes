from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection


class TagsSelect:
    """Pick one bundle (and its label) out of a `TagsCombinator` list by index.

    The memory-safe counterpart to feeding a `TagsCombinator` list straight
    into the image pipeline. Fanning out all N combinations in a single Run
    materialises N copies of every intermediate tensor (300 decoded images +
    300 detailer outputs + ...), which overflows system RAM at large N.
    Instead, wire `index` to an incrementing `Seed` (or use this node's own
    `control_after_generate` on `index`) and queue the prompt N times: each
    Run resolves to a single combination, so peak memory stays at one image's
    worth, progress is saved incrementally, and a crash mid-sweep is
    resumable.

    `index` wraps modulo the list length, so queuing exactly N runs walks the
    whole sweep once and keeps cycling beyond that.
    """

    INPUT_IS_LIST: ClassVar[bool] = True
    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE, "STRING", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle", "label", "index")
    FUNCTION: ClassVar[str] = "select"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "index": (
                    "INT",
                    {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True},
                ),
            },
            "optional": {
                "bundles": (TAGS_TYPE,),
                "labels": ("STRING", {"forceInput": True}),
            },
        }

    def select(
        self,
        index: list[int],
        bundles: list[tuple[TaggedSelection, ...]] | None = None,
        labels: list[str] | None = None,
    ) -> tuple[tuple[TaggedSelection, ...], str, int]:
        # INPUT_IS_LIST=True makes every input a list, even the scalar widget.
        idx = index[0] if index else 0
        items = [b for b in (bundles or [])]
        if not items:
            return ((), "", 0)
        effective = idx % len(items)
        label_list = labels or []
        label = str(label_list[effective]) if effective < len(label_list) else ""
        return (tuple(items[effective]), label, effective)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsSelect": TagsSelect}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsSelect": "Select"}
