from nodes.tags._base import TaggedSelection
from nodes.tags.combinator import TagsCombinator
from nodes.tags.explode import TagsExplode
from nodes.tags.rules import TagsBuildFromRules, TagsRulesToJson, axes_to_rules, rules_to_axes


def _sel(category: str, tags: tuple[str, ...], mutex_within: bool = False) -> TaggedSelection:
    return TaggedSelection(category=category, layer="test", tags=tags, mutex_within=mutex_within)


def _make_explode_axis(category: str, tags: tuple[str, ...]) -> list[tuple[TaggedSelection, ...]]:
    (bundles,) = TagsExplode().explode((_sel(category, tags),))
    return bundles


def test_axes_to_rules_then_rules_to_axes_roundtrips() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    axes = [hair]
    rules = axes_to_rules(axes)
    assert rules_to_axes(rules) == axes


def test_rules_to_axes_empty_string_yields_no_axes() -> None:
    assert rules_to_axes("") == []


def test_rules_to_axes_malformed_json_yields_no_axes() -> None:
    assert rules_to_axes("{not valid json") == []


def test_rules_to_json_serializes_same_axes_combinator_would_expand() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    figure = _make_explode_axis("body.figure", ("muscular", "slim"))
    (rules,) = TagsRulesToJson().build(axis_1=hair, axis_2=figure)
    assert rules_to_axes(rules) == [hair, figure]


def test_build_from_rules_matches_combinator_expansion() -> None:
    hair = _make_explode_axis("hair.color", ("red_hair", "blue_hair"))
    figure = _make_explode_axis("body.figure", ("muscular", "slim", "curvy"))

    combinator_bundles, combinator_labels, combinator_indices = TagsCombinator().combine(axis_1=hair, axis_2=figure)

    (rules,) = TagsRulesToJson().build(axis_1=hair, axis_2=figure)
    rule_bundles, rule_labels, rule_indices = TagsBuildFromRules().build(rules)

    assert rule_bundles == combinator_bundles
    assert rule_labels == combinator_labels
    assert rule_indices == combinator_indices
    assert len(rule_bundles) == 2 * 3


def test_build_from_rules_empty_rules_yields_no_combinations() -> None:
    assert TagsBuildFromRules().build("[]") == ([], [], [])
