from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.random_pick import TagsRandomPick


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def test_random_pick_returns_tag_pick_spec() -> None:
    bundle = (_sel("x", ("a", "b", "c", "d", "e")),)
    (spec,) = TagsRandomPick().pick(3, Spec(kind="fixed", pool=bundle))
    assert spec.kind == "tag_pick"
    assert spec.seed == 0
    assert spec.count == 3
    assert spec.pool == bundle


def test_random_pick_defaults_pool_to_empty_for_unwired_bundle() -> None:
    (spec,) = TagsRandomPick().pick(3, None)
    assert spec.pool == ()
