from itertools import product
from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, TaggedSelection, mix_seed

Axis = list[Spec]


def split_deferred_axes(axes_in: list[list[Spec]]) -> tuple[list[Axis], list[Spec]]:
    """Split raw axis lists into enumerable axes vs. deferred (random) axes.

    Both kinds ride the same `CUUN_TAGS` socket:

    - An **enumerable** axis: a list of `kind="fixed"` Specs (typically from
      `TagsExplode`/`TagsCollect`/a preset) — every value is cross-multiplied.
    - A **deferred** axis: wiring a `TagsRandomPick`/`TagsRandomBundle` scalar
      output directly into `axis_i` arrives (via ComfyUI's `INPUT_IS_LIST`
      wrapping, or via a single-entry axis round-tripped through
      `rules.py`) as a length-1 list holding one still-unresolved Spec. It is
      *not* cross-multiplied — it rides along on every combo, resolved later.

    Drops empty bundles (e.g. `TagsExplode` on a node with no checked tags
    emits a single empty-pool Spec as a sentinel) and axes left entirely empty.
    """
    axes: list[Axis] = []
    deferred: list[Spec] = []
    for v in axes_in:
        if not v:
            continue
        if len(v) == 1 and v[0].kind != "fixed":
            deferred.append(v[0])
            continue
        non_empty = [s for s in v if s.kind == "fixed" and s.pool]
        if not non_empty:
            continue
        axes.append(non_empty)
    return axes, deferred


def collect_axes(kwargs: dict[str, Any], max_axes: int) -> tuple[list[Axis], list[Spec]]:
    """Pull `axis_1..axis_max_axes` out of a kwargs dict and split them (see `split_deferred_axes`)."""
    raw = [v for i in range(1, max_axes + 1) if (v := kwargs.get(f"axis_{i}")) is not None]
    return split_deferred_axes(raw)


def expand_axes(axes: list[Axis]) -> tuple[list[tuple[TaggedSelection, ...]], list[str], list[int]]:
    """Cartesian-product expansion over combinator axes.

    Each combination's axis Specs are concatenated in axis order; conflict
    resolution is deferred to a downstream `TagsMerge`.
    """
    if not axes:
        return ([], [], [])

    bundles: list[tuple[TaggedSelection, ...]] = []
    labels: list[str] = []
    indices: list[int] = []
    for idx, combo in enumerate(product(*axes)):
        merged = tuple(sel for spec in combo for sel in spec.pool)
        bundles.append(merged)
        labels.append(label_combo(combo))
        indices.append(idx)
    return (bundles, labels, indices)


def label_combo(combo: tuple[Spec, ...]) -> str:
    """Build a human-readable label for one cartesian-product combination.

    Shared by ``TagsCombinator`` and ``TagsBuildFromRules`` — both expand axes
    of Specs the same way, so both combos are labeled the same way.
    """
    parts: list[str] = []
    for spec in combo:
        non_extra = [s for s in spec.pool if s.category != "extra"]
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


def combine_axes(axes: list[Axis], deferred: list[Spec]) -> tuple[list[Spec], list[str], list[int], list[Spec]]:
    """Expand the enumerable axes and attach the deferred (random) axes to every combo.

    Shared by ``TagsCombinator.combine`` and ``TagsBuildFromRules.build`` so
    the "at most one deferred-spec output, however many deferred axes fed it"
    behavior lives in one place.
    """
    bundles, labels, indices = expand_axes(axes)
    if not bundles and deferred:
        # No enumerable axis at all (only deferred ones) — still exactly one
        # combo, just with an empty fixed portion.
        bundles, labels, indices = [()], ["anon"], [0]

    fixed_specs = [Spec(kind="fixed", pool=b) for b in bundles]

    base_deferred: Spec | None
    if not deferred:
        base_deferred = None
    elif len(deferred) == 1:
        base_deferred = deferred[0]
    else:
        base_deferred = Spec(kind="composite", children=tuple(deferred))

    deferred_specs = (
        [mix_seed(base_deferred, idx) for idx in indices]
        if base_deferred is not None
        else [Spec(kind="fixed", pool=()) for _ in indices]
    )

    return (fixed_specs, labels, indices, deferred_specs)


class TagsCombinator:
    """Cartesian product over axes of CUUN_TAGS Specs.

    Each axis input is either a list of resolved (`kind="fixed"`) candidates
    — typically produced by `TagsExplode` for tag-toggle nodes, `TagsCollect`
    for whole-bundle alternatives, or wired directly from a preset for
    single-value axes — or a single unresolved Spec wired directly from
    `TagsRandomPick`/`TagsRandomBundle` (a *deferred* axis: not
    cross-multiplied, carried through to every combo and resolved later, one
    independent roll per combo).

    The node generates every combination of the enumerable axes and emits
    each as a `kind="fixed"` Spec via `bundle` — it does *not* merge or
    resolve conflicts itself. Any deferred axes are folded into the `
    deferred_spec` output (composited together if there's more than one).
    Wire both `bundle` and `deferred_spec` into two different `TagsMerge`
    ("Merge & Validate") `bundle_i` slots; ComfyUI broadcasts that node over
    the output lists, so it runs once per combination and produces the
    per-combo prompt / warnings, with each combo's deferred axes independently
    resolved.

    Axis order is the priority order — `TagsMerge`'s MUTEX_GROUPS is
    last-wins, so put base / fixed axes earlier and override axes later
    (a later HairColor red_hair will defeat an earlier preset's
    brown_hair once merged).
    """

    INPUT_IS_LIST: ClassVar[bool] = True
    RETURN_TYPES: ClassVar[tuple[str, ...]] = (TAGS_TYPE, "STRING", "INT", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("bundle", "label", "index", "deferred_spec")
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
            "required": {},
            "optional": optional,
        }

    def combine(
        self,
        **kwargs: Any,
    ) -> tuple[list[Spec], list[str], list[int], list[Spec]]:
        axes, deferred = collect_axes(kwargs, self._MAX_AXES)
        return combine_axes(axes, deferred)


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsCombinator": TagsCombinator}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {
    "UtilityNodesTagsCombinator": "Combinator",
}
