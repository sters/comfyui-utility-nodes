from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.shuffle import TagsShuffle


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_shuffle_reorders_tags_within_selection() -> None:
    bundle = _fixed(_sel("hair.color", ("a", "b", "c", "d", "e", "f")))
    out = TagsShuffle().shuffle(42, bundle)
    (new_bundle,) = out
    assert set(new_bundle.pool[0].tags) == {"a", "b", "c", "d", "e", "f"}
    # With seed=42, output must differ from input order (proves shuffle ran).
    assert new_bundle.pool[0].tags != ("a", "b", "c", "d", "e", "f")
    assert new_bundle.pool[0].category == "hair.color"


def test_shuffle_preserves_selection_metadata() -> None:
    bundle = _fixed(
        _sel("hair.color", ("red", "blue", "green"), mutex_within=True),
        _sel("clothing.tops", ("shirt", "blouse")),
    )
    out = TagsShuffle().shuffle(7, bundle)
    (new_bundle,) = out
    assert len(new_bundle.pool) == 2
    assert new_bundle.pool[0].category == "hair.color"
    assert new_bundle.pool[0].mutex_within is True
    assert new_bundle.pool[1].category == "clothing.tops"
    assert new_bundle.pool[1].mutex_within is False


def test_shuffle_is_deterministic_for_same_seed() -> None:
    bundle = _fixed(_sel("x", ("a", "b", "c", "d", "e", "f", "g")))
    r1 = TagsShuffle().shuffle(999, bundle)[0]
    r2 = TagsShuffle().shuffle(999, bundle)[0]
    assert r1 == r2


def test_shuffle_skips_extra_and_single_tag_selections() -> None:
    bundle = _fixed(
        _sel("extra", ("freeform text",)),
        _sel("hair.color", ("only_one",)),
        _sel("clothing.tops", ("a", "b", "c")),
    )
    (out,) = TagsShuffle().shuffle(1, bundle)
    assert out.pool[0].tags == ("freeform text",)
    assert out.pool[1].tags == ("only_one",)
    # Last one with 3 tags should be reordered.
    assert set(out.pool[2].tags) == {"a", "b", "c"}


def test_shuffle_empty_bundle_is_passthrough() -> None:
    out = TagsShuffle().shuffle(1, Spec(kind="fixed", pool=()))
    (bundle,) = out
    assert ", ".join(t for sel in out[0].pool for t in sel.tags) == ""
    assert bundle == Spec(kind="fixed", pool=())
