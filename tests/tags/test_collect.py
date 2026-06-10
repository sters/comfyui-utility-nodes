from nodes.tags._base import TaggedSelection
from nodes.tags.collect import TagsCollect
from nodes.tags.sources.preset.character import CharacterPreset


def _sel(category: str, tags: tuple[str, ...]) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags)


def test_collect_keeps_each_bundle_whole() -> None:
    a = (_sel("character.a", ("long_hair", "serafuku")),)
    b = (_sel("character.b", ("medium_hair", "blazer_uniform")),)
    (bundles,) = TagsCollect().collect(bundle_1=a, bundle_2=b)
    assert bundles == [a, b]


def test_collect_skips_unwired_and_empty_inputs() -> None:
    a = (_sel("character.a", ("long_hair",)),)
    # bundle_1 wired, bundle_2 empty, bundle_3 wired — output stays compact.
    (bundles,) = TagsCollect().collect(bundle_1=a, bundle_2=(), bundle_3=a)
    assert bundles == [a, a]


def test_collect_no_inputs_returns_empty_list() -> None:
    (bundles,) = TagsCollect().collect()
    assert bundles == []


def test_collect_two_characters_feeds_combinator_as_two_values() -> None:
    # The motivating example from issue #23: two characters stay as two
    # discrete axis values, not flattened-then-exploded per tag.
    (blazer,) = CharacterPreset().build("blazer_schoolgirl")
    (serafuku,) = CharacterPreset().build("serafuku_schoolgirl")
    (bundles,) = TagsCollect().collect(bundle_1=tuple(blazer), bundle_2=tuple(serafuku))
    assert len(bundles) == 2
    assert tuple(blazer) in bundles
    assert tuple(serafuku) in bundles
