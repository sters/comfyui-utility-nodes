import pytest

from nodes.prompt_combinator import PromptCombinator


def test_expand_basic() -> None:
    node = PromptCombinator()
    prompts, labels, indices = node.expand(
        template="{a} {b}",
        axes="a: x, y\nb: 1, 2, 3",
        delimiter=",",
    )
    assert prompts == ["x 1", "x 2", "x 3", "y 1", "y 2", "y 3"]
    assert labels == [
        "a=x__b=1",
        "a=x__b=2",
        "a=x__b=3",
        "a=y__b=1",
        "a=y__b=2",
        "a=y__b=3",
    ]
    assert indices == [0, 1, 2, 3, 4, 5]


def test_realistic_character_axes() -> None:
    node = PromptCombinator()
    prompts, _, _ = node.expand(
        template="{hair} hair, {eye} eyes",
        axes="hair: short, long\neye: red, blue",
        delimiter=",",
    )
    assert len(prompts) == 4
    assert "short hair, red eyes" in prompts
    assert "long hair, blue eyes" in prompts


def test_unknown_placeholder_raises() -> None:
    node = PromptCombinator()
    with pytest.raises(ValueError, match="unknown axes"):
        node.expand(template="{nope}", axes="a: 1, 2", delimiter=",")


def test_missing_colon_raises() -> None:
    node = PromptCombinator()
    with pytest.raises(ValueError, match="':'"):
        node.expand(template="{a}", axes="bogus line", delimiter=",")


def test_empty_axis_values_raise() -> None:
    node = PromptCombinator()
    with pytest.raises(ValueError, match="no values"):
        node.expand(template="{a}", axes="a:  , ", delimiter=",")


def test_blank_and_comment_lines_ignored() -> None:
    node = PromptCombinator()
    prompts, _, _ = node.expand(
        template="{a}",
        axes="# comment\n\na: 1, 2\n",
        delimiter=",",
    )
    assert prompts == ["1", "2"]


def test_empty_axes_returns_empty() -> None:
    node = PromptCombinator()
    prompts, labels, indices = node.expand(template="", axes="", delimiter=",")
    assert prompts == []
    assert labels == []
    assert indices == []
