import pytest

from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.concat import TagsConcat
from nodes.tags.random_pick import TagsRandomPick
from nodes.tags.sources.preset.character import CharacterPreset


def _sel(category: str, tags: tuple[str, ...]) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_concat_flattens_selections_in_input_order() -> None:
    a = _fixed(_sel("scene.indoor", ("bedroom", "kitchen")))
    b = _fixed(_sel("scene.outdoor", ("beach", "park")))
    (spec,) = TagsConcat().concat(bundle_1=a, bundle_2=b)
    assert spec.kind == "fixed"
    assert spec.pool == (
        _sel("scene.indoor", ("bedroom", "kitchen")),
        _sel("scene.outdoor", ("beach", "park")),
    )


def test_concat_does_not_apply_conflict_resolution() -> None:
    # Two selections from the same mutex category both survive intact —
    # TagsConcat never runs mutex_within/MUTEX_GROUPS, unlike TagsBuild.
    a = _fixed(TaggedSelection(category="hair.length", layer="test", tags=("long_hair",), mutex_within=True))
    b = _fixed(TaggedSelection(category="hair.length", layer="test", tags=("short_hair",), mutex_within=True))
    (spec,) = TagsConcat().concat(bundle_1=a, bundle_2=b)
    assert len(spec.pool) == 2
    assert spec.pool[0].tags == ("long_hair",)
    assert spec.pool[1].tags == ("short_hair",)


def test_concat_skips_unwired_inputs() -> None:
    a = _fixed(_sel("x", ("a",)))
    (spec,) = TagsConcat().concat(bundle_1=a, bundle_3=a)
    assert spec.pool == (_sel("x", ("a",)), _sel("x", ("a",)))


def test_concat_no_inputs_returns_empty_bundle() -> None:
    (spec,) = TagsConcat().concat()
    assert spec == Spec(kind="fixed", pool=())


def test_concat_rejects_unresolved_input() -> None:
    (pick,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("x", ("a", "b"))))
    with pytest.raises(ValueError, match="TagsConcat"):
        TagsConcat().concat(bundle_1=pick)


def test_concat_feeds_random_pick_over_combined_pool() -> None:
    # The motivating use case: pick 1 tag out of the union of two nodes'
    # tags without TagsBuild's conflict rules running first.
    (blazer,) = CharacterPreset().build("blazer_schoolgirl")
    (serafuku,) = CharacterPreset().build("serafuku_schoolgirl")
    (pool,) = TagsConcat().concat(bundle_1=blazer, bundle_2=serafuku)
    (spec,) = TagsRandomPick().pick(count=1, bundle=pool)
    assert spec.pool == pool.pool
    assert spec.count == 1
