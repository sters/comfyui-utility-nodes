from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.explode import TagsExplode


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def test_explode_emits_one_bundle_per_tag() -> None:
    bundle = _fixed(_sel("hair.color", ("red_hair", "blue_hair", "green_hair"), mutex_within=True))
    out = TagsExplode().explode(bundle)
    (specs,) = out
    assert len(specs) == 3
    assert specs[0].pool[0].tags == ("red_hair",)
    assert specs[1].pool[0].tags == ("blue_hair",)
    assert specs[2].pool[0].tags == ("green_hair",)


def test_explode_preserves_mutex_and_category() -> None:
    bundle = _fixed(_sel("hair.color", ("red_hair", "blue_hair"), mutex_within=True))
    (specs,) = TagsExplode().explode(bundle)
    for spec in specs:
        assert spec.pool[0].mutex_within is True
        assert spec.pool[0].category == "hair.color"


def test_explode_skips_extra_category() -> None:
    bundle = _fixed(
        _sel("hair.color", ("red_hair",)),
        _sel("extra", ("free_text",)),
    )
    (specs,) = TagsExplode().explode(bundle)
    assert len(specs) == 1
    assert specs[0].pool[0].tags == ("red_hair",)


def test_explode_empty_bundle_yields_sentinel() -> None:
    (specs,) = TagsExplode().explode(Spec(kind="fixed", pool=()))
    # Single empty Spec keeps TagsCombinator's product math sane.
    assert specs == [Spec(kind="fixed", pool=())]
