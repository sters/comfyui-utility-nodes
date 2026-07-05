from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.collect import TagsCollect
from nodes.tags.sources.preset.character import CharacterPreset


def _sel(category: str, tags: tuple[str, ...]) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_collect_keeps_each_bundle_whole() -> None:
    a = _fixed(_sel("character.a", ("long_hair", "serafuku")))
    b = _fixed(_sel("character.b", ("medium_hair", "blazer_uniform")))
    (specs,) = TagsCollect().collect(bundle_1=a, bundle_2=b)
    assert specs == [a, b]


def test_collect_skips_unwired_and_empty_inputs() -> None:
    a = _fixed(_sel("character.a", ("long_hair",)))
    # bundle_1 wired, bundle_2 empty, bundle_3 wired — output stays compact.
    (specs,) = TagsCollect().collect(bundle_1=a, bundle_2=Spec(kind="fixed", pool=()), bundle_3=a)
    assert specs == [a, a]


def test_collect_no_inputs_returns_empty_list() -> None:
    (specs,) = TagsCollect().collect()
    assert specs == []


def test_collect_two_characters_feeds_combinator_as_two_values() -> None:
    # The motivating example from issue #23: two characters stay as two
    # discrete axis values, not flattened-then-exploded per tag.
    (blazer,) = CharacterPreset().build("blazer_schoolgirl")
    (serafuku,) = CharacterPreset().build("serafuku_schoolgirl")
    (specs,) = TagsCollect().collect(bundle_1=blazer, bundle_2=serafuku)
    assert len(specs) == 2
    assert blazer in specs
    assert serafuku in specs
