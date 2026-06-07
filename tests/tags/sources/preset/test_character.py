from typing import Any

from nodes.tags._base import TaggedSelection
from nodes.tags.merge import TagsMerge
from nodes.tags.sources.preset.character import PRESETS, CharacterPreset


def _build(preset: str, **kw: Any) -> tuple[str, tuple[TaggedSelection, ...]]:
    out = CharacterPreset().build(preset, ", ", **kw)
    return str(out["result"][0]), tuple(out["result"][1])


def test_input_types_lists_all_presets() -> None:
    spec = CharacterPreset.INPUT_TYPES()
    options, meta = spec["required"]["preset"]
    assert set(options) == set(PRESETS)
    assert meta["default"] in PRESETS


def test_preset_emits_full_tag_list() -> None:
    prompt, bundle = _build("miko")
    assert prompt == ", ".join(PRESETS["miko"])
    assert len(bundle) == 1
    assert bundle[0].tags == PRESETS["miko"]
    assert bundle[0].category == "preset.miko"


def test_preset_extra_appended_as_separate_selection() -> None:
    prompt, bundle = _build("miko", extra="1girl")
    assert prompt.endswith(", 1girl")
    assert len(bundle) == 2
    assert bundle[1].category == "extra"
    assert bundle[1].tags == ("1girl",)


def test_preset_pipes_through_tagsmerge_cleanly() -> None:
    _, bundle = _build("miko")
    out = TagsMerge().merge(", ", bundle_1=bundle)
    assert out["result"][0] == ", ".join(PRESETS["miko"])


def test_two_presets_with_conflicts_get_resolved() -> None:
    # nun adds nude-not-but-long_dress+veil. Combine with maid which has
    # frilled_apron + thighhighs + mary_janes. Both have long_hair which
    # gets deduped via mutex_group (hair length).
    _, nun_bundle = _build("nun")
    _, maid_bundle = _build("maid")
    out = TagsMerge().merge(", ", bundle_1=nun_bundle, bundle_2=maid_bundle)
    prompt = str(out["result"][0])
    tokens = prompt.split(", ")
    # long_hair appears in both presets and is kept (duplicates are
    # harmless; mutex_group only drops *different* tags from a group).
    assert "long_hair" in tokens
    # Hair color mutex: nun has silver_hair, maid has black_hair → last wins
    assert "black_hair" in tokens
    assert "silver_hair" not in tokens


def test_preset_layered_with_nude_drops_clothing() -> None:
    # If user explicitly adds nude on top of a preset, conflict resolution
    # drops the preset's clothing tags.
    _, miko_bundle = _build("miko")
    nude_sel = (TaggedSelection("body.exposure", "exposure", ("nude",), False),)
    out = TagsMerge().merge(", ", bundle_1=nude_sel, bundle_2=miko_bundle)
    prompt = str(out["result"][0])
    tokens = prompt.split(", ")
    assert "nude" in tokens
    assert "miko" not in tokens  # dropped via _ALL_CLOTHING (uniform)
    assert "long_hair" in tokens  # not clothing, kept
