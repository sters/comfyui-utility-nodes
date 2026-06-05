from typing import Any

from nodes.tags._base import TaggedSelection
from nodes.tags.merge import TagsMerge
from nodes.tags.personality import PERSONALITY_PRESETS, PersonalityPreset
from nodes.tags.preset import CharacterPreset


def _build_personality(name: str) -> tuple[TaggedSelection, ...]:
    return tuple(PersonalityPreset().build(name, ", ")["result"][1])


def _build_character(name: str) -> tuple[TaggedSelection, ...]:
    return tuple(CharacterPreset().build(name, ", ")["result"][1])


def test_personality_preset_input_lists_all() -> None:
    spec = PersonalityPreset.INPUT_TYPES()
    options, meta = spec["required"]["personality"]
    assert set(options) == set(PERSONALITY_PRESETS)
    assert meta["default"] in PERSONALITY_PRESETS


def test_tsundere_emits_expected_tags() -> None:
    bundle = _build_personality("tsundere")
    tags = bundle[0].tags
    for expected in ("blush", "embarrassed", "pouting", "looking_away", "frown"):
        assert expected in tags


def test_character_plus_personality_layers_cleanly() -> None:
    # Pick miko + tsundere — tsundere adds blush/embarrassed/pouting/frown
    # to the otherwise neutral miko bundle.
    miko = _build_character("miko")
    tsundere = _build_personality("tsundere")
    out = TagsMerge().merge(", ", bundle_1=miko, bundle_2=tsundere)
    tokens = str(out["result"][0]).split(", ")
    # miko visuals
    for t in ("miko", "hakama", "long_hair", "black_hair"):
        assert t in tokens
    # tsundere mood
    for t in ("blush", "embarrassed", "pouting", "frown"):
        assert t in tokens


def test_genki_and_tsundere_conflict_resolves() -> None:
    # genki has happy + smile + grin, tsundere has frown. The merge
    # collapses the smile/grin/laughing vs frown mutex pairs.
    genki = _build_personality("genki")
    tsundere = _build_personality("tsundere")
    out = TagsMerge().merge(", ", bundle_1=genki, bundle_2=tsundere)
    tokens = str(out["result"][0]).split(", ")
    # First bundle wins for mouth-curve mutex
    assert "smile" in tokens
    assert "grin" in tokens
    assert "frown" not in tokens
    # happy vs sad: tsundere doesn't have sad but happy is unique
    assert "happy" in tokens


def test_kuudere_expressionless_drops_active_expression() -> None:
    # If user combines kuudere (expressionless) with a smile from extra,
    # expressionless wins via MUTEX_GROUPS.
    kuudere = _build_personality("kuudere")
    smile_bundle = (TaggedSelection("ext", "ext", ("smile",), False),)
    out = TagsMerge().merge(", ", bundle_1=kuudere, bundle_2=smile_bundle)
    tokens = str(out["result"][0]).split(", ")
    assert "expressionless" in tokens
    assert "smile" not in tokens


def test_personality_extra_appended() -> None:
    out = PersonalityPreset().build("genki", ", ", extra="1girl")
    prompt = str(out["result"][0])
    assert prompt.endswith(", 1girl")
    bundle = tuple(out["result"][1])
    assert len(bundle) == 2
    assert bundle[1].category == "extra"


def test_all_personality_tags_exist_in_some_tag_node() -> None:
    """Sanity: every personality tag should be registered somewhere
    in the tag index (or be acceptable free-text). Otherwise the
    intent is unclear and AI may not recognise it."""
    from tests.tags.test_merge import _TAG_INDEX

    unknown: dict[str, list[str]] = {}
    for name, tags in PERSONALITY_PRESETS.items():
        for t in tags:
            if t not in _TAG_INDEX:
                unknown.setdefault(name, []).append(t)
    assert not unknown, f"unknown tags: {unknown}"


def _build_personality_full(name: str) -> Any:
    return PersonalityPreset().build(name, ", ")
