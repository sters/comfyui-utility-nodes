from nodes.tags._base import Spec, TaggedSelection
from nodes.tags.build import TagsBuild
from nodes.tags.sources.preset._base import RANDOM_OPTION
from nodes.tags.sources.preset.character import CharacterPreset
from nodes.tags.sources.preset.nsfw_act import NSFW_ACT_PRESETS, NsfwActPreset
from nodes.tags.sources.preset.personality import PersonalityPreset


def _build(act: str) -> Spec:
    return NsfwActPreset().build(act)[0]


def _merged(*specs: Spec) -> Spec:
    return Spec(kind="fixed", pool=tuple(sel for spec in specs for sel in spec.pool))


def test_input_types_lists_all_acts() -> None:
    spec = NsfwActPreset.INPUT_TYPES()
    options, meta = spec["required"]["act"]
    assert set(options) == set(NSFW_ACT_PRESETS) | {RANDOM_OPTION}
    assert meta["default"] == RANDOM_OPTION


def test_vanilla_emits_expected_tags() -> None:
    bundle = _build("vanilla_missionary")
    tags = bundle.pool[0].tags
    for expected in ("missionary", "vaginal", "kissing", "nude", "blush"):
        assert expected in tags


def test_nude_preset_drops_layered_clothing() -> None:
    nsfw = _build("mating_press")
    shirt_sel = Spec(kind="fixed", pool=(TaggedSelection("clothing.tops", "clothing", ("shirt",), False),))
    out = TagsBuild().build(", ", bundle=_merged(nsfw, shirt_sel))
    tokens = str(out[0]).split(", ")
    assert "nude" in tokens
    assert "shirt" not in tokens


def test_lingerie_preset_does_not_drop_its_own_underwear() -> None:
    bundle = _build("lingerie_tease")
    out = TagsBuild().build(", ", bundle=bundle)
    tokens = str(out[0]).split(", ")
    for t in ("lingerie", "bra", "panties", "garter_belt", "thighhighs"):
        assert t in tokens


def test_character_plus_nsfw_drops_outfit() -> None:
    girl = CharacterPreset().build("serafuku_schoolgirl")[0]
    sex = _build("first_time_shy")
    out = TagsBuild().build(", ", bundle=_merged(girl, sex))
    tokens = str(out[0]).split(", ")
    assert "nude" in tokens
    assert "serafuku" not in tokens
    assert "pleated_skirt" not in tokens
    assert "thighhighs" not in tokens
    assert "long_hair" in tokens
    assert "embarrassed" in tokens


def test_personality_layered_with_nsfw_act() -> None:
    p = PersonalityPreset().build("yandere")[0]
    s = _build("shibari_suspension")
    out = TagsBuild().build(", ", bundle=_merged(p, s))
    tokens = str(out[0]).split(", ")
    for t in ("yandere", "smirk", "shibari", "rope", "suspension_bondage"):
        assert t in tokens


def test_all_nsfw_act_tags_exist_in_some_tag_node() -> None:
    """Every tag in every NSFW act preset should be registered in one of
    the tag nodes — otherwise it's a typo or invented tag."""
    from tests.tags.test_build import _TAG_INDEX

    unknown: dict[str, list[str]] = {}
    for name, tags in NSFW_ACT_PRESETS.items():
        for t in tags:
            if t not in _TAG_INDEX:
                unknown.setdefault(name, []).append(t)
    assert not unknown, f"unknown tags: {unknown}"
