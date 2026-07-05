from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.build import TagsBuild
from nodes.tags.combinator import TagsCombinator
from nodes.tags.explode import TagsExplode
from nodes.tags.random_bundle import TagsRandomBundle
from nodes.tags.random_pick import TagsRandomPick
from nodes.tags.sources.preset.character import CharacterPreset


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _fixed(*sels: TaggedSelection) -> Spec:
    return Spec(kind="fixed", pool=sels)


def _make_explode_axis(category: str, tags: tuple[str, ...], mutex: bool = False) -> list[Spec]:
    (specs,) = TagsExplode().explode(_fixed(_sel(category, tags, mutex_within=mutex)))
    return specs


def _prompt(bundle: Spec) -> str:
    # Combinator now emits Specs; merging is the downstream TagsBuild's job.
    prompt, _, _ = TagsBuild().build(", ", bundle_1=bundle)
    return str(prompt)


def test_combinator_cartesian_product_count() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    figure = _make_explode_axis("body.figure", ("muscular", "slim", "curvy", "plump"))
    out = TagsCombinator().combine(axis_1=hair, axis_2=figure)
    bundles, labels, indices, deferred = out
    assert len(bundles) == 2 * 4
    assert len(labels) == 8
    assert indices == list(range(8))
    assert all(d.kind == "fixed" and d.pool == () for d in deferred)


def test_combinator_emits_concatenated_bundle_in_axis_order() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair",))
    figure = _make_explode_axis("body.figure", ("muscular",))
    out = TagsCombinator().combine(axis_1=hair, axis_2=figure)
    bundles = out[0]
    assert len(bundles) == 1
    # Both axis selections are present, in axis order, unmerged.
    assert [s.tags for s in bundles[0].pool] == [("red_hair",), ("muscular",)]


def test_combinator_label_uses_distinguishing_segment() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    out = TagsCombinator().combine(axis_1=hair)
    labels = out[1]
    assert labels == ["red_hair", "blue_hair"]


def test_combinator_preset_axis_uses_category_suffix_for_label() -> None:
    # CharacterPreset emits category like "character.serafuku_schoolgirl"
    (bundle,) = CharacterPreset().build("serafuku_schoolgirl")
    out = TagsCombinator().combine(axis_1=[bundle])
    labels = out[1]
    assert labels == ["serafuku_schoolgirl"]


def test_combinator_preset_x_explode_full_example() -> None:
    # The motivating example: 1 character × 4 hair colors × 4 figures × 4 sizes = 64.
    (char_bundle,) = CharacterPreset().build("serafuku_schoolgirl")
    char_axis = [char_bundle]
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair", "green_hair", "black_hair"))
    figure = _make_explode_axis("body.figure", ("muscular", "slim", "curvy", "plump"))
    breasts = _make_explode_axis(
        "breasts.size",
        ("flat_chest", "small_breasts", "medium_breasts", "large_breasts"),
        mutex=True,
    )
    out = TagsCombinator().combine(axis_1=char_axis, axis_2=hair, axis_3=figure, axis_4=breasts)
    bundles, labels, _, _ = out
    assert len(bundles) == 1 * 4 * 4 * 4
    # Pick one combination, run it through the downstream merge, and verify
    # it resolves to the expected prompt (override hair + preset clothing).
    sample_label = "serafuku_schoolgirl__red_hair__muscular__flat_chest"
    assert sample_label in labels
    idx = labels.index(sample_label)
    tokens = _prompt(bundles[idx]).split(", ")
    assert "red_hair" in tokens
    # Preset's brown_hair must be dropped — last-wins mutex group
    # lets red_hair (later axis) override the preset's brown_hair.
    assert "brown_hair" not in tokens
    # Preset's clothing should still be there
    for t in ("serafuku", "sailor_collar", "pleated_skirt"):
        assert t in tokens
    # Override tag from later axes
    assert "muscular" in tokens
    assert "flat_chest" in tokens


def test_combinator_skips_unwired_axes() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    out = TagsCombinator().combine(axis_1=hair)
    bundles = out[0]
    assert len(bundles) == 2


def test_combinator_no_axes_returns_empty_lists() -> None:
    out = TagsCombinator().combine()
    bundles, labels, indices, deferred = out
    assert bundles == []
    assert labels == []
    assert indices == []
    assert deferred == []


def test_combinator_deferred_axis_rides_along_without_multiplying() -> None:
    # A TagsRandomPick output wired directly into axis_i is a length-1,
    # unresolved axis: not cross-multiplied, carried through to every combo.
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    (spec,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("eyes.color", ("blue_eyes", "red_eyes"))))
    bundles, labels, indices, deferred = TagsCombinator().combine(axis_1=hair, axis_2=[spec])
    assert len(bundles) == 2
    assert len(deferred) == 2
    assert all(d.kind == "tag_pick" for d in deferred)
    # Each combo's deferred spec resolves independently (mixed by index — no
    # seed lives on TagsRandomPick itself anymore).
    assert deferred[0].seed != deferred[1].seed


def test_combinator_multiple_deferred_axes_composite_into_one_output() -> None:
    (pick,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("eyes.color", ("blue_eyes", "red_eyes"))))
    (choice,) = TagsRandomBundle().pick(
        bundle_1=_fixed(_sel("character.a", ("a_tag",))),
        bundle_2=_fixed(_sel("character.b", ("b_tag",))),
    )
    out = TagsCombinator().combine(axis_1=[pick], axis_2=[choice])
    bundles, labels, indices, deferred = out
    # No enumerable axis at all — still exactly one combo.
    assert len(bundles) == 1
    assert deferred[0].kind == "composite"
    assert len(deferred[0].children) == 2


def test_combinator_no_enumerable_axis_with_deferred_still_yields_one_combo() -> None:
    (spec,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("eyes.color", ("blue_eyes",))))
    bundles, labels, indices, deferred = TagsCombinator().combine(axis_1=[spec])
    assert bundles == [Spec(kind="fixed", pool=())]
    assert indices == [0]
    assert len(deferred) == 1
