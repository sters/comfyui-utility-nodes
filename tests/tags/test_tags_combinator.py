from nodes.tags._base import TaggedSelection
from nodes.tags.explode import TagsExplode
from nodes.tags.sources.preset.character import CharacterPreset
from nodes.tags.tags_combinator import TagsCombinator


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _make_explode_axis(category: str, tags: tuple[str, ...], mutex: bool = False) -> list[tuple[TaggedSelection, ...]]:
    (bundles,) = TagsExplode().explode((_sel(category, tags, mutex_within=mutex),))
    return bundles


def test_combinator_cartesian_product_count() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    figure = _make_explode_axis("body.figure", ("muscular", "slim", "curvy", "plump"))
    out = TagsCombinator().combine([", "], axis_1=hair, axis_2=figure)
    prompts, labels, indices, _ = out
    assert len(prompts) == 2 * 4
    assert len(labels) == 8
    assert indices == list(range(8))


def test_combinator_label_uses_distinguishing_segment() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    out = TagsCombinator().combine([", "], axis_1=hair)
    labels = out[1]
    assert labels == ["red_hair", "blue_hair"]


def test_combinator_preset_axis_uses_category_suffix_for_label() -> None:
    # CharacterPreset emits category like "character.serafuku_schoolgirl"
    (bundle,) = CharacterPreset().build("serafuku_schoolgirl", ", ")["result"]
    out = TagsCombinator().combine([", "], axis_1=[tuple(bundle)])
    labels = out[1]
    assert labels == ["serafuku_schoolgirl"]


def test_combinator_preset_x_explode_full_example() -> None:
    # The motivating example: 1 character × 4 hair colors × 4 figures × 4 sizes = 64.
    (char_bundle,) = CharacterPreset().build("serafuku_schoolgirl", ", ")["result"]
    char_axis = [tuple(char_bundle)]
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair", "green_hair", "black_hair"))
    figure = _make_explode_axis("body.figure", ("muscular", "slim", "curvy", "plump"))
    breasts = _make_explode_axis(
        "breasts.size",
        ("flat_chest", "small_breasts", "medium_breasts", "large_breasts"),
        mutex=True,
    )
    out = TagsCombinator().combine([", "], axis_1=char_axis, axis_2=hair, axis_3=figure, axis_4=breasts)
    prompts, labels, _, _ = out
    assert len(prompts) == 1 * 4 * 4 * 4
    # Pick one combination, verify it contains the override hair color
    # and the preset's clothing.
    sample_label = "serafuku_schoolgirl__red_hair__muscular__flat_chest"
    assert sample_label in labels
    idx = labels.index(sample_label)
    tokens = prompts[idx].split(", ")
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
    out = TagsCombinator().combine([", "], axis_1=hair)
    prompts = out[0]
    assert len(prompts) == 2


def test_combinator_no_axes_returns_empty_lists() -> None:
    out = TagsCombinator().combine([", "])
    prompts, labels, indices, warnings = out
    assert prompts == []
    assert labels == []
    assert indices == []
    assert warnings == []


def test_combinator_decodes_separator_escape() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    out = TagsCombinator().combine([r"\n"], axis_1=hair)
    # Single-tag axis with newline separator — within a single-axis combo
    # there's only one tag per prompt so the separator doesn't show, but
    # the decoder must not crash on the escape.
    assert out[0] == ["red_hair", "blue_hair"]
