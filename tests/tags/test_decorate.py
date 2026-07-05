"""Tests for TagsDecorate + ColorPalette."""

from __future__ import annotations

import importlib
import pkgutil

import nodes.tags
from nodes.tags._base import TAG_CATEGORY_REGISTRY, Spec, TaggedSelection
from nodes.tags.decorate import TagsDecorate
from nodes.tags.sources.decoration.color import ColorPalette


def _populate_registry() -> None:
    """TAG_CATEGORY_REGISTRY is filled lazily as TagNodeBase subclasses are
    imported. The top-level __init__.py walks for ComfyUI, but in pytest we
    have to do it ourselves."""
    for _f, name, ispkg in pkgutil.walk_packages(nodes.tags.__path__, "nodes.tags."):
        if ispkg or name.rsplit(".", 1)[1].startswith("_"):
            continue
        importlib.import_module(name)


_populate_registry()


def _bundle(*selections: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=tuple(selections))


def _call(
    target: str,
    bundle: Spec | list[Spec] | None = None,
    decoration: Spec | list[Spec] | None = None,
    *,
    sep: str = ", ",
) -> tuple[list[str], list[str], list[Spec]]:
    """Helper mimicking ComfyUI's INPUT_IS_LIST contract: every arg is a list.

    Returns (prompts, warnings, bundles) — prompts are reconstructed from the
    bundles so callers don't need to know decorate dropped its prompt output.
    """
    b = bundle if isinstance(bundle, list) else ([bundle] if bundle is not None else None)
    d = decoration if isinstance(decoration, list) else ([decoration] if decoration is not None else None)
    out = TagsDecorate().decorate(
        target_category=[target],
        bundle=b,
        decoration=d,
    )
    warnings, bundles = out
    prompts = [sep.join(t for sel in bun.pool for t in sel.tags) for bun in bundles]
    return prompts, warnings, bundles


def test_registry_populated_from_subclasses() -> None:
    assert TAG_CATEGORY_REGISTRY.get("pleated_skirt") == "clothing.bottoms"
    assert TAG_CATEGORY_REGISTRY.get("plaid") == "clothing.pattern"
    assert TAG_CATEGORY_REGISTRY.get("silk") == "clothing.material"
    assert TAG_CATEGORY_REGISTRY.get("red") == "decoration.color"


def test_prefix_matches_target_category() -> None:
    bundle = _bundle(
        TaggedSelection(
            category="preset.character",
            layer="preset",
            tags=("long_hair", "serafuku", "pleated_skirt", "thighhighs"),
        )
    )
    decoration = _bundle(
        TaggedSelection(category="decoration.color", layer="decoration", tags=("red", "green")),
        TaggedSelection(category="clothing.pattern", layer="clothing", tags=("plaid",)),
    )
    prompts, warnings, _ = _call("clothing.bottoms", bundle, decoration)
    assert len(prompts) == 1
    assert "red green plaid pleated skirt" in prompts[0]
    assert "thighhighs" in prompts[0]
    assert "long_hair" in prompts[0]
    assert warnings[0] == ""


def test_no_match_emits_warning_and_leaves_bundle_alone() -> None:
    bundle = _bundle(TaggedSelection(category="preset.character", layer="preset", tags=("long_hair",)))
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",)))
    prompts, warnings, out_bundles = _call("clothing.bottoms", bundle, decoration)
    assert prompts == ["long_hair"]
    assert out_bundles == [bundle]
    assert "no tags in bundle matched" in warnings[0]


def test_no_decoration_is_passthrough() -> None:
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    prompts, warnings, out_bundles = _call("clothing.bottoms", bundle, None)
    assert prompts == ["pleated_skirt"]
    assert out_bundles == [bundle]
    assert warnings == [""]


def test_none_target_with_decoration_warns_and_passes_through() -> None:
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",)))
    prompts, warnings, _ = _call("(none)", bundle, decoration)
    assert prompts == ["pleated_skirt"]
    assert "no target_category selected" in warnings[0]


def test_extra_selection_passes_through_untouched() -> None:
    bundle = _bundle(
        TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)),
        TaggedSelection(category="extra", layer="extra", tags=("my custom phrase",)),
    )
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",)))
    prompts, _, out_bundles = _call("clothing.bottoms", bundle, decoration)
    assert "red pleated skirt" in prompts[0]
    assert "my custom phrase" in prompts[0]
    assert out_bundles[0].pool[-1].category == "extra"
    assert out_bundles[0].pool[-1].tags == ("my custom phrase",)


def test_chained_decorate_applies_independent_rules() -> None:
    bundle = _bundle(
        TaggedSelection(
            category="preset.character",
            layer="preset",
            tags=("pleated_skirt", "thighhighs"),
        )
    )
    skirt_deco = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",)))
    leg_deco = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("white",)))
    _, _, stage1 = _call("clothing.bottoms", bundle, skirt_deco)
    prompts, _, _ = _call("clothing.legwear", stage1, leg_deco)
    assert len(prompts) == 1
    assert "red pleated skirt" in prompts[0]
    assert "white thighhighs" in prompts[0]


def test_underscore_in_decoration_becomes_space() -> None:
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("light_blue",)))
    prompts, _, _ = _call("clothing.bottoms", bundle, decoration)
    assert "light blue pleated skirt" in prompts[0]


def test_color_palette_emits_decoration_color_selection() -> None:
    node = ColorPalette()
    out = node.build("", red=True, green=True)
    (spec,) = out
    bundle = spec.pool
    assert ", ".join(t for sel in bundle for t in sel.tags) == "red, green"
    assert len(bundle) == 1
    assert bundle[0].category == "decoration.color"
    assert bundle[0].layer == "decoration"
    assert bundle[0].tags == ("red", "green")


# ----------------------------------------------------------------------
# Cross-product semantics (INPUT_IS_LIST = True)
# ----------------------------------------------------------------------


def test_single_bundle_x_decoration_list_broadcasts() -> None:
    """`Decorate(Character, skirt, [red, green, blue])` → 3 prompts. The
    legacy use case — must continue to work when decoration is a list."""
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    decos = [
        _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",))),
        _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("green",))),
        _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("blue",))),
    ]
    prompts, _, _ = _call("clothing.bottoms", bundle, decos)
    assert len(prompts) == 3
    assert "red pleated skirt" in prompts[0]
    assert "green pleated skirt" in prompts[1]
    assert "blue pleated skirt" in prompts[2]


def test_bundle_list_x_decoration_list_is_cross_product() -> None:
    """2 bundles × 3 decorations = 6 prompts in (bundle outer, decoration inner) order."""
    tops = [
        _bundle(TaggedSelection(category="clothing.tops", layer="clothing", tags=("shirt",))),
        _bundle(TaggedSelection(category="clothing.tops", layer="clothing", tags=("blouse",))),
    ]
    colors = [
        _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",))),
        _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("green",))),
        _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("blue",))),
    ]
    prompts, _, _ = _call("clothing.tops", tops, colors)
    assert prompts == ["red shirt", "green shirt", "blue shirt", "red blouse", "green blouse", "blue blouse"]


def test_empty_lists_collapse_to_passthrough() -> None:
    """Unwired (None) decoration shouldn't zero out the cross product —
    bundles pass through with no decoration applied."""
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    prompts, warnings, _ = _call("clothing.bottoms", bundle, None)
    assert prompts == ["pleated_skirt"]
    assert warnings == [""]
