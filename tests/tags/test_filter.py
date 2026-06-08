from nodes.tags._base import TAG_CATEGORY_REGISTRY, TaggedSelection
from nodes.tags.filter import TagsFilter


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _run(target: str, bundle: tuple[TaggedSelection, ...]) -> tuple[str, tuple[TaggedSelection, ...]]:
    out = TagsFilter().filter(", ", target, bundle=bundle)
    return str(out["ui"]["text"][0]), tuple(out["result"][0])


def test_none_target_passes_bundle_through() -> None:
    bundle = (_sel("clothing.tops", ("shirt",)),)
    prompt, kept = _run("(none)", bundle)
    assert prompt == "shirt"
    assert kept == bundle


def test_drops_tags_with_matching_registry_category() -> None:
    # CharacterPreset(serafuku_schoolgirl) packs everything into one
    # selection with category "preset.X"; per-tag categories come from
    # TAG_CATEGORY_REGISTRY. Filtering clothing.legwear must drop only
    # `thighhighs` from inside the preset selection.
    assert TAG_CATEGORY_REGISTRY.get("thighhighs") == "clothing.legwear"
    bundle = (_sel("preset.serafuku_schoolgirl", ("serafuku", "thighhighs", "loafers")),)
    prompt, kept = _run("clothing.legwear", bundle)
    assert prompt == "serafuku, loafers"
    assert len(kept) == 1
    assert kept[0].tags == ("serafuku", "loafers")
    assert kept[0].category == "preset.serafuku_schoolgirl"


def test_selection_dropped_when_all_tags_removed() -> None:
    bundle = (
        _sel("clothing.tops", ("shirt",)),
        _sel("preset.x", ("thighhighs",)),
    )
    assert TAG_CATEGORY_REGISTRY.get("thighhighs") == "clothing.legwear"
    prompt, kept = _run("clothing.legwear", bundle)
    assert prompt == "shirt"
    assert len(kept) == 1
    assert kept[0].category == "clothing.tops"


def test_extra_selection_always_passes_through() -> None:
    bundle = (
        _sel("clothing.legwear", ("thighhighs",)),
        _sel("extra", ("free text",)),
    )
    prompt, kept = _run("clothing.legwear", bundle)
    assert prompt == "free text"
    assert len(kept) == 1
    assert kept[0].category == "extra"


def test_unregistered_tag_kept() -> None:
    # Free-form tag that isn't in the registry must not get dropped just
    # because the selection's own category coincidentally matches.
    bundle = (_sel("clothing.legwear", ("totally_made_up_tag",)),)
    prompt, kept = _run("clothing.legwear", bundle)
    assert prompt == "totally_made_up_tag"
    assert kept == bundle


def test_no_matches_is_noop() -> None:
    bundle = (_sel("clothing.tops", ("shirt",)),)
    prompt, kept = _run("clothing.legwear", bundle)
    assert prompt == "shirt"
    assert kept == bundle


def test_empty_bundle() -> None:
    prompt, kept = _run("clothing.legwear", ())
    assert prompt == ""
    assert kept == ()


def test_preserves_mutex_within_metadata() -> None:
    bundle = (
        _sel("hair.color", ("red_hair",), mutex_within=True),
        _sel("preset.x", ("thighhighs", "shirt")),
    )
    prompt, kept = _run("clothing.legwear", bundle)
    assert kept[0].mutex_within is True
    assert kept[1].mutex_within is False
    assert kept[1].tags == ("shirt",)
    assert prompt == "red_hair, shirt"


def test_separator_escape() -> None:
    bundle = (_sel("clothing.tops", ("shirt", "blouse")),)
    out = TagsFilter().filter(r"\n", "(none)", bundle=bundle)
    assert out["ui"]["text"] == ("shirt\nblouse",)


def test_no_bundle_input_returns_empty() -> None:
    out = TagsFilter().filter(", ", "(none)")
    assert out["ui"]["text"] == ("",)
    assert out["result"] == ((),)
