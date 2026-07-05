from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.sources.meta.pony import MetaPony


def _all_scores_on() -> dict[str, bool]:
    return {
        "score_9": True,
        "score_8_up": True,
        "score_7_up": True,
        "score_6_up": True,
        "score_5_up": True,
        "score_4_up": True,
    }


def _preview(result: tuple[Spec]) -> str:
    bundle = result[0].pool
    return ", ".join(t for sel in bundle for t in sel.tags)


def _bundle(result: tuple[Spec]) -> tuple[TaggedSelection, ...]:
    return result[0].pool


def test_build_recommended() -> None:
    node = MetaPony()
    out = node.build("1girl, smile", rating_safe=True, source_anime=True, **_all_scores_on())
    assert _preview(out) == (
        "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, rating_safe, source_anime, 1girl, smile"
    )


def test_build_subset_of_scores() -> None:
    node = MetaPony()
    scores = _all_scores_on()
    scores["score_5_up"] = False
    scores["score_4_up"] = False
    assert _preview(node.build("", **scores)) == "score_9, score_8_up, score_7_up, score_6_up"


def test_build_all_scores_off() -> None:
    node = MetaPony()
    scores = dict.fromkeys(_all_scores_on(), False)
    assert _preview(node.build("", **scores)) == ""


def test_build_negative_style() -> None:
    node = MetaPony()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_4_up"] = True
    scores["score_5_up"] = True
    out = _preview(node.build("worst quality, blurry", **scores))
    assert out == "score_5_up, score_4_up, worst quality, blurry"


def test_score_order_is_fixed() -> None:
    node = MetaPony()
    scores = {
        "score_4_up": True,
        "score_9": True,
        "score_7_up": True,
        "score_8_up": False,
        "score_6_up": False,
        "score_5_up": False,
    }
    assert _preview(node.build("", **scores)) == "score_9, score_7_up, score_4_up"


def test_extra_trimmed() -> None:
    node = MetaPony()
    scores = dict.fromkeys(_all_scores_on(), False)
    assert _preview(node.build("  hello  ", **scores)) == "hello"


def test_extra_blank_skipped() -> None:
    node = MetaPony()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_9"] = True
    assert _preview(node.build("   ", **scores)) == "score_9"


def test_preview_joins_with_comma_space() -> None:
    node = MetaPony()
    scores = dict.fromkeys(_all_scores_on(), False)
    scores["score_9"] = True
    out = _preview(node.build("x", rating_safe=True, source_pony=True, **scores))
    assert out == "score_9, rating_safe, source_pony, x"


def test_bundle_categorises_tags_under_meta_pony() -> None:
    node = MetaPony()
    out = node.build("1girl", rating_safe=True, source_anime=True, **_all_scores_on())
    bundle = _bundle(out)
    assert bundle[0].category == "meta.pony"
    assert bundle[0].layer == "meta"
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
    node = MetaPony()
    scores = dict.fromkeys(_all_scores_on(), False)
    out = node.build("", **scores)
    assert _bundle(out) == ()


def test_input_types_has_all_toggles() -> None:
    spec = MetaPony.INPUT_TYPES()
    for tag in ("score_9", "score_4_up", "rating_safe", "rating_explicit", "source_pony", "source_anime"):
        kind, _ = spec["required"][tag]
        assert kind == "BOOLEAN", f"{tag} should be BOOLEAN"


def test_all_toggles_default_off() -> None:
    spec = MetaPony.INPUT_TYPES()
    for tag in (
        "score_9",
        "score_4_up",
        "rating_safe",
        "rating_questionable",
        "rating_explicit",
        "source_pony",
        "source_anime",
    ):
        assert spec["required"][tag][1]["default"] is False, f"{tag} should default False"
