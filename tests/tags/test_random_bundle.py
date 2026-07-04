from nodes.tags._base import TaggedSelection
from nodes.tags.random_bundle import TagsRandomBundle


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def test_random_bundle_returns_bundle_choice_spec() -> None:
    a = (_sel("character.a", ("long_hair", "serafuku")),)
    b = (_sel("character.b", ("short_hair", "blazer")),)
    c = (_sel("character.c", ("ponytail", "hoodie")),)
    (spec,) = TagsRandomBundle().pick(0, bundle_1=a, bundle_2=b, bundle_3=c)
    assert spec.kind == "bundle_choice"
    assert spec.seed == 0
    assert spec.bundles == (a, b, c)


def test_random_bundle_skips_unwired_and_empty_inputs() -> None:
    a = (_sel("x", ("a",)),)
    # only bundle_2 and bundle_5 carry content; the rest are empty/unwired.
    (spec,) = TagsRandomBundle().pick(0, bundle_2=a, bundle_3=(), bundle_5=a)
    assert spec.bundles == (a, a)


def test_random_bundle_no_inputs_returns_empty_candidates() -> None:
    (spec,) = TagsRandomBundle().pick(0)
    assert spec.bundles == ()
