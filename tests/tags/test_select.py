from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.collect import TagsCollect
from nodes.tags.combinator import TagsCombinator
from nodes.tags.select import TagsSelect
from nodes.tags.sources.preset.character import CharacterPreset


def _sel(category: str, tags: tuple[str, ...]) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_select_returns_indexed_bundle_and_label() -> None:
    a = _fixed(_sel("character.a", ("long_hair",)))
    b = _fixed(_sel("character.b", ("short_hair",)))
    bundle, label, eff = TagsSelect().select([1], bundles=[a, b], labels=["a", "b"])
    assert bundle == b
    assert label == "b"
    assert eff == 1


def test_select_wraps_index_modulo_length() -> None:
    a = _fixed(_sel("character.a", ("long_hair",)))
    b = _fixed(_sel("character.b", ("short_hair",)))
    # index 3 over 2 items wraps to 3 % 2 == 1.
    bundle, label, eff = TagsSelect().select([3], bundles=[a, b], labels=["a", "b"])
    assert bundle == b
    assert label == "b"
    assert eff == 1


def test_select_without_labels_returns_empty_label() -> None:
    a = _fixed(_sel("character.a", ("long_hair",)))
    bundle, label, eff = TagsSelect().select([0], bundles=[a])
    assert bundle == a
    assert label == ""
    assert eff == 0


def test_select_empty_bundles_returns_empty() -> None:
    bundle, label, eff = TagsSelect().select([5], bundles=[])
    assert bundle == Spec(kind="fixed", pool=())
    assert label == ""
    assert eff == 0


def test_select_walks_full_combinator_sweep_one_per_index() -> None:
    # The motivating pattern: queue N runs, index increments, each run picks
    # exactly one combination — no list-wide fanout downstream.
    (blazer,) = CharacterPreset().build("blazer_schoolgirl")
    (serafuku,) = CharacterPreset().build("serafuku_schoolgirl")
    (bundles,) = TagsCollect().collect(bundle_1=blazer, bundle_2=serafuku)
    combo_bundles, labels, _, _ = TagsCombinator().combine(axis_1=bundles)

    picked = [TagsSelect().select([i], bundles=combo_bundles, labels=labels) for i in range(len(combo_bundles))]
    picked_labels = [p[1] for p in picked]
    assert picked_labels == labels
    # Each pick is a single whole bundle, not the full list.
    for bundle, _, _ in picked:
        assert bundle in combo_bundles
