from typing import Any

from nodes.tags.sources.pony_prompt_builder import PonyPromptBuilder


def _all_scores_on() -> dict[str, bool]:
    return {
        "score_9": True,
        "score_8_up": True,
        "score_7_up": True,
        "score_6_up": True,
        "score_5_up": True,
        "score_4_up": True,
    }


def _prompt(result: dict[str, Any]) -> str:
    return str(result["result"][0])


def _bundle(result: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(result["result"][1])


def test_build_recommended() -> None:
    node = PonyPromptBuilder()
    out = node.build(", ", "safe", "anime", "1girl, smile", **_all_scores_on())
    assert _prompt(out) == (
        "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, rating_safe, source_anime, 1girl, smile"
    )


def test_build_subset_of_scores() -> None:
    node = PonyPromptBuilder()
    scores = _all_scores_on()
    scores["score_5_up"] = False
    scores["score_4_up"] = False
    assert _prompt(node.build(", ", "none", "none", "", **scores)) == "score_9, score_8_up, score_7_up, score_6_up"


def test_build_all_scores_off() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    assert _prompt(node.build(", ", "none", "none", "", **scores)) == ""


def test_build_negative_style() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_4_up"] = True
    scores["score_5_up"] = True
    out = _prompt(node.build(", ", "none", "none", "worst quality, blurry", **scores))
    assert out == "score_5_up, score_4_up, worst quality, blurry"


def test_score_order_is_fixed() -> None:
    node = PonyPromptBuilder()
    scores = {
        "score_4_up": True,
        "score_9": True,
        "score_7_up": True,
        "score_8_up": False,
        "score_6_up": False,
        "score_5_up": False,
    }
    assert _prompt(node.build(", ", "none", "none", "", **scores)) == "score_9, score_7_up, score_4_up"


def test_extra_trimmed() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    assert _prompt(node.build(", ", "none", "none", "  hello  ", **scores)) == "hello"


def test_extra_blank_skipped() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_9"] = True
    assert _prompt(node.build(", ", "none", "none", "   ", **scores)) == "score_9"


def test_custom_separator() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_9"] = True
    out = _prompt(node.build(" | ", "safe", "pony", "x", **scores))
    assert out == "score_9 | rating_safe | source_pony | x"


def test_output_node_flag() -> None:
    assert PonyPromptBuilder.OUTPUT_NODE is True


def test_bundle_categorises_tags_under_preset_pony() -> None:
    node = PonyPromptBuilder()
    out = node.build(", ", "safe", "anime", "1girl", **_all_scores_on())
    bundle = _bundle(out)
    assert bundle[0].category == "preset.pony"
    assert bundle[0].layer == "preset"
    assert bundle[0].tags == (
        "score_9",
        "score_8_up",
        "score_7_up",
        "score_6_up",
        "score_5_up",
        "score_4_up",
        "rating_safe",
        "source_anime",
    )
    assert bundle[1].category == "extra"
    assert bundle[1].tags == ("1girl",)


def test_bundle_empty_when_nothing_selected() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    out = node.build(", ", "none", "none", "", **scores)
    assert _bundle(out) == ()
