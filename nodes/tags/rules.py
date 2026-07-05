"""Serialize/expand combinator axes as portable JSON "rules" (issue #27).

Wiring a heavy TagMaster graph (many toggle nodes + presets) just to re-run
the same combinatorial expansion every time is expensive to manage. These two
nodes split that in half:

- ``TagsRulesToJson`` takes the same `axis_i` (`CUUN_TAGS` list) inputs as
  `TagsCombinator` and serializes the *candidates* (not the expansion) to a
  single JSON STRING — run once, inspect/save it with `PreviewAny`, and the
  source graph is no longer needed. A deferred (random_pick/bundle_choice)
  axis serializes just as compactly as an enumerable one — its `Spec` is
  written out whole, not expanded into per-tag candidates.
- ``TagsBuildFromRules`` takes that JSON STRING back and performs the exact
  same cartesian-product expansion (plus deferred-axis resolution)
  `TagsCombinator` does, without needing any of the original toggle/preset
  nodes wired up.
"""

from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, TaggedSelection
from .combinator import Axis, collect_axes, combine_axes, split_deferred_axes

_MAX_AXES = 8


def _selection_to_dict(sel: TaggedSelection) -> dict[str, Any]:
    return {"category": sel.category, "layer": sel.layer, "tags": list(sel.tags), "mutex_within": sel.mutex_within}


def _selection_from_dict(d: dict[str, Any]) -> TaggedSelection:
    return TaggedSelection(
        category=d["category"], layer=d["layer"], tags=tuple(d["tags"]), mutex_within=d["mutex_within"]
    )


def _spec_to_dict(spec: Spec) -> dict[str, Any]:
    if spec.kind == "fixed":
        return {"kind": "fixed", "pool": [_selection_to_dict(s) for s in spec.pool]}
    if spec.kind == "tag_pick":
        return {
            "kind": "tag_pick",
            "seed": spec.seed,
            "count": spec.count,
            "pool": [_selection_to_dict(s) for s in spec.pool],
        }
    if spec.kind == "bundle_choice":
        return {
            "kind": "bundle_choice",
            "seed": spec.seed,
            "bundles": [[_selection_to_dict(s) for s in b] for b in spec.bundles],
        }
    return {"kind": "composite", "children": [_spec_to_dict(c) for c in spec.children]}


def _spec_from_dict(d: dict[str, Any]) -> Spec:
    kind = d["kind"]
    if kind == "fixed":
        return Spec(kind="fixed", pool=tuple(_selection_from_dict(s) for s in d["pool"]))
    if kind == "tag_pick":
        return Spec(
            kind="tag_pick",
            seed=d["seed"],
            count=d["count"],
            pool=tuple(_selection_from_dict(s) for s in d["pool"]),
        )
    if kind == "bundle_choice":
        return Spec(
            kind="bundle_choice",
            seed=d["seed"],
            bundles=tuple(tuple(_selection_from_dict(s) for s in b) for b in d["bundles"]),
        )
    return Spec(kind="composite", children=tuple(_spec_from_dict(c) for c in d["children"]))


def axes_to_rules(axes: list[Axis]) -> str:
    """Serialize a list of combinator axes (each a list of Specs) to JSON."""
    import json

    return json.dumps([[_spec_to_dict(spec) for spec in axis] for axis in axes])


def rules_to_axes(rules: str) -> list[Axis]:
    """Inverse of :func:`axes_to_rules`. Malformed/empty input yields no axes.

    Detects and rejects the pre-Spec-unification format (axis entries were
    plain bundle lists with no `"kind"` key) rather than silently
    misinterpreting it.
    """
    import json

    try:
        data = json.loads(rules) if rules else []
    except ValueError:
        data = []
    if data and data[0] and isinstance(data[0][0], list):
        raise ValueError(
            "TagsBuildFromRules: pre-Spec-unification rules JSON detected — regenerate with the current TagsRulesToJson"
        )
    return [[_spec_from_dict(spec) for spec in axis] for axis in data]


class TagsRulesToJson:
    """Serialize combinator axes (candidates, not the expansion) to a JSON STRING.

    Takes the same wiring as `TagsCombinator` — up to 8 `axis_i` inputs, each
    either a list of resolved `CUUN_TAGS` candidates (from
    `TagsExplode`/`TagsCollect`/a preset) or a single unresolved Spec wired
    directly from `TagsRandomPick`/`TagsRandomBundle` (a deferred axis) — and
    dumps them verbatim as JSON. Preview or save the result once; feed it
    into `TagsBuildFromRules` later to regenerate every combination (and
    re-resolve every deferred axis, one independent roll per combo) without
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
        axes, deferred = collect_axes(kwargs, _MAX_AXES)
        all_axes: list[Axis] = [*axes, *([d] for d in deferred)]
        return (axes_to_rules(all_axes),)


class TagsBuildFromRules:
    """Expand a JSON `rules` STRING (from `TagsRulesToJson`) into combination Specs.

    Performs the identical cartesian-product expansion (plus deferred-axis
    resolution) `TagsCombinator` does, sourcing candidates from the JSON
    instead of live upstream nodes — wire `bundle` and `deferred_bundle` into
    two different `TagsMerge` `bundle_i` slots, exactly like
    `TagsCombinator`'s.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE, "STRING", "INT", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle", "label", "index", "deferred_bundle")
    OUTPUT_IS_LIST: ClassVar[tuple[bool, ...]] = (True, True, True, True)
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

    def build(self, rules: str) -> tuple[list[Spec], list[str], list[int], list[Spec]]:
        axes, deferred = split_deferred_axes(rules_to_axes(rules))
        return combine_axes(axes, deferred)


NODE_CLASS_MAPPINGS: dict[str, type] = {
    "UtilityNodesTagsRulesToJson": TagsRulesToJson,
    "UtilityNodesTagsBuildFromRules": TagsBuildFromRules,
}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesTagsRulesToJson": "Rules to JSON",
    "UtilityNodesTagsBuildFromRules": "Build from Rules",
}
