from nodes.tags._base import TaggedSelection
from nodes.tags.merge import TagsMerge
from nodes.tags.nsfw_preset import NSFW_SCENE_PRESETS, NsfwScenePreset
from nodes.tags.personality import PersonalityPreset
from nodes.tags.preset import CharacterPreset


def _build(scene: str) -> tuple[TaggedSelection, ...]:
    return tuple(NsfwScenePreset().build(scene, ", ")["result"][1])


def test_input_types_lists_all_scenes() -> None:
    spec = NsfwScenePreset.INPUT_TYPES()
    options, meta = spec["required"]["scene"]
    assert set(options) == set(NSFW_SCENE_PRESETS)
    assert meta["default"] in NSFW_SCENE_PRESETS


def test_vanilla_emits_expected_tags() -> None:
    bundle = _build("vanilla_missionary")
    tags = bundle[0].tags
    for expected in ("missionary", "vaginal", "kissing", "nude", "blush"):
        assert expected in tags


def test_nude_preset_drops_layered_clothing() -> None:
    # NSFW preset with `nude` should drop a separately-added shirt.
    nsfw = _build("mating_press")
    shirt_sel = (TaggedSelection("clothing.tops", "clothing", ("shirt",), False),)
    out = TagsMerge().merge(", ", bundle_1=nsfw, bundle_2=shirt_sel)
    tokens = str(out["result"][0]).split(", ")
    assert "nude" in tokens
    assert "shirt" not in tokens


def test_lingerie_preset_does_not_drop_its_own_underwear() -> None:
    # lingerie_tease has no `nude`, so bra/panties/garter_belt survive.
    bundle = _build("lingerie_tease")
    out = TagsMerge().merge(", ", bundle_1=bundle)
    tokens = str(out["result"][0]).split(", ")
    for t in ("lingerie", "bra", "panties", "garter_belt", "thighhighs"):
        assert t in tokens


def test_character_plus_nsfw_drops_outfit() -> None:
    # serafuku_schoolgirl + first_time_shy (has nude) — outfit drops,
    # character traits like hair stay.
    girl = tuple(CharacterPreset().build("serafuku_schoolgirl", ", ")["result"][1])
    sex = _build("first_time_shy")
    out = TagsMerge().merge(", ", bundle_1=girl, bundle_2=sex)
    tokens = str(out["result"][0]).split(", ")
    assert "nude" in tokens
    assert "serafuku" not in tokens  # uniform dropped by nude
    assert "pleated_skirt" not in tokens  # bottoms dropped
    assert "thighhighs" not in tokens  # legwear dropped
    assert "long_hair" in tokens  # hair stays
    assert "embarrassed" in tokens  # NSFW preset mood stays


def test_personality_layered_with_nsfw_scene() -> None:
    # yandere personality + bondage shibari → smirk + ahegao + bound
    p = tuple(PersonalityPreset().build("yandere", ", ")["result"][1])
    s = _build("shibari_suspension")
    out = TagsMerge().merge(", ", bundle_1=p, bundle_2=s)
    tokens = str(out["result"][0]).split(", ")
    for t in ("yandere", "smirk", "shibari", "rope", "suspension_bondage"):
        assert t in tokens


def test_all_nsfw_preset_tags_exist_in_some_tag_node() -> None:
    """Every tag in every NSFW preset should be registered in one of
    the tag nodes — otherwise it's a typo or invented tag."""
    from tests.tags.test_merge import _TAG_INDEX

    unknown: dict[str, list[str]] = {}
    for name, tags in NSFW_SCENE_PRESETS.items():
        for t in tags:
            if t not in _TAG_INDEX:
                unknown.setdefault(name, []).append(t)
    assert not unknown, f"unknown tags: {unknown}"
