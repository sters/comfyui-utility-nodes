from itertools import product
from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection


class TagsCombinator:
    """Cartesian product over axes of CUUN_TAGS bundles.

    Each axis input is a list of bundles (typically produced by
    `TagsExplode` for tag-toggle nodes, `TagsCollect` for whole-bundle
    alternatives, or wired directly from a preset for single-bundle
    axes). The node generates every combination and emits each as a
    **concatenated CUUN_TAGS bundle** — it does *not* merge or resolve
    conflicts itself. Wire the `bundle` output into `TagsMerge`
    ("Merge & Validate"); ComfyUI broadcasts that node over the output
    list, so it runs once per combination and produces the per-combo
    prompt / warnings.

    Axis order is the priority order — `TagsMerge`'s MUTEX_GROUPS is
    last-wins, so put base / fixed axes earlier and override axes later
    (a later HairColor red_hair will defeat an earlier preset's
    brown_hair once merged).
    """

    INPUT_IS_LIST: ClassVar[bool] = True
    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE, "STRING", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle", "label", "index")
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True, True, True)
    FUNCTION: ClassVar[str] = "combine"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    _MAX_AXES: ClassVar[int] = 8

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        optional: dict[str, Any] = {}
        for i in range(1, cls._MAX_AXES + 1):
            optional[f"axis_{i}"] = (TAGS_TYPE,)
        return {
            "required": {},
            "optional": optional,
        }

    def combine(
        self,
        **kwargs: Any,
    ) -> tuple[list[tuple[TaggedSelection, ...]], list[str], list[int]]:
        axes: list[list[tuple[TaggedSelection, ...]]] = []
        for i in range(1, self._MAX_AXES + 1):
            v = kwargs.get(f"axis_{i}")
            if not v:
                continue
            # Drop empty bundles (e.g. TagsExplode on a node with no
            # checked tags emits a single empty tuple as a sentinel).
            non_empty = [b for b in v if b]
            if not non_empty:
                continue
            axes.append(non_empty)

        if not axes:
            return ([], [], [])

        bundles: list[tuple[TaggedSelection, ...]] = []
        labels: list[str] = []
        indices: list[int] = []

        for idx, combo in enumerate(product(*axes)):
            # Concatenate the chosen axis bundles in axis order; conflict
            # resolution is deferred to a downstream TagsMerge.
            merged = tuple(sel for bundle in combo for sel in bundle)
            bundles.append(merged)
            labels.append(self._label(combo))
            indices.append(idx)

        return (bundles, labels, indices)

    @staticmethod
    def _label(combo: tuple[tuple[TaggedSelection, ...], ...]) -> str:
        parts: list[str] = []
        for bundle in combo:
            non_extra = [s for s in bundle if s.category != "extra"]
            if not non_extra:
                parts.append("anon")
                continue
            sel = non_extra[0]
            if len(sel.tags) == 1:
                parts.append(sel.tags[0])
            elif "." in sel.category:
                parts.append(sel.category.rsplit(".", 1)[-1])
            else:
                parts.append(sel.tags[0])
        return "__".join(parts)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsCombinator": TagsCombinator}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesTagsCombinator": "Combinator",
}
