from nodes.tags._base import TaggedSelection
from nodes.tags.explode import TagsExplode


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def test_explode_emits_one_bundle_per_tag() -> None:
    bundle = (_sel("hair.color", ("red_hair", "blue_hair", "green_hair"), mutex_within=True),)
    out = TagsExplode().explode(bundle)
    (bundles,) = out
    assert len(bundles) == 3
    assert bundles[0][0].tags == ("red_hair",)
    assert bundles[1][0].tags == ("blue_hair",)
    assert bundles[2][0].tags == ("green_hair",)


def test_explode_preserves_mutex_and_category() -> None:
    bundle = (_sel("hair.color", ("red_hair", "blue_hair"), mutex_within=True),)
    (bundles,) = TagsExplode().explode(bundle)
    for b in bundles:
        assert b[0].mutex_within is True
        assert b[0].category == "hair.color"


def test_explode_skips_extra_category() -> None:
    bundle = (
        _sel("hair.color", ("red_hair",)),
        _sel("extra", ("free_text",)),
    )
    (bundles,) = TagsExplode().explode(bundle)
    assert len(bundles) == 1
    assert bundles[0][0].tags == ("red_hair",)


def test_explode_empty_bundle_yields_sentinel() -> None:
    (bundles,) = TagsExplode().explode(())
    # Single empty bundle keeps TagsCombinator's product math sane.
    assert bundles == [()]
