from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.build import TagsBuild
from nodes.tags.combinator import TagsCombinator
from nodes.tags.concat import TagsConcat
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
    prompt, _, _ = TagsBuild().build(", ", bundle=bundle)
    return str(prompt)


def test_combinator_cartesian_product_count() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    figure = _make_explode_axis("body.figure", ("muscular", "slim", "curvy", "plump"))
    out = TagsCombinator().combine(axis_1=hair, axis_2=figure)
    bundles, labels, indices = out
    assert len(bundles) == 2 * 4
    assert len(labels) == 8
    assert indices == list(range(8))
    assert all(b.kind == "fixed" for b in bundles)


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
    bundles, labels, _ = out
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
    bundles, labels, indices = out
    assert bundles == []
    assert labels == []
    assert indices == []


def test_combinator_deferred_axis_rides_along_without_multiplying() -> None:
    # A TagsRandomPick output wired directly into axis_i is a length-1,
    # unresolved axis: not cross-multiplied, carried through to every combo
    # folded into that combo's single Spec (as a composite of the fixed part
    # and the deferred pick).
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    (spec,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("eyes.color", ("blue_eyes", "red_eyes"))))
    bundles, labels, indices = TagsCombinator().combine(axis_1=hair, axis_2=[spec])
    assert len(bundles) == 2
    assert all(b.kind == "composite" for b in bundles)
    deferred = [b.children[1] for b in bundles]
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
    bundles, labels, indices = out
    # No enumerable axis at all — still exactly one combo.
    assert len(bundles) == 1
    assert bundles[0].kind == "composite"
    deferred = bundles[0].children[1]
    assert deferred.kind == "composite"
    assert len(deferred.children) == 2


def test_combinator_no_enumerable_axis_with_deferred_still_yields_one_combo() -> None:
    (spec,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("eyes.color", ("blue_eyes",))))
    bundles, labels, indices = TagsCombinator().combine(axis_1=[spec])
    assert len(bundles) == 1
    assert bundles[0].kind == "composite"
    assert bundles[0].children[0] == Spec(kind="fixed", pool=())
    assert indices == [0]


def test_combinator_deeply_nested_mixed_axes_resolves_end_to_end() -> None:
    # Mirrors a real graph:
    #   Combinator(
    #     Concat(Pony, Quality),                                     # fixed axis
    #     RandomBundle(char_a, char_b, char_c),                      # deferred axis
    #     Combinator(RandomPick(hair_style), RandomPick(hair_color), # nested Combinator's
    #                RandomPick(eye_color)),                         # own deferred axis
    #   )
    # Exercises composite-of-composite resolution: the inner Combinator's
    # single combo is itself a composite (all-deferred, no enumerable axis),
    # which then rides as one more deferred axis on the outer Combinator.
    pony = _fixed(_sel("meta.pony", ("score_9", "score_8_up")))
    quality = _fixed(_sel("meta.quality", ("masterpiece",)))
    (base,) = TagsConcat().concat(bundle_1=pony, bundle_2=quality)

    char_a = _fixed(_sel("character.a", ("char_a",)))
    char_b = _fixed(_sel("character.b", ("char_b",)))
    char_c = _fixed(_sel("character.c", ("char_c",)))
    (char_choice,) = TagsRandomBundle().pick(bundle_1=char_a, bundle_2=char_b, bundle_3=char_c)

    (hair_style_pick,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("hair.style", ("twin_tails", "ponytail"))))
    (hair_color_pick,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("hair.color", ("red_hair", "blue_hair"))))
    (eye_color_pick,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("eyes.color", ("red_eyes", "blue_eyes"))))
    inner_bundles, _, _ = TagsCombinator().combine(
        axis_1=[hair_style_pick], axis_2=[hair_color_pick], axis_3=[eye_color_pick]
    )
    assert len(inner_bundles) == 1
    assert inner_bundles[0].kind == "composite"

    outer_bundles, _, _ = TagsCombinator().combine(axis_1=[base], axis_2=[char_choice], axis_3=inner_bundles)
    assert len(outer_bundles) == 1
    assert outer_bundles[0].kind == "composite"

    prompt, warnings, _ = TagsBuild().build(", ", seed=123, bundle=outer_bundles[0])
    assert warnings == ""
    tokens = prompt.split(", ")

    assert "score_9" in tokens
    assert "score_8_up" in tokens
    assert "masterpiece" in tokens
    assert sum(t in tokens for t in ("char_a", "char_b", "char_c")) == 1
    assert sum(t in tokens for t in ("twin_tails", "ponytail")) == 1
    assert sum(t in tokens for t in ("red_hair", "blue_hair")) == 1
    assert sum(t in tokens for t in ("red_eyes", "blue_eyes")) == 1


def test_combinator_deeply_nested_axes_reroll_independently_across_seeds() -> None:
    # Same shape as above, run across many seeds — the random branches (which
    # character, which hair style/color, which eye color) should each vary
    # independently rather than collapsing to one fixed outcome or moving in
    # lockstep with each other (they share the same top-level salt via
    # mix_seed, so this also guards against that coincidentally degenerating
    # into correlated picks).
    char_a = _fixed(_sel("character.a", ("char_a",)))
    char_b = _fixed(_sel("character.b", ("char_b",)))
    (char_choice,) = TagsRandomBundle().pick(bundle_1=char_a, bundle_2=char_b)

    (hair_pick,) = TagsRandomPick().pick(count=1, bundle=_fixed(_sel("hair.color", ("red_hair", "blue_hair"))))
    inner_bundles, _, _ = TagsCombinator().combine(axis_1=[hair_pick])
    outer_bundles, _, _ = TagsCombinator().combine(axis_2=[char_choice], axis_3=inner_bundles)

    seen_chars: set[str] = set()
    seen_hair: set[str] = set()
    for seed in range(30):
        prompt, _, _ = TagsBuild().build(", ", seed=seed, bundle=outer_bundles[0])
        tokens = set(prompt.split(", "))
        seen_chars |= tokens & {"char_a", "char_b"}
        seen_hair |= tokens & {"red_hair", "blue_hair"}

    assert seen_chars == {"char_a", "char_b"}
    assert seen_hair == {"red_hair", "blue_hair"}
