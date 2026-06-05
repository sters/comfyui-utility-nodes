from typing import Any

from nodes.text.pony_prompt_builder import PonyPromptBuilder


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
    assert result["ui"]["text"] == result["result"]
    return str(result["result"][0])


def test_build_recommended() -> None:
    node = PonyPromptBuilder()
    out = _prompt(node.build(", ", "safe", "anime", "1girl, smile", **_all_scores_on()))
    assert out == (
        "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, rating_safe, source_anime, 1girl, smile"
    )


def test_build_subset_of_scores() -> None:
    node = PonyPromptBuilder()
    scores = _all_scores_on()
    scores["score_5_up"] = False
    scores["score_4_up"] = False
    out = _prompt(node.build(", ", "none", "none", "", **scores))
    assert out == "score_9, score_8_up, score_7_up, score_6_up"


def test_build_all_scores_off() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    out = _prompt(node.build(", ", "none", "none", "", **scores))
    assert out == ""


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
    out = _prompt(node.build(", ", "none", "none", "", **scores))
    assert out == "score_9, score_7_up, score_4_up"


def test_extra_trimmed() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    out = _prompt(node.build(", ", "none", "none", "  hello  ", **scores))
    assert out == "hello"


def test_extra_blank_skipped() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_9"] = True
    out = _prompt(node.build(", ", "none", "none", "   ", **scores))
    assert out == "score_9"


def test_custom_separator() -> None:
    node = PonyPromptBuilder()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_9"] = True
    out = _prompt(node.build(" | ", "safe", "pony", "x", **scores))
    assert out == "score_9 | rating_safe | source_pony | x"


def test_output_node_flag() -> None:
    assert PonyPromptBuilder.OUTPUT_NODE is True
