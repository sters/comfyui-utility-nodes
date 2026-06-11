from nodes.tags._base import TaggedSelection
from nodes.tags.random_bundle import TagsRandomBundle


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def test_random_bundle_returns_one_input_intact() -> None:
    a = (_sel("character.a", ("long_hair", "serafuku")),)
    b = (_sel("character.b", ("short_hair", "blazer")),)
    c = (_sel("character.c", ("ponytail", "hoodie")),)
    (out,) = TagsRandomBundle().pick(0, bundle_1=a, bundle_2=b, bundle_3=c)
    # Whatever is chosen, it is one of the inputs returned unchanged.
    assert out in (a, b, c)


def test_random_bundle_preserves_category_and_mutex() -> None:
    a = (_sel("clothing.bottoms", ("skirt",), mutex_within=True),)
    (out,) = TagsRandomBundle().pick(0, bundle_1=a)
    assert out == a
    assert out[0].category == "clothing.bottoms"
    assert out[0].mutex_within is True


def test_random_bundle_skips_unwired_and_empty_inputs() -> None:
    a = (_sel("x", ("a",)),)
    # only bundle_2 and bundle_5 carry content; the rest are empty/unwired.
    (out,) = TagsRandomBundle().pick(0, bundle_2=a, bundle_3=(), bundle_5=a)
    assert out == a


def test_random_bundle_is_deterministic_for_same_seed() -> None:
    cands = {f"bundle_{i}": (_sel(f"c{i}", (f"tag_{i}",)),) for i in range(1, 9)}
    r1 = TagsRandomBundle().pick(12345, **cands)[0]
    r2 = TagsRandomBundle().pick(12345, **cands)[0]
    assert r1 == r2


def test_random_bundle_different_seeds_span_all_candidates() -> None:
    cands = {f"bundle_{i}": (_sel(f"c{i}", (f"tag_{i}",)),) for i in range(1, 4)}
    seen = {TagsRandomBundle().pick(s, **cands)[0] for s in range(50)}
    # Across many seeds every candidate should be reachable.
    assert len(seen) == 3


def test_random_bundle_no_inputs_returns_empty() -> None:
    (out,) = TagsRandomBundle().pick(0)
    assert out == ()
