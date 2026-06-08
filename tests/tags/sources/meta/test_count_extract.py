from typing import Any

from nodes.tags.sources.meta.count_extract import MetaCountExtract


def _run(prompt: str) -> tuple[str, int, int, int, int]:
    out: dict[str, Any] = MetaCountExtract().extract(prompt)
    r = out["result"]
    return str(r[0]), int(r[1]), int(r[2]), int(r[3]), int(r[4])


def test_single_girl() -> None:
    tags, total, girls, boys, others = _run("1girl, long_hair, miko, looking_at_viewer")
    assert tags == "1girl"
    assert (total, girls, boys, others) == (1, 1, 0, 0)


def test_mixed_girls_and_boys_sum() -> None:
    tags, total, girls, boys, others = _run("masterpiece, 2girls, 1boy, kissing")
    assert "2girls" in tags and "1boy" in tags
    assert (total, girls, boys, others) == (3, 2, 1, 0)


def test_plus_form_counts_as_floor() -> None:
    tags, total, girls, _, _ = _run("6+girls, crowd")
    assert tags == "6+girls"
    assert total == 6
    assert girls == 6


def test_multiple_without_number_floors_to_two() -> None:
    _, total, girls, _, _ = _run("multiple_girls, scenery")
    assert girls == 2
    assert total == 2


def test_explicit_number_wins_over_multiple() -> None:
    _, total, girls, _, _ = _run("3girls, multiple_girls")
    assert girls == 3
    assert total == 3


def test_total_only_tag_fallback() -> None:
    _, total, girls, boys, others = _run("solo, duo, scenery")
    # no numbered/gendered tags — fall back to max(solo=1, duo=2) -> 2
    assert (girls, boys, others) == (0, 0, 0)
    assert total == 2


def test_solo_maps_to_one() -> None:
    _, total, _, _, _ = _run("solo, masterpiece")
    assert total == 1


def test_group_alone_is_unknown_zero() -> None:
    tags, total, _, _, _ = _run("group, crowd, scenery")
    assert "group" in tags
    assert total == 0


def test_others_counted() -> None:
    _, total, girls, boys, others = _run("1girl, 1other, holding_hands")
    assert (girls, boys, others) == (1, 0, 1)
    assert total == 2


def test_no_count_tags_is_zero() -> None:
    tags, total, girls, boys, others = _run("scenery, no_humans, landscape")
    assert tags == ""
    assert (total, girls, boys, others) == (0, 0, 0, 0)


def test_does_not_match_inside_words() -> None:
    # "otherwise" / "1080p" / "girlfriend" must not be parsed as count tags.
    tags, total, girls, boys, others = _run("otherwise, 1080p, girlfriend material")
    assert tags == ""
    assert (total, girls, boys, others) == (0, 0, 0, 0)


def test_preview_text_surfaced() -> None:
    out = MetaCountExtract().extract("2girls, 1boy")
    assert out["ui"]["text"][0] == "3 subject(s): 2girls, 1boy"
