from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.random_bundle import TagsRandomBundle


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_random_bundle_returns_bundle_choice_spec() -> None:
    a = _fixed(_sel("character.a", ("long_hair", "serafuku")))
    b = _fixed(_sel("character.b", ("short_hair", "blazer")))
    c = _fixed(_sel("character.c", ("ponytail", "hoodie")))
    (spec,) = TagsRandomBundle().pick(bundle_1=a, bundle_2=b, bundle_3=c)
    assert spec.kind == "bundle_choice"
    assert spec.seed == 0
    assert spec.bundles == (a, b, c)


def test_random_bundle_skips_unwired_and_empty_inputs() -> None:
    a = _fixed(_sel("x", ("a",)))
    # only bundle_2 and bundle_5 carry content; the rest are empty/unwired.
    (spec,) = TagsRandomBundle().pick(bundle_2=a, bundle_3=Spec(kind="fixed", pool=()), bundle_5=a)
    assert spec.bundles == (a, a)


def test_random_bundle_no_inputs_returns_empty_candidates() -> None:
    (spec,) = TagsRandomBundle().pick()
    assert spec.bundles == ()


def test_random_bundle_accepts_unresolved_candidates() -> None:
    # A candidate need not already be fixed — it may be another
    # TagsRandomPick/TagsRandomBundle output, resolved later by TagsBuild.
    fixed_candidate = _fixed(_sel("x", ("a",)))
    deferred_candidate = Spec(kind="tag_pick", pool=(_sel("y", ("b", "c")),), count=1)
    (spec,) = TagsRandomBundle().pick(bundle_1=fixed_candidate, bundle_2=deferred_candidate)
    assert spec.bundles == (fixed_candidate, deferred_candidate)
