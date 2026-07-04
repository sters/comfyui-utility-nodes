"""Serialize/expand combinator axes as portable JSON "rules" (issue #27).

Wiring a heavy TagMaster graph (many toggle nodes + presets) just to re-run
the same combinatorial expansion every time is expensive to manage. These two
nodes split that in half:

- ``TagsRulesToJson`` takes the same `axis_i` (`CUUN_TAGS` list) inputs as
  `TagsCombinator` and serializes the *candidates* (not the expansion) to a
  single JSON STRING — run once, inspect/save it with `PreviewAny`, and the
  source graph is no longer needed.
- ``TagsBuildFromRules`` takes that JSON STRING back and performs the exact
  same cartesian-product expansion `TagsCombinator` does, without needing any
  of the original toggle/preset nodes wired up.
"""

from typing import Any, ClassVar

from ._base import TAGS_TYPE, TaggedSelection
from .combinator import Axis, collect_axes, expand_axes

_MAX_AXES = 8


def _selection_to_dict(sel: TaggedSelection) -> dict[str, Any]:
    return {"category": sel.category, "layer": sel.layer, "tags": list(sel.tags), "mutex_within": sel.mutex_within}


def _selection_from_dict(d: dict[str, Any]) -> TaggedSelection:
    return TaggedSelection(
        category=d["category"], layer=d["layer"], tags=tuple(d["tags"]), mutex_within=d["mutex_within"]
    )


def axes_to_rules(axes: list[Axis]) -> str:
    """Serialize a list of combinator axes (each a list of bundles) to JSON."""
    import json

    return json.dumps([[[_selection_to_dict(sel) for sel in bundle] for bundle in axis] for axis in axes])


def rules_to_axes(rules: str) -> list[Axis]:
    """Inverse of :func:`axes_to_rules`. Malformed/empty input yields no axes."""
    import json

    try:
        data = json.loads(rules) if rules else []
    except ValueError:
        data = []
    return [[tuple(_selection_from_dict(sel) for sel in bundle) for bundle in axis] for axis in data]


class TagsRulesToJson:
    """Serialize combinator axes (candidates, not the expansion) to a JSON STRING.

    Takes the same wiring as `TagsCombinator` — up to 8 `axis_i` inputs, each a
    list of `CUUN_TAGS` bundles (from `TagsExplode`/`TagsCollect`/a preset) —
    and dumps them verbatim as JSON. Preview or save the result once; feed it
    into `TagsBuildFromRules` later to regenerate every combination without
    the source graph.
    """

    INPUT_IS_LIST: ClassVar[bool] = True
    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING",)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("rules",)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        optional: dict[str, Any] = {}
        for i in range(1, _MAX_AXES + 1):
            optional[f"axis_{i}"] = (TAGS_TYPE,)
        return {"required": {}, "optional": optional}

    def build(self, **kwargs: Any) -> tuple[str]:
        return (axes_to_rules(collect_axes(kwargs, _MAX_AXES)),)


class TagsBuildFromRules:
    """Expand a JSON `rules` STRING (from `TagsRulesToJson`) into combination bundles.

    Performs the identical cartesian-product expansion `TagsCombinator` does,
    sourcing candidates from the JSON instead of live upstream nodes — wire
    the `bundle` output into `TagsMerge` exactly like `TagsCombinator`'s.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE, "STRING", "INT")
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle", "label", "index")
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True, True, True)
    FUNCTION: ClassVar[str] = "build"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "rules": (
                    "STRING",
                    {"multiline": True, "default": "[]", "tooltip": "JSON produced by Rules to JSON."},
                ),
            },
        }

    def build(self, rules: str) -> tuple[list[tuple[TaggedSelection, ...]], list[str], list[int]]:
        return expand_axes(rules_to_axes(rules))


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesTagsRulesToJson": TagsRulesToJson,
    "UtilityNodesTagsBuildFromRules": TagsBuildFromRules,
}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesTagsRulesToJson": "Rules to JSON",
    "UtilityNodesTagsBuildFromRules": "Build from Rules",
}
