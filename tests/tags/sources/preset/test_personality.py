from typing import Any

from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.build import TagsBuild
from nodes.tags.sources.preset.character import CharacterPreset
from nodes.tags.sources.preset.personality import PERSONALITY_PRESETS, PersonalityPreset


def _build_personality(name: str) -> Spec:
    return PersonalityPreset().build(name)[0]


def _build_character(name: str) -> Spec:
    return CharacterPreset().build(name)[0]


def test_personality_preset_input_lists_all() -> None:
    spec = PersonalityPreset.INPUT_TYPES()
    options, meta = spec["required"]["personality"]
    assert set(options) == set(PERSONALITY_PRESETS)
    assert meta["default"] in PERSONALITY_PRESETS


def test_tsundere_emits_expected_tags() -> None:
    bundle = _build_personality("tsundere")
    tags = bundle.pool[0].tags
    for expected in ("blush", "embarrassed", "pouting", "looking_away", "frown"):
        assert expected in tags


def test_character_plus_personality_layers_cleanly() -> None:
    # Pick miko + tsundere — tsundere adds blush/embarrassed/pouting/frown
    # to the otherwise neutral miko bundle.
    miko = _build_character("miko")
    tsundere = _build_personality("tsundere")
    out = TagsBuild().build(", ", bundle_1=miko, bundle_2=tsundere)
    tokens = str(out[0]).split(", ")
    # miko visuals
    for t in ("miko", "hakama", "long_hair", "black_hair"):
        assert t in tokens
    # tsundere mood
    for t in ("blush", "embarrassed", "pouting", "frown"):
        assert t in tokens


def test_genki_and_tsundere_conflict_resolves() -> None:
    # genki has happy + smile + grin; tsundere has frown. MUTEX_GROUPS is
    # last-wins, so wiring genki first and tsundere second lets tsundere's
    # frown override genki's smile/grin.
    genki = _build_personality("genki")
    tsundere = _build_personality("tsundere")
    out = TagsBuild().build(", ", bundle_1=genki, bundle_2=tsundere)
    tokens = str(out[0]).split(", ")
    assert "frown" in tokens
    assert "smile" not in tokens
    assert "grin" not in tokens
    # happy vs sad: tsundere doesn't have sad, so happy survives.
    assert "happy" in tokens


def test_kuudere_expressionless_drops_active_expression() -> None:
    # MUTEX_GROUPS is last-wins. If kuudere (expressionless) is wired
    # first and a smile bundle second, smile overrides expressionless.
    # Put the smile bundle first to keep expressionless.
    kuudere = _build_personality("kuudere")
    smile_bundle = Spec(kind="fixed", pool=(TaggedSelection("ext", "ext", ("smile",), False),))
    out = TagsBuild().build(", ", bundle_1=smile_bundle, bundle_2=kuudere)
    tokens = str(out[0]).split(", ")
    assert "expressionless" in tokens
    assert "smile" not in tokens


def test_personality_extra_appended() -> None:
    out = PersonalityPreset().build("genki", extra="1girl")
    bundle = out[0].pool
    preview = ", ".join(t for sel in bundle for t in sel.tags)
    assert preview.endswith(", 1girl")
    assert len(bundle) == 2
    assert bundle[1].category == "extra"


def test_all_personality_tags_exist_in_some_tag_node() -> None:
    """Sanity: every personality tag should be registered somewhere
    in the tag index (or be acceptable free-text). Otherwise the
    intent is unclear and AI may not recognise it."""
    from tests.tags.test_build import _TAG_INDEX

    unknown: dict[str, list[str]] = {}
    for name, tags in PERSONALITY_PRESETS.items():
        for t in tags:
            if t not in _TAG_INDEX:
                unknown.setdefault(name, []).append(t)
    assert not unknown, f"unknown tags: {unknown}"


def _build_personality_full(name: str) -> Any:
    return PersonalityPreset().build(name)
