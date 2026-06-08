from itertools import product
from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection
from .merge import TagsMerge


class TagsCombinator:
    """Cartesian product over axes of CUUN_TAGS bundles.

    Each axis input is a list of bundles (typically produced by
    `TagsExplode` for tag-toggle nodes, or wired directly from a
    preset for single-bundle axes). The node generates every
    combination, runs each through `TagsMerge` for conflict
    resolution, and outputs STRING lists that downstream
    `CLIPTextEncode` / `KSampler` / `SaveImage` iterate over.

    Axis order is the priority order — MUTEX_GROUPS is last-wins,
    so put base / fixed axes earlier and override axes later (a
    later HairColor red_hair will defeat an earlier preset's
    brown_hair).
    """

    INPUT_IS_LIST: ClassVar[bool] = True
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "STRING", "INT", "STRING")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "label", "index", "warnings")
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True, True, True, True)
    FUNCTION: ClassVar[str] = "combine"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    _MAX_AXES: ClassVar[int] = 8

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        optional: dict[str, Any] = {}
        for i in range(1, cls._MAX_AXES + 1):
            optional[f"axis_{i}"] = (TAGS_TYPE,)
        return {
            "required": {
                "separator": ("STRING", {"multiline": False, "default": ", "}),
            },
            "optional": optional,
        }

    def combine(
        self,
        separator: list[str],
        **kwargs: Any,
    ) -> tuple[list[str], list[str], list[int], list[str]]:
        sep_raw = separator[0] if separator else ", "
        sep = sep_raw.encode("utf-8").decode("unicode_escape") if sep_raw else ", "

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
            return ([], [], [], [])

        prompts: list[str] = []
        labels: list[str] = []
        indices: list[int] = []
        warnings_list: list[str] = []

        merger = TagsMerge()
        for idx, combo in enumerate(product(*axes)):
            merge_kwargs: dict[str, Any] = {f"bundle_{i + 1}": bundle for i, bundle in enumerate(combo)}
            result = merger.merge(sep, **merge_kwargs)
            prompt, warnings, _ = result["result"]
            prompts.append(str(prompt))
            labels.append(self._label(combo))
            indices.append(idx)
            warnings_list.append(str(warnings))

        return (prompts, labels, indices, warnings_list)

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


NODE_CLASS_MAPPINGS: dict[str, type] = {"TagsCombinator": TagsCombinator}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "TagsCombinator": "Combinator",
}
