from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.random_bundle import TagsRandomBundle


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_random_bundle_returns_bundle_choice_spec() -> None:
    a = (_sel("character.a", ("long_hair", "serafuku")),)
    b = (_sel("character.b", ("short_hair", "blazer")),)
    c = (_sel("character.c", ("ponytail", "hoodie")),)
    (spec,) = TagsRandomBundle().pick(0, bundle_1=_fixed(*a), bundle_2=_fixed(*b), bundle_3=_fixed(*c))
    assert spec.kind == "bundle_choice"
    assert spec.seed == 0
    assert spec.bundles == (a, b, c)


def test_random_bundle_skips_unwired_and_empty_inputs() -> None:
    a = (_sel("x", ("a",)),)
    # only bundle_2 and bundle_5 carry content; the rest are empty/unwired.
    (spec,) = TagsRandomBundle().pick(0, bundle_2=_fixed(*a), bundle_3=Spec(kind="fixed", pool=()), bundle_5=_fixed(*a))
    assert spec.bundles == (a, a)


def test_random_bundle_no_inputs_returns_empty_candidates() -> None:
    (spec,) = TagsRandomBundle().pick(0)
    assert spec.bundles == ()
