from nodes.tags._base import TaggedSelection
from nodes.tags.random_pick import TagsRandomPick
from nodes.tags.shuffle import TagsShuffle


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


# --- TagsShuffle ----------------------------------------------------------


def test_shuffle_reorders_tags_within_selection() -> None:
    bundle = (_sel("hair.color", ("a", "b", "c", "d", "e", "f")),)
    out = TagsShuffle().shuffle(", ", 42, bundle)
    _, new_bundle = out["result"]
    assert set(new_bundle[0].tags) == {"a", "b", "c", "d", "e", "f"}
    # With seed=42, output must differ from input order (proves shuffle ran).
    assert new_bundle[0].tags != ("a", "b", "c", "d", "e", "f")
    assert new_bundle[0].category == "hair.color"


def test_shuffle_preserves_selection_metadata() -> None:
    bundle = (
        _sel("hair.color", ("red", "blue", "green"), mutex_within=True),
        _sel("clothing.tops", ("shirt", "blouse")),
    )
    out = TagsShuffle().shuffle(", ", 7, bundle)
    _, new_bundle = out["result"]
    assert len(new_bundle) == 2
    assert new_bundle[0].category == "hair.color"
    assert new_bundle[0].mutex_within is True
    assert new_bundle[1].category == "clothing.tops"
    assert new_bundle[1].mutex_within is False


def test_shuffle_is_deterministic_for_same_seed() -> None:
    bundle = (_sel("x", ("a", "b", "c", "d", "e", "f", "g")),)
    r1 = TagsShuffle().shuffle(", ", 999, bundle)["result"][1]
    r2 = TagsShuffle().shuffle(", ", 999, bundle)["result"][1]
    assert r1 == r2


def test_shuffle_skips_extra_and_single_tag_selections() -> None:
    bundle = (
        _sel("extra", ("freeform text",)),
        _sel("hair.color", ("only_one",)),
        _sel("clothing.tops", ("a", "b", "c")),
    )
    out = TagsShuffle().shuffle(", ", 1, bundle)["result"][1]
    assert out[0].tags == ("freeform text",)
    assert out[1].tags == ("only_one",)
    # Last one with 3 tags should be reordered.
    assert set(out[2].tags) == {"a", "b", "c"}


def test_shuffle_empty_bundle_is_passthrough() -> None:
    prompt, bundle = TagsShuffle().shuffle(", ", 1, ())["result"]
    assert prompt == ""
    assert bundle == ()


# --- TagsRandomPick ------------------------------------------------------


def test_random_pick_count_equals_sample_size() -> None:
    bundle = (_sel("x", ("a", "b", "c", "d", "e")),)
    _, out_bundle = TagsRandomPick().pick(", ", 3, 42, bundle)["result"]
    assert len(out_bundle) == 1
    assert len(out_bundle[0].tags) == 3
    assert set(out_bundle[0].tags) <= {"a", "b", "c", "d", "e"}


def test_random_pick_flattens_across_selections() -> None:
    bundle = (
        _sel("hair.color", ("red", "blue")),
        _sel("clothing.tops", ("shirt", "blouse")),
    )
    _, out_bundle = TagsRandomPick().pick(", ", 4, 7, bundle)["result"]
    assert set(out_bundle[0].tags) == {"red", "blue", "shirt", "blouse"}
    assert out_bundle[0].category == "random_pick"
    assert out_bundle[0].layer == "random"


def test_random_pick_count_larger_than_pool_returns_all() -> None:
    bundle = (_sel("x", ("a", "b")),)
    _, out_bundle = TagsRandomPick().pick(", ", 99, 1, bundle)["result"]
    assert set(out_bundle[0].tags) == {"a", "b"}


def test_random_pick_preserves_extra() -> None:
    bundle = (
        _sel("x", ("a", "b", "c")),
        _sel("extra", ("freeform",)),
    )
    _, out_bundle = TagsRandomPick().pick(", ", 1, 1, bundle)["result"]
    # extra selection is preserved at the end.
    assert out_bundle[-1].category == "extra"
    assert out_bundle[-1].tags == ("freeform",)


def test_random_pick_is_deterministic_for_same_seed() -> None:
    bundle = (_sel("x", tuple(f"tag_{i}" for i in range(20))),)
    r1 = TagsRandomPick().pick(", ", 5, 12345, bundle)["result"][1]
    r2 = TagsRandomPick().pick(", ", 5, 12345, bundle)["result"][1]
    assert r1 == r2


def test_random_pick_empty_bundle() -> None:
    prompt, bundle = TagsRandomPick().pick(", ", 3, 1, ())["result"]
    assert prompt == ""
    assert bundle == ()
