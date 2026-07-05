from typing import Any, ClassVar

from ._base import TAGS_TYPE, Spec, TaggedSelection, mix_seed, resolve_spec
from ._conflicts import MUTEX_GROUPS, TAG_CONFLICTS

_MAX_INPUTS = 20
_EXTRA_CATEGORY = "extra"


class TagsMerge:
    """The pipeline's terminal build step: resolves any unresolved specs, then
    applies cross-bundle conflict rules, and flattens everything into a prompt.

    Every `bundle_i` input is a `Spec` — either already-resolved
    (`kind="fixed"`, from tag-toggle nodes, presets, `TagsCombinator`, etc.)
    or still-unresolved (from `TagsRandomPick` / `TagsRandomBundle`, or a
    `TagsCombinator`/`TagsBuildFromRules` `deferred_spec` output). This is the
    only node in the pipeline with a `seed` — `TagsRandomPick`/`TagsRandomBundle`
    carry none of their own. Each unresolved spec is resolved here using
    `seed` XOR-mixed with its own slot index (so multiple unresolved specs on
    one call still diverge), then their resulting selections are merged
    alongside the already-fixed inputs through the same mutex/conflict
    pipeline.
    """

    RETURN_TYPES: ClassVar[tuple[str, ...]] = ("STRING", "STRING", TAGS_TYPE)
    RETURN_NAMES: ClassVar[tuple[str, ...]] = ("prompt", "warnings", "bundle")
    FUNCTION: ClassVar[str] = "merge"
    CATEGORY: ClassVar[str] = "UtilityNodes/TagMaster"

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
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True}),
            },
            "optional": optional,
        }

    def merge(self, separator: str, seed: int = 0, extra: str = "", **kwargs: Any) -> tuple[str, str, Spec]:
        sep = separator.encode("utf-8").decode("unicode_escape") if separator else ", "
        warnings: list[str] = []

        # 1. Collect all incoming selections in input order: unresolved specs
        #    resolved (mixing this node's `seed` with each one's own slot
        #    index) first, then already-fixed ones. Unresolved specs going
        #    first means an explicit `bundle_i` override (e.g. a HairColor
        #    node) wins over a random pick via the usual
        #    last-occurrence-wins MUTEX_GROUPS rule below.
        selections: list[TaggedSelection] = []
        specs: list[tuple[int, Spec]] = []
        for i in range(1, _MAX_INPUTS + 1):
            spec = kwargs.get(f"bundle_{i}")
            if spec is None:
                continue
            specs.append((i, spec))
        for i, spec in specs:
            if spec.kind != "fixed":
                selections.extend(resolve_spec(mix_seed(spec, seed ^ i)))
        for _i, spec in specs:
            if spec.kind == "fixed":
                selections.extend(spec.pool)

        # 2. Apply mutex_within: per category, keep only the first selection.
        seen_mutex: dict[str, TaggedSelection] = {}
        post_mutex: list[TaggedSelection] = []
        for sel in selections:
            if sel.mutex_within and sel.category:
                if sel.category in seen_mutex:
                    warnings.append(f"mutex: dropped extra '{sel.category}' selection ({', '.join(sel.tags)})")
                    continue
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

        # 3. Apply MUTEX_GROUPS: cross-category subsets where only one
        #    member may survive (e.g. long_hair vs short_hair). **Last
        #    occurrence wins** so that user-added overrides (later in
        #    input order) defeat preset defaults — e.g. wiring
        #    CharacterPreset(brown_hair) then HairColor(red_hair) keeps
        #    red_hair. Dedupe the per-group hit list first so a tag
        #    appearing twice (e.g. same tag from two presets) isn't
        #    mistaken for a sibling conflict.
        mutex_drop: set[str] = set()
        ordered_tags = [t for sel in post_mutex if sel.category != _EXTRA_CATEGORY for t in sel.tags]
        for group in MUTEX_GROUPS:
            seen_in_group: list[str] = []
            for t in ordered_tags:
                if t in group and t not in seen_in_group:
                    seen_in_group.append(t)
            if len(seen_in_group) > 1:
                group_kept = seen_in_group[-1]
                group_dropped = seen_in_group[:-1]
                mutex_drop.update(group_dropped)
                warnings.append(f"mutex_group: kept '{group_kept}', dropped {group_dropped}")

        # 4. Per-tag conflict suppression. Build the drop set from triggers
        #    present in any non-extra selection, then filter each non-extra
        #    selection's tags. The trigger tags themselves are never dropped.
        all_tags_present = {t for sel in post_mutex if sel.category != _EXTRA_CATEGORY for t in sel.tags}
        drop_tags: set[str] = set()
        triggers: set[str] = set()
        for tag in all_tags_present:
            if tag in TAG_CONFLICTS:
                drop_tags.update(TAG_CONFLICTS[tag])
                triggers.add(tag)
        drop_tags -= triggers
        all_drop = drop_tags | mutex_drop

        final: list[TaggedSelection] = []
        for sel in post_mutex:
            if sel.category == _EXTRA_CATEGORY:
                final.append(sel)
                continue
            kept = tuple(t for t in sel.tags if t not in all_drop)
            conflict_dropped = tuple(t for t in sel.tags if t in drop_tags)
            if conflict_dropped:
                warnings.append(
                    f"conflict: dropped {list(conflict_dropped)} from '{sel.category}' "
                    f"(triggered by {sorted(triggers)})"
                )
            if not kept:
                continue
            if kept != sel.tags:
                sel = TaggedSelection(
                    category=sel.category,
                    layer=sel.layer,
                    tags=kept,
                    mutex_within=sel.mutex_within,
                )
            final.append(sel)

        # 4. Flatten into prompt + append user-supplied extra.
        parts: list[str] = []
        for sel in final:
            parts.extend(sel.tags)
        extra_stripped = extra.strip()
        if extra_stripped:
            parts.append(extra_stripped)
        prompt = sep.join(parts)
        warnings_str = "\n".join(warnings)
        return (prompt, warnings_str, Spec(kind="fixed", pool=tuple(final)))


NODE_CLASS_MAPPINGS: dict[str, type] = {"UtilityNodesTagsMerge": TagsMerge}
NODE_DISPLAY_NAME_MAPPINGS: dict[str, str] = {"UtilityNodesTagsMerge": "Merge & Validate"}
