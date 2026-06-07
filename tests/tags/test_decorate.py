"""Tests for TagDecorate + ColorPalette."""

from __future__ import annotations

import importlib
import pkgutil

import nodes.tags
from nodes.tags._base import TAG_CATEGORY_REGISTRY, TaggedSelection
from nodes.tags.decorate import TagDecorate
from nodes.tags.decoration.color import ColorPalette


def _populate_registry() -> None:
    """TAG_CATEGORY_REGISTRY is filled lazily as TagNodeBase subclasses are
    imported. The top-level __init__.py walks for ComfyUI, but in pytest we
    have to do it ourselves."""
    for _f, name, ispkg in pkgutil.walk_packages(nodes.tags.__path__, "nodes.tags."):
        if ispkg or name.rsplit(".", 1)[1].startswith("_"):
            continue
        importlib.import_module(name)


_populate_registry()


def _result(out: dict[str, object]) -> tuple[str, str, tuple[TaggedSelection, ...]]:
    return out["result"]  # type: ignore[return-value]


def _bundle(*selections: TaggedSelection) -> tuple[TaggedSelection, ...]:
    return tuple(selections)


def test_registry_populated_from_subclasses() -> None:
    # Spot-check tags from several modules.
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
    prompt, warnings, _ = _result(TagDecorate().decorate(", ", "clothing.bottoms", bundle, decoration))
    assert "red green plaid pleated skirt" in prompt
    assert "thighhighs" in prompt
    assert "long_hair" in prompt
    assert warnings == ""


def test_no_match_emits_warning_and_leaves_bundle_alone() -> None:
    bundle = _bundle(TaggedSelection(category="preset.character", layer="preset", tags=("long_hair",)))
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",)))
    prompt, warnings, out_bundle = _result(TagDecorate().decorate(", ", "clothing.bottoms", bundle, decoration))
    assert prompt == "long_hair"
    assert out_bundle == bundle
    assert "no tags in bundle matched" in warnings


def test_no_decoration_is_passthrough() -> None:
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    prompt, warnings, out_bundle = _result(TagDecorate().decorate(", ", "clothing.bottoms", bundle, ()))
    assert prompt == "pleated_skirt"
    assert out_bundle == bundle
    assert warnings == ""


def test_none_target_with_decoration_warns_and_passes_through() -> None:
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",)))
    prompt, warnings, _ = _result(TagDecorate().decorate(", ", "(none)", bundle, decoration))
    assert prompt == "pleated_skirt"
    assert "no target_category selected" in warnings


def test_extra_selection_passes_through_untouched() -> None:
    bundle = _bundle(
        TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)),
        TaggedSelection(category="extra", layer="extra", tags=("my custom phrase",)),
    )
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("red",)))
    prompt, _, out_bundle = _result(TagDecorate().decorate(", ", "clothing.bottoms", bundle, decoration))
    assert "red pleated skirt" in prompt
    assert "my custom phrase" in prompt
    # extra selection preserved untouched at its position.
    assert out_bundle[-1].category == "extra"
    assert out_bundle[-1].tags == ("my custom phrase",)


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
    _, _, stage1 = _result(TagDecorate().decorate(", ", "clothing.bottoms", bundle, skirt_deco))
    prompt, _, _ = _result(TagDecorate().decorate(", ", "clothing.legwear", stage1, leg_deco))
    assert "red pleated skirt" in prompt
    assert "white thighhighs" in prompt


def test_underscore_in_decoration_becomes_space() -> None:
    bundle = _bundle(TaggedSelection(category="clothing.bottoms", layer="clothing", tags=("pleated_skirt",)))
    decoration = _bundle(TaggedSelection(category="decoration.color", layer="decoration", tags=("light_blue",)))
    prompt, _, _ = _result(TagDecorate().decorate(", ", "clothing.bottoms", bundle, decoration))
    assert "light blue pleated skirt" in prompt


def test_color_palette_emits_decoration_color_selection() -> None:
    node = ColorPalette()
    out = node.build(", ", preset="custom", red=True, green=True)
    prompt, bundle = out["result"]
    assert prompt == "red, green"
    assert len(bundle) == 1
    assert bundle[0].category == "decoration.color"
    assert bundle[0].layer == "decoration"
    assert bundle[0].tags == ("red", "green")
